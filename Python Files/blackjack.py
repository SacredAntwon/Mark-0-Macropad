# Author: SacredAntwon
# Purpose: Game of blackjack.

import layout
from time import sleep
from collections import namedtuple
import random
import json

# Initialize Display
layout.oled.init_display()

# Read save file
with open('JSONFiles/save.json', 'r') as f:
    getBalance = json.load(f)

balance = getBalance["blackjackBalance"]

layout.oled.text("Play", 1, 1)
layout.oled.text(("Blnc: $"+str(balance)), 1, 11)

layout.oled.show()

buttonBounce = True

# This function will save information to save.json
def jsonSave(key, value):
    saveJson = open("JSONFiles/save.json", "r")
    jsonObject = json.load(saveJson)
    saveJson.close()

    jsonObject[key] = value

    saveJson = open("JSONFiles/save.json", "w")
    json.dump(jsonObject, saveJson)
    saveJson.close()

# Function for updating the screen
def updateScreen(text, line):
    if line == 1:
        layout.oled.fill_rect(1, 1, layout.width, 10, 0)
        layout.oled.text((text), 1, 1)
    elif line == 2:
        layout.oled.fill_rect(1, 11, layout.width, 10, 0)
        layout.oled.text((text), 1, 11)
    elif line == 3:
        layout.oled.fill_rect(1, 21, layout.width, 10, 0)
        layout.oled.text((text), 1, 21)
    layout.oled.show()

# Function for making a bet
def betAmountFunc(balance):
    layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
    layout.oled.show()
    layout.oled.text("Stp:10", 1, 1)
    layout.oled.text("Stp:100", 60, 1)
    layout.oled.text("Confirm", 1, 21)
    layout.oled.show()
    bet = 0
    increment = 10
    updateScreen(("$ "+str(bet)), 2)
    previousValue = True
    while (layout.button13.value() != True):
        if layout.button11.value():
            increment = 10
            sleep(.5)
        elif layout.button21.value():
            increment = 100
            sleep(.5)

        if previousValue != layout.stepPin.value():
            if layout.stepPin.value() == False:

                # Turned Left
                if layout.directionPin.value() == False:
                    tempBet = bet - increment
                    if tempBet >= 0:
                        bet -= increment
                        updateScreen(("$ "+str(bet)), 2)

                # Turned Right
                else:
                    tempBet = bet + increment
                    if tempBet <= balance:
                        bet += increment
                        updateScreen(("$ "+str(bet)), 2)
        previousValue = layout.stepPin.value()
    sleep(1)
    layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
    layout.oled.show()
    return bet

# Function for creating deck of cards
def cards():
    Card = namedtuple("Card", ["rank", "suit"])
    ranks = ["Ace"] + [str(x) for x in range(2, 11)] + \
        "Jack Queen King".split()
    suits = "Clubs Hearts Spades Diamonds".split()
    deck = [Card(rank, suit) for suit in suits for rank in ranks]
    fullDeck = []
    for i in range(6):
        fullDeck += deck
    for i in range(len(fullDeck)-1, 0, -1):
        j = random.randint(0, i + 1)
        fullDeck[i], fullDeck[j] = fullDeck[j], fullDeck[i]

    return fullDeck

# Function for returning the number value of cards
def valueCard(currentCard):
    if currentCard == "Ace" or "King" or "Queen" or "Jack":
        return {"Ace": 11, "King": 10, "Queen": 10, "Jack": 10}.get(
            currentCard, currentCard
        )

# Function to get the total value of cards
def getTotal(cards):
    total = 0
    numberOfAces = 0
    for i in range(1, len(cards)):
        cardVal = int(valueCard(cards[i].rank))
        total += cardVal
        if cardVal == 11:
            numberOfAces += 1
    while total > 21:
        if numberOfAces >= 1:
            total -= 10
            numberOfAces -= 1
        else:
            break
    return total

# Function to create a string for a card
def createCardString(cards):
    cardString = cards[0][0] + ":"
    for i in reversed(range(1, len(cards))):
        cardString += " " + cards[i].rank[0] + cards[i].suit[0]
    return cardString

# Main game function
def game():
    # Initializing variables
    global balance
    decks = cards()
    playerCards = ["You"]
    dealerCards = ["Dealer"]
    playerTotal = 0
    dealerTotal = 0
    if (balance <= 0):
        balance = 10000
    betAmount = betAmountFunc(balance)
    balance -= betAmount

    table = [playerCards, dealerCards]

    # Passing cards in order
    for i in range(2):
        for person in table:
            card = decks.pop(0)
            person.append(card)
            sleep(1)
            if (i != 1) or (person[0] != "Dealer"):
                if (person[0] == "You"):
                    updateScreen(createCardString(person), 1)
                else:
                    updateScreen(createCardString(person), 2)

    updateScreen(createCardString(playerCards), 1)
    updateScreen(createCardString(dealerCards[:-1]), 2)
    playerTotal = getTotal(playerCards)
    dealerTotal = getTotal(dealerCards[:-1])
    updateScreen(("YTtl:" + str(playerTotal) +
                 "  DTtl:" + str(dealerTotal)), 3)

    while (playerTotal < 21):
        # Press hit button
        if layout.button13.value():
            card = decks.pop(0)
            playerCards.append(card)
            playerTotal = getTotal(playerCards)
            updateScreen(createCardString(playerCards), 1)
            updateScreen(("YTtl:" + str(playerTotal) +
                         "  DTtl:" + str(dealerTotal)), 3)
            sleep(.5)
        # Press stand button
        elif layout.button23.value():
            break

    updateScreen(createCardString(playerCards), 1)
    updateScreen(("YTtl:" + str(playerTotal) +
                 "  DTtl:" + str(dealerTotal)), 3)

    dealerTotal = getTotal(dealerCards)
    updateScreen(createCardString(dealerCards), 2)
    updateScreen(("YTtl:" + str(playerTotal) +
                 "  DTtl:" + str(dealerTotal)), 3)

    # Dealers turn
    while (dealerTotal < 17 and playerTotal <= 21):
        sleep(1)
        card = decks.pop(0)
        dealerCards.append(card)
        dealerTotal = getTotal(dealerCards)
        updateScreen(createCardString(dealerCards), 2)
        updateScreen(("YTtl:" + str(playerTotal) +
                     "  DTtl:" + str(dealerTotal)), 3)

    dealerTotal = getTotal(dealerCards)
    updateScreen(createCardString(dealerCards), 2)
    updateScreen(("YTtl:" + str(playerTotal) +
                 "  DTtl:" + str(dealerTotal)), 3)
    sleep(3)
    layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
    layout.oled.show()

    # This will go through if dealer wins
    if (dealerTotal <= 21 and dealerTotal > playerTotal or playerTotal > 21):
        updateScreen("Dealer Wins!", 1)
        sleep(1)
        updateScreen(("- $"+str(betAmount)), 2)
        sleep(1)
        updateScreen(("Blnc: $"+str(balance)), 3)

    # This will go through if player wins
    elif (dealerTotal > 21 or playerTotal > dealerTotal):
        balance += betAmount * 2
        updateScreen("You Win!", 1)
        sleep(1)
        updateScreen(("+ $"+str(betAmount*2)), 2)
        sleep(1)
        updateScreen(("Blnc: $"+str(balance)), 3)

    # This will go through if there is a push
    elif (dealerTotal <= 21 and playerTotal <= 21 and dealerTotal == playerTotal):
        balance += betAmount
        updateScreen("Push!", 1)
        sleep(1)
        updateScreen(("+ $"+str(betAmount)), 2)
        sleep(1)
        updateScreen(("Blnc: $"+str(balance)), 3)

    # Check if balance is 0
    if (balance <= 0):
        sleep(1)
        layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
        layout.oled.show()
        sleep(1)
        updateScreen(("Balance at $0."), 1)
        sleep(1)
        updateScreen(("$10000 added."), 2)
        sleep(1)
        updateScreen(("Play better!"), 3)
        balance = 10000

    # Save information
    jsonSave("blackjackBalance", balance)
    sleep(2)
    layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
    layout.oled.show()
    updateScreen("Play", 1)
    updateScreen(("Blnc: $"+str(balance)), 2)


# Runs in blackjack main menu
while buttonBounce:
    if layout.button11.value():
        sleep(1)
        game()

    # Back to menu
    if layout.buttonPin.value() == False:
        layout.oled.fill_rect(0, 0, layout.width, layout.height, 0)
        layout.oled.text("Going Back", 1, 10)
        layout.oled.text("To Menu", 1, 21)
        layout.oled.show()
        sleep(1)
        buttonBounce = False

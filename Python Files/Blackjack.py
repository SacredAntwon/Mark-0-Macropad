import layout
from time import sleep
from collections import namedtuple
import random

layout.oled.init_display()

file1 = open("save.txt","r")
balance = int(file1.read())
file1.close()

layout.oled.text("Play",1,1)
layout.oled.text(("Blnc: $"+str(balance)),1,11)

layout.oled.show()

button_bounce = True
def updateScreen(text, line):
    if line == 1:
        layout.oled.fill_rect(1,1,layout.width,10,0)
        layout.oled.text((text),1,1)
    elif line == 2:
        layout.oled.fill_rect(1,11,layout.width,10,0)
        layout.oled.text((text),1,11)
    elif line == 3:
        layout.oled.fill_rect(1,21,layout.width,10,0)
        layout.oled.text((text),1,21)
    layout.oled.show()

def betAmountFunc(balance):
    layout.oled.fill_rect(0,0,layout.width,layout.height,0)
    layout.oled.show()
    layout.oled.text("Stp:10",1,1)
    layout.oled.text("Stp:100",60,1)
    layout.oled.text("Confirm",1,21)
    layout.oled.show()
    bet = 0
    increment = 10
    updateScreen(("$ "+str(bet)), 2)
    previous_value = True
    while (layout.button13.value() != True):
        if layout.button11.value():
            increment = 10
            sleep(.5)
        elif layout.button21.value():
            increment = 100
            sleep(.5)
            
        if previous_value != layout.step_pin.value():
            if layout.step_pin.value() == False:

                # Turned Left
                if layout.direction_pin.value() == False:
                    tempBet = bet - increment
                    if  tempBet >= 0:
                        bet -= increment
                        updateScreen(("$ "+str(bet)), 2)

                # Turned Right
                else:
                    tempBet = bet + increment
                    if tempBet <= balance:
                        bet += increment
                        updateScreen(("$ "+str(bet)), 2)
        previous_value = layout.step_pin.value()
    sleep(1)
    layout.oled.fill_rect(0,0,layout.width,layout.height,0)
    layout.oled.show()
    return bet
            

            
            
        
def cards():
    Card = namedtuple("Card", ["rank", "suit"])
    ranks = ["Ace"] + [str(x) for x in range(2, 11)] + "Jack Queen King".split()
    suits = "Clubs Hearts Spades Diamonds".split()
    deck = [Card(rank, suit) for suit in suits for rank in ranks]
    fullDeck = []
    for i in range(6):
        fullDeck += deck
    for i in range(len(fullDeck)-1, 0, -1):
        j = random.randint(0, i + 1)
        fullDeck[i], fullDeck[j] = fullDeck[j], fullDeck[i]
        
#     for item in fullDeck:
        # print("{} of {}".format(item.rank, item.suit))
    #print(len(fullDeck))
    return fullDeck

def valueCard(currentCard):
    if currentCard == "Ace" or "King" or "Queen" or "Jack":
        return {"Ace": 11, "King": 10, "Queen": 10, "Jack": 10}.get(
            currentCard, currentCard
        )
    
def getTotal(cards):
    total = 0
    numberOfAces = 0
    for i in range(1, len(cards)):
        card_val = int(valueCard(cards[i].rank))
        total += card_val
        if card_val == 11:
            numberOfAces += 1
    while total > 21:
        if numberOfAces >= 1:
            total -= 10
            numberOfAces -= 1
        else:
            break
    return total

def createCardString(cards):
    cardString = cards[0][0] + ":"
    for i in reversed(range(1, len(cards))):
        cardString += " " + cards[i].rank[0] + cards[i].suit[0]
    #print(cardString)
    return cardString
    
def game():
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
    for i in range(2):  
        for person in table:
            card = decks.pop(0)
            person.append(card)
            sleep(1)
            if (i != 1) or (person[0] != "Dealer"):
                #print("{} got {} of {}".format(person[0], card.rank, card.suit))
                if (person[0] == "You"):
                    updateScreen(createCardString(person), 1)
                else:
                    updateScreen(createCardString(person), 2)
           # else:
                #print("Dealer hides second card")
    
    #playerString = createCardString(playerCards)
    #dealerString = createCardString(dealerCards[:-1])
    updateScreen(createCardString(playerCards), 1)
    updateScreen(createCardString(dealerCards[:-1]), 2)
    playerTotal = getTotal(playerCards)
    dealerTotal = getTotal(dealerCards[:-1])
    # stringTotal = ("Y Tot: " + str(playerTotal) + " D Tot: " + str(dealerTotal))
    updateScreen(("YTtl:" + str(playerTotal) + "  DTtl:" + str(dealerTotal)), 3)
    #print(playerTotal)
    #print(dealerTotal)
    
    #print("Your Turn")
    while (playerTotal < 21):
#         playerInput = input("Hit(h) or Stand(s)")
        #HIT
        if layout.button13.value():
            card = decks.pop(0)
            playerCards.append(card)
            playerTotal = getTotal(playerCards)
            updateScreen(createCardString(playerCards), 1)
            updateScreen(("YTtl:" + str(playerTotal) + "  DTtl:" + str(dealerTotal)), 3)
            #print("Your Total: ", playerTotal)
            sleep(.5)
        elif layout.button23.value():
            break
        
    updateScreen(createCardString(playerCards), 1)
    updateScreen(("YTtl:" + str(playerTotal) + "  DTtl:" + str(dealerTotal)), 3)
    
    dealerTotal = getTotal(dealerCards)
    updateScreen(createCardString(dealerCards), 2)
    updateScreen(("YTtl:" + str(playerTotal) + "  DTtl:" + str(dealerTotal)), 3)
    
    #print("Dealers Turn")
    while (dealerTotal < 17 and playerTotal <= 21):
        sleep(1)
        card = decks.pop(0)
        dealerCards.append(card)
        dealerTotal = getTotal(dealerCards)
        updateScreen(createCardString(dealerCards), 2)
        updateScreen(("YTtl:" + str(playerTotal) + "  DTtl:" + str(dealerTotal)), 3)
        #print("Dealer Total: ", dealerTotal)
        
    
    dealerTotal = getTotal(dealerCards)
    updateScreen(createCardString(dealerCards), 2)
    updateScreen(("YTtl:" + str(playerTotal) + "  DTtl:" + str(dealerTotal)), 3)
    #print("Dealer Has: ", dealerTotal)
    sleep(3)
    layout.oled.fill_rect(0,0,layout.width,layout.height,0)
    layout.oled.show()
    if (dealerTotal <= 21 and dealerTotal > playerTotal or playerTotal > 21):
        #print("Dealer Wins!")
        updateScreen("Dealer Wins!", 1)
        sleep(1)
        updateScreen(("- $"+str(betAmount)), 2)
        sleep(1)
        updateScreen(("Blnc: $"+str(balance)), 3)
        
    elif (dealerTotal > 21 or playerTotal > dealerTotal):
        #print("You Win!")
        balance += betAmount * 2
        updateScreen("You Win!", 1)
        sleep(1)
        updateScreen(("+ $"+str(betAmount*2)), 2)
        sleep(1)
        updateScreen(("Blnc: $"+str(balance)), 3)
        
    elif (dealerTotal <= 21 and playerTotal <= 21 and dealerTotal == playerTotal):
        #print("Push!")
        balance += betAmount
        updateScreen("Push!",1)
        sleep(1)
        updateScreen(("+ $"+str(betAmount)), 2)
        sleep(1)
        updateScreen(("Blnc: $"+str(balance)), 3)
    
    if (balance <= 0):
        sleep(1)
        layout.oled.fill_rect(0,0,layout.width,layout.height,0)
        layout.oled.show()
        sleep(1)
        updateScreen(("Balance at $0."), 1)
        sleep(1)
        updateScreen(("$10000 added."), 2)
        sleep(1)
        updateScreen(("Play better!"), 3)
    
    file1 = open("save.txt","w")
    file1.write(str(balance))
    file1.close()
    
    sleep(2)
    layout.oled.fill_rect(0,0,layout.width,layout.height,0)
    layout.oled.show()
    updateScreen("Play", 1)
    updateScreen(("Blnc: $"+str(balance)), 2)
    #StartEnd()

def StartEnd():
    positions = [[1,1], [1,11], [1,21], [60,1], [60,11], [60,21]]
    while (layout.button_pin.value() != False):
        for i in positions:
            layout.oled.text("Play",i[0],i[1])
            layout.oled.show()
            sleep(1.5)
        layout.oled.fill_rect(0,0,layout.width,layout.height,0)
        layout.oled.show()
        sleep(1)
            
        
while button_bounce:
    if layout.button11.value():
        #decks = cards()
        sleep(1)
        game()
        
    elif layout.button12.value():
        sleep(.5)
    elif layout.button13.value():
        sleep(.5)
    elif layout.button21.value():
        sleep(.5)
    elif layout.button22.value():
        sleep(.5)
    elif layout.button23.value():
        sleep(.5)
        
    if layout.button_pin.value() == False:
        layout.oled.fill_rect(0,0,layout.width,layout.height,0)
        layout.oled.text("Going Back", 1, 10)
        layout.oled.text("To Menu", 1, 21)
        layout.oled.show()
        sleep(1)
        button_bounce = False
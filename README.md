# Mark-0-Macropad


## Parts List

## Uploading Firmware
_Step 1:_ With the device disconnected from the computer, hold the boot button located on the bottom of the board.

_Step 2:_ While holding the boot button on the device, plug it into the computer and let go of the boot button.

_Step 3:_ A new directory should now appear for the device.

_Step 4:_ Drag the file named `firmware.   ` , which should be located in the `firmware` folder in this repo, into the device directory, and the device should then automatically reboot.

## Uploading Code
_Step 1:_ Install a software called `thonny` onto your system.

_Step 2:_ Once it is installed, click on `Tools` located on the top and then select `Options...`, which will make a menu appear. Select `Interpreter` from this menu. When it asks which interpreter you would like to use from the drop down, select `MicroPython (Raspberry Pi Pico)`. For the Port drop down selection, select a device that includes `COM`.

_Step 3:_ Exit the menu and select the `View` button on the top. Click on `Files` and a checkmark should appear next to it.

## Files
_main.py_: This is the main file that will run on boot.

_keycode.py_: This will hold all HID Keycodes.

_layout.py_: Pins for all components are assigned here, along with HID support.

_macros.py_: The dictionary for the macros are stored here. This is where more macros are added.

_Test.py_: Allows for users to test the components and HID for the device. Enter it by pressing `Top Left, Middle Right, Bottom Left` buttons at the same time.

_etch.py_: Etch is a way to draw on the device. Enter etch by pressing `Top Left, Top Right` buttons at the same time. `Rotate` is the `Top Left` button, `Invert` colors is the `Top Right` button, `Clear` screen is `Middle Left` button, and `PC Draw` is `Middle Right` button. `PC Draw` will move the cursor on your screen along the same trace you drew on the device.

_Blackjack.py_: Enter blackjack by pressing `Middle Left, Middle Right` buttons at the same time. Once you see `Play` press `Top Left` button. In the bet screen, use `Top Left` button to set increment to $10 or `Top Right` button to set increment to $100. Use rotary encoder and spin either right to increase bet or left to decrease bet. To `Confirm` bet, press `Bottom Left` button. `YTtl` is the total of your cards, and `DTtl` is the dealers total. To `Hit` press `Bottom Left` button and to `Stand` press `Bottom Right` button. $10000 will be added to the balance if a balance of $0 is reached.

_save.txt_: This is where the balance in `Blackjack.py` is stored so it will always be saved.
## How-To Add Macros

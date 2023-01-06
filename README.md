# Mark-0-Macropad


## Parts List
_Microcontroller:_ Seeed Studio XIAO RP2040

_Screen:_ SSD1306 OLED 128x32

_Rotary Encoder:_ CYT1100

_Buttons x 6:_ 6x6x4.3mm 4 Pin Micro SMD

_Custom PCB_

## Uploading Firmware
_Step 1:_ With the device disconnected from the computer, hold the button labeled `boot` located on the bottom of the microcontroller which is below the macropad.

_Step 2:_ While holding the boot button on the device, plug it into the computer and let go of the boot button.

_Step 3:_ A new directory should now appear for the device.

_Step 4:_ Drag the file named `firmware.uf2`, which should be located in the `firmware` folder in this repo, into the device directory, and the device should then automatically reboot.

## Uploading Code
_Step 1:_ Install a software called [`Thonny`](https://thonny.org) onto your system.

_Step 2:_ Once it is installed, click on `Tools` located on the top and then select `Options...`, which will make a menu appear. Select `Interpreter` from this menu. When it asks which interpreter you would like to use from the drop down, select `MicroPython (Raspberry Pi Pico)`. For the Port drop down selection, select a device that includes `COM`.

_Step 3:_ Exit the menu and select the `View` button on the top. Click on `Files` and a checkmark should appear next to it.

_Step 4:_ On the left side you will see the `Files` section, the top part being files on your computer and the bottom part being the files on the device.

_Step 5:_ If there are files in your device, select all of the files and delete them.

_Step 6:_ In the top portion of the `Files` section, find the folder named `Python Files` which should be downloaded from this repo.

_Step 7:_ Select all files in the `Python Files` folder and right click on it. Select the option labeled `Upload to /` and all files should be uploaded to the device.

_Step 8:_ You could check if the files uploaded successfully by running `maintest.py` or `main.py`, depending on what you have it named. To run it press the `Green Play Button` on the top of your screen.

_Step 9:_ If no files need to be modified, rename `maintest.py` to `main.py`. This will allow it to boot `main.py` if the device restarts and will not need `Thonny` to run it again.

_Tip:_ Use `Thonny` if you need/want to modify any of the files. If you are unable to see the files after renaming to `main.py`, you will need to upload a firmware that will rename `main.py` back to `main-1.py`. Here is the link to download a file named [`MicroPython_RenameMainDotPy`](https://forums.raspberrypi.com/download/file.php?id=45227&sid=cec97039a4f7ce336c4e816c979cb3d3). Follow the steps from the 'Uploading Firmware' section to upload `MicroPython_RenameMainDotPy.uf2` firmware. After it is done, upload `firmware.uf2`, which is located in the `firmware` folder, once again.

## Files
_main.py_: This is the main file that will run on boot.

_keycode.py_: This will hold all HID Keycodes.

_layout.py_: Pins for all components are assigned here, along with HID support.

_rgb.py_: Enter the RGB selection menu by selecting `RGB` on the screen using the rotary encoder. Select the color from the menu to be shown and it will be saved to `JSONFiles/save.json`.

_Test.py_: Allows for users to test the components and HID for the device. Enter it by pressing `Top Left, Bottom Right` buttons at the same time.

_colormemory.py_: Color memory game that will get flash colors in a certain order, and the user is required to repeat the order by selecting the colors. Enter Colormemory by selecting `Colormemory` on the screen using the rotary encoder. `Back` will remove the last character entered and it is done by pressing `Bottom Right`. To confirm the order you created, select `Confirm` by pressing `Bottom Right`.

_etch.py_: Etch is a way to draw on the device. Enter etch by selecting `Etch` on the screen using the rotary encoder. `Rotate` is the `Top Left` button, `Invert` colors is the `Top Right` button, `Clear` screen is `Middle Left` button, and `PC Draw` is `Middle Right` button. `PC Draw` will move the cursor on your screen along the same trace you drew on the device.

_Blackjack.py_: Enter blackjack by selecting `Blackjack` on the screen using the rotary encoder. Once you see `Play` press `Top Left` button. In the bet screen, use `Top Left` button to set increment to $10 or `Top Right` button to set increment to $100. Use rotary encoder and spin either right to increase bet or left to decrease bet. To `Confirm` bet, press `Bottom Left` button. `YTtl` is the total of your cards, and `DTtl` is the dealers total. To `Hit` press `Bottom Left` button and to `Stand` press `Bottom Right` button. $10000 will be added to the balance if a balance of $0 is reached.

_JSONFiles/save.json_: This is where the balance in `Blackjack.py`, last selected color for the RGB light, and the high score for `colormemory.py` is stored so it will always be saved.

_JSONFiles/color.json_: This is where the color and their color codes are stored to be used for the RGB light. This could be modified to add more colors.

_JSONFiles/macros.json_: The dictionary for the macros are stored here. This is where more macros are added.

## How-To Add Macros
The macros are stored in `JSONFiles/macros.json` and are editable. This is stored in a dictionary layout where items in the first indent are the categories, which are usually broad and are the items that are displayed in the main screen. The items in the next indent are the individual macros for that category. The first element will be the name of that macro. The name then contains three essential items which are the `type`, `wait` and `keys`.

There are three types which are `separate`, `together` and `control`. The `separate` type is when you want to press and release each individual key as it goes through the list of keys. With `together`, it will press all keys and release them at the same time. The final is `control` and this is for using consumer control elements such as play and pause.

The `wait` element is to let macro pad know how long to wait after a macro is selected to prevent the same macro from being selected inside the time frame. The time is in seconds.

The final option is `keys` and is what keys to be sent. The individual keys are separated by capitalization, so if we have _ABCOneBackspaceF2_, it would separate it as _A B C One Backspace F2_ and then type out _a b c 1_ and the press _Backspace_ and _F2_. All the names of the keys could be found in `keycode.py` and be used to make a macro.

There are many examples already made in `JSONFiles/macros.json` to get an idea of the layout.

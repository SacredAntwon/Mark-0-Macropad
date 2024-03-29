# Mark-0-Macropad

![Mark0](Images/mark0.gif)

## Parts List

_Microcontroller:_ Seeed Studio XIAO RP2040

_Screen:_ SSD1306 OLED 128x32

_Rotary Encoder:_ CYT1100

_Buttons x 6:_ 6x6x4.3mm 4 Pin Micro SMD

_Custom PCB:_ `gerber.zip` stored in `Board Design`

## Uploading Firmware

_Before you begin:_ If the macropad begins to run once it is connected to your computer, this means that device already has code in it that allows it to launch once connected to a system. In order to make modifications, `main.py` has to be renamed to `main-1.py`. Follow the `TIPS FOR EDITING` step in the `Uploading Code` category to do this.

_Step 1:_ Download the repository from GitHub. This is done by clicking the green button labeled `< > Code` on the top of the Mark-0 repository. On the drop down menu, select `Download ZIP` and a compressed folder will be installed on to your computer. Unzip this folder and the folder should be named `Mark-0-Macropad-main`.

_Step 2:_ With the device disconnected from the computer, hold the button labeled `boot` or `b` located on the bottom of the microcontroller which is below the macropad.

_Step 3:_ While holding the boot button on the device, plug it into the computer and let go of the boot button.

_Step 4:_ A new directory should now appear connected to your computer labled `RPI-RP2` for the macropad. There should be two files named `INDEX.HTM` and `INFO_UF2.TXT` and we will just leave them there.

_Step 5:_ Drag the file named `firmware.uf2`, which is located in the `Mark-0-Macropad-main/Firmware` folder , into the macropad directory and the macropad should then automatically reboot.

## Uploading Code

_Step 1:_ Install [`Thonny`](https://thonny.org) onto your system.

_Step 2:_ Once it is installed, click on `Tools` located on the top and then select `Options...`, which will make a menu appear. Select `Interpreter` from this menu. When it asks which interpreter you would like to use from the drop down, select `MicroPython (Raspberry Pi Pico)`. For the `Port` drop down selection, select a device that includes `COM`.

_Step 3:_ Exit the menu and select the `View` button on the top. Click on `Files` and a checkmark should appear next to it.

_Step 4:_ On the left side you will see the `Files` section, the top part being files on your computer and the bottom part being the files on the macropad which is labeled `Raspberry Pi Pico`.

_Step 5:_ If there are files in your macropad, select all of the files, right click on them and select to delete them from the macropad.

_Step 6:_ In the top portion of the `Files` section, find the folder named `Python Files` which should be downloaded from this repo.

_Step 7:_ Select all files in the `Mark-0-Macropad-main/Python Files` folder and right click on it. Select the option labeled `Upload to /` and all files should be uploaded to the device.

_Step 8:_ You could check if the files uploaded successfully by running `main-1.py`, which is a temporary name. To run it press the `Green Play Button` on the top of your screen. This is a good time to modify or add any of the files, including the macros.

_Step 9:_ If no files need to be modified, rename `main-1.py` to `main.py`. Thonny has no option to rename, so rename it on your computer. Delete `main-1.py` from the macropad and upload the renamed `main.py` from the computer to the macropad. This will allow it to boot `main.py` if the device restarts and will not need Thonny to run it again.

_TIPS FOR EDITING:_ Use `Thonny` if you need/want to modify any of the files. If you are unable to see the files after renaming to `main.py`, you will need to upload a firmware that will rename `main.py` back to `main-1.py`. Here is the link to download a file named [`MicroPython_RenameMainDotPy`](https://forums.raspberrypi.com/download/file.php?id=45227&sid=cec97039a4f7ce336c4e816c979cb3d3). Follow the steps from the `Uploading Firmware` section to upload `MicroPython_RenameMainDotPy.uf2` firmware. After it is done, upload `firmware.uf2`, which is located in the `Mark-0-Macropad-main/Firmware` folder, once again.

## Files

All of these files are located in `Python Files`.

-_main.py:_ This is the main file that will run on boot.

-_macropad.py:_ This is the program that will display an interactive menu to select different programs and categories. Option are selected by highlighting an item and clicking the rotary encoder.

-_logo.py:_ This will display the logo.

-_keycode.py:_ This will hold all HID Keycodes.

-_layout.py:_ Pins for all components are assigned here, along with HID support.

-_rgb.py:_ Enter the RGB selection menu by selecting `RGB` on the screen using the rotary encoder. Select the color from the menu to be shown and it will be saved to `JSONFiles/save.json`.

-_test.py:_ Allows for users to test the components and HID for the device. Enter it by pressing `Middle Left, Middle Right` buttons at the same time.

-_colormemory.py:_ Color memory game that will flash colors in a certain order, and the user is required to repeat the order by selecting the colors. Enter Colormemory by selecting `Colormemory` on the screen using the rotary encoder. `Back` will remove the last character entered and it is done by pressing `Bottom Right`. To confirm the order you created, select `Confirm` by pressing `Bottom Right`.

-_etch.py:_ Etch is a way to draw on the device. Enter etch by selecting `Etch` on the screen using the rotary encoder. `Rotate` is the `Top Left` button, `Invert` colors is the `Top Right` button, `Clear` screen is `Middle Left` button, and `PC Draw` is `Middle Right` button. `PC Draw` will move the cursor on your screen along the same trace you drew on the device.

-_blackjack.py:_ Enter blackjack by selecting `Blackjack` on the screen using the rotary encoder. Once you see `Play` press `Top Left` button. In the bet screen, use `Top Left` button to set increment to $10 or `Top Right` button to set increment to $100. Use rotary encoder and spin either right to increase bet or left to decrease bet. To `Confirm` bet, press `Bottom Left` button. `YTtl` is the total of your cards, and `DTtl` is the dealers total. To `Hit` press `Bottom Left` button and to `Stand` press `Bottom Right` button. $10000 will be added to the balance if a balance of $0 is reached.

-_/JSONFiles/save.json:_ This is where the balance in `blackjack.py`, last selected color for the RGB light, and the high score for `colormemory.py` is stored so it will always be saved. It also includes the last set brightness levels for both the RGB LED and OLED display.

-_/JSONFiles/color.json:_ This is where the color and their color codes are stored to be used for the RGB light. This could be modified to add more colors.

-_/JSONFiles/macros.json:_ The dictionary for the macros are stored here. This is where more macros are added.

-_/LogoAnimation:_ This is a folder that contains all the frames for the launch animation.

_MAIN MENU TIPS_

-Option to lower or higher the volume of the system it is connected to by holding `Top Left` button and turning the rotary encoder.

-Option to lower or higher the brightness of the macropads oled screen by holding `Top Right` button and turning the rotary encoder. There will be a percentage that appears on the top right of the screen that shows what the brightness is at. 0% is not off but it is the lowest brightness for the oled.

-Option to lower or higher the brightness of the macropads RGB LED by holding `Bottom Right` button and turning the rotary encoder. There will be a percentage that appears on the top right of the screen that shows what the brightness is at. 0% is off and 100% is at full brightness.

## How-To Add Macros

The macros are stored in `JSONFiles/macros.json` and are modifiable. This is stored in a dictionary layout where items in the first indent are the categories, which are usually broad and are the items that are displayed in the main screen. The items in the next indent are the individual macros for that category. The first element will be the name of that macro. The name then contains three essential items which are the `type`, `wait` and `keys`.

There are three types which are `separate`, `together` and `control`. The `separate` type is when you want to press and release each individual key as it goes through the list of keys. With `together`, it will press all keys and release them at the same time. The final is `control` and this is for using consumer control elements such as play and pause.

The `wait` element is to let macro pad know how long to wait after a macro is selected to prevent the same macro from being selected inside the time frame. The time is in seconds.

The final option is `keys` and this is what keys get sent to the system. The individual keys are separated by capitalization, so if we have _ABCOneBackspaceF2_, it would separate it as _A B C One Backspace F2_ and then type out _a b c 1_ press _Backspace_, _F2_. All the names of the keys could be found in `keycode.py` and be used to make a macro.

There are many examples already made in `JSONFiles/macros.json` to get an idea of the layout.

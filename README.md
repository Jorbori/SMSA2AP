# SMSA2

Prerequisites
- Download Archipelago Launcher: https://github.com/ArchipelagoMW/Archipelago/releases
- Download Dolphin Emulator: https://dolphin-emu.org/download/
- Patch legally obtained USA Super Mario Sunshine iso with Super Mario Sunshine Arcade 2: https://gamebanana.com/mods/563498
- (Optional) Download the most recent version of Universal Tracker: https://github.com/FarisTheAncient/Archipelago/releases

Adding the .apworld to your custom_worlds
[Option 1]
1. Open the smsa2.apworld file. This will create a copy in the custom_worlds folder
[Option 2]
1. Open the Archipelago launcher
2. Locate the **Browse Files** option and select it. This will open a new File Explorer window
3. Within the Archipelago folder, locate and open the **custom_worlds** folder
4. Move the *smsa2.apworld* file into this folder
5. Close the File Explorer Window

NOTE: These steps should be repeated for the tracker.apworld file if you wish to take advantage of Universal Tracker support

Adding the Gecko Codes to Dolphin
1. Navigate to the main menu in the Dolphin Emulator
2. Locate and select the File option along the ribbon
3. Within the File dropdown, locate and select the Open **User Folder** option. This will open a new File Explorer window
4. Within the Dolphin Emulator folder, locate and open the "GameSettings" folder
5. Move the *GMSE21.ini* file into this folder
6. Close the File Explorer Window

Enabling the Gecko Codes
1. Navigate to the main menu in the Dolphin Emulator
2. Locate and select the **Config** option. This will open a new Dolphin Settings window
3. Within the Settings window, make sure you are in the **General** tab. This should be the default tab after selecting Config
4. Within the General tab, locate and enable the **Enable Cheats** option
5. Close the Dolphin Settings window

Verify the Gecko Codes are Correctly Set Up
1. Navigate to the main menu in the Dolphin Emulator
2. Locate your copy of Super Mario Sunshine Arcade 2 within the available games and right-click it
3. Within the right-click dropdown, locate and select the **Properties** option. This will open a new Dolphin Settings window
4. Within the Settings window, locate and select the **Gecko Codes** tab
5. Make sure that there is a list of Gecko Codes in the Gecko Codes tab and that they are enabled. If not, revisit the "Adding the Gecko Codes to Dolphin" instructions and make sure you moved your *GMSE21.ini* file to the correct folder
6. Make sure that there is no warning that cheats aren't enabled. If there is, click the provided **Configure Dolphin** button. This will open a new Dolphin Settings window. Revisit steps 3-5 of "Enabling the Gecko Codes"

Connecting to Your Multiworld Slot
1. Navigate to the main menu in the Dolphin Emulator
2. Locate your copy of Super Mario Sunshine Arcade 2 within the available games and left-click it
3. Locate and select the **Play** option. This will open a new Dolphin Emulator window and begin running Super Mario Sunshine Arcade 2
4. In the game, press *start* at the title screen, but do not select a file to begin playing
5. Open the Archipelago Launcher
6. Locate the **Super Mario Sunshine Arcade 2 Client** option and select it. This will open a new Archipelago Client window
7. Within the Client, ensure the text terminal in the **Archipelago** tab says "Dolphin Connected Sucessfully"
8. Type your room code and information into the textbox along the top of the window and click the **Connect** button
9. Input your password (if necessary) and your slot name when prompted

Other Gameplay Instructions
- The hub world consists of 12 sets of pipes. Each of these sets represents a world, and each world has 8 levels. The levels are organized within each set like this:
████████LAND███████
████           ████
████ [7]   [8] ████
████           ████
███             ███
███ [5]     [6] ███
███             ███
██               ██
██ [3]       [4] ██
██               ██
█                 █
█ [1]         [2] █
█                 █
~ ~ ~ ~WATER~ ~ ~ ~

- The secondary nozzles you recive can be switched to using the D-Pad. The Commands are as follows:
Hover Nozzle: Left
Rocket Nozzle: Up
Turbo Nozzle: Right

- You can access levels using thier associated level Ticket. Each ticket has a name titled "World 1 Ticket" Through "World 12 Ticket". Each ticket unlocks its associated World's levels 1 through 8, with the exception of the following:
World 1: Levels 1-6 and 1-8 are not in the randomizer due to issues with the memory addresses of thier Shine Sprites and Blue Coins
World 12: Level 12-8 is the Goal Level and has it's own ticket

For any remaining issues, as well as other information about the randomizer, please visit the SMSA2AP Dev Documents at https://docs.google.com/spreadsheets/d/1GR2YlgtzbS9nE8lbuc8qBnGu7zM443l06eFABxiX4w4/edit?usp=sharing

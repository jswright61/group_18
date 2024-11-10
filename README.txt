What is SlideScape?
     SlideScape is a fun and interactive game specifically designed to engage minds with an intriguing sliding number puzzle with a twist of urgency due to the included timer. SlideScape was created by "Group 18" as a Programming Problem Solving project at Kennesaw State University. [Group 18 includes: Ernie Fichtel, Scott Wright, Oneeb Khan, and Sequoya Jackson]

How to Play:
     The object of the game is to slide each number tile one-by-one to put them in ascending order from left to right and top to bottom. When a tile with an empty space next to it is clicked, the tile will then move into that empty space. The user must maneuver these tiles skillfully until the tiles are in the correct ascending order starting from the lowest number at the top left corner to the largest number at the bottom right.

Installation:
     PyCharm Instructions~
        Download Group18.zip file. Unzip the file into a new directory.
        Open PyCharm IDE and create a project. Name it SlideScape.
        Go to file at the top left. Click on settings. Press the '+' and type 'Pygame'. Click 'install package' and then click 'ok'.
        Go to File Explorer (Windows) or the Finder (Mac) and copy all the extracted files and paste/move them to the SlideScape directory in PyCharm.
        All files will be pasted under the scripts directory.
        Select 'SlideScape.py'
        Optional: click the 3 vertical dots to the right of the debug option. Under configutration select 'Edit' in the Script Parameters box enter any Command Line arguments you wish. Each argument should be in double quotes and separated by a space.
        Click the run icon to start the game.

Special Keys:
        Ctrl + u ~ Increases the volume level of the background music. [Supplementary sound effects are still active.]
        Ctrl + d ~ Decreases the volume level of the background music. [Supplementary sound effects are still active.]
        Ctrl + m ~ Mutes background music. [Supplementary sound effects are still active.]
        Escape Key ~ Immediately exits the program from any screen.
        Ctrl + e [ONLY IN CHEAT MODE] ~ Causes the timer to drop to 5 seconds to check the time expiration.
        Ctrl + c [ONLY IN CHEAT MODE] ~ Rearranges the tiles to display obvious moves to win the game quickly.
        Ctrl + p [ONLY IN DEBUG MODE] ~ pauses the user in a Python REPL where the user has the ability to observe variables.

Command Line Arguments:
     There are several Command Line arguments that can alter certain aspects of the game.
     Command Line arguments ase words, separated by spaces, after the program name when launching. The order does not matter. They can appear in any order.
     example:
     $ python3 SlideScape.py cheat mute

     The following is a list of Command Line Arguments with a very brief description of what each does:
     cheat - Enables Cheat mode (see special keys section).
     debug - Enables Debug Mode (see special keys section) plus additional logging to the console.
     mute - Gameplay starts with backround music muted.
     skip_instructions - Goes right to the Gameplay on launch, skipping the instructions screen (unless show_instructions argument is also present).
     show_instructions - Will ALWAYS show instructions when game is launched, regardless of the presence of the "skip_instructions.txt" file or the skip_instructions Command Line Argument.

Control Files:
     The existence of a file named "skip_instructions.txt" in the same folder as "SlideScape.py" will have the same effect as as the skip_instructions Command Line Argument.
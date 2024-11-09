                                                       README.TXT
What is SlideScape?

     SlideScape is a fun and interactive game specifically designed to engage minds with an intriguing sliding number puzzle with a twist of urgency due to the included timer. SlideScape was created by "Group 18" as a Programming Problem Solving project at Kennesaw State University. [Group 18 includes: Ernie Fichtel, Scott Wright, Oneeb Khan, and Sequoya Jackson]


How to Play:

     The object of the game is to slide each number tile one-by-one to put them in ascending order from left to right and top to bottom. When a tile with an empty space next to it is clicked, the tile will then move into that empty space. The user must maneuver these tiles skillfully until the tiles are in the correct ascending order starting from the lowest number at the top left corner to the largest number at the bottom right.

Installation:
     PyCharm Instructions~

        Download SlideScape.py zip file. Then open the file from File Explorer and extract the files.

        Open PyCharm IDE and create a project. Go to file at the top left. Click on settings. Press the '+' and type 'Pygame'. Click 'install package' and then click 'ok'.

        Go to file explorer and copy all the extracted files and paste/move them to the SlideScape directory in PyCharm.

        All files will be pasted under the scripts directory. Click 'SlideScape.py' and run the game.




Special Keys:

        Ctrl + e [ONLY IN CHEAT MODE] ~ Causes the timer to drop to 5 seconds to check the time expiration.

        Ctrl + c [ONLY IN CHEAT MODE] ~ Rearranges the tiles to display obvious moves to win the game quickly.

        Ctrl + p [DEBUG] ~ pauses the user in a Python REPL where the user has the ability to observe variables and extends supplementary output.

        Ctrl + u ~ Increases the volume level of the background music. [Supplementary sound effects are still active.]

        Ctrl + d ~ Decreases the volume level of the background music. [Supplementary sound effects are still active.]

        Ctrl + m ~ Mutes background music. [Supplementary sound effects are still active.]

        Shift + esc ~ Immediately exits gameplay on any screen.

       "skip_instructions ~ Allows user to launch into gameplay rather than an instruction screen.

           To immediately launch into gameplay and skip the instructions screen a file labeled "skip_instructions.txt" should be present in the same directory as the game file

           Run the following command from your terminal in the same directory where your game exists: "touch skip_instructions.txt"

To use these special keys, click the 3 vertical dots at the top of the screen next to 'play' and 'debug'. Click 'edit configurations' and in the script parameters enter "cheat" "debug" [with quotes and space in between]. Save that configuration and run SlideScape.


Troubleshooting FAQ:

Cheat Codes~ Launch SlideScape in terminal. Enter 'python3 SlideScape.py cheat'.

<div align="center">    
 
<!--- DO NOT FORGET TO REMOVE ALL THE COMMENTS -->  
  
# EvoCraft-SCOPE  
 
<!--- MIGHT NEED SOME EDITING. DON'T THINK THIS IS COMPLETE --> 
 This project focuses on using Compositional Pattern Producing Networks (a form of neural network) and [**NeuroEvolution of Augmenting Topologies**](https://www.cs.ucf.edu/~kstanley/neat.html) (a form of evolutionary computation) to create different structures in Minecraft. Shapes can be evolved interactively, with a fitness function, or using [**Novelty Search**](http://eplex.cs.ucf.edu/noveltysearch/userspage/). This repository was made in the summer of 2022 as a part of [**SCOPE**](https://www.southwestern.edu/undergraduate-research/scope/), an undergraduate research summer program at [**Southwestern University**](https://www.southwestern.edu/), under the supervision of [**Dr. Schrum**](https://people.southwestern.edu/~schrum2/).
<!--- DO NOT FORGET TO SITE THE TWO SOURCES -->  
<!--- IS THIS WHERE THE SOURCES NEED TO BE SITED? OR SHOULD IT BE SOMEWHERE ELSE? -->
<!--- RIGHT NOW JUST THE LINKS ARE HERE. NEEDS TO CITED IT BETTER. -->  

</div>

<!--- THE BATCH FILE TAKES AWAY THE NEED -->
### 1. Set-up
<!--- AFTER LAYOUT AND TEXT IS MORE OR LESS PLACED, FIND WAY TO MAKE LOOK CLEANER BY INDENTING  --> 

NOTE: This code only works with Python 3.7 and 3.8!

1. Install Java 8 (a.k.a. 1.8). You can check what version you currently have with `java -version`
    - Unix: `sudo apt-get install openjdk-8-jre`
    - OSX:
        - brew tap AdoptOpenJDK/openjdk
        - brew cask install adoptopenjdk8 
        - If you have trouble installing, look at [**How to install Java JDK on macOS**](https://mkyong.com/java/how-to-install-java-on-mac-osx/)
    - Windows: [**Java for Windows 8**](https://www.oracle.com/java/technologies/downloads/#java8)

2. Clone repo:
    - `git clone https://github.com/schrum2/EvoCraft-SCOPE.git`

3. Run the batch file `SetUpServer.bat` (Windows only). By doing this, it will:
    - pip install the requirements.txt file
    - Create a copy of the `EvoCraft-py-Backup` directory under the name `EvoCraft-py` (different command needed on Mac/Linux/Unix)

4. Run the batch file `LaunchServer.bat` in the root project directory (launches the `spongevanilla-1.12.2-7.3.0.jar` file in `EvoCraft-py`)
    - Will setup some extra files associated with the server, but the server cannot run properly until the next step is completed.

5. Change the `eula=true` in the `eula.txt` file located in the `EvoCraft-py` copy

You can now connect to the server by launching minecraft!

To connect to the server from within the game:
1. Make sure the batch file `LaunchServer.bat` is running and the `eula` is set to `true`.
2. Open up the minecraft launcher, and play the java edition 1.12.2
3. Select the gamemode Multiplayer.
4. Select Direct Connect, and in the server address box, type 'localhost'.
5. Join Server!

<!--- ANOTHER PICTURE THAT NEEDS TO BE RECONSIDERED -->
![localhost login](/images/localhost_login.png)
<!--- THINK OF A BETTER NAME FOR THIS HEADING -->

### 3. Recommendations
If you run `python main.py --help`, then you will be able to see all of the available command line parameters that can be changed when running `main.py`.

<!--- RECONSIDER IMAGE HERE. -->
![help in cmd](/images/Command_Line_Parameters.png)

There are also different batch files that you can run. These batch files are in the directory `batch` and execute the `main.py` script in combination with some commonly used command line parameter sets.

You can run a batch file by:
1. Opening a command prompt in one of the three sudirectories (`Fitness-Functions`, `Interactive-Evolution`, and `Novelty-Search`) in the directory called `batch`.
2. Type in the apporpriate name of the batch file you want to run (or press tab to look for a batch file that interests you).
3. Include a space followed by any digit within the range of 0-100. This value will be the random seed for the world and is required for the batch files to run.

Here's an example of what it would look like for a fitness function:
```
.\FitnessFillSpaceSnakes.bat 0
```

Currently, you can select from three types of batch files:
- Fitness functions: This set runs different tests that  attempt to maximize the space with certain blocks by generating snakes or cubes.
- Interactive evolution: This set allows you as the player to choose what kind of structures (snakes or cubes) should continue to generate either through the console or through in-game input. You can select any of the structures by right clicking the levers that are before each structure. Then when you are finished selecting your favorites, you can press any of the buttons that are on the switches nearest to you to start the next generation. In `InteractiveInGameCube.bat`, you are also able to change the blocks that are present in each structure. Simply destroy any of the blocks that are behind the switches and replace it with any block you like. Run this command to try it:
```
.\InteractiveInGameCubes.bat 0
```
![interactive instructions](/images/Instructions-Interactive-Evolution.png)
- Novelty search: This set runs a type of exploration algorithm that tests many different aspects of snake or cubic generation
<!--- CHECK AGAIN IF THE RANGE OF RANDOM SEEDS IS 0-100 AND IF THAT IS INCLUSIVE/EXCLUSIVE --> 

<!--- ASK IF THERE SHOULD BE ANY MENTION OF THE PYTESTS IN HERE. -->

<!--- NEED BETTER WAY TO WORD THIS SECTION -->
#### This repository utilizes/builds upon/expands on the following repositories
- [**neat-python**](https://github.com/CodeReclaimers/neat-python)
- [**Evocraft-py**](https://github.com/real-itu/Evocraft-py)

#### Contributors
- Dr. Jacob Schrum
- Melanie Richey
- Mark Mueller
- Alejandro Medina

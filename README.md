<div align="center">    
 
<!--- DO NOT FORGET TO REMOVE ALL THE COMMENTS -->  
  
# EvoCraft-SCOPE  
 
<!--- RIGHT HERE THERE NEEDS TO BE SOME SORT OF "INTRODUCTION" OR SHORT EXPLANATION OF WHAT THIS REPOSITORY IS (LIKE MOST OF THE OTHER REPOS DO) --> 
 
<!--- DO NOT FORGET TO SITE THE TWO SOURCES -->  
<!--- IS THIS WHERE THE SOURCES NEED TO BE SITED? OR SHOULD IT BE SOMEWHERE ELSE? -->
<!--- RIGHT NOW JUST THE LINKS ARE HERE. NEEDS TO CITED IT BETTER. -->  

</div>

<!--- THE BATCH FILE TAKES AWAY THE NEED -->
### 1. Install Requirements
<!--- AFTER LAYOUT AND TEXT IS MORE OR LESS PLACED, FIND WAY TO MAKE LOOK CLEANER BY INDENTING  --> 

1. You need to install this project's dependencies by running `pip install --user -r requirements.txt` (the version for python needs to be 3.7+)

<!--- CONSIDER COMBINING #1 AND #2 INTO ONE HEADING AREA -->

### 2. Server Setup
Before you begin setting up your server directory, you should look at the setup steps in [**Evocraft-py**](https://github.com/real-itu/Evocraft-py).
There you can also find useful minecraft commands that you may need.

To set up  the server directory:
1. Make a copy of the directory called `EvoCraft-py-Backup`.
2. Rename the newly made copy `EvoCraft-py`.
3. Launch the batch file `LaunchServer.bat` to launch the server stored there (you will have to set the eula to true first).

You can now connect to the server by launching minecraft!
To connect to the server from within the game:
1. Make sure the batch file `LaunchServer.bat` is running and the eula is set to true.
2. Open up the minecraft launcher, and play the java edition 1.12.2
3. Select the gamemode Multiplayer.
4. Select Direct Connect, and in the server address box, type 'localhost'.
5. Join Server!

<!--- ANOTHER PICTURE THAT NEEDS TO BE RECONSIDERED -->
<img src="https://user-images.githubusercontent.com/100097809/171940906-a4be83fd-0825-4cdf-b339-01d8810a1b01.png" width="500">
<!--- THINK OF A BETTER NAME FOR THIS HEADING -->

### 3. Recommendations
If you run `python main.py --help`, then you will be able to see all of the available command line parameters that can be changed when running `main.py`.

<!--- RECONSIDER IMAGE HERE. -->
![help in cmd](https://user-images.githubusercontent.com/100097809/171904819-f48e61f5-7746-47da-b94f-db2d100d32bc.png)

There are also batch files that you can run. These batch files are in the directory `batch` and execute the `main.py` script in combination with some commonly used command line parameter sets. 
You can run a batch file by:
1. Opening a command prompt in the directory `batch`.
2. Type in the apporpriate name of the batch file you want to run (or press tab to look for a batch file that interests you).
3. Include a space followed by any digit within the range of 0-100. This value will be the random seed for the world and is required for the batch files to run. 
<!--- CHECK AGAIN IF THE RANGE OF RANDOM SEEDS IS 0-100 AND IF THAT IS INCLUSIVE/EXCLUSIVE --> 

<!--- ASK IF THERE SHOULD BE ANY MENTION OF THE PYTESTS IN HERE. -->

<!--- NEED BETTER WAY TO WORD THIS SECTION -->
#### This repository utilizes/builds upon/expands on the following repositories
- [**neat-python**](https://github.com/CodeReclaimers/neat-python)
- [**Evocraft-py**](https://github.com/real-itu/Evocraft-py)

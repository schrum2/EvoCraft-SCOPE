<div align="center">    
 
<!--- DO NOT FORGET TO REMOVE ALL THE COMMENTS -->  
  
# EvoCraft-SCOPE  
  
A Python interface for Minecraft built on [grpc](https://github.com/real-itu/minecraft-rpc). 

<!--- DO NOT FORGET TO SITE THE TWO SOURCES -->  
<!--- IS THIS WHERE THE SOURCES NEED TO BE SITED? OR SHOULD IT BE SOMEWHERE ELSE? -->
  
**Site original EvoCraft repo**
<br>
**Site original NEAT-Python**

</div>

<!--- THE BATCH FILE TAKES AWAY THE NEED -->
### 1. Install Requirements

<!--- AFTER LAYOUT AND TEXT IS MORE OR LESS PLACED, FIND WAY TO MAKE LOOK CLEANER BY INDENTING  --> 

- You can install the project's dependencies by running `pip install --user -r requirements.txt`

<!--- CONSIDER COMBINING #1 AND #2 INTO ONE HEADING AREA -->

### 2. Server Setup
To set up  the server directory:
1. Make a copy of the directory called `EvoCraft-py-Backup`.
2. Rename the newly made copy `EvoCraft-py`.
3. Launch the batch file `LaunchServer.bat` to launch the server stored there (you will have to set the eula to true first).

You can now connect to the server by launching minecraft!
To connect to the server from within the game:
1. Make sure the batch file `LaunchServer.bat` is running and the eula is set to true.
2. Open up the minecraft launcher, and play the jave edition 1.12.2
3. Select the gamemode Multiplayer.
4. Select Direct Connect, and in the server address box, type 'localhost'.
5. Join Server!

<!--- THINK OF A BETTER NAME FOR THIS HEADING -->
### 3. Recommendations
If you run `python main.py --help`, then you will be able to see all of the available command line parameters that can be changed when running `main.py`.


<!--- RECONSIDER IMAGE HERE. -->
![help in cmd](https://user-images.githubusercontent.com/100097809/171904819-f48e61f5-7746-47da-b94f-db2d100d32bc.png)

There are also batch files that you can run. These batch files are in the directory `batch` and execute the `main.py` script in combination with some commonly used command line parameter sets. 
You can run a batch file by:
1. Opening a command prompt in the directory `batch`.
2. Tpye in the apporpriate name of the batch file you want to run (or press tab to look for a batch file that interests you).
3. Include a space followed by any digit within the range of 0-100. This value will be the random seed for the world and is required for the batch files to run. 
<!--- CHECK AGAIN IF THE RANGE OF RANDOM SEEDS IS 0-100 AND IF THAT IS INCLUSIVE/EXCLUSIVE --> 

<!--- ASK IF THERE SHOULD BE ANY MENTION OF THE PYTESTS IN HERE. -->

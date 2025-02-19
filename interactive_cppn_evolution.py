"""
Code originally taken from the offline simplified version of Picbreeder
that comes with NEAT-Python. Just wanted a starting point for evolving CPPNs.
Modifying the code to apply to Minecraft.
"""
# For CPPNs and NEAT
import neat
import custom_genomes as cg

# for Minecraft
import grpc
import minecraft_pb2_grpc
from minecraft_pb2 import *

# For minecraft generation
import minecraft_structures
import threading
import os


# For CPPN generations
import cppn_generation
class MinecraftBreeder(object):
    def __init__(self, args, block_list):
        """
        Construct a class for evolving Minecraft shapes
        interactively. The shapes are generated by CPPNs.

        Parameters:
        args (argparse.Namespace): Command line parameter bundle
        block_list ([int]): List where each int represents a Minecraft block type.
                            This will be empty if block lists are maintained within
                            each genome rather than shared among them.
        """
        self.args = args
        self.block_list = block_list

        self.position_information = dict()
        self.position_information["startx"] = 0
        self.position_information["starty"] = 5
        self.position_information["startz"] = 0
        self.position_information["xrange"] = self.args.XRANGE
        self.position_information["yrange"] = self.args.YRANGE
        self.position_information["zrange"] = self.args.ZRANGE

        # Connect to Minecraft server
        channel = grpc.insecure_channel('localhost:5001')
        self.client = minecraft_pb2_grpc.MinecraftServiceStub(channel)

        if(self.args.IN_GAME_CONTROL):
            t = threading.Thread(target=self.console_reset,args=())
            t.start()

        self.reset_ground_and_numbers()

        # If EVOLVE_SNAKE is true, it will generate a snake,
        # otherwise it will create the normal structures
        self.query_cppn = cppn_generation.query_cppn_for_snake_shape if self.args.EVOLVE_SNAKE else cppn_generation.query_cppn_for_shape

        self.generation = 0

    def reset_ground_and_numbers(self):
        """
        Resets the ground and numbers above the shapes. Extracted from __init__
        """
        # Restore ground at the start of evolution
        minecraft_structures.restore_ground(self.client, self.position_information, self.args.POPULATION_SIZE, self.args.SPACE_BETWEEN)

        self.place_0_to_9()
        
    def place_0_to_9(self):
        """
            Place the numbers 0 to 9 above shapes to help identify them for selection
        """
        # Figure out the lower corner of each shape in advance
        self.corners = []
        for n in range(self.args.POPULATION_SIZE):
            corner = (self.position_information["startx"] + n*(self.position_information["xrange"]+2+self.args.SPACE_BETWEEN), self.position_information["starty"], self.position_information["startz"])
            self.corners.append(corner)
            # Place the numbers just once. Only works for 0-9
            minecraft_structures.place_number(self.client,self.position_information,corner,n)


    def eval_fitness(self, genomes, config):
        """
        This function is expected by the NEAT-Python framework.
        It takes a population of genomes and configuration information,
        and assigns fitness values to each of the genome objects in
        the population. Nothing is returned, since the genomes themselves
        are modified.
        
        Parameters:
        genomes ([DefaultGenome]): list of CPPN genomes
        config  (Config): NEAT configurations
        """                                                                                                                    
        self.current_genomes = genomes
        self.current_config = config
        all_blocks = []
        try:
            all_blocks = self.clear_area_and_generate_shapes(genomes, config)  
            if self.args.IN_GAME_CONTROL:
                selected = self.in_game_control_options(genomes, config)
            else:
                # Controlled externally by keyboard
                # Creates a string that is the user's input, then either resets or quits the program, saves it, or converts it into a list of selected shapes
                vals_selected = False
                selected_vals = []
                while(not vals_selected):
                    vals = input("Select the shapes you like, or type r to reset,q to quit, or s to save:")
                    if(vals=='r'): # Resets structures and shapes
                        self.reset_ground_and_numbers() #resets ground and numbers
                        self.clear_area_and_generate_shapes(self.current_genomes, self.current_config) #resets shapes and fences
                    elif vals== 'q': # Quits the program
                        quit()
                    elif vals== 's':   
                        self.save_by_user(config, genomes)
                    else:
                        try: # Otherwise, tries to split string with spaces of values for selection. If it can't loops through again
                            split_vals = vals.split(' ')
                            selected_vals = list(map(int,split_vals))
                            vals_selected = True
                        except ValueError:
                            print("This command was not recognized. Please try again")
                            vals_selected = False #turns back to false if not able

                # Initialize to all False
                selected = [False for i in range(config.pop_size)]
                # Then set to True for the items that are selected
                for ind in selected_vals:
                    selected[ind] = True
            
            print("Selected: {}".format(selected))
            for n, (genome_id, genome) in enumerate(genomes):
                if selected[n]:
                    genome.fitness = 1.0
                else:
                    genome.fitness = 0.0
                print("{}. {}: {}".format(n,genome_id,genome.fitness))

            if self.args.USE_ELITISM:
                # To assure that all selected individuals survive, the elitism setting is changed
                elite_count = int(sum(map(lambda b : 1 if b else 0, selected)))
                print("{} elite survivors".format(elite_count))
                config.reproduction_config.elitism = elite_count

        finally:
            # Take the originally generated shape and replace each block with AIR,
            # then spawn the blocks to clear the previous shape, even if parts were
            # out of bounds (mainly an issue for snakes)
            for s in all_blocks:
                s.type = AIR

            self.client.spawnBlocks(Blocks(blocks=all_blocks))

        self.generation += 1

    def save_by_user(self, config, genomes):
        """
        Generates new directories, or accesses them if they exist, and then saves the infromation
        on the shapes generated to the computer

        Parameters: 
        config  (Config): NEAT configurations
        genomes ([int,DefaultGenome]): list of tuples of id numbers and genome pairs
        """
        # Build dictionary out of the lisst of 2-tuples
        population = {}
        for (genome_id, genome) in genomes:
            population[genome_id] = genome

        base_path = '{}'.format(self.args.BASE_DIR)
        dir_exists = os.path.isdir(base_path)
        if not dir_exists:
            os.mkdir(base_path)
    
        # Makes a sub dir too
        sub_path = '{}/{}{}'.format(base_path,self.args.EXPERIMENT_PREFIX,self.args.RANDOM_SEED)
        dir_exists = os.path.isdir(sub_path)
        if not dir_exists:
            os.mkdir(sub_path)
                        
        # Makes one more method
        pop_path = '{}/gen/'.format(sub_path)
        dir_exists = os.path.isdir(pop_path)
        if not dir_exists:
            os.mkdir(pop_path)

        checkpointer = neat.Checkpointer(self.args.CHECKPOINT_FREQUENCY, self.args.TIME_INTERVAL, "{}gen".format(pop_path))
        print(self.generation)
        checkpointer.save_checkpoint(config, population, neat.DefaultSpeciesSet, self.generation)

    def clear_area_and_generate_shapes(self, genomes, config):
        """
        Clears the area and generates the shapes based on genomes. Then also places the fences.
        Extracted from eval_fitness

        Parameters:
        genomes([DefaultGenome]): list of CPPN genomes
        config(Config): NEAT configurations

        Return:

        all_blocks(list of Blocks): Stores info as to where blocks were placed for deleting snakes
        """
        all_blocks = []
        #clears area for structures
        minecraft_structures.clear_area(self.client, self.position_information, self.args.POPULATION_SIZE, self.args.SPACE_BETWEEN, self.args.MAX_SNAKE_LENGTH) 
        self.place_0_to_9()
        # This loop could be parallelized
        #for n, (genome_id, genome) in enumerate(genomes):
        for n in range(self.args.POPULATION_SIZE):
            (genome_id, genome) = genomes[n]
            # See how CPPN fills out the shape
            print("{}. {}: ".format(n,genome_id), end = "") # Preceding number before info from query
            shape = self.query_cppn(genome, config, self.corners[n], self.position_information, self.args, self.block_list)
            shape_set = (list(set(map(lambda x: BlockType.values()[x.type], shape))))

            if self.args.BLOCK_LIST_EVOLVES:
                minecraft_structures.place_blocks_in_block_list(genome.block_list,self.client,self.corners[n],self.position_information,shape_set,self.args.ONLY_SHOW_PLACED)
            # fill the empty space with the evolved shape
            self.client.spawnBlocks(Blocks(blocks=shape))
            # Remember block locations in order to clear them out later
            all_blocks.extend(shape) # Blocks from all shapes in one flat list
            # Place the fences where the shape will appear
            minecraft_structures.place_fences(self.client, self.position_information, self.corners[n])
        return all_blocks

    def in_game_control_options(self, genomes, config):
        """
        Has the loop that allows for in game controls. Loops until a selection has been made. Extracted
        from eval_fitness

        Parameters:
        genomes([DefaultGenome]): list of CPPN genomes
        config(Config): NEAT configurations

        Return:
        selected (list of booleans): List that determines which shapes the user selected
        """
        #generates switches and gets locations to read for
        (on_block_positions,next_block_positions) = minecraft_structures.player_selection_switches(self.client, self.position_information, self.corners)

        selected = [False for _ in range(config.pop_size)] #initializes selected as a list of False's
        player_select_done = False
            
        while not player_select_done: #player is still selecting
                # constantly reads the position right below the redstone lamp
                # to see if the player has switched on a lever
            for i in range(config.pop_size):
                first = on_block_positions[i]
                blocks = self.client.readCube(Cube(
                        min=Point(x=first[0], y=first[1], z=first[2]),
                        max=Point(x=first[0], y=first[1], z=first[2])
                    ))
                selected[i] = blocks.blocks[0].type == REDSTONE_BLOCK
            player_select_done = False
            j = 0
                # Checks the hidden DIAMOND BLOCK associated with each next generation switch. 
                # If any one is sensed, then player selection is done 
            while not player_select_done and j < config.pop_size:
                pressed = next_block_positions[j]
                done_button = self.client.readCube(Cube(
                        min=Point(x=pressed[0], y=pressed[1]-1, z=pressed[2]),
                        max=Point(x=pressed[0], y=pressed[1]-1, z=pressed[2])
                    ))
                player_select_done = done_button.blocks[0].type == DIAMOND_BLOCK
                j += 1
                    
            if self.args.BLOCK_LIST_EVOLVES:
                    # TODO: This will currently only work with in-game selection, but not with console-based selection. Need to fix.

                # Reads in the blocks and stores them
                read_current_blocks=minecraft_structures.read_current_block_options(self.client,self.corners,self.position_information)

                # Compares each index of the block lists of the genome to what was read in.
                for n, (_, genome) in enumerate(genomes):
                    if(genome.block_list != read_current_blocks[n]):
                        for i in range(len(genome.block_list)):
                                # If there was a difference, and it wasn't air, it replaces the blocks in the block_list and regenerates the structure 
                            if genome.block_list[i] != read_current_blocks[n][i] and read_current_blocks[n][i] != AIR:
                                print(genome.block_list)
                                    # print("Genome {} swaps {} for {}".format(genome.key, BlockType.keys()[genome.block_list[i]], BlockType.keys()[read_current_blocks[n][i]]))
                                genome.block_list[i]=read_current_blocks[n][i]
                                new_shape = self.query_cppn(genome, config, self.corners[n], self.position_information, self.args, self.block_list)
                                self.client.spawnBlocks(Blocks(blocks=new_shape))
    
        return selected

    def console_reset(self):
        """
        Continusouly prompts the user for a letter. r resets everything that was generate s saves the shapes, and q quits the program. Any
        other letter asks for the user to try again. This is multithreaded so that it runs in the background while 
        the rest of the code does its thing. If anything gets destroyed, reset ensures its still usuable
        """
        while 1:
            val = input("Press r to reset the world,q to quit, or s to save\n")
            if(val=='r'):
                self.reset_ground_and_numbers() #resets ground and numbers
                self.clear_area_and_generate_shapes(self.current_genomes, self.current_config) #resets shapes and fences
                minecraft_structures.player_selection_switches(self.client, self.position_information, self.corners) #resets switches
            elif(val=='q'):
                os._exit(0)
            elif val== 's':   
                self.save_by_user(self.current_config, self.current_genomes)
            else:
                print("This command was not recognized. Please try again")
                
if __name__ == '__main__':
    print("Do not launch this file directly. Launch main.py instead.")
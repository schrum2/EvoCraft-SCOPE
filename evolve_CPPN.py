"""
Code originally taken from the offline simplified version of Picbreeder
that comes with NEAT-Python. Just wanted a starting point for evolving CPPNs.
Modifying the code to apply to Minecraft.
"""
# Are these still needed?
from http import client
import math
import os
import pickle

# For CPPNs and NEAT
import neat
import custom_genomes as cg

# for Minecraft
import grpc
import minecraft_pb2_grpc
from minecraft_pb2 import *

# For utility functions
import util

# For minecraft structures
import minecraft_structures

# For InteractiveStagnation class
import neat_stagnation

BLOCK_LIST_EVOLVES = True
BLOCK_LIST_SIZE = 5

class MinecraftBreeder(object):
    def __init__(self, args, block_list):
        """

        UPDATE THIS!

        :param xrange: range of x-coordinate values rendered
        :param zrange: range of y-coordinate values rendered
        :param xrange: range of z-coordinate values rendered
        """
        self.args = args
        self.block_list = block_list

        self.startx = 0
        self.starty = 5
        self.startz = 0
        
        self.generation = 0
        self.xrange = self.args.XRANGE
        self.yrange = self.args.YRANGE
        self.zrange = self.args.ZRANGE
        
        # Don't try any multithreading yet
        self.num_workers = 1

        # Connect to Minecraft server
        channel = grpc.insecure_channel('localhost:5001')
        self.client = minecraft_pb2_grpc.MinecraftServiceStub(channel)

        # Place numbers 0-9, use yrange + 2
        for i in range(10): # Problems if pop_size is not 10!
            minecraft_structures.place_number(self.client,self.startx+(i*(self.xrange+1))+int(self.xrange/2),self.starty+self.yrange+2,self.startz,i)

    def query_cppn_for_shape(self, genome, config, corner, xrange, yrange, zrange):
        """
        Query CPPN at all voxel coordinates to generate the list of
        blocks that will eventually be rendered in the Minecraft server.

        Parameters:
        genome (DefaultGenome): A CPPN or some class that extends CPPNs
        config (Config): NEAT configurations
        corner (int,int,int): three-tuple of initial x,y,z coordinates
        xrange (int): number of voxel blocks for each shape along x-dimension
        yrange (int): number of voxel blocks for each shape along y-dimension
        zrange (int): number of voxel blocks for each shape along z-dimension

        Returns:
        [Block]:List of Blocks to generate in Minecraft
        """
        if not BLOCK_LIST_EVOLVES:
            block_options = self.block_list
        else:
            block_options = genome.block_list

        net = neat.nn.FeedForwardNetwork.create(genome, config) # Create CPPN out of genome
        shape = []
        for xi in range(xrange):
            x = util.scale_and_center(xi,xrange)
            for yi in range(yrange):
                y = util.scale_and_center(yi,yrange)
                for zi in range(zrange):
                    z = util.scale_and_center(zi,zrange)
                    # math.sqrt(2) is the usual scaling for radial distances in CPPNs
                    output = net.activate([x, y, z, util.distance((x,y,z),(0,0,0)) * math.sqrt(2), 1.0])
                    
                    # First output determines whether there is a block at all.
                    # If there is a block, argmax determines the max value and places the specified block 
                    # from the list of possible blocks

                    #print(output)
                                                
                    if output[0] < self.args.PRESENCE_THRESHOLD: 
                        block = Block(position=Point(x=corner[0]+xi, y=corner[1]+yi, z=corner[2]+zi), type=AIR, orientation=NORTH)
                    else:
                        output_val = util.argmax(output[1:])
                        block = Block(position=Point(x=corner[0]+xi, y=corner[1]+yi, z=corner[2]+zi), type=block_options[output_val], orientation=NORTH)
                        

                    shape.append(block)
        
        return shape

    

    def eval_fitness(self, genomes, config):
        """
            This function is expected by the NEAT-Python framework.
            It takes a population of genomes and configuration information,
            and assigns fitness values to each of the genome objects in
            the population.
        """                                                                                                                           
        minecraft_structures.clear_area(self.client, self.startx, self.starty, self.startz, self.xrange, self.yrange, self.zrange, self.args.POPULATION_SIZE)
        minecraft_structures.place_fences(self.client, self.startx, self.starty, self.startz, self.xrange, self.yrange, self.zrange, self.args.POPULATION_SIZE)

        (done_block_position, on_block_positions) = minecraft_structures.player_selection_switches(self.args.POPULATION_SIZE)
        
        selected = []
        shapes = []
        
        # This loop could be parallelized
        for n, (genome_id, genome) in enumerate(genomes):
            # Initially, none are selected
            selected.append(False)
            # See how CPPN fills out the shape
            corner = (self.startx + n*(self.xrange+1), self.starty, self.startz)
            shapes.append(self.query_cppn_for_shape(genome, config, corner, self.xrange, self.yrange, self.zrange))

        # Render shapes in Minecraft world
        for i in range(len(shapes)):
            # fill the empty space with the evolved shape
            self.client.spawnBlocks(Blocks(blocks=shapes[i]))

        if self.args.IN_GAME_CONTROL:
            selected = [False for chosen in range(config.pop_size)]
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

                # if the player has clicked the switch for next, then 
                # exit while 
                done = self.client.readCube(Cube(
                    min=Point(x=done_block_position[0], y=done_block_position[1], z=done_block_position[2]),
                    max=Point(x=done_block_position[0], y=done_block_position[1], z=done_block_position[2])
                ))
                player_select_done = done.blocks[0].type == REDSTONE_BLOCK
                #print("Next gen? : {}".format(player_select_done))
                    
                #print(selected)

        else:
            # Controlled externally by keyboard

            # Creates a string that is the user's input, and the converts it to a list
            vals = input("Select the ones you like:")
            split_vals = vals.split(' ')
            selected_vals = list(map(int,split_vals))

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

        if self.args.USE_ELITISM:
            # To assure that all selected individuals survive, the elitism setting is changed
            elite_count = int(sum(map(lambda b : 1 if b else 0, selected)))
            print("{} elite survivors".format(elite_count))
            config.reproduction_config.elitism = elite_count

    # End of MinecraftBreeder

# Various functions

def run(args):
    if not BLOCK_LIST_EVOLVES:
        # Contains all possible blocks that could be placed
        # block_list = [REDSTONE_BLOCK,QUARTZ_BLOCK,EMERALD_BLOCK,GOLD_BLOCK,DIAMOND_BLOCK,REDSTONE_LAMP]
        block_list = [REDSTONE_BLOCK,PISTON,WATER, LAVA]
        genome_type = neat.DefaultGenome
        config_file = 'cppn_minecraft_config'
    else:
        block_list = [] # Won't be used, but parameter is still needed
        genome_type = cg.CustomBlocksGenome
        config_file = 'cppn_minecraft_custom_blocks_config'

    mc = MinecraftBreeder(args,block_list)

    # Determine path to configuration file.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, config_file)

    # Note that we provide the custom stagnation class to the Config constructor.
    config = neat.Config(genome_type, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat_stagnation.InteractiveStagnation,
                         config_path)

    config.pop_size = args.POPULATION_SIZE
    # Changing the number of CPPN outputs after initialization. Could cause problems.
    config.genome_config.num_outputs = BLOCK_LIST_SIZE+1
    config.genome_config.output_keys = [i for i in range(config.genome_config.num_outputs)]

    pop = neat.Population(config)



    # Add a stdout reporter to show progress in the terminal.
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    while 1:
        mc.generation = pop.generation + 1
        pop.run(mc.eval_fitness, 1)


if __name__ == '__main__':
    print("Do not launch this file directly. Launch main.py instead.")
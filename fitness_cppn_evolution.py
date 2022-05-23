"""
TODO
"""
# For CPPNs and NEAT
import neat
import custom_genomes as cg

# for Minecraft
import grpc
import minecraft_pb2_grpc
from minecraft_pb2 import *

# For minecraft structures
import minecraft_structures

# For CPPN generations
import cppn_generation

# For fitness functions
import fitness_functions as ff

### TODO: Change name of class
class FitnessEvolutionMinecraftBreeder(object):
    def __init__(self, args, block_list):
        """
        TODO

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

        # Restore ground at the start of evolution
        minecraft_structures.restore_ground(self.client, self.position_information, self.args.POPULATION_SIZE, self.args.SPACE_BETWEEN)

        # Figure out the lower corner of each shape in advance
        self.corners = []
        for n in range(self.args.POPULATION_SIZE):
            corner = (self.position_information["startx"] + n*(self.position_information["xrange"]+2+self.args.SPACE_BETWEEN), self.position_information["starty"], self.position_information["startz"])
            self.corners.append(corner)

        self.generation = 0
        
        # Don't try any multithreading yet, but consider for later
        self.num_workers = 1


    def eval_fitness(self, genomes, config):
        """
        TODO
        
        Parameters:
        genomes ([DefaultGenome]): list of CPPN genomes
        config  (Config): NEAT configurations
        """            
        minecraft_structures.clear_area(self.client, self.position_information, self.args.POPULATION_SIZE, self.args.SPACE_BETWEEN)                                                                                                               
        
        # This loop could be parallelized
        for n, (genome_id, genome) in enumerate(genomes):
            # See how CPPN fills out the shape
            print("{}. {}: ".format(n,genome_id), end = "") # Preceding number before info from query
            shape = cppn_generation.query_cppn_for_shape(genome, config, self.corners[n], self.position_information, self.args, self.block_list)
            # fill the empty space with the evolved shape
            self.client.spawnBlocks(Blocks(blocks=shape))

            # REDSTONE_BLOCK is hard coded for now, but need to change/generalize later
            genome.fitness = ff.type_count(self.client, self.position_information, self.corners[n], REDSTONE_BLOCK)

            print("{}. {}: {}".format(n,genome_id,genome.fitness))

    # End of FitnessEvolutionMinecraftBreeder                                                                                                            

if __name__ == '__main__':
    print("Do not launch this file directly. Launch main.py instead.")
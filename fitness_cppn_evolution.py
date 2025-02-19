
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

class FitnessEvolutionMinecraftBreeder(object):
    def __init__(self, args, block_list):
        """
        Construct a class for evolving Minecraft shapes
        in an automatic manner (not interactively). 
        The shapes are generated by CPPNs.

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

        self.query_cppn = cppn_generation.query_cppn_for_snake_shape if self.args.EVOLVE_SNAKE else cppn_generation.query_cppn_for_shape

        self.generation = 0

    def eval_fitness(self, genomes, config):
        """
        This function is expected by the NEAT-Python framework.
        It takes a population of genomes and configuration information,
        and assigns fitness values to each of the genome objects in
        the population based on how many blocks are the desired blocks in the shape. 
        Nothing is returned, since the genomes themselves
        are modified.

        Parameters:
        genomes ([DefaultGenome]): list of CPPN genomes
        config  (Config): NEAT configurations
        """        
        # clear previous floating arrows
        position_information_copy = self.position_information.copy()
        position_information_copy["starty"] = self.position_information["starty"]+self.position_information["yrange"]
        minecraft_structures.clear_area(self.client, position_information_copy, self.args.POPULATION_SIZE*2, self.args.SPACE_BETWEEN, self.args.MAX_SNAKE_LENGTH)                                                                                                               
        all_blocks = []                                                                                                             

        champion_found = False 

        # This loop could be parallelized
        for n, (genome_id, genome) in enumerate(genomes):
            # If the number of individuals has grown beyond the original size,
            # more corners need to be added to reserve a slot in the world for the shape.
            if n >= self.args.POPULATION_SIZE:
                corner = (self.position_information["startx"] + n*(self.position_information["xrange"]+2+self.args.SPACE_BETWEEN), self.position_information["starty"], self.position_information["startz"])
                self.corners.append(corner)

            # See how CPPN fills out the shape
            print("{}. {}: ".format(n,genome_id), end = "") # Preceding number before info from query
            shape = self.query_cppn(genome, config, self.corners[n], self.position_information, self.args, self.block_list)
            # fill the empty space with the evolved shape
            self.client.spawnBlocks(Blocks(blocks=shape))
            all_blocks.extend(shape)
            #genome.fitness = ff.type_count(self.client, self.position_information, self.corners[n], self.args)
            fit_function = getattr(ff, self.args.FITNESS_FUNCTION)
            genome.fitness = fit_function(self.client, self.position_information, self.corners[n], self.args)
            
            print("{}. {}: Fitness = {}".format(n,genome_id,genome.fitness))

            # if the genome meets the fitness_threshold, it is the champion and should have some illustration to show that
            # also the program will stop executing after this loop ends since the threshold was met. 
            if genome.fitness >= config.fitness_threshold:
                minecraft_structures.declare_champion(self.client, self.position_information, self.corners[n])
                champion_found = True
      
        if self.args.USE_ELITISM:
            elite_count = self.args.NUM_FITNESS_ELITES
            print("{} elite survivors".format(elite_count))
            config.reproduction_config.elitism = elite_count

        if not champion_found and (self.generation < self.args.MAX_NUM_GENERATIONS or not self.args.KEEP_WORLD_ON_EXIT):      
            for s in all_blocks:
                s.type = AIR
            self.client.spawnBlocks(Blocks(blocks=all_blocks))
        self.generation += 1
        print(self.generation)

        
    
    # End of FitnessEvolutionMinecraftBreeder                                                                                                            

if __name__ == '__main__':
    print("Do not launch this file directly. Launch main.py instead.")
import interactive_cppn_evolution as ice
import fitness_cppn_evolution as fce
import neat
from minecraft_pb2 import *
import neat_stagnation
import minecraft_structures
import os
import custom_genomes as cg

def run(args):
    # If the block list evolves, customGenome is used. Otherwise it's the Default 
    if not args.BLOCK_LIST_EVOLVES:
        # Contains all possible blocks that could be placed, if the block list does not evolve, can be edited to have any blocks here
        block_list = [REDSTONE_BLOCK,PISTON,STONE, SLIME] # TODO: Make this a command line parameter somehow?
        genome_type = neat.DefaultGenome
        config_file = 'cppn_minecraft_fitness_config'
        block_list_length = len(block_list)
    else:
        block_list = [] # Won't be used, but parameter is still needed
        genome_type = cg.CustomBlocksGenome
        config_file = 'cppn_minecraft_fitness_custom_blocks_config'
        block_list_length = args.NUM_EVOLVED_BLOCK_LIST_TYPES
        cg.BLOCK_CHANGE_PROBABILITY = args.BLOCK_CHANGE_PROBABILITY
        #print("Set BLOCK_CHANGE_PROBABILITY to {}".format(cg.BLOCK_CHANGE_PROBABILITY))

    # TODO: need new config file, maybe?

    if args.INTERACTIVE_EVOLUTION:
        mc = ice.MinecraftBreeder(args,block_list)
        stagnation = neat_stagnation.InteractiveStagnation
    else: 
        mc = fce.FitnessEvolutionMinecraftBreeder(args, block_list)
        stagnation = neat.DefaultStagnation

    # Determine path to configuration file.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, config_file)

    # Note that we provide the custom stagnation class to the Config constructor.
    config = neat.Config(genome_type, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, stagnation,
                         config_path)

    config.pop_size = args.POPULATION_SIZE
    # Changing the number of CPPN outputs after initialization. Could cause problems.
    config.genome_config.num_outputs = block_list_length+1
    config.genome_config.output_keys = [i for i in range(config.genome_config.num_outputs)]

    pop = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    # Evolve forever: TODO: Add use means of stopping
    try:
        while True:
            mc.generation = pop.generation + 1
            pop.run(mc.eval_fitness, 1)
    finally:
        # Clear and reset lots of extra space on exit/crash unless KEEP_WORLD_ON_EXIT is true. Population size doubled to clear more space
        if not args.KEEP_WORLD_ON_EXIT:
            minecraft_structures.restore_ground(mc.client, mc.position_information, mc.args.POPULATION_SIZE*2, mc.args.SPACE_BETWEEN)
            minecraft_structures.clear_area(mc.client, mc.position_information, mc.args.POPULATION_SIZE*2, mc.args.SPACE_BETWEEN)                                                                                                               
            # Clear space in the air to get rid of numbers
            mc.position_information["starty"] = mc.position_information["starty"]+mc.position_information["yrange"]
            minecraft_structures.clear_area(mc.client, mc.position_information, mc.args.POPULATION_SIZE*2, mc.args.SPACE_BETWEEN)                                                                                                               

if __name__ == '__main__':
    print("Do not launch this file directly. Launch main.py instead.")
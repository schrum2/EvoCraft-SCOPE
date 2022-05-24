import interactive_cppn_evolution as ice
import fitness_cppn_evolution as fce
import neat
from minecraft_pb2 import *
import neat_stagnation
import minecraft_structures
import os
import custom_genomes as cg
import block_sets
import fitness_functions as ff

def run(args):
    # If the block list evolves, customGenome is used. Otherwise it's the Default 
    if not args.BLOCK_LIST_EVOLVES:
        # Contains all possible blocks that could be placed, if the block list does not evolve, can be edited to have any blocks here
        block_list = [REDSTONE_BLOCK,PISTON,STONE, SLIME] # TODO: Make this a command line parameter somehow?
        genome_type = neat.DefaultGenome
        config_file = 'cppn_minecraft_config' if args.INTERACTIVE_EVOLUTION else 'cppn_minecraft_fitness_config'
        block_list_length = len(block_list)
    else:
        block_list = [] # Won't be used, but parameter is still needed
        genome_type = cg.CustomBlocksGenome
        config_file = 'cppn_minecraft_custom_blocks_config' if args.INTERACTIVE_EVOLUTION else 'cppn_minecraft_fitness_custom_blocks_config'
        block_list_length = args.NUM_EVOLVED_BLOCK_LIST_TYPES
        cg.BLOCK_CHANGE_PROBABILITY = args.BLOCK_CHANGE_PROBABILITY
        cg.BLOCK_LIST_LENGTH = block_list_length
        cg.POTENTIAL_BLOCK_TYPE_LIST = block_sets.select_possible_block_sets(args.POTENTIAL_BLOCK_SET) # for sending specified block set to custom genome
        #print("Set BLOCK_CHANGE_PROBABILITY to {}".format(cg.BLOCK_CHANGE_PROBABILITY))

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

    if args.INTERACTIVE_EVOLUTION:
        # Selected items have a fitness of 1, but there is no final/best option
        config.fitness_threshold = 1.01
    else:
        # TODO: Change this so it is set depending on the specific fitness function used.
        # At this point, any invalid fitness function name would have been caught in main.
        fit_function = getattr(ff, args.FITNESS_FUNCTION)
        config.fitness_threshold = fit_function(None, mc.position_information, None, args)
        #config.fitness_threshold = 1000
    config.pop_size = args.POPULATION_SIZE
    # Changing the number of CPPN outputs after initialization. 
    # Evolved snakes have 7 additional outputs.
    config.genome_config.num_outputs = block_list_length + 1 + (7 if args.EVOLVE_SNAKE else 0)
    config.genome_config.output_keys = [i for i in range(config.genome_config.num_outputs)]

    print("CPPNs will have {} output neurons".format(config.genome_config.num_outputs))

    pop = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    
    #neat.save_genome_fitness(self, delimeter=' ', filename = 'fitness_history.csv')
    #neat.save_genome_fitness()

    # Evolve forever: TODO: Add use means of stopping
    try:
        if args.INTERACTIVE_EVOLUTION:
            while True:
                mc.generation = pop.generation + 1
                pop.run(mc.eval_fitness, 1)
        else: # Fitness-based evolution
            # TODO: Change 1000 to a command line parameter NUM_GENERATIONS
            generations = 1000
            print("Evolve for {} generations".format(generations))
            pop.run(mc.eval_fitness, generations)
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
import interactive_cppn_evolution as ice
import fitness_cppn_evolution as fce
import novelty_cppn_evolution as nce
import neat
from minecraft_pb2 import *
import neat_stagnation
import minecraft_structures
import os
import custom_genomes as cg
import block_sets
import fitness_functions as ff
import novelty_characterizations as nc
import pickle
# For loading novelty shapes
from os import listdir
from os.path import isfile, join
import visualize

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
        cg.PREVENT_DUPLICATES = args.PREVENT_DUPLICATE_BLOCK_TYPES
        #print("Set BLOCK_CHANGE_PROBABILITY to {}".format(cg.BLOCK_CHANGE_PROBABILITY))

    if args.INTERACTIVE_EVOLUTION:
        print("Interactive evolution")
        mc = ice.MinecraftBreeder(args,block_list)
        stagnation = neat_stagnation.InteractiveStagnation
    elif args.EVOLVE_NOVELTY:
        print("Novelty Search")
        mc = nce.NoveltyMinecraftBreeder(args, block_list)
        stagnation = neat.DefaultStagnation
    elif(args.EVOLVE_FITNESS): 
        print("Objective-based evolution")
        mc = fce.FitnessEvolutionMinecraftBreeder(args, block_list)
        stagnation = neat.DefaultStagnation
    else:
        print("Please select a way to evolve!")
        quit()

    # Determine path to configuration file.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, config_file)

    # Note that we provide the custom stagnation class to the Config constructor.
    config = neat.Config(genome_type, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, stagnation,
                         config_path)

    # If loading generated novelty structures
    if args.LOAD_NOVELTY and not args.SAVE_NOVELTY:  
        novel_genomes = [] 
        file_path = "C:/schrum2MM-NEAT/EvoCraft-SCOPE/{}/{}{}/archive".format(args.BASE_DIR,args.EXPERIMENT_PREFIX,args.LOAD_SAVED_SEED) # File path for loop below
        # Finds all shapes in the archive folder and makes them into a list. The length of this list is how long the next loop runs for
        novel_shapes = [f for f in listdir(file_path) if isfile(join(file_path, f))]

        # Gets the start point based on the command line param
        if(args.LOAD_NOVELTY_MIN>args.LOAD_NOVELTY_MAX):
            print("Invalid range. The start is bigger than the end. Try again")
            quit()
        elif(args.LOAD_NOVELTY_MAX-args.LOAD_NOVELTY_MIN>1000):
            user_ch=input("WARNING: Printing over 1000 shapes at a time could crash the server. Press \"c\" to continue, or any other key to quit: ")
            if(user_ch!='c'):
                quit()
        len_files = len(novel_shapes)
        if args.LOAD_NOVELTY_MIN > -1 and args.LOAD_NOVELTY_MIN<len_files:
            i = args.LOAD_NOVELTY_MIN
        elif(args.LOAD_NOVELTY_MIN>len_files):
            print("Your start value was larger than the ammount of files in the archive. Please try again")
            quit()
        else: 
            i = 0

        # Gets the end point based on the command line param
        if args.LOAD_NOVELTY_MAX > -1 and args.LOAD_NOVELTY_MAX<len_files:
            end = args.LOAD_NOVELTY_MAX
        elif(args.LOAD_NOVELTY_MAX>len_files):
            print("Your end value was larger than the ammount of files in the archive. The rest of the files in the archive will be generated")
            end = len_files
        else: 
            end = len_files
        print("Loading {} saved structures from {}/{}{}/archive".format(end-i,args.BASE_DIR,args.EXPERIMENT_PREFIX,args.LOAD_SAVED_SEED))

        # Clear space for shapes
        minecraft_structures.clear_area(mc.client, mc.position_information, (end-i)*2, mc.args.SPACE_BETWEEN, mc.args.MAX_SNAKE_LENGTH)
        print("cleared area")
        # Loops through from start to end, generating all shapes
        while i <end:
            with open( "{}/{}{}/archive/shape{}".format(args.BASE_DIR,args.EXPERIMENT_PREFIX,args.LOAD_SAVED_SEED,i),'rb') as handle:
                genome_from_pickle = pickle.load(handle)
            novel_genomes.append( (genome_from_pickle.key , genome_from_pickle) )
            i+=1

        # The shapes in the list are generated, returned for clearing
        loaded_blocks = mc.eval_fitness(novel_genomes, config)
        print("All shapes from the archive were generated!")

        user_input = input("Press q to quit and delete the shapes: ")
        while(user_input!="q"):
            user_input = input("That wasn't q! Press q to quit and delete the shapes: ")
        #Clears all blocks that were generated
        for s in loaded_blocks:
            s.type = AIR
        mc.client.spawnBlocks(Blocks(blocks=loaded_blocks))
        print("Area cleared, program terminating")
        quit() # Quit because nothing else will be evolved

    if args.INTERACTIVE_EVOLUTION:
        # Selected items have a fitness of 1, but there is no final/best option
        config.fitness_threshold = 1.01
    elif args.EVOLVE_NOVELTY:
        config.fitness_threshold = float("inf") # No predetermined cutoff
    else: # Fitness-based evolution
        # TODO: Change this so it is set depending on the specific fitness function used.
        # At this point, any invalid fitness function name would have been caught in main.
        # start of fitness evolution, clear previous world of 'champion arrows'
        fit_function = getattr(ff, args.FITNESS_FUNCTION)
        config.fitness_threshold = fit_function(None, mc.position_information, None, args)

    config.pop_size = args.POPULATION_SIZE
    
    # Changing the number of CPPN outputs after initialization. 
    # Evolved snakes have 7 additional outputs. Evolved orientation will have 6
    config.genome_config.num_outputs = block_list_length + 1 + (7 if args.EVOLVE_SNAKE else 0) + (6 if args.EVOLVE_ORIENTATION else 0)
    config.genome_config.output_keys = [i for i in range(config.genome_config.num_outputs)]

    print("CPPNs will have {} output neurons".format(config.genome_config.num_outputs))

    pop = neat.Population(config)

    # do not save unless SAVE_FITNESS_LOG is true and names for BASE_DIR and EXPERIMENT_PREFIX other than None are given 
    invalid_dir_names = args.BASE_DIR is None or args.EXPERIMENT_PREFIX is None
    print(invalid_dir_names)
    if args.SAVE_FITNESS_LOG and not invalid_dir_names or args.INTERACTIVE_EVOLUTION:
        # Add a stdout reporter to show progress in the terminal.
        pop.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        pop.add_reporter(stats)
        base_path = '{}'.format(args.BASE_DIR)
        dir_exists = os.path.isdir(base_path)
        if not dir_exists:
            os.mkdir(base_path)
        
        # make sub dir too
        sub_path = '{}/{}{}'.format(base_path,args.EXPERIMENT_PREFIX,args.RANDOM_SEED)
        dir_exists = os.path.isdir(sub_path)
        if not dir_exists:
            os.mkdir(sub_path)
        
        pop_path = '{}/gen/'.format(sub_path)
        dir_exists = os.path.isdir(pop_path)
        if not dir_exists:
            os.mkdir(pop_path)

        checkpointer = neat.Checkpointer(args.CHECKPOINT_FREQUENCY, args.TIME_INTERVAL, "{}gen".format(pop_path))
    
        pop.add_reporter(checkpointer)

    # Evolve forever: TODO: Add use means of stopping
    try:
        if args.INTERACTIVE_EVOLUTION:
            while True:
                if(args.LOAD_SAVED_NO_EVOLUTION and args.LOAD_SAVED_SEED!= None and args.LOAD_GENERATION !=None):
                    pop = checkpointer.restore_checkpoint('{}/{}{}/gen/gen{}'.format(args.BASE_DIR, args.EXPERIMENT_PREFIX, args.LOAD_SAVED_SEED, args.LOAD_GENERATION))
                elif(args.LOAD_SAVED_NO_EVOLUTION and (args.LOAD_SAVED_SEED== None or args.LOAD_GENERATION ==None)):
                    print("In order to load, make sure you set both the LOAD_SAVED_SEED and the LOAD_GENERATION")
                    quit()

                #mc.eval_fitness(novel_genomes,config)
                pop.run(mc.eval_fitness, 1)
        else: # Fitness-based evolution
            # TODO: Change 1000 to a command line parameter NUM_GENERATIONS
            generations = args.MAX_NUM_GENERATIONS
            print("Evolve for {} generations".format(generations))
            
            if not args.SAVE_FITNESS_LOG and args.LOAD_SAVED_POPULATION:
                pop = checkpointer.restore_checkpoint('{}/{}{}/gen/gen{}'.format(args.BASE_DIR, args.EXPERIMENT_PREFIX, args.LOAD_SAVED_SEED, args.LOAD_GENERATION))
                print("Evaluate 1 Generation")
                pop.run(mc.eval_fitness, 1)
                # When loading, the most recently saved generation is loaded, but no further evolution happens and the program crashes. 

            elif args.LOAD_PARAMETERS and args.LOAD_SAVED_POPULATION: # restore checkpoint when loading saved command line parameters.
                print('Load from: {}/{}{}/gen/gen{}'.format(args.BASE_DIR, args.EXPERIMENT_PREFIX, args.LOAD_SAVED_SEED, args.LOAD_GENERATION))
                # Equivalent?
                #pop = neat.checkpoint.Checkpointer.restore_checkpoint('{}/{}{}/gen/gen{}'.format(args.BASE_DIR, args.EXPERIMENT_PREFIX, args.LOAD_SAVED_SEED, args.LOAD_GENERATION))
                pop = checkpointer.restore_checkpoint('{}/{}{}/gen/gen{}'.format(args.BASE_DIR, args.EXPERIMENT_PREFIX, args.LOAD_SAVED_SEED, args.LOAD_GENERATION))
                print("Evaluate 1 Generation")
                pop.run(mc.eval_fitness, 1)
                # When loading, the most recently saved generation is loaded, but no further evolution happens and the program crashes.

            else:
                print("Start evolving")
                pop.run(mc.eval_fitness, generations)

    finally:
        # only save to csv for fitness based evolution
        print('outside the nested loops')
        if not args.INTERACTIVE_EVOLUTION:
            print('inside the inner loop of nested loops')
            if not args.LOAD_SAVED_POPULATION and args.SAVE_FITNESS_LOG and not invalid_dir_names:
                print('inside nested else statement')
                checkpointer.save_checkpoint(config, pop.population, neat.DefaultSpeciesSet ,pop.generation)
                stats.save()
                # cross_validation has to be false, true produces an error, also the git thing said
                stats.save_genome_fitness(filename='{}/{}{}/results.csv'.format(args.BASE_DIR, args.EXPERIMENT_PREFIX, args.RANDOM_SEED),with_cross_validation=False)

                # visualize
                visualize.plot_stats(stats, ylog=True, view=True, filename='{}/{}{}/stats.svg'.format(args.BASE_DIR, args.EXPERIMENT_PREFIX, args.RANDOM_SEED))
                visualize.plot_species(stats, view=True, filename='{}/{}{}/species.svg'.format(args.BASE_DIR, args.EXPERIMENT_PREFIX, args.RANDOM_SEED))

                # save neural network
                node_names = {-1: 'x', -2: 'y', -3: 'z', -4: 'radius', -5: 'bias', 0: 'presence'}
                i = 1   
                while i < block_list_length + 1:
                    node_names[i] = 'bt {}'.format(i - 1)
                    i+=1
                
                orientations = ['oriented e', 'oriented n', 'oriented ne', 'oriented w', 'oriented s','oriented sw']
                xi = 0 
                if args.EVOLVE_ORIENTATION:
                    for x in orientations:
                        node_names[i] = orientations[xi]
                        i+=1
                        xi+=1

                xi = 0
                snake_directions = ['x neg', 'y neg', 'z neg','x pos', 'y pos', 'z pos','continue snake']
                if args.EVOLVE_SNAKE:
                    for x in snake_directions:
                        node_names[i] = snake_directions[xi]
                        i+=1
                        xi+=1
            
                visualize.draw_net(config, stats.best_genome(), view=True, filename='{}/{}{}/champion_neural_network.gv'.format(args.BASE_DIR, args.EXPERIMENT_PREFIX, args.RANDOM_SEED), node_names=node_names)
            
        # Clear and reset lots of extra space on exit/crash unless KEEP_WORLD_ON_EXIT is true. Population size doubled to clear more space
        if not args.KEEP_WORLD_ON_EXIT:
            minecraft_structures.restore_ground(mc.client, mc.position_information, mc.args.POPULATION_SIZE*2, mc.args.SPACE_BETWEEN)
            minecraft_structures.clear_area(mc.client, mc.position_information, mc.args.POPULATION_SIZE*2, mc.args.SPACE_BETWEEN, mc.args.MAX_SNAKE_LENGTH)                                                                                                               
            
            # Should not need this since we clear to such a high ceiling now
            # Clear space in the air to get rid of numbers
            #mc.position_information["starty"] = mc.position_information["starty"]+mc.position_information["yrange"]
            #minecraft_structures.clear_area(mc.client, mc.position_information, mc.args.POPULATION_SIZE*2, mc.args.SPACE_BETWEEN)                                                                                                               

if __name__ == '__main__':
    print("Do not launch this file directly. Launch main.py instead.")
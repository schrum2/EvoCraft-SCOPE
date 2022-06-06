import argparse
import sys
from tokenize import String
import evolution
import random
import os
from os.path import exists
from os import mkdir
from minecraft_pb2 import *
import fitness_functions as ff
import block_sets
import ast

def boolean_string(s):
    """
    Checks a string that should only be either True or False and converts to associated boolean.
    This is required to make argparse handle bool types correctly.

    Parameter:
    s (string): String that is "True" or "False"

    Return:
    (bool): String converted to corresponding bool
    """
    if s not in {'False', 'True'}:
        raise ValueError('Not a valid boolean string')
    return s == 'True'

def block_int(name):
    """
    Converts the name of a block into its corresponding int value.
    """
    return BlockType.Value(name)

def tryeval(val):
    """
    Converts the string value into its appropriate value type.
    """
    try:
        val = ast.literal_eval(val)
    except ValueError:
        pass
    return val

def main(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('--USE_ELITISM', type=boolean_string, default=True, metavar='', 
                        help='When true, selected shapes will be present in the proceeding generation.')
    parser.add_argument('--IN_GAME_CONTROL', type=boolean_string, default=False, metavar='',
                        help='Whether the player can control evolution within the game (via switches).')
    parser.add_argument('--PRESENCE_THRESHOLD', type=float, default=0.5, metavar='',
                        help='The activation value determining if a block is present or not.')
    parser.add_argument('--POPULATION_SIZE', type=int, default=10, metavar='',
                        help='Number of the population size.')
    parser.add_argument('--XRANGE', type=int, default=10, metavar='',
                        help='The range of x coordinate values. This value must be at least 1.')
    parser.add_argument('--YRANGE', type=int, default=10, metavar='',
                        help='The range of y coordinate values. This value must be at least 1.')
    parser.add_argument('--ZRANGE', type=int, default=10, metavar='',
                        help='The range of z coordinate values. This value must be at least 1.')
    parser.add_argument('--BLOCK_LIST_EVOLVES', type=boolean_string, default=True, metavar='',
                        help='When true, blocks list for each genome is different and evolves.')
    parser.add_argument('--NUM_EVOLVED_BLOCK_LIST_TYPES', type=int, default=5, metavar='',
                        help='The number of possible block list types when the block list is evolved.')
    parser.add_argument('--BLOCK_CHANGE_PROBABILITY', type=float, default=0.1, metavar='',
                        help='Probability of randomly changing a block type when the block list evolves.')
    parser.add_argument('--DISTANCE_PRESENCE_THRESHOLD', type=boolean_string, default=False, metavar='',
                        help='Whether or not the presence threshold depends on the distance of the candidate block from the center of the generated shape.')
    parser.add_argument('--DISTANCE_PRESENCE_MULTIPLIER', type=float, default=0.1, metavar='',
                        help='The multiplier used when DISTANC_PRESENCE_THRESHOLD is true.')
    parser.add_argument('--RANDOM_SEED', type=int, default=random.randrange(0,100,1), metavar='',
                        help='Random seed of the shapes produced on the initial time.')
    parser.add_argument('--SPACE_BETWEEN', type=int, default=1, metavar='',
                        help='The space between the fences of each shape.')
    parser.add_argument('--KEEP_WORLD_ON_EXIT', type = boolean_string, default = False, metavar='',
                        help='Whether or not the world is reset whenever the program exits.')
    parser.add_argument('--EVOLVE_SNAKE', type=boolean_string, default=False, metavar='',
                        help='Changes the CPPN to generate snake-like structures.')
    parser.add_argument('--MAX_SNAKE_LENGTH', type=int, default=100, metavar='',
                        help='The maximum length a snake-like structure can be when EVOLVE_SNAKE is true.')
    parser.add_argument('--CONFINE_SNAKES', type=boolean_string, default=True, metavar='',
                        help='Confines the snake generations so that they do not cross with other snakes.')
    parser.add_argument('--REDIRECT_CONFINED_SNAKES', type=boolean_string, default=False, metavar='',
                        help='If the snake goes out of bounds, the direction will change so that it stays within bounds.')
    parser.add_argument('--REDIRECT_CONFINED_SNAKES_UP', type=boolean_string, default=False, metavar='',
                        help='If the snake goes out of bounds, the direction will change to go up so that it stays within bounds.')
    parser.add_argument('--STOP_CONFINED_SNAKES', type=boolean_string, default=False, metavar='',
                        help='If the snake goes out of bounds, the snake will stop rendering.')      
    parser.add_argument('--CONTINUATION_THRESHOLD', type=float, default=0.5, metavar='',
                        help='Neuron output required for a snake-like structure to continue generating when EVOLVE_SNAKE is true.')
    parser.add_argument('--INTERACTIVE_EVOLUTION', type=boolean_string, default=True, metavar='',
                        help='Whether or not interactive evolution will be used.')
    parser.add_argument('--POTENTIAL_BLOCK_SET', help='Choose which block set is used for generation', # Can add additional 
                        action='store', choices=['all', 'undroppable','machine','restrictive_machine'], default='undroppable', required=False)
    parser.add_argument('--MINIMUM_REQUIRED_BLOCKS', type=int, default=10, metavar='',
                        help='The number of minimum required blocks to be used.')
    parser.add_argument('--USE_MIN_BLOCK_REQUIREMENT', type=boolean_string, default=True, metavar='',
                        help='Whether or not to use the minimum required block requirement.')
    parser.add_argument('--MIN_BLOCK_PRESENCE_INCREMENT', type=float, default=0.1, metavar='',
                        help='How big the step size is for the minimum block presence.')
    parser.add_argument('--DESIRED_BLOCK', type=block_int, default=None, metavar='',
                        help='The desired block.')
    parser.add_argument('--DESIRED_BLOCK_COUNT', type=int, default=0, metavar='',
                        help='The desired block count of a specific block.')
    parser.add_argument('--EVOLVE_FITNESS', type=boolean_string, default=False, metavar='',
                        help='Whether or not to evolve with Objective-based evolution. FITNESS_FUNCTION is also needed with this')
    parser.add_argument('--FITNESS_FUNCTION', type=str, metavar='',
                        help='The fitness function to be used.')
    parser.add_argument('--EVOLVE_NOVELTY', type=boolean_string, default=False, metavar='',
                        help='Whether or not to evolve with novelty search. NOVELTY_CHARACTER is also needed with this')
    parser.add_argument('--NOVELTY_CHARACTER', type=str, metavar='',
                        help='The way novelty is characterized in a shape')
    parser.add_argument('--NOVELTY_DISTANCE', type=str, metavar='',
                        help='The distance metric specified for novelty search')
    parser.add_argument('--NOVELTY_RANDOM_SCORE', type=float, default=0.02, metavar='',
                        help='Probability that shapes will be added to the archive. Should be between 0.0 and 1.0.')
    parser.add_argument('--SAVE_NOVELTY', type=boolean_string, default=False, metavar='',
                        help='Whether or not to save archive in noevlty search')
    parser.add_argument('--LOAD_NOVELTY', type=boolean_string, default=False, metavar='',
                        help='Whether or not to load archive in noevlty search')
    parser.add_argument('--LOAD_NOVELTY_MIN', type=int, default=-1, metavar='',
                        help='Number to start loading generations from')
    parser.add_argument('--LOAD_NOVELTY_MAX', type=int, default=-1, metavar='',
                        help='Number to dtop loading generations from')
    parser.add_argument('--ONLY_SHOW_PLACED', type=boolean_string, default=True, metavar='',
                        help='Shows only the blocks that were placed in the shape in front of the shape')
    parser.add_argument('--PREVENT_DUPLICATE_BLOCK_TYPES', type=boolean_string, default=True, metavar='',
                        help='Shows only the blocks that were placed in the shape in front of the shape')
    parser.add_argument('--EVOLVE_ORIENTATION', type=boolean_string, default=True, metavar='',
                        help='Evloves the orientation of the blocks')
    parser.add_argument('--SAVE_FITNESS_LOG', type=boolean_string, default=False, metavar='',
                        help='Save CPPN population.')
    parser.add_argument('--BASE_DIR', type=str, default=None, metavar='',
                        help='Directory where results from several experiments can be stored.')
    parser.add_argument('--EXPERIMENT_PREFIX', type=str, default=None, metavar='',
                        help='Subdir in the BASE_DIR where directories from different runs are stored.')
    parser.add_argument('--CHECKPOINT_FREQUENCY', type=int, default=10, metavar='',
                        help='How often in relation to generation number a checkpointer saves the population.')
    parser.add_argument('--TIME_INTERVAL', type=int, default=10000, metavar='',
                        help='How often in relation to time a checkpointer saves the population.')
    parser.add_argument('--LOAD_SAVED_POPULATION', type=boolean_string, default=False, metavar='',
                        help='Whether or not to load a previously saved experiment.')
    parser.add_argument('--LOAD_GENERATION', type=int, default=None, metavar='',
                        help='Generation to load.')
    parser.add_argument('--LOAD_SAVED_SEED', type=int, default=None, metavar='',
                        help='Generation seed to load.')
    parser.add_argument('--NUM_FITNESS_ELITES', type=int, default=2, metavar='',
                        help='Specific number of top elites to copy into the next generation for fitness cppn evolution.')
    parser.add_argument('--MAX_NUM_GENERATIONS', type=int, default=1000, metavar='',
                        help='Max number of generations that can occur if not stopped by a champion.')
    parser.add_argument('--LOAD_SAVED_NO_EVOLUTION', type=boolean_string, default=False, metavar='',
                        help='Whether or not to load a previously saved set of shapes that will not evolve')
    parser.add_argument('--SAVE_PARAMETERS', type=boolean_string, default=False, metavar='',
                        help='Whether or not to the parameters being used for future use.')
    parser.add_argument('--MIN_BLOCK_FAILSAFE_ITERATIONS', type=int, default=500, metavar='',
                        help='The number of chances given to creating a minimum number of blocks before the presence threshold is set to negative infinity (meaning that every block will generate).')
    parser.add_argument('--CONTINUATION_INCREMENT', type=float, default=0.1, metavar='',
                        help='How big the step size is for the snake continuation.')
    parser.add_argument('--MAINTAIN_EVOLUTIONARY_HISTORY', type=boolean_string, default=False, metavar='',
                        help='Whether or not to keep all generated shapes')


    args = parser.parse_args()
   
    if args.BLOCK_CHANGE_PROBABILITY < 0.0 or args.BLOCK_CHANGE_PROBABILITY > 1.0:
        raise ValueError("BLOCK_CHANGE_PROBABILITY must be in range [0,1].")

    if args.XRANGE < 1:
        raise ValueError("XRANGE value must be at least one.")
    elif args.XRANGE >= 25:
        print("XRANGE values larger than 25 may cause the server to slow down or crash.")   

    if args.YRANGE < 1:
        raise ValueError("YRANGE value must be at least one.")
    elif args.YRANGE >= 25:
        print("YRANGE values larger than 25 may cause the server to slow down or crash.")   

    if args.ZRANGE < 1:
        raise ValueError("ZRANGE value must be at least one.")
    elif args.ZRANGE >= 25:
        print("ZRANGE values larger than 25 may cause the server to slow down or crash.")   
    
    if args.POPULATION_SIZE < 2:
        raise ValueError("Population size must at least two.")

    if args.NUM_EVOLVED_BLOCK_LIST_TYPES < 2:
        raise ValueError("Block list size must at least two.")

    if args.PREVENT_DUPLICATE_BLOCK_TYPES and args.NUM_EVOLVED_BLOCK_LIST_TYPES>len(block_sets.select_possible_block_sets(args.POTENTIAL_BLOCK_SET)):
        print(len(block_sets.select_possible_block_sets(args.POTENTIAL_BLOCK_SET)))
        raise ValueError("Block list size is too small to not have duplicates.")
    
    if not args.INTERACTIVE_EVOLUTION and not args.EVOLVE_NOVELTY:
        try: is_function = getattr(ff, args.FITNESS_FUNCTION)
        except: print('{}/{}{}/ is not a valid fitness function name.'.format(args.FITNESS_FUNCTION))

    random.seed(args.RANDOM_SEED)
    
    #if not args.FITNESS_FUNCTION in dir(ff): 
     #   print('The fitness function name you have given does not exist.')
    
    base_path = '{}'.format(args.BASE_DIR)
    dir_exists = os.path.isdir(base_path)
    if not dir_exists:
        os.mkdir(base_path)
         
    path = '{}/{}{}'.format(args.BASE_DIR,args.EXPERIMENT_PREFIX,args.RANDOM_SEED)
    dir_exists = os.path.isdir(path)
    if not dir_exists:
        os.mkdir(path)
    
    # if the file of parameters already exists in the specified location, then load it
    if exists('{}/parameters.txt'.format(path)):
        with open('{}/parameters.txt'.format(path)) as f:
            # read all of the lines
            lines = f.readlines()
            # split all of the lines to get the value
            for line in lines:
                rhs = line.split(':')[1]
                # get rid of the \n that was being saved with it
                new_line = rhs[0:len(rhs)-1]
                        
                k = line.split(':')[0]
                if str(args.__dict__[k]) != new_line:
                    raise Exception("The value you have chosen for {} does not match the value loaded from the already existing parameters file. \nProposed Value: {} \nPreexisting Value: {}".format(k, tryeval(new_line), args.__dict__[k]))
               
                setattr(args, k, tryeval(new_line))
    
    # save the parameters if SAVE_PARAMETERS is true.      
    if args.SAVE_PARAMETERS:    
        try:
        # does not already exist, make new file and save args
          with open('{}/parameters.txt'.format(path), 'x') as f:
                for arg in args.__dict__:
                    f.write('{}:{}\n'.format(arg,args.__dict__[arg]))      
        except FileExistsError:
            # already exists, not overriding the data in a preexisting file
            # letting this exception pass since it will be loaded anyways by the code above.
            pass
    
    # check if loaded value differs from attempted saved value and crash with message similar to 'The proposed command line parameter differs from the existing command line parameter.'


    evolution.run(args)

if __name__ == '__main__':
    main(sys.argv)
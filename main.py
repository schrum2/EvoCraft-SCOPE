import argparse
import string
import sys
import evolution
import random
from os.path import exists
from os import mkdir
from minecraft_pb2 import *


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

def main(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('--USE_ELITISM', type=boolean_string, default=False, metavar='', 
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
    parser.add_argument('--RANDOM_SEED', type=random.Random, default=random.randrange(0,100,1), metavar='',
                        help='Random seed of the shapes produced on the initial time.')
    parser.add_argument('--SPACE_BETWEEN', type=int, default=1, metavar='',
                        help='The space between the fences of each shape.')
    parser.add_argument('--KEEP_WORLD_ON_EXIT', type = boolean_string, default = False, metavar='',
                        help='Whether or not the world is reset whenever the program exits.')
    parser.add_argument('--EVOLVE_SNAKE', type=boolean_string, default=False, metavar='',
                        help='Changes the CPPN to generate snake-like structures.')
    parser.add_argument('--MAX_SNAKE_LENGTH', type=int, default=100, metavar='',
                        help='The maximum length a snake-like structure can be when EVOLVE_SNAKE is true.')
    parser.add_argument('--CONTINUATION_THRESHOLD', type=float, default=0.5, metavar='',
                        help='The maximum length a snake-like structure can be when EVOLVE_SNAKE is true.')
    parser.add_argument('--INTERACTIVE_EVOLUTION', type=boolean_string, default=True, metavar='',
                        help='Whether or not interactive evolution will be used.')
    parser.add_argument('--POTENTIAL_BLOCK_SET', help='Choose which block set is used for generation', # Can add additional 
                        action='store', choices=['all', 'undroppable','machine'], default='all', required=False)
    parser.add_argument('--MINIMUM_REQUIRED_BLOCKS', type=int, default=sys.maxsize, metavar='',
                        help='The number of minimum required blocks to be used.')
    parser.add_argument('--USE_MIN_BLOCK_REQUIREMENT', type=boolean_string, default=False, metavar='',
                        help='Whether or not to use the minimum required block requirement.')
    parser.add_argument('--MIN_BLOCK_PRESENCE_INCREMENT', type=float, default=0.1, metavar='',
                        help='How big the step size is for the minimum block presence.')
    parser.add_argument('--DESIRED_BLOCK', type=block_int, default=None, metavar='',
                        help='The desired block.')
    parser.add_argument('--ONLY_SHOW_PLACED', type=boolean_string, default=True, metavar='',
                        help='Shows only the blocks that were placed in the shape in front of the shape')


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

    random.seed(args.RANDOM_SEED)
        
    evolution.run(args)

if __name__ == '__main__':
    main(sys.argv)
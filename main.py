import argparse
import sys
import evolve_CPPN
from os.path import exists
from os import mkdir

def main(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('--USE_ELITISM', type=bool, default=False, metavar='', 
                        help='When true, selected shapes will be present in the proceeding generation.')
    parser.add_argument('--IN_GAME_CONTROL', type=bool, default=False, metavar='',
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
    parser.add_argument('--BLOCK_LIST_EVOLVES', type=bool, default=True, metavar='',
                        help='When true, blocks list for each genome is different and evolves.')
    parser.add_argument('--NUM_EVOLVED_BLOCK_LIST_TYPES', type=int, default=5, metavar='',
                        help='The number of possible block list types when the block list is evolved.')
    parser.add_argument('--BLOCK_CHANGE_PROBABILITY', type=float, default=0.1, metavar='',
                        help='Probability of randomly changing a block type when the block list evolves.')

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

    evolve_CPPN.run(args)

if __name__ == '__main__':
    main(sys.argv)
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
                        help='Whether the player can control evolution within the game.')
    parser.add_argument('--PRESENCE_THRESHOLD', type=float, default=0.5, metavar='',
                        help='The activation value determining if a block is present or not.')
    parser.add_argument('--POPULATION_SIZE', type=int, default=10, metavar='',
                        help='Number of the population size.')

    args = parser.parse_args()

    evolve_CPPN.run(args)

if __name__ == '__main__':
    main(sys.argv)
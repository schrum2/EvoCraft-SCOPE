# For neat
import neat

# For utility functions
import util

# For the dictionary of position information
import interactive_cppn_evolution

# For simple math functions
import math

# For minecraft
import grpc
import minecraft_pb2_grpc
from minecraft_pb2 import *

def query_cppn_for_shape(genome, config, corner, position_information, args, block_list):
        """
        Query CPPN at all voxel coordinates to generate the list of
        blocks that will eventually be rendered in the Minecraft server.

        Parameters:
        genome (DefaultGenome): A CPPN or some class that extends CPPNs
        config (Config): NEAT configurations
        corner (int,int,int): three-tuple of initial/minimal x,y,z coordinates for shape
        args (argparse.Namespace): a collection of argument values collected at the command line
        block_list ([Block]): List of blocks that can be spawned in

        Returns:
        [Block]:List of Blocks to generate in Minecraft
        """
        # If not evolving block list, use the static one specified lower in the code. Otherwise, use the genome's list
        if not args.BLOCK_LIST_EVOLVES:
            block_options = block_list
        else:
            block_options = genome.block_list

        
        shape = []
        for xi in range(position_information["xrange"]):
            x = util.scale_and_center(xi,position_information["xrange"])
            for yi in range(position_information["yrange"]):
                y = util.scale_and_center(yi,position_information["yrange"])
                for zi in range(position_information["zrange"]):
                    z = util.scale_and_center(zi,position_information["zrange"])
                    scaled_point = (x, y, z)
                    change = (xi, yi, zi)
                    block = generate_block(genome, config, corner, args, block_options, scaled_point, change)
                    if block is not None:
                        shape.append(block)
        
        if(len(shape) == 0):
            print("Genome at corner {} is empty".format(corner))
        else:
            #print(list(BlockType.items()))
            #print(list(BlockType.keys()))
            print("Genome at corner {} generated {} blocks of these types: {}".format(corner,len(shape),set(map(lambda x: BlockType.keys()[x.type], shape))))

        return shape

def generate_block(genome, config, corner, args, block_options, scaled_point, change): 
    """
    Returns whether or not there is a block at a specific position and None
    if there isn't

    Parameters:
    genome (DefaultGenome): A CPPN or a class that extends CPPNs
    config (Config): NEAT configurations
    corner (int, int, int): three-tuple of initial/minimal x,y,z coordinates for shape
    args (argparse.Namespace): a collection of argument values collected at the command line 
    block_options ([Block]): List of blocks that can be spawned in 
    scaled_point (int, int, int): three-tuple of the position being looked at
    change (int, int, int): three-tuple used to scale the position of the point

    Returns:
    (Block): If a block is present it will 
    """
    # Create CPPN out of genome
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    # math.sqrt(2) is the usual scaling for radial distances in CPPNs
    center_dist = util.distance((scaled_point[0],scaled_point[1],scaled_point[2]),(0,0,0))
    output = net.activate([scaled_point[0], scaled_point[1], scaled_point[2], center_dist * math.sqrt(2), 1.0])
                    
    # First output determines whether there is a block at all.
    # If there is a block, argmax determines the max value and places the specified block 
    # from the list of possible blocks
    presence_threshold = args.PRESENCE_THRESHOLD 
                    
    if args.DISTANCE_PRESENCE_THRESHOLD:
        presence_threshold = args.DISTANCE_PRESENCE_MULTIPLIER * center_dist                            

    # Only generate non-air blocks by returning the block. If there is no
    # block, return None
    if output[0] >= presence_threshold: 
        output_val = util.argmax(output[1:])
        assert (output_val >= 0 and output_val < len(block_options)),"{} out of bounds: {}".format(output_val,block_options)
        block = Block(position=Point(x=corner[0]+change[0], y=corner[1]+change[1], z=corner[2]+change[2]), type=block_options[output_val], orientation=NORTH)
        return block
    else:
        return None

def query_cppn_for_snake_shape(genome, config, corner, position_information, args, block_list):
    done = False

    # If not evolving block list, use the static one specified lower in the code. Otherwise, use the genome's list
    if not args.BLOCK_LIST_EVOLVES:
       block_options = block_list
    else:
        block_options = genome.block_list
    
    xi = int(interactive_cppn_evolution.position_information["xrange"]/2)
    yi = int(interactive_cppn_evolution.position_information["yrange"]/2)
    zi = int(interactive_cppn_evolution.position_information["zrange"]/2)
    change = (xi, yi, zi)

    snake = []
    while not done:
        x = util.scale_and_center(xi,position_information["xrange"])
        y = util.scale_and_center(yi,position_information["yrange"])
        z = util.scale_and_center(zi,position_information["zrange"])

        if 
        scaled_point = (x, y, z)

        block = generate_block(genome, config, corner, args, block_options, scaled_point, change)
        if block is not None:
            snake.append(block)

        # Once it has reach the maximum length, it should stop
        if(len(snake) == args.MAX_SNAKE_LENGTH):
            done = True

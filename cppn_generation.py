# For neat
import neat

# For utility functions
import util

# For simple math functions
import math

# For minecraft
import grpc
import minecraft_pb2_grpc
from minecraft_pb2 import *

# Number of total directions the snake can move in
NUM_DIRECTIONS = 6

def query_cppn_for_shape(genome, config, corner, position_information, args, block_list):
        """
        Query CPPN at all voxel coordinates to generate the list of
        blocks that will eventually be rendered in the Minecraft server.

        Parameters:
        genome (DefaultGenome): A CPPN or some class that extends CPPNs
        config (Config): NEAT configurations
        corner (int,int,int): three-tuple of initial/minimal x,y,z coordinates for shape
        position_information (dict): A dictionary that contains the values of x, y, and z starting points and ranges
        args (argparse.Namespace): a collection of argument values collected at the command line
        block_list ([Block]): List of blocks that can be spawned in

        Returns:
        [Block]:List of Blocks to generate in Minecraft
        """
        # Create CPPN out of genome
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        
        # If not evolving block list, use the static one specified earlier. Otherwise, use the genome's list
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
                    # Ignores direction and stop results from 3-tuple result
                    (block, _, _) = generate_block(net, position_information, corner, args, block_options, scaled_point, change)
                    if block is not None:
                        shape.append(block)
        
        if(len(shape) == 0):
            print("Genome at corner {} is empty".format(corner))
        else:
            #print(list(BlockType.items()))
            #print(list(BlockType.keys()))
            print("Genome at corner {} generated {} blocks of these types: {}".format(corner,len(shape),set(map(lambda x: BlockType.keys()[x.type], shape))))

        return shape

def generate_block(net, position_information, corner, args, block_options, scaled_point, change): 
    """
    Returns a block to generate if it is present at a specific position and None
    if it isn't

    Parameters:
    net (FeedForwardNetwork): CPPN created from genome
    corner (int, int, int): three-tuple of initial/minimal x,y,z coordinates for shape
    args (argparse.Namespace): a collection of argument values collected at the command line 
    block_options ([Block]): List of blocks that can be spawned in 
    scaled_point (int, int, int): three-tuple of the position being looked at
    change (int, int, int): three-tuple used to scale the position of the point

    Returns:
    ((Block), (int,int,int), (bool)): Returns a tuple, including a block if it is present, None otherwise;
                                      a tuple that represents the direction that a block should be placed in next;
                                      a boolean that stops the snake from generating more blocks
    """
    # math.sqrt(2) is the usual scaling for radial distances in CPPNs
    center_dist = util.distance((scaled_point[0],scaled_point[1],scaled_point[2]),(0,0,0))
    output = net.activate([scaled_point[0], scaled_point[1], scaled_point[2], center_dist * math.sqrt(2), 1.0])
                    
    # First output determines whether there is a block at all.
    # If there is a block, argmax determines the max value and places the specified block 
    # from the list of possible blocks
    presence_threshold = args.PRESENCE_THRESHOLD 
                    
    if args.DISTANCE_PRESENCE_THRESHOLD:
        presence_threshold = args.DISTANCE_PRESENCE_MULTIPLIER * center_dist                            

    #print("block_options {}".format(block_options))
    #print("Outputs: {}".format(output))

    # Only generate non-air blocks by returning the block. If there is no
    # block, return None
    if output[0] >= presence_threshold: 
        block_preferences = output[1:len(block_options)+1]
        #print("Block prefs {}".format(block_preferences))
        output_val = util.argmax(block_preferences)
        assert (output_val >= 0 and output_val < len(block_options)),"{} out of bounds: {}".format(output_val,block_options)
        block = Block(position=Point(x=corner[0]+change[0], y=corner[1]+change[1], z=corner[2]+change[2]), type=block_options[output_val], orientation=NORTH)
    else:
        block = None

    direction = None
    stop = False

    if args.EVOLVE_SNAKE:
        direction_preferences = output[len(block_options)+1:len(block_options)+1+NUM_DIRECTIONS]
        direction_index = util.argmax(direction_preferences)
        print("Dir prefs before {}".format(direction_preferences))

        for i in range(NUM_DIRECTIONS):
            direction = next_direction(i)
            if args.CONFINE_SNAKES:
                if args.REDIRECT_CONFINED_SNAKES:
                    # changes the value to any direction that is out of bounds to float('-inf')
                    if (change[0] + direction[0] >= position_information["xrange"] or change[0] + direction[0] < 0) or (change[2] + direction[2] >= position_information["zrange"] or change[2] + direction[2] < 0):
                        direction_preferences[i] = float('-inf')
                        print("Dir prefs after {}".format(direction_preferences))
                if args.STOP_CONFINED_SNAKES:
                    # changes stop to true when the snake goes out of bounds
                    if (change[0] + direction[0] >= position_information["xrange"] or change[0] + direction[0] < 0) or (change[1] + direction[1] >= position_information["yrange"] or change[1] + direction[1] < 0) or (change[2] + direction[2] >= position_information["zrange"] or change[2] + direction[2] < 0):
                        stop = True
                    else:
                        stop = output[len(block_options)+1+NUM_DIRECTIONS] <= args.CONTINUATION_THRESHOLD
        #print("DIRECTION! {}, {}, {}".format(direction,direction_preferences,direction_index))
        

         

    return (block, direction, stop)

def next_direction(direction_index):
    """
    Returns a tuple that represents the change in direction the next block
    will be placed

    Parameters:
    direction_index (int): The index in the direction preferences list

    Returns:
    (int, int, int): Three-Tuple that represents the next direction the next block
                     should be placed
    """
    direction = [0,0,0] # One for x,y,z, but starts as list because tuples are immutable
    direction[direction_index % 3] = -1 if direction_index < 3 else 1
    direction = tuple(direction)
    return direction

def query_cppn_for_snake_shape(genome, config, corner, position_information, args, block_list):
    """
    Query cppn at the relative location of 0,0,0 to then render snake-like figures
    based on the continuation output. Once it has either reached a certain amount of 
    iterations or the length of the snake is now at the max, it will stop rendering.

    Parameters:
    genome (DefaultGenome): A CPPN or some class that extends CPPNs
    config (Config): NEAT configurations
    corner (int, int, int): three-tuple of initial/minimal x,y,z coordinates for shape
    position_information (dict): A dictionary that contains the values of x, y, and z starting points and ranges
    args (argparse.Namespace): a collection of argument values collected at the command line
    block_list ([Block]): List of blocks that will be used during rendering

    Returns:
    [Block]: List of blocks that render each of the snakes
    """
    
    # Create CPPN out of genome
    net = neat.nn.FeedForwardNetwork.create(genome, config)
        
    done = False

    number_of_iterations = 0

    # If not evolving block list, use the static one specified earlier. Otherwise, use the genome's list
    if not args.BLOCK_LIST_EVOLVES:
        block_options = block_list
    else:
        block_options = genome.block_list
    
    # Used to scale the point
    xi = int(position_information["xrange"]/2)
    yi = int(position_information["yrange"]/2)
    zi = int(position_information["zrange"]/2)

    snake = []
    while not done:
        number_of_iterations += 1
        print(number_of_iterations)
        x = util.scale_and_center(xi,position_information["xrange"])
        y = util.scale_and_center(yi,position_information["yrange"])
        z = util.scale_and_center(zi,position_information["zrange"])
        scaled_point = (x, y, z)
        change = (xi, yi, zi)

        (block, direction, stop) = generate_block(net, position_information, corner, args, block_options, scaled_point, change)

        #print("Returned direction: {}".format(direction))

        if block is not None:
            #print("block is not None")
            snake.append(block)


        #print("Stop? : {}".format(stop))
        #print("Length of snake: {}".format(len(snake)))
        #print("Snake contains {} blocks".format(snake))


        #print("Before: ({},{},{})".format(xi,yi,zi))

        # Once it has reach the maximum length, it should stop
        if(stop or number_of_iterations == args.MAX_SNAKE_LENGTH):
            #print("Stoped")
            done = True
            #print(done)
        else:
            xi += direction[0]
            yi += direction[1]
            zi += direction[2]

        

    
        #print("After : ({},{},{})".format(xi,yi,zi))

    return snake

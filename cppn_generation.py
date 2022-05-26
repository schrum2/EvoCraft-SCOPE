# For neat
import neat

# For utility functions
import util

# For simple math functions
import math

# For minecraft
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
        presence_threshold = args.PRESENCE_THRESHOLD
        done = False
        while not done:
            for xi in range(position_information["xrange"]):
                x = util.scale_and_center(xi,position_information["xrange"])
                for yi in range(position_information["yrange"]):
                    y = util.scale_and_center(yi,position_information["yrange"])
                    for zi in range(position_information["zrange"]):
                        z = util.scale_and_center(zi,position_information["zrange"])
                        scaled_point = (x, y, z)
                        change = (xi, yi, zi)
                        # Ignores direction and stop results from 3-tuple result
                        (block, _, _) = generate_block(net, position_information, corner, args, block_options, scaled_point, change, presence_threshold)
                        if block is not None:
                            shape.append(block)
            
            # If USE_MIN_BLOCK_REQUIREMENT is true, then we stop the while loop if the size of the shape meets the min number of required blocks
            if args.USE_MIN_BLOCK_REQUIREMENT: done = len(shape) >= args.MINIMUM_REQUIRED_BLOCKS
            # At this point we are done regardless of the if statement above.
            else: done = True
            
            # Decrease presence_thresold to decrease number of empty shapes
            if not done: presence_threshold -= args.MIN_BLOCK_PRESENCE_INCREMENT 

        if(len(shape) == 0):
            print("Genome at corner {} is empty".format(corner))
        else:
            print("Genome at corner {} generated {} blocks of these types: {}".format(corner,len(shape),set(map(lambda x: BlockType.keys()[x.type], shape))))

        return shape

def generate_block(net, position_information, corner, args, block_options, scaled_point, relative_position, presence_threshold): 
    """
    Returns a block to generate if it is present at a specific position and None
    if it isn't

    Parameters:
    net (FeedForwardNetwork): CPPN created from genome
    corner (int, int, int): three-tuple of initial/minimal x,y,z coordinates for shape
    args (argparse.Namespace): a collection of argument values collected at the command line 
    block_options ([Block]): List of blocks that can be spawned in 
    scaled_point (int, int, int): three-tuple of the position being looked at
    relative_position (int, int, int): three-tuple used to scale the position of the point

    Returns:
    ((Block), (int,int,int), (bool)): Returns a tuple, including a block if it is present, None otherwise;
                                      a tuple that represents the direction that a block should be placed in next;
                                      a boolean that stops the snake from generating more blocks
    """
    # math.sqrt(2) is the usual scaling for radial distances in CPPNs
    center_dist = util.distance((scaled_point[0],scaled_point[1],scaled_point[2]),(0,0,0))
    output = net.activate([scaled_point[0], scaled_point[1], scaled_point[2], center_dist * math.sqrt(2), 1.0])
                    
    if args.DISTANCE_PRESENCE_THRESHOLD:
        presence_threshold = args.DISTANCE_PRESENCE_MULTIPLIER * center_dist                            

    # Only generate non-air blocks by returning the block. If there is no
    # block, return None
    if output[0] >= presence_threshold: 
        block_preferences = output[1:len(block_options)+1]
        output_val = util.argmax(block_preferences)
        assert (output_val >= 0 and output_val < len(block_options)),"{} out of bounds: {}".format(output_val,block_options)

        # By default, block orientation is NORTH. can be altered by evolving orientation. If also
        # evolving snakes, sets parameters accordingly
        block_orientation = NORTH
        if args.EVOLVE_ORIENTATION:
            if args.EVOLVE_SNAKE:
                orientation_preferences = output[len(block_options)+NUM_DIRECTIONS+1:len(block_options)+1+2*NUM_DIRECTIONS]
            else: 
                orientation_preferences = output[len(block_options)+1:len(block_options)+1+NUM_DIRECTIONS] 
            block_orientation = util.argmax(orientation_preferences) # Argmax from 0-5 to get orienation of block
        block = Block(position=Point(x=corner[0]+relative_position[0], y=corner[1]+relative_position[1], z=corner[2]+relative_position[2]), type=block_options[output_val], orientation=block_orientation)
    else:
        block = None

    direction = None
    stop = False

    if args.EVOLVE_SNAKE:
        #print("generate_block:EVOLVE_SNAKE")
        direction_preferences = output[len(block_options)+1:len(block_options)+1+NUM_DIRECTIONS]
        if args.CONFINE_SNAKES and args.REDIRECT_CONFINED_SNAKES:
            # Movements that go out of bounds are made undesirable with a preference of negative infinity
            for i in range(NUM_DIRECTIONS):
                possible_direction = next_direction(i)
                # relative_position the value to any direction that is out of bounds to float('-inf')
                if check_out_of_bounds(relative_position, possible_direction, position_information):
                    direction_preferences[i] = float('-inf')

        # Pick most preferred direction
        direction_index = util.argmax(direction_preferences)
        direction = next_direction(direction_index)

        if args.CONFINE_SNAKES and args.STOP_CONFINED_SNAKES:
            # If confining snakes, simply stop when going out of bounds
            if check_out_of_bounds(relative_position, direction, position_information):
                stop = True

        # No matter what, do not allow placement at y lower than 0 since this is illegal
        if relative_position[1] + direction[1] < 0 :
            stop = True
        else: # Otherwise, stopping depends on continuation output
            stop = output[len(block_options)+1+NUM_DIRECTIONS] <= args.CONTINUATION_THRESHOLD

    return (block, direction, stop)

def check_out_of_bounds(initial_position, possible_direction, position_information):
    """
    Checks to see if the new possible position relative to the initial position is still
    in bounds

    Parameters:
    initial_position (int, int, int): Three-tuple that represents initial position
    possible_direction (int, int, int): Three-tuple that represents the change in from current position
    position_information (dict): Dictionary that stores the x, y, and z starting points and ranges

    Returns:
    (bool): True if it is out of bounds, false otherwise
    """
    out_of_bounds = False
    if initial_position[0] + possible_direction[0] >= position_information["xrange"] or initial_position[0] + possible_direction[0] < 0:
        out_of_bounds = True
    if initial_position[1] + possible_direction[1] >= position_information["yrange"] or initial_position[1] + possible_direction[1] < 0:
        out_of_bounds = True
    if initial_position[2] + possible_direction[2] >= position_information["zrange"] or initial_position[2] + possible_direction[2] < 0:
        out_of_bounds = True

    return out_of_bounds

def next_direction(direction_index):
    """
    Returns a tuple that represents the initial_position in direction the next block
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
    
    # Why is this separated out when args is already passed as a parameter?
    # For regular shape generation, this is required to make USE_MIN_BLOCK_REQUIREMENT
    # work. Such an option may also be used here eventually.
    presence_threshold = args.PRESENCE_THRESHOLD

    # Used to scale the point
    xi = int(position_information["xrange"]/2)
    yi = int(position_information["yrange"]/2)
    zi = int(position_information["zrange"]/2)

    snake = []
    while not done:
        number_of_iterations += 1
        x = util.scale_and_center(xi,position_information["xrange"])
        y = util.scale_and_center(yi,position_information["yrange"])
        z = util.scale_and_center(zi,position_information["zrange"])
        scaled_point = (x, y, z)
        initial_position = (xi, yi, zi)

        (block, direction, stop) = generate_block(net, position_information, corner, args, block_options, scaled_point, initial_position, presence_threshold)

        if block is not None:
            snake.append(block)

        # Once it has reach the maximum length, it should stop
        if(stop or number_of_iterations == args.MAX_SNAKE_LENGTH):
            done = True
        else:
            xi += direction[0]
            yi += direction[1]
            zi += direction[2]

    if(len(snake) == 0):
        print("Genome at corner {} is empty".format(corner))
    else:
        print("Genome at corner {} generated {} blocks of these types: {}".format(corner,len(snake),set(map(lambda x: BlockType.keys()[x.type], snake))))

    return snake

from minecraft_pb2 import *

def type_count(client, position_information, corner, args):
    """
    This function takes a starting corner as a parameter and goes 
    through all of the voxels in the space and counts the number of 
    occurences of the specified block type.

    Parameters:
    client (MinecraftServiceStub): Minecraft server stub being used.
    position_information (dict): Dictionary containing location related information.
    corner ((int, int, int)): Starting coordinates for search area.
    args (argparse.Namespace): A collection of argument values collected at the command line.

    Returns:
    int: The number of occurences of the specified block.
    """
    # return the max value fitness threshold if client is none
    # XRANGE * YRANGE * ZRANGE gives the max threshold since that would be the volume of the shape if all the blocks were non air blocks.
    if client is None: return args.XRANGE * args.YRANGE * args.ZRANGE
    
    # get the ending coordinates for x, y, and z
    endx= corner[0] + position_information["xrange"]
    endy= corner[1] + position_information["yrange"]
    endz= corner[2] + position_information["zrange"]
    
    # read all the blocks at once as one big block
    block_collection = client.readCube(Cube(
        min=Point(x=corner[0], y=corner[1], z=corner[2]),
        max=Point(x=endx, y=endy, z=endz)
    ))

    # The number of blocks is equal to the number of blocks in each coordinate times each other (x * y * z)
    block_count = 0
    for block in block_collection.blocks:
        if block.type == args.DESIRED_BLOCK:
            block_count += 1

    return block_count        

def type_target(client, position_information, corner, args):
    """
    This function function awards shapes that generate a specific number 
    of occurrences of a particular block.

    Parameters:
    client (MinecraftServiceStub): Minecraft server stub being used.
    position_information (dict): Dictionary containing location related information.
    corner ((int, int, int)): Starting coordinates for search area.
    args (argparse.Namespace): A collection of argument values collected at the command line.

    Returns:
    int: The absolute value of the desired block count minus the absolute value of the difference between the desired block count and the actual count.
    """
    # return the max value if client is none
    # args.DESIRED_BLOCK_COUNT would be the max threshold since that is the exact value of blocks that the shapes are measured against. 
    if client is None: return args.DESIRED_BLOCK_COUNT
    
    # Get the number of desired blocks
    current_block_count = type_count(client, position_information, corner, args)

    # Calculate the fitness
    return args.DESIRED_BLOCK_COUNT - abs((args.DESIRED_BLOCK_COUNT - current_block_count))
#def eval_fitness(genomes, config, fitness):

def occupied_count(client, position_information, corner, args):

    # return the max value fitness threshold if client is none
    if client is None: 
        volume = args.XRANGE * args.YRANGE * args.ZRANGE
        # Cannot have more blocks filled than the snake length if snakes are being evolved
        if args.EVOLVE_SNAKE: return min(volume,args.MAX_SNAKE_LENGTH)
        # XRANGE * YRANGE * ZRANGE gives the max threshold since that would be the volume of the shape if all the blocks were non air blocks.
        else: return volume

    # Counts the number of blocks
    number_of_blocks = 0

    endx= corner[0] + position_information["xrange"]
    endy= corner[1] + position_information["yrange"]
    endz= corner[2] + position_information["zrange"]

    # Read in all the blocks within the x, y, and z range
    all_the_blocks = client.readCube(Cube(
        min=Point(x=corner[0], y=corner[1], z=corner[2]),
        max=Point(x=endx, y=endy, z=endz)
    ))

    for filled in all_the_blocks.blocks:
        if filled.type != AIR:
            number_of_blocks += 1

    return number_of_blocks




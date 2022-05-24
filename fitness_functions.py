from minecraft_pb2 import *

def type_count(client, position_information, corner, block_type):
    """
    This function takes a starting corner as a parameter and goes 
    through all of the voxels in the space and counts the number of 
    occurences of the specified block type.

    Parameters:
    client (MinecraftServiceStub): Minecraft server stub being used.
    position_information (dict): Dictionary containing location related information.
    corner ((int, int, int)): Starting coordinates for search area.
    block_type (Block): Block being searched for.

    Returns:
    int: The number of occurences of the specified block.
    """

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
        if block.type == block_type:
            block_count += 1

    return block_count        

#def eval_fitness(genomes, config, fitness):

def occupied_count(client, position_information, corner):
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

    for filled in all_the_blocks:
        if filled.type is not AIR
            number_of_blocks += 1

    return number_of_blocks




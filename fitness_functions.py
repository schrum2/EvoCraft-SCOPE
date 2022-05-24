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
        if block.type == args.DESIRED_BLOCK:
            block_count += 1

    return block_count        

#def eval_fitness(genomes, config, fitness):
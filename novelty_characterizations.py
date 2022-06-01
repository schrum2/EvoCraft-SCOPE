from minecraft_pb2 import *
import collections
import block_sets

def presence_characterization(client, position_information, corner, args):
    """
    Creates a list of whether or not blocks exisit in a shape. To be compared to
    with one another

    Parameters:
    client (MinecraftServiceStub): Minecraft server stub being used.
    position_information (dict): Dictionary containing location related information.
    corner (int,int,int): 3-tuple defining minimal coordinates of generated object

    Return:
    block_character (list of ints): List containing where blocks are or are not present
    """
    # End points for all of the shapes
    endx= corner[0] + position_information["xrange"]-1
    endy= corner[1] + position_information["yrange"]-1
    endz= corner[2] + position_information["zrange"]-1

    # read all the blocks at once as one big block
    block_collection = client.readCube(Cube(
        min=Point(x=corner[0], y=corner[1], z=corner[2]),
        max=Point(x=endx, y=endy, z=endz)
    ))

    block_character = [] 
    # If a block is present, adds a 1 otherwise, adds 0 (air is not a block)
    for block in block_collection.blocks:
        if block.type == AIR:
            block_character.append(0)
        else:
            block_character.append(1)
    return block_character

def block_type_characterization(client, position_information, corner, args):
    """
    Adds all the blocks that were read in to a list based on their constant value

    Parameters:
    client (MinecraftServiceStub): Minecraft server stub being used.
    position_information (dict): Dictionary containing location related information.
    corner (int,int,int): 3-tuple defining minimal coordinates of generated object

    Return:
    block_types ([int]): list of all values in the shape
    """
    # End points for all of the shapes
    endx= corner[0] + position_information["xrange"]-1
    endy= corner[1] + position_information["yrange"]-1
    endz= corner[2] + position_information["zrange"]-1

    # read all the blocks at once as one big block
    block_collection = client.readCube(Cube(
        min=Point(x=corner[0], y=corner[1], z=corner[2]),
        max=Point(x=endx, y=endy, z=endz)
    ))
    block_types = []

    for block in block_collection.blocks:
        block_types.append(block.type)
    return block_types

def composition_characterization(client, position_information, corner, args):
     # End points for all of the shapes
    endx= corner[0] + position_information["xrange"]-1
    endy= corner[1] + position_information["yrange"]-1
    endz= corner[2] + position_information["zrange"]-1

    block_collection = client.readCube(Cube(
        min=Point(x=corner[0], y=corner[1], z=corner[2]),
        max=Point(x=endx, y=endy, z=endz)
    ))

    block_collection_types =[]
    for block in block_collection.blocks:
        block_collection_types.append(block.type)
    
    all_blocks_counter=collections.Counter(block_collection_types)

    final_result = []
    block_set = block_sets.select_possible_block_sets(args.POTENTIAL_BLOCK_SET)
    for type in block_set:
        final_result.append(all_blocks_counter[type])
    return final_result



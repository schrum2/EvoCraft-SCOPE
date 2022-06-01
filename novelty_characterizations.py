from minecraft_pb2 import *

def presence_characterization(client, position_information, corner):
    """
    Creates a list of whether or not blocks exisit in a shape. To be compared to
    with one another

    Parameters:
    client (MinecraftServiceStub): Minecraft server stub being used.
    position_information (dict): Dictionary containing location related information.

    Return:
    block_character (list of ints): List containing where blocks are or are not present
    """
    # End points for all of the shapes
    endx= corner[0] + position_information["xrange"]
    endy= corner[1] + position_information["yrange"]
    endz= corner[2] + position_information["zrange"]

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

def block_type_characterization(client, position_information, corner):
    # End points for all of the shapes
    endx= corner[0] + position_information["xrange"]
    endy= corner[1] + position_information["yrange"]
    endz= corner[2] + position_information["zrange"]

    # read all the blocks at once as one big block
    block_collection = client.readCube(Cube(
        min=Point(x=corner[0], y=corner[1], z=corner[2]),
        max=Point(x=endx, y=endy, z=endz)
    ))

    block_types = []

    for block in block_collection.blocks:
        block_types.append(block.type)
    return block_types
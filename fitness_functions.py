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

    block_count = 0
    endx= corner[0] + position_information["xrange"]
    endy= corner[1] + position_information["yrange"]
    endz= corner[2] + position_information["zrange"]
    
    # loop through x coordinates
    for xi in range(endx):

        # loop through y coordinates
        for yi in range(endy):

            # loop through z coordinates
            for zi in range(endz):

                # get the block to compare
                current_block = client.readCube(Cube(
                min=Point(x=corner[0] + xi, y=corner[1] + yi, z=corner[2] + zi),
                min=Point(x=corner[0] + xi, y=corner[1] + yi, z=corner[2] + zi)
                ))

                # increase block_count if the block is the same as block_type
                if current_block.blocks[0].type == block_type:
                    block_count += 1 

    return block_count        
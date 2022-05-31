from minecraft_pb2 import *

def presence_characterization(client, position_information, corner, args):
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
    for block in block_collection.blocks:
        if block.type == AIR:
            block_character.append(0)
        else:
            block_character.append(1)
    # for i in range(len(blocks)):
        
    #     if(blocks[i].blocks.value==AIR):
    #         block_collection.append(0)
    #     else:
    #         block_collection.append(1)
    return block_collection

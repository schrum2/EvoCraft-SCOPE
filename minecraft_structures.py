"""
Functions that alter any types of minecraft structures will be
kept in this module.
"""

# for Minecraft
#import grpc
from re import S
import minecraft_pb2_grpc
from minecraft_pb2 import *

# Extra space around the populated area to clear and reset
BUFFER_ZONE = 10
# Space above shapes to place the numbers
HEADROOM = 5
# y-coordinate for the ground
GROUND_LEVEL = 4
# y-coordinate for bedrock bottom
BEDROCK_LEVEL = 0

def place_fences(client, position_information, corner):
    """
    Places a fenced in area around a specific shape from the population
    that will be rendered in Minecraft. The size of the fenced in area
    is based off of the position_information and the mininal corner of the object.

    Parameters:
    client (MinecraftServiceStub): Minecraft server stub being used.
    position_information (dict): contains initial x,y,z coordinates and the x,y,z-sizes of each shape
    corner (int,int,int): 3-tuple defining minimal coordinates of generated object
    """

    fence = []
        
    # fill both x sides
    for xi in range(position_information["xrange"]+2):
        fence.append(Block(position=Point(x=corner[0]-1 + xi, y=GROUND_LEVEL, z=position_information["startz"]-1), type=DARK_OAK_FENCE, orientation=NORTH))
        fence.append(Block(position=Point(x=corner[0]-1 + xi, y=GROUND_LEVEL, z=position_information["startz"]+position_information["zrange"]), type=DARK_OAK_FENCE, orientation=NORTH))

    # fill both z sides
    for zi in range(position_information["zrange"]):
        fence.append(Block(position=Point(x=corner[0]-1,                                    y=GROUND_LEVEL,z=position_information["startz"]+zi), type=DARK_OAK_FENCE, orientation=NORTH))
        fence.append(Block(position=Point(x=corner[0]-1 + position_information["xrange"]+1, y=GROUND_LEVEL,z=position_information["startz"]+zi), type=DARK_OAK_FENCE, orientation=NORTH))

    client.spawnBlocks(Blocks(blocks=fence))

def clear_area(client, position_information, pop_size, space_between):
    """
    This function clears a large area by creating one
    large cube and filling it with air blocks.

    Parameters:
    client (MinecraftServiceStub): Minecraft server stub being used.
    position_information (dict): contains initial x,y,z coordinates and the x,y,z-sizes of each shape
    pop_size (int): The size of the population.
    space_between (int): block units between adjacent shapes
    """
    # Block units around the area that are also wiped
    zplacement = position_information["startz"] - BUFFER_ZONE

    # clear out a big area rather than individual cubes
    client.fillCube(FillCubeRequest(  
        cube=Cube(
            min=Point(x=position_information["startx"]-BUFFER_ZONE, y=GROUND_LEVEL, z=zplacement-BUFFER_ZONE),
            max=Point(x=position_information["startx"]-1 + (pop_size+1)*(position_information["xrange"]+space_between)+BUFFER_ZONE, y=position_information["starty"]+BUFFER_ZONE, z=position_information["startz"]+position_information["zrange"]+BUFFER_ZONE)
        ),
        type=AIR
    ))

def restore_ground(client, position_information, pop_size, space_between):
    """
    Resets the ground that could have been damaged by the structures or 
    that may contain a selection switch. 

    Parameters:
    client (MinecraftServiceStub): Minecraft server stub being used.
    position_information (dict): contains initial x,y,z coordinates and the x,y,z-sizes of each shape
    pop_size (int): The size of the population
    space_between (int): block units between adjacent shapes
    """    
    zplacement = position_information["startz"] - BUFFER_ZONE

    # fill the ground with dirt up until bedrock
    client.fillCube(FillCubeRequest(  
        cube=Cube(
            min=Point(x=position_information["startx"]-BUFFER_ZONE, y=GROUND_LEVEL-3, z=zplacement-BUFFER_ZONE),
            max=Point(x=position_information["startx"]-1 + pop_size*(position_information["xrange"]+space_between)+BUFFER_ZONE, y=GROUND_LEVEL-1, z=position_information["startz"]+position_information["zrange"]+BUFFER_ZONE)
        ),
        type=GRASS
    ))

    # fill out the bedrock since there may be pistons in there
    client.fillCube(FillCubeRequest(  
        cube=Cube(
            min=Point(x=position_information["startx"]-7, y=BEDROCK_LEVEL, z=zplacement-7),
            max=Point(x=position_information["startx"]-1 + pop_size*(position_information["xrange"]+1)+7, y=BEDROCK_LEVEL, z=position_information["zrange"]+7)
        ),
        type=BEDROCK
    ))

def place_number(client,position_information,corner,num):
    """
    Places a glowstone-generated number above a generated shape depending on what digit it is
    in the range of 0-9. 

    Parameters:
    client (MinecraftServiceStub): Minecraft server stub being used.
    position_information (dict): contains initial x,y,z coordinates and the x,y,z-sizes of each shape
    corner (int,int,int): 3-tuple defining minimal coordinates of generated object
    num (int): The digit that will be placed
    """

    # Coordinates for bottom of number shape
    x = corner[0] + int(position_information["xrange"]/2) - 2
    y = corner[1] + position_information["yrange"] + HEADROOM
    z = corner[2]

    if num == 0:
        number = [
            Block(position=Point(x=x,   y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+1,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+3,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+1,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+3,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH)]
    elif num == 1:
        number = [
            Block(position=Point(x=x,   y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+1,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+3,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH)]
    elif num == 2:
        number = [ 
            Block(position=Point(x=x,   y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+3,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+1,  z=z), type=GLOWSTONE, orientation=NORTH)]
           
    elif num == 3:
        number = [
            Block(position=Point(x=x,   y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            
            Block(position=Point(x=x,   y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            
            Block(position=Point(x=x,   y=y+3,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+1,  z=z), type=GLOWSTONE, orientation=NORTH)]
    elif num == 4:
        number = [
            Block(position=Point(x=x,   y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+1,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+3,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+3,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH)]
    elif num == 5:
        number = [
            Block(position=Point(x=x,   y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+1,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+3,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH)]
    elif num == 6:
        number = [
            Block(position=Point(x=x,   y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+1,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+1,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+3,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH)]
    elif num == 7:
        number = [
            Block(position=Point(x=x,   y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+3,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+1,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y,    z=z), type=GLOWSTONE, orientation=NORTH)]
    elif num == 8:
        number = [
            Block(position=Point(x=x,   y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+1,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+1,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+3,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+3,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH)]
    else:
        # number is 9 at this point
        number = [
            Block(position=Point(x=x,   y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+1,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+3,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+3,  z=z), type=GLOWSTONE, orientation=NORTH)]

    client.spawnBlocks(Blocks(blocks=number))

def place_blocks_in_block_list(block_list,client,corners,position_information,shape_set,only_show_placed):
    """
    Takes in the block list from a genome and places instances of each of the blocks
    in front of the generated shape.

    Parameters:
    block_list(list of ints): holds all of the block types to be placed 
    client (MinecraftServiceStub): Minecraft server stub being used
    corners(tuple(int,int,int)): holds the points to be used for placing the blocks
    position_information(dict): contains all the information regarding the start positions and ranges 
    """
    blocks_in_list = []
    # Start positions relative to each of the shape's corners
    x=0 
    z=-8
    index=0

    while(index<len(block_list)):
        # Generates blovk at the specified index, places emerald block underneath it
        if(only_show_placed):
            if(block_list[index] in shape_set):
                place_spawned_blocks(block_list, corners, blocks_in_list, x, z, index)
            else:
                blocks_in_list.append(Block(position=Point(x=corners[0]+x, y=corners[1]-2,z=corners[2]+z), type=RED_SANDSTONE, orientation=NORTH))
        else:
            place_spawned_blocks(block_list, corners, blocks_in_list, x, z, index)

        index=index+1
        x=x+2 # x increase by two for a one block gap
        if(x>=position_information["xrange"]): # Once it gets to the end of the range, goes to the next row
            z=z+2
    # Spawns in all the blocks
    client.spawnBlocks(Blocks(blocks=blocks_in_list))

def place_spawned_blocks(block_list, corners, blocks_in_list, x, z, index):
    """
    Helper method refactored from place_blocks_in_block_list. Places the blocks specified, adding an emerald block
    underneath all generated blocks

    Parameters:
    block_list(list of ints): holds all of the block types to be placed 
    corners(tuple(int,int,int)): holds the points to be used for placing the blocks
    x(int): used to palce blocks at correct x cooridnate based on corners
    z(int): used to palce blocks at correct z cooridnate based on corners
    index(int): USed to get correct index from the block_list
    """
    generated_block=(Block(position=Point(x=corners[0]+x, y=corners[1]-1,z=corners[2]+z), type=block_list[index], orientation=NORTH))
    blocks_in_list.append(generated_block)
    blocks_in_list.append(Block(position=Point(x=corners[0]+x, y=corners[1]-2,z=corners[2]+z), type=EMERALD_BLOCK, orientation=NORTH))

    # If the block is lava or water, places a box around it
    if(generated_block.type==LAVA or generated_block.type==WATER or generated_block.type==FLOWING_LAVA or generated_block.type==FLOWING_WATER):
        blocks_in_list.append(Block(position=Point(x=corners[0]+x, y=corners[1]-1,z=corners[2]+z+1), type=STONE_BRICK_STAIRS, orientation=NORTH))
        blocks_in_list.append(Block(position=Point(x=corners[0]+x, y=corners[1]-1,z=corners[2]+z-1), type=STONE_BRICK_STAIRS, orientation=SOUTH))
        blocks_in_list.append(Block(position=Point(x=corners[0]+x+1, y=corners[1]-1,z=corners[2]+z), type=STONE_BRICK_STAIRS, orientation=WEST))
        blocks_in_list.append(Block(position=Point(x=corners[0]+x-1, y=corners[1]-1,z=corners[2]+z), type=STONE_BRICK_STAIRS, orientation=EAST))
    
def player_selection_switches(client, position_information, corners):
    """
    Spawns the switches the a player can use to select their preferred
    structures along with the switch that is used to indicate that they are
    done selecting. Then it returns the position of all the points
    right below the redstone lamps for both the selection switches and
    the next generation switch

    Parameters:
    client (MinecraftServiceStub): Interface to Minecraft
    position_information (dict): contains initial x,y,z coordinates and the x,y,z-sizes of each shape
    corners [(int,int,int)]: list of 3-tuples defining minimal coordinates of each generated object

    Returns:
    ([(int,int,int)],[(int,int,int)]):  List of positions of the spaces below the redstone lamps for 
                                        selection, followed by list of spaces below pistons that activate
                                        to switch to the next generation.
    """
    # Block lists that will be spawned
    to_spawn = []

    # z coordinate needs to back away from the shapes if they generate water or lava
    zplacement = position_information["startz"] - BUFFER_ZONE

    # list that stores the position of the redstone block 
    # that is moved when the player flicks the switch
    on_block_positions = []

    # stores the positions underneath the piston which indicate
    # if the player wants to see the next generation of structures
    next_block_positions = []

    #add the lamp in first when there is still ground underneath it to avoid the spawning of the grass blocks
    for corner in corners:
        middle = corner[0] + int(position_information["xrange"]/2)
        to_spawn.append(Block(position=Point(x=middle - 1, y=GROUND_LEVEL, z=zplacement-4), type=REDSTONE_LAMP, orientation=UP))
        # clear out the section for the redstone part of the swtich
        client.fillCube(FillCubeRequest(  
            cube=Cube(
                min=Point(x=middle - 3, y=GROUND_LEVEL-3, z=zplacement-5), 
                max=Point(x=middle + 1, y=GROUND_LEVEL-1, z=zplacement-2)   
            ),
            type=AIR
        ))

        # Now spawn in everything for the selection switches
        # add in the piston, redstone block, redstone lamp, lever, cobblestone blocks, and redstone dust to switch
        to_spawn.append(Block(position=Point(x=middle - 1, y=BEDROCK_LEVEL, z=zplacement-4), type=STICKY_PISTON, orientation=UP))
        to_spawn.append(Block(position=Point(x=middle - 1, y=BEDROCK_LEVEL+1, z=zplacement-4), type=SLIME, orientation=NORTH))

        # this is the position of each redstone block when the lever is switched on
        on_block_position = (middle - 1, GROUND_LEVEL-1, zplacement-4)
        to_spawn.append(Block(position=Point(x=on_block_position[0], y=on_block_position[1] - 1, z=on_block_position[2]), type=REDSTONE_BLOCK, orientation=NORTH))
        # stores the positions from above
        on_block_positions.append(on_block_position)

        # Ground that was emptied into AIR earlier. Some of it needs to be restored
        to_spawn.append(Block(position=Point(x=middle,     y=GROUND_LEVEL-1, z=zplacement-5), type=GRASS, orientation=NORTH))
        to_spawn.append(Block(position=Point(x=middle - 1, y=GROUND_LEVEL-1, z=zplacement-5), type=GRASS, orientation=NORTH)) # has a tail now
        to_spawn.append(Block(position=Point(x=middle - 2, y=GROUND_LEVEL-1, z=zplacement-5), type=GRASS, orientation=NORTH))
        to_spawn.append(Block(position=Point(x=middle - 3, y=GROUND_LEVEL-1, z=zplacement-5), type=GRASS, orientation=NORTH))

        # slabs to put around the mechanism
        for slab in range(0,3):
            to_spawn.append(Block(position=Point(x=middle + 1, y=GROUND_LEVEL, z=zplacement-4 + slab), type=STONEBRICK, orientation=NORTH))
            to_spawn.append(Block(position=Point(x=middle,     y=GROUND_LEVEL, z=zplacement-4 + slab), type=STONE_SLAB, orientation=NORTH))
            to_spawn.append(Block(position=Point(x=middle - 1, y=GROUND_LEVEL, z=zplacement-3 + slab), type=STONE_SLAB, orientation=NORTH)) # has a tail now
            to_spawn.append(Block(position=Point(x=middle - 2, y=GROUND_LEVEL, z=zplacement-4 + slab), type=STONE_SLAB, orientation=NORTH))
            to_spawn.append(Block(position=Point(x=middle - 3, y=GROUND_LEVEL, z=zplacement-4 + slab), type=STONEBRICK, orientation=NORTH))
            to_spawn.append(Block(position=Point(x=middle - 2 + slab, y=GROUND_LEVEL, z=zplacement- 1), type=STONEBRICK, orientation=NORTH)) # makes tail less noticeable

        # add in the rest of the blocks needed 
        to_spawn.append(Block(position=Point(x=middle - 3, y=GROUND_LEVEL, z=zplacement-5), type=LEVER, orientation=UP))
        to_spawn.append(Block(position=Point(x=middle - 3, y=BEDROCK_LEVEL+1, z=zplacement-3), type=COBBLESTONE, orientation=NORTH))
        to_spawn.append(Block(position=Point(x=middle - 3, y=BEDROCK_LEVEL+2, z=zplacement-4), type=COBBLESTONE, orientation=NORTH))
        to_spawn.append(Block(position=Point(x=middle - 1, y=BEDROCK_LEVEL+1, z=zplacement-3), type=REDSTONE_WIRE, orientation=NORTH))
        to_spawn.append(Block(position=Point(x=middle - 2, y=BEDROCK_LEVEL+1, z=zplacement-3), type=REDSTONE_WIRE, orientation=NORTH))
        to_spawn.append(Block(position=Point(x=middle - 3, y=BEDROCK_LEVEL+2, z=zplacement-3), type=REDSTONE_WIRE, orientation=NORTH))
        to_spawn.append(Block(position=Point(x=middle - 3, y=BEDROCK_LEVEL+3, z=zplacement-4), type=REDSTONE_WIRE, orientation=NORTH))
   
        # add in the piston and button
        # stores the position underneath one piston as it loops through
        next_block_position = (middle + 1,GROUND_LEVEL - 2,zplacement-5)
        to_spawn.append(Block(position=Point(x=next_block_position[0], y=next_block_position[1]+1, z=next_block_position[2]), type=PISTON, orientation=DOWN))
        next_block_positions.append(next_block_position)
        to_spawn.append(Block(position=Point(x=next_block_position[0], y=GROUND_LEVEL, z=zplacement-5), type=WOODEN_BUTTON, orientation=NORTH))
    
    # spawn in all the blocks
    client.spawnBlocks(Blocks(blocks=to_spawn))

    return (on_block_positions,next_block_positions)

def read_current_block_options(client,placements,position_information):
    """
    Used when users can change the blocks in evolved shapes from within the game.
    Checks the blocks on display in front of each evolved shape and collects them in a list,
    where each such list is combined into a list of lists that is returned. The returned
    list will indicate all block types currently specified (on display) for each shape.

    Parameters:
    client (MinecraftServiceStub): Interface to Minecraft
    placements(list of tuples(int,int,int)): list of all of the corner coordinates for the shapes
    position_information (dict): contains initial x,y,z coordinates and the x,y,z-sizes of each shape

    Returns:
    blocks_for_shape(list of lists of ints): returns what was read in from the minecraft world for each shape
    """
    blocks_for_shape = []
    # Loops through all corners for each shape
    for corner in placements:
        # Reads in all blocks on the x range
        blocks = client.readCube(Cube(
                    min=Point(x=corner[0], y=position_information["starty"]-1, z=position_information["startz"]-8),
                    max=Point(x=corner[0]+position_information["xrange"]-2, y=position_information["starty"]-1, z=position_information["startz"]-8)
                 ))
        
        block_list = []
        index = 0
        # loops through every other block, getting its block type
        while index < len(blocks.blocks):
            block_list.append(blocks.blocks[index].type)
            index += 2 # Skip over spaces between blocks 
        blocks_for_shape.append(block_list) # Adds the list to a list
    return blocks_for_shape # Returns all blocks for all shapes

def declare_champion(client,position_information,corner,args):
    """
    Places a glowstone-generated arrow pointing down on the shape that met the fitness
    threshold value. 

    Parameters:
    client (MinecraftServiceStub): Minecraft server stub being used.
    position_information (dict): contains initial x,y,z coordinates and the x,y,z-sizes of each shape
    corner (int,int,int): 3-tuple defining minimal coordinates of generated object
    args (argparse.Namespace): A collection of argument values collected at the command line
    """

    # Coordinates for bottom of number shape
    x = corner[0] + int(position_information["xrange"]/2) - 2
    y = corner[1] + position_information["yrange"] + HEADROOM - 1
    z = corner[2]

    # make arrow out of glowstone
    arrow = [            
            Block(position=Point(x=x+1,   y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1,   y=y+1,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1,   y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1,   y=y+3,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1,   y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1,   y=y+5,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2,   y=y,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2,   y=y+1,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2,   y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2,   y=y+3,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2,   y=y+4,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2,   y=y+5,  z=z), type=GLOWSTONE, orientation=NORTH),            
            Block(position=Point(x=x+3, y=y+1,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x, y=y+1,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+4, y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x, y=y+2,    z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x-1, y=y+2,  z=z), type=GLOWSTONE, orientation=NORTH)]
    
    client.spawnBlocks(Blocks(blocks=arrow))

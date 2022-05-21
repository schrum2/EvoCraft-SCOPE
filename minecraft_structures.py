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

def place_fences(client, position_information, corner, pop_size):
    """
    Places a fenced in area around each of the shapes from the population
    that will be rendered in Minecraft. The size of the fenced in areas
    is based off of instance variables, as is the location.

    THESE PARAMETERS NEED TO BE UPDATED!

    Parameters:
    client (MinecraftServiceStub): Minecraft server stub being used.
    position_information (dict): contains initial x,y,z coordinates and the x,y,z-sizes of each shape
    corner (???): ???
    pop_size (int): Fenced in areas to generate in a row
    """
    # clear out previous fences
    client.fillCube(FillCubeRequest(  
            cube=Cube(
                min=Point(x=corner[0]-1, y=position_information["starty"]-1, z=position_information["startz"]-1),
                max=Point(x=corner[0]-1 + pop_size*(position_information["xrange"]+1)+1, y=position_information["starty"]-1, z=position_information["startz"]+2)
            ),
            type=AIR
        ))

    fence = []
        
    # fill both x sides
    for xi in range(position_information["xrange"]+2):
        fence.append(Block(position=Point(x=corner[0]-1 + xi, y=position_information["starty"]-1,z=position_information["startz"]-1), type=DARK_OAK_FENCE, orientation=NORTH))
        fence.append(Block(position=Point(x=corner[0]-1 + xi, y=position_information["starty"]-1,z=position_information["startz"]+position_information["zrange"]), type=DARK_OAK_FENCE, orientation=NORTH))

    # fill both z sides
    for zi in range(position_information["zrange"]+1):
        fence.append(Block(position=Point(x=corner[0]-1, y=position_information["starty"]-1,z=position_information["startz"] + zi), type=DARK_OAK_FENCE, orientation=NORTH))
        fence.append(Block(position=Point(x=corner[0]-1 + position_information["xrange"]+1, y=position_information["starty"]-1,z=position_information["startz"]+zi), type=DARK_OAK_FENCE, orientation=NORTH))

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
            min=Point(x=position_information["startx"]-BUFFER_ZONE, y=position_information["starty"]-1, z=zplacement-BUFFER_ZONE),
            max=Point(x=position_information["startx"]-1 + pop_size*(position_information["xrange"]+space_between)+BUFFER_ZONE, y=position_information["starty"]+BUFFER_ZONE, z=position_information["startz"]+position_information["zrange"]+BUFFER_ZONE)
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
            min=Point(x=position_information["startx"]-BUFFER_ZONE, y=position_information["starty"]-4, z=zplacement-BUFFER_ZONE),
            max=Point(x=position_information["startx"]-1 + pop_size*(position_information["xrange"]+space_between)+BUFFER_ZONE, y=position_information["starty"]-2, z=position_information["startz"]+position_information["zrange"]+BUFFER_ZONE)
        ),
        type=GRASS
    ))

    # fill out the bedrock since there may be pistons in there
    client.fillCube(FillCubeRequest(  
        cube=Cube(
            min=Point(x=position_information["startx"]-7, y=position_information["starty"]-5, z=zplacement-7),
            max=Point(x=position_information["startx"]-1 + pop_size*(position_information["xrange"]+1)+7, y=position_information["starty"]-5, z=position_information["zrange"]+7)
        ),
        type=BEDROCK
    ))

def place_number(client,x,y,z,num):
    """
        Places a glowstone-generated number above a generated shape depending on what digit it is
        in the range of 0-9. 

        Parameters:
        client (MinecraftServiceStub): Minecraft server stub being used.
        x (int): The x coordinate where the number will start
        y (int): The y coordinate where the number will start
        z (int): The z coordinate where the number will start
        num (int): The digit that will be placed
    """
        
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

def place_blocks_in_block_list(block_list,client,position_information,genome_id):
    blocks_in_list = []
    block_list_to_compare = []
    # for i  in range(pop_size):
    x=0
    z=-9
    index=0

    
    while(index<len(block_list)):
        generated_block=(Block(position=Point(x=position_information["startx"]+11*genome_id+x, y=position_information["starty"]-1,z=position_information["startz"]+z), type=block_list[index], orientation=NORTH))
        blocks_in_list.append(generated_block)
        blocks_in_list.append(Block(position=Point(x=position_information["startx"]+11*genome_id+x, y=position_information["starty"]-2,z=position_information["startz"]+z), type=EMERALD_BLOCK, orientation=NORTH))
        
        block_list_to_compare.append(generated_block)

        if(generated_block.type==LAVA or generated_block.type==WATER):
            blocks_in_list.append(Block(position=Point(x=position_information["startx"]+11*genome_id+x-1, y=position_information["starty"]-1,z=position_information["startz"]+z), type=STONE_BRICK_STAIRS, orientation=EAST))
            blocks_in_list.append(Block(position=Point(x=position_information["startx"]+11*genome_id+x+1, y=position_information["starty"]-1,z=position_information["startz"]+z), type=STONE_BRICK_STAIRS, orientation=WEST))

            blocks_in_list.append(Block(position=Point(x=position_information["startx"]+11*genome_id+x, y=position_information["starty"]-1,z=position_information["startz"]+z+1), type=STONE_BRICK_STAIRS, orientation=NORTH))
            blocks_in_list.append(Block(position=Point(x=position_information["startx"]+11*genome_id+x, y=position_information["starty"]-1,z=position_information["startz"]+z-1), type=STONE_BRICK_STAIRS, orientation=SOUTH))

        # TODO: Generalize and explain these magic numbers. Define in terms of other position values
        x=x+2
        if(x>8):
            z=z+2
        index=index+1
    # print(block_list_to_compare)
    client.spawnBlocks(Blocks(blocks=blocks_in_list))
    
def player_selection_switches(pop_size, client, position_information):
    """
    Spawns the switches the a player can use to select their preferred
    structures along with the switch that is used to indicate that they are
    done selected. Then it returns the position of all the points
    right below the redstone lamps for both the selection switches and
    the next generation switch

    Parameters:
    pop_size (int): Number of selection switches being selected
    client (MinecraftServiceStub): Interface to Minecraft
    position_information["startx"] (int): Integer that indicates the start of the range in x direction
    startz (int): Integer that indicates the start of the range in z direction
    xrange (int): Range of the x coordinate values

    Returns:
    [(int,int,int)]:The position of the space below the redstone lamp for the
                    list of positions right under each of the redstone lamps for
                    the selection switches
    """
    switch = []
    lamps = []

    # z coordinate needs to back away from the shapes if they generate water or lava
    zplacement = position_information["startz"] - 10

    #add the lamp in first when there is still ground underneath it to avoid the spawning of the grass blocks
    for p in range(pop_size):
        lamps.append(Block(position=Point(x=position_information["startx"] + p*(position_information["xrange"]+1) + int(position_information["xrange"]/2) - 1, y=position_information["starty"]-1, z=zplacement-4), type=REDSTONE_LAMP, orientation=UP))
        #lamps.append(Block(position=Point(x=position_information["startx"] + p*(position_information["xrange"]+1) + int(position_information["xrange"]/2), y=position_information["starty"]-1, z=zplacement-4), type=AIR, orientation=UP))
        #lamps.append(Block(position=Point(x=position_information["startx"] + p*(position_information["xrange"]+1) + int(position_information["xrange"]/2) - 1, y=position_information["starty"]-1, z=zplacement-5), type=AIR, orientation=UP))
    client.spawnBlocks(Blocks(blocks=lamps))

    # clear out the section for the redstone part of the swtich
    for n in range(pop_size):
        client.fillCube(FillCubeRequest(  
                cube=Cube(
                        min=Point(x=position_information["startx"] + n*(position_information["xrange"]+1) + int(position_information["xrange"]/2) - 3, y=1, z=zplacement-4), # subject to change
                        max=Point(x=position_information["startx"] + n*(position_information["xrange"]+1) + int(position_information["xrange"]/2) - 1, y=3, z=zplacement-2)  # subject to change (y = 4 is ground level)
                ),
                type=AIR
            ))

    # Now spawn in everything for the selection switches

    # list that stores the position of the redstone block 
    # that is moved when the player flicks the switch
    on_block_positions = []

    # add in the piston, redstone block, redstone lamp, lever, cobblestone blocks, and redstone dust to switch
    for p in range(pop_size):
        switch.append(Block(position=Point(x=position_information["startx"] + p*(position_information["xrange"]+1) + int(position_information["xrange"]/2) - 1, y=position_information["starty"]-5, z=zplacement-4), type=STICKY_PISTON, orientation=UP))
        switch.append(Block(position=Point(x=position_information["startx"] + p*(position_information["xrange"]+1) + int(position_information["xrange"]/2) - 1, y=position_information["starty"]-4, z=zplacement-4), type=SLIME, orientation=NORTH))

        # this is the position of each redstone block when the lever is switched on
        on_block_position = (position_information["startx"] + p*(position_information["xrange"]+1) + int(position_information["xrange"]/2) - 1, position_information["starty"]-2, zplacement-4)
        switch.append(Block(position=Point(x=on_block_position[0], y=on_block_position[1] - 1, z=on_block_position[2]), type=REDSTONE_BLOCK, orientation=NORTH))
        # stores the positions from above
        on_block_positions.append(on_block_position)

        # slabs to put around the mechanism
        for slab in range(0,3):
            switch.append(Block(position=Point(x=position_information["startx"] + p*(position_information["xrange"] +1) + int(position_information["xrange"]/2) + 1, y=position_information["starty"] - 1, z=zplacement-4 + slab), type=STONEBRICK, orientation=NORTH))
            switch.append(Block(position=Point(x=position_information["startx"]  + p*(position_information["xrange"]+1) + int(position_information["xrange"]/2), y=position_information["starty"] - 1, z=zplacement-4 + slab), type=STONE_SLAB, orientation=NORTH))
            switch.append(Block(position=Point(x=position_information["startx"]  + p*(position_information["xrange"]+1) + int(position_information["xrange"]/2) - 1, y=position_information["starty"] - 1, z=zplacement-3 + slab), type=STONE_SLAB, orientation=NORTH)) # has a tail now
            switch.append(Block(position=Point(x=position_information["startx"]  + p*(position_information["xrange"]+1) + int(position_information["xrange"]/2) - 2, y=position_information["starty"] - 1, z=zplacement-4 + slab), type=STONE_SLAB, orientation=NORTH))
            switch.append(Block(position=Point(x=position_information["startx"]  + p*(position_information["xrange"]+1) + int(position_information["xrange"]/2) - 3, y=position_information["starty"] - 1, z=zplacement-4 + slab), type=STONEBRICK, orientation=NORTH))
            switch.append(Block(position=Point(x=position_information["startx"]  + p*(position_information["xrange"]+1) + int(position_information["xrange"]/2) - 2 + slab, y=position_information["starty"] - 1, z=zplacement- 1), type=STONEBRICK, orientation=NORTH)) # makes tail less noticeable

        # add in the rest of the blocks needed 
        switch.append(Block(position=Point(x=position_information["startx"]  + p*(position_information["xrange"]+1) + int(position_information["xrange"]/2) - 3, y=position_information["starty"] - 1, z=zplacement-5), type=LEVER, orientation=UP))
        switch.append(Block(position=Point(x=position_information["startx"]  + p*(position_information["xrange"]+1) + int(position_information["xrange"]/2) - 3, y=position_information["starty"] - 4, z=zplacement-3), type=COBBLESTONE, orientation=NORTH))
        switch.append(Block(position=Point(x=position_information["startx"]  + p*(position_information["xrange"]+1) + int(position_information["xrange"]/2) - 3, y=position_information["starty"] - 3, z=zplacement-4), type=COBBLESTONE, orientation=NORTH))
        switch.append(Block(position=Point(x=position_information["startx"]  + p*(position_information["xrange"]+1) + int(position_information["xrange"]/2) - 1, y=position_information["starty"] - 4, z=zplacement-3), type=REDSTONE_WIRE, orientation=NORTH))
        switch.append(Block(position=Point(x=position_information["startx"]  + p*(position_information["xrange"]+1) + int(position_information["xrange"]/2) - 2, y=position_information["starty"] - 4, z=zplacement-3), type=REDSTONE_WIRE, orientation=NORTH))
        switch.append(Block(position=Point(x=position_information["startx"]  + p*(position_information["xrange"]+1) + int(position_information["xrange"]/2) - 3, y=position_information["starty"] - 3, z=zplacement-3), type=REDSTONE_WIRE, orientation=NORTH))
        switch.append(Block(position=Point(x=position_information["startx"]  + p*(position_information["xrange"]+1) + int(position_information["xrange"]/2) - 3, y=position_information["starty"] - 2, z=zplacement-4), type=REDSTONE_WIRE, orientation=NORTH))
   
    # spawn in all the switches
    client.spawnBlocks(Blocks(blocks=switch))

    return on_block_positions

def player_next_gen_switch(position_information, client):
    """
    Adds in all the blocks necessary to make a next generation
    button that the player can use to indicate when they want to
    move on to see the next generation of structures and returns the 
    position under the redstone lamp that indicates whether the player
    is done or not.

    Parameters:
    startx (int): Integer that indicates the start of the range in x direction
    startz (int): Integer that indicates the start of the range in z direction
    client (MinecraftServiceStub): TODO

    Returns:
    (int, int, int): Position of the space underneath the redstone lamp that
            is used to indicate if the player is ready to see the next generation
            of structures 
    """

    next_gen_switch = []
    lamp = []
    
    # z coordinate needs to back away from the shapes if they generate water or lava
    zplacement = position_information["startz"] - 10

    # add the lamp in first when there is still ground underneath it to avoid the spawning of the grass blocks
    lamp.append(Block(position=Point(x=position_information["startx"] - 4, y=position_information["starty"] - 1, z=zplacement-4), type=REDSTONE_LAMP, orientation=DOWN))
    lamp.append(Block(position=Point(x=position_information["startx"] - 3, y=position_information["starty"] - 1, z=zplacement-4), type=AIR, orientation=UP))
    lamp.append(Block(position=Point(x=position_information["startx"] - 4, y=position_information["starty"] - 1, z=zplacement-5), type=AIR, orientation=UP))
    client.spawnBlocks(Blocks(blocks=lamp))

    # clear out the section for the next gen switch
    client.fillCube(FillCubeRequest(  
            cube=Cube(
                min=Point(x=position_information["startx"] - 6, y=position_information["starty"] - 4, z=zplacement-4), 
                max=Point(x=position_information["startx"] - 4, y=position_information["starty"] - 2, z=zplacement-2)  
            ),
            type=AIR
        ))
        
    # add in all the components for the next gen switch to switch
    next_gen_switch.append(Block(position=Point(x=position_information["startx"] - 4, y=position_information["starty"] - 5, z=zplacement-4), type=STICKY_PISTON, orientation=UP))
    next_gen_switch.append(Block(position=Point(x=position_information["startx"] - 4, y=position_information["starty"] - 4, z=zplacement-4), type=SLIME, orientation=UP))
    done_block_position = (position_information["startx"] - 4, position_information["starty"]- 2, zplacement-4)
    next_gen_switch.append(Block(position=Point(x=done_block_position[0], y=done_block_position[1] - 1, z=done_block_position[2]), type=REDSTONE_BLOCK, orientation=NORTH))

    for slab in range(0,3):
        next_gen_switch.append(Block(position=Point(x=position_information["startx"] - 2, y=position_information["starty"] - 1, z=zplacement-4 + slab), type=EMERALD_BLOCK, orientation=NORTH))
        next_gen_switch.append(Block(position=Point(x=position_information["startx"] - 3, y=position_information["starty"] - 1, z=zplacement-4 + slab), type=STONE_SLAB, orientation=NORTH))
        next_gen_switch.append(Block(position=Point(x=position_information["startx"] - 4, y=position_information["starty"] - 1, z=zplacement-3 + slab), type=STONE_SLAB, orientation=NORTH)) # has a tail now
        next_gen_switch.append(Block(position=Point(x=position_information["startx"] - 5, y=position_information["starty"] - 1, z=zplacement-4 + slab), type=STONE_SLAB, orientation=NORTH))
        next_gen_switch.append(Block(position=Point(x=position_information["startx"] - 6, y=position_information["starty"] - 1, z=zplacement-4 + slab), type=EMERALD_BLOCK, orientation=NORTH))
        next_gen_switch.append(Block(position=Point(x=position_information["startx"] - 5 + slab, y=position_information["starty"] - 1, z=zplacement- 1), type=EMERALD_BLOCK, orientation=NORTH)) # makes the tail less noticeable

    
    next_gen_switch.append(Block(position=Point(x=position_information["startx"] - 6, y=position_information["starty"] - 1, z=zplacement-5), type=LEVER, orientation=UP))
    next_gen_switch.append(Block(position=Point(x=position_information["startx"] - 6, y=position_information["starty"] - 4, z=zplacement-3), type=COBBLESTONE, orientation=NORTH))
    next_gen_switch.append(Block(position=Point(x=position_information["startx"] - 6, y=position_information["starty"] - 3, z=zplacement-4), type=COBBLESTONE, orientation=NORTH))
    next_gen_switch.append(Block(position=Point(x=position_information["startx"] - 4, y=position_information["starty"] - 4, z=zplacement-3), type=REDSTONE_WIRE, orientation=NORTH))
    next_gen_switch.append(Block(position=Point(x=position_information["startx"] - 5, y=position_information["starty"] - 4, z=zplacement-3), type=REDSTONE_WIRE, orientation=NORTH))
    next_gen_switch.append(Block(position=Point(x=position_information["startx"] - 6, y=position_information["starty"] - 3, z=zplacement-3), type=REDSTONE_WIRE, orientation=NORTH))
    next_gen_switch.append(Block(position=Point(x=position_information["startx"] - 6, y=position_information["starty"] - 2, z=zplacement-4), type=REDSTONE_WIRE, orientation=NORTH))

    # spawn in the switches
    client.spawnBlocks(Blocks(blocks=next_gen_switch))

    return done_block_position

def next_gen_button(pop_size,position_information, client):
    """
    Spawns in a button and a piston at each of the switches
    that is used to more easily indicate if the player wants to move 
    on to the next generation and returns the point right below the piston
    which is useful in knowing if the button was pressed or not

    Parameters:
    pop_size (int): Number of buttons and pistons that will be generated
    startx (int): Integer that indicates the start of the range in x direction
    startz (int): Integer that indicates the start of the range in z direction
    xrange (int): Range of the x coordinate values
    client (MinecraftServiceStub) TODO

    Returns:
    [(int,int,int)]: List of all the positions right under the pistons
    """
    next_gen_button = []

    # stores the positions underneath the piston which indicate
    # if the player wants to see the next generation of structures
    next_block_positions = []

    # z coordinate needs to back away from the shapes if they generate water or lava
    zplacement = position_information["startz"] - 10

    # clear out the hole for the next gen button
    for n in range(pop_size):
        client.fillCube(FillCubeRequest(  
                cube=Cube(
                    min=Point(x=position_information["startx"] + n*(position_information["xrange"]+1) + int(position_information["xrange"]/2) + 1, y=position_information["starty"] - 3, z=zplacement-5), 
                    max=Point(x=position_information["startx"] + n*(position_information["xrange"]+1) + int(position_information["xrange"]/2) + 1, y=position_information["starty"] - 2, z=zplacement-5)  
                ),
                type=AIR
            ))
    
    # add in the piston amd button
    for p in range(pop_size):
        # stores the position underneath one piston as it loops through
        next_block_position = (position_information["startx"] + p*(position_information["xrange"]+1) + int(position_information["xrange"]/2) + 1,position_information["starty"] - 3,zplacement-5)
        next_gen_button.append(Block(position=Point(x=next_block_position[0], y=next_block_position[1]+1, z=next_block_position[2]), type=PISTON, orientation=DOWN))
        next_block_positions.append(next_block_position)
        next_gen_button.append(Block(position=Point(x=position_information["startx"] + p*(position_information["xrange"]+1) + int(position_information["xrange"]/2) + 1, y=position_information["starty"] - 1, z=zplacement-5), type=WOODEN_BUTTON, orientation=NORTH))
    
    # spawn in all the switches
    client.spawnBlocks(Blocks(blocks=next_gen_button))

    return next_block_positions

def read_current_block_options(client,placements,position_information):
    """
    Used when users can change the blocks in evolved shapes from within the game.
    Checks the blocks on display in front of each evolved shape and collects them in a list,
    where each such list is combined into a list of lists that is returned. The returned
    list will indicate all block types currently specified (on display) for each shape.

    Parameters:
    client ():

    """
    blocks_for_shape = []
    for corner in placements:
        # Change these coordinates to be an appropriate offset based on start x/y/z and x/y/z range
        blocks = client.readCube(Cube(
                    min=Point(x=corner[0], y=position_information["starty"]-1, z=position_information["startz"]-9),
                    max=Point(x=corner[0]+position_information["xrange"]-2, y=position_information["starty"]-1, z=position_information["startz"]-9)
                 ))
        
        block_list = []
        index = 0
        while index < len(blocks.blocks):
            block_list.append(blocks.blocks[index].type)
            index += 2 # Skip over spaces between blocks 
        blocks_for_shape.append(block_list)
    return blocks_for_shape
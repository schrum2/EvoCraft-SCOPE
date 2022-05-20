"""
Functions that alter any types of minecraft structures will be
kept in this module.
"""

# for Minecraft
#import grpc
import minecraft_pb2_grpc
from minecraft_pb2 import *

def place_fences(client, startx, starty, startz, xrange, yrange, zrange, pop_size):
        """
        Places a fenced in area around each of the shapes from the population
        that will be rendered in Minecraft. The size of the fenced in areas
        is based off of instance variables, as is the location.

        Parameters:
        client   (MinecraftServiceStub): TODO: put appropriate description here
        startx   (int): Starting x coordinate value
        starty   (int): Starting y coordinate value
        startz   (int): Starting z coordinate value
        xrange   (int): Range for x coordinate values
        yrange   (int): Range for y coordinate values
        zrange   (int): Range for z coordinate values
        pop_size (int): Fenced in areas to generate in a row
        """

        # clear out previous fences
        client.fillCube(FillCubeRequest(  
                cube=Cube(
                    min=Point(x=startx-1, y=starty-1, z=startz-1),
                    max=Point(x=startx-1 + pop_size*(xrange+1)+1, y=starty-1, z=zrange+2)
                ),
                type=AIR
            ))

        fence = []
        # Make the first row because this is a fence post problem
        # 0 5 0 to 0 5 11
        for first in range(zrange+2):
            fence.append(Block(position=Point(x=startx-1, y=starty-1,z=startz-1 + first), type=DARK_OAK_FENCE, orientation=NORTH))

        # Make nested for loops that will make the fence going in the 
        # top and bottom and other column that divides each structure
        for m in range(pop_size): # still don't know how to get it to repeat itself
            for i in range(xrange+2): 
                # do the fence in front of player going in the x direction (when facing south)
                fence.append(Block(position=Point(x=startx-1 + m*(xrange + 1) + i, y=starty-1,z=startz-1), type=DARK_OAK_FENCE, orientation=NORTH))
            for j in range(xrange+2):
                # do the fence in back of the structure going in the x direction (when facing south)
                fence.append(Block(position=Point(x=startx-1 + m*(xrange + 1) + j, y=starty-1,z=startz+zrange), type=DARK_OAK_FENCE, orientation=NORTH))
            for k in range(zrange+2):
                # do the one that divides the structures z changes
                # there is problem with where the divisions are being placed. Each division isn't the same size
                fence.append(Block(position=Point(x=startx-1 + (m+1)*(xrange + 1), y=starty-1,z=startz-1 + k), type=DARK_OAK_FENCE, orientation=NORTH)) 

        client.spawnBlocks(Blocks(blocks=fence))

def clear_area(client, startx, starty, startz, xrange,yrange, zrange, pop_size):
        """
        This function clears a large area by creating one
        large cube and filling it with air blocks.

        Parameters:
        client (MinecraftServiceStub): TODO: put appropriate description here
        startx (int): Starting value for x coordinate.
        starty (int): Starting value for y coordinate.
        startz (int): Starting value for z coordinate.
        xrange (int): Range for x coordinate values.
        yrange   (int): Range for y coordinate values.
        zrange (int): Range for z coordinate values.
        pop_size (int): The size of the population.
        """
        # clear out a big area rather than individual cubes
        client.fillCube(FillCubeRequest(  
                cube=Cube(
                    min=Point(x=startx-7, y=starty-1, z=startz-7),
                    max=Point(x=startx-1 + pop_size*(xrange+1)+7, y=starty+11, z=zrange+7)
                ),
                type=AIR
            ))


def place_number(client,x,y,z,num):
    """
        Places a glowstone-generated number above a generated shape depending on what digit it is
        in the range of 0-9. 

        Parameters:
        client (MinecraftServiceStub): TODO
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

def place_blocks_in_block_list(block_list,client, startx, starty, startz, xrange, yrange, zrange, pop_size):
    i =0
    blocks_in_list =[]
    print(xrange)
    blocks_in_list.append(Block(position=Point(x=startx+11*xrange+8, y=starty-1,z=startz-9), type=block_list[0], orientation=NORTH))
    blocks_in_list.append(Block(position=Point(x=startx+11*xrange+6, y=starty-1,z=startz-9), type=block_list[1], orientation=NORTH))
    blocks_in_list.append(Block(position=Point(x=startx+11*xrange+4, y=starty-1,z=startz-9), type=block_list[2], orientation=NORTH))
    blocks_in_list.append(Block(position=Point(x=startx+11*xrange+2, y=starty-1,z=startz-9), type=block_list[3], orientation=NORTH))
    blocks_in_list.append(Block(position=Point(x=startx+11*xrange, y=starty-1,z=startz-9), type=block_list[4], orientation=NORTH))

    client.spawnBlocks(Blocks(blocks=blocks_in_list))
    
def player_selection_switches(pop_size, client, startx, startz, xrange):
    """
    Spawns the switches the a player can use to select their preferred
    structures along with the switch that is used to indicate that they are
    done selected. Then it returns the position of all the points
    right below the redstone lamps for both the selection switches and
    the next generation switch

    Parameters:
    pop_size (int): Number of selection switches being selected

    Returns:
    [(int,int,int)]:The position of the space below the redstone lamp for the
                    list of positions right under each of the redstone lamps for
                    the selection switches
    """
    switch = []
    lamps = []

    # z coordinate needs to back away from the shapes if they generate water or lava
    zplacement = startz - 10

    #add the lamp in first when there is still ground underneath it to avoid the spawning of the grass blocks
    for p in range(pop_size):
        lamps.append(Block(position=Point(x=startx + p*(xrange+1) + int(xrange/2) - 1, y=4, z=zplacement-4), type=REDSTONE_LAMP, orientation=UP))
        lamps.append(Block(position=Point(x=startx + p*(xrange+1) + int(xrange/2), y=4, z=zplacement-4), type=AIR, orientation=UP))
        lamps.append(Block(position=Point(x=startx + p*(xrange+1) + int(xrange/2) - 1, y=4, z=zplacement-5), type=AIR, orientation=UP))
    client.spawnBlocks(Blocks(blocks=lamps))

    # clear out the section for the redstone part of the swtich
    for n in range(pop_size):
        client.fillCube(FillCubeRequest(  
                cube=Cube(
                        min=Point(x=startx + n*(xrange+1) + int(xrange/2) - 3, y=1, z=zplacement-4), # subject to change
                        max=Point(x=startx + n*(xrange+1) + int(xrange/2) - 1, y=3, z=zplacement-2)  # subject to change (y = 4 is ground level)
                ),
                type=AIR
            ))
        
        
    # Now spawn in everything for the selection switches

    # list that stores the position of the redstone block 
    # that is moved when the player flicks the switch
    on_block_positions = []

    # add in the piston, redstone block, redstone lamp, lever, cobblestone blocks, and redstone dust to switch
    for p in range(pop_size):
        switch.append(Block(position=Point(x=startx + p*(xrange+1) + int(xrange/2) - 1, y=0, z=zplacement-4), type=STICKY_PISTON, orientation=UP))
        switch.append(Block(position=Point(x=startx + p*(xrange+1) + int(xrange/2) - 1, y=1, z=zplacement-4), type=SLIME, orientation=NORTH))

        # this is the position of each redstone block when the lever is switched on
        on_block_position = (startx + p*(xrange+1) + int(xrange/2) - 1, 3, zplacement-4)
        switch.append(Block(position=Point(x=on_block_position[0], y=on_block_position[1] - 1, z=on_block_position[2]), type=REDSTONE_BLOCK, orientation=NORTH))
        # stores the positions from above
        on_block_positions.append(on_block_position)

        # slabs to put around the mechanism
        for slab in range(0,3):
            switch.append(Block(position=Point(x=startx + p*(xrange+1) + int(xrange/2) + 1, y=4, z=zplacement-4 + slab), type=STONEBRICK, orientation=NORTH))
            switch.append(Block(position=Point(x=startx + p*(xrange+1) + int(xrange/2), y=4, z=zplacement-4 + slab), type=STONE_SLAB, orientation=NORTH))
            switch.append(Block(position=Point(x=startx + p*(xrange+1) + int(xrange/2) - 1, y=4, z=zplacement-3 + slab), type=STONE_SLAB, orientation=NORTH)) # has a tail now
            switch.append(Block(position=Point(x=startx + p*(xrange+1) + int(xrange/2) - 2, y=4, z=zplacement-4 + slab), type=STONE_SLAB, orientation=NORTH))
            switch.append(Block(position=Point(x=startx + p*(xrange+1) + int(xrange/2) - 3, y=4, z=zplacement-4 + slab), type=STONEBRICK, orientation=NORTH))
            switch.append(Block(position=Point(x=startx + p*(xrange+1) + int(xrange/2) - 2 + slab, y=4, z=zplacement- 1), type=STONEBRICK, orientation=NORTH)) # makes tail less noticeable

        # add in the rest of the blocks needed 
        switch.append(Block(position=Point(x=startx + p*(xrange+1) + int(xrange/2) - 3, y=4, z=zplacement-5), type=LEVER, orientation=UP))
        switch.append(Block(position=Point(x=startx + p*(xrange+1) + int(xrange/2) - 3, y=1, z=zplacement-3), type=COBBLESTONE, orientation=NORTH))
        switch.append(Block(position=Point(x=startx + p*(xrange+1) + int(xrange/2) - 3, y=2, z=zplacement-4), type=COBBLESTONE, orientation=NORTH))
        switch.append(Block(position=Point(x=startx + p*(xrange+1) + int(xrange/2) - 1, y=1, z=zplacement-3), type=REDSTONE_WIRE, orientation=NORTH))
        switch.append(Block(position=Point(x=startx + p*(xrange+1) + int(xrange/2) - 2, y=1, z=zplacement-3), type=REDSTONE_WIRE, orientation=NORTH))
        switch.append(Block(position=Point(x=startx + p*(xrange+1) + int(xrange/2) - 3, y=2, z=zplacement-3), type=REDSTONE_WIRE, orientation=NORTH))
        switch.append(Block(position=Point(x=startx + p*(xrange+1) + int(xrange/2) - 3, y=3, z=zplacement-4), type=REDSTONE_WIRE, orientation=NORTH))
   
    # spawn in all the switches
    client.spawnBlocks(Blocks(blocks=switch))

    return on_block_positions

def player_next_gen_switch(startx, startz, client):
    """
    Adds in all the blocks necessary to make a next generation
    button that the player can use to indicate when they want to
    move on to see the next generation of structures and returns the 
    position under the redstone lamp that indicates whether the player
    is done or not.

    Returns:
    (int, int, int): Position of the space underneath the redstone lamp that
            is used to indicate if the player is ready to see the next generation
            of structures 
    """

    next_gen_switch = []
    lamp = []
    
    # z coordinate needs to back away from the shapes if they generate water or lava
    zplacement = startz - 10

    # add the lamp in first when there is still ground underneath it to avoid the spawning of the grass blocks
    lamp.append(Block(position=Point(x=startx - 4, y=4, z=zplacement-4), type=REDSTONE_LAMP, orientation=DOWN))
    lamp.append(Block(position=Point(x=startx - 3, y=4, z=zplacement-4), type=AIR, orientation=UP))
    lamp.append(Block(position=Point(x=startx - 4, y=4, z=zplacement-5), type=AIR, orientation=UP))
    client.spawnBlocks(Blocks(blocks=lamp))

    # clear out the section for the next gen switch
    client.fillCube(FillCubeRequest(  
            cube=Cube(
                min=Point(x=startx - 6, y=1, z=zplacement-4), 
                max=Point(x=startx - 4, y=3, z=zplacement-2)  
            ),
            type=AIR
        ))
        
    # add in all the components for the next gen switch to switch
    next_gen_switch.append(Block(position=Point(x=startx - 4, y=0, z=zplacement-4), type=STICKY_PISTON, orientation=UP))
    next_gen_switch.append(Block(position=Point(x=startx - 4, y=1, z=zplacement-4), type=SLIME, orientation=UP))
    done_block_position = (startx - 4, 3, zplacement-4)
    next_gen_switch.append(Block(position=Point(x=done_block_position[0], y=done_block_position[1] - 1, z=done_block_position[2]), type=REDSTONE_BLOCK, orientation=NORTH))

    for slab in range(0,3):
        next_gen_switch.append(Block(position=Point(x=startx - 2, y=4, z=zplacement-4 + slab), type=EMERALD_BLOCK, orientation=NORTH))
        next_gen_switch.append(Block(position=Point(x=startx - 3, y=4, z=zplacement-4 + slab), type=STONE_SLAB, orientation=NORTH))
        next_gen_switch.append(Block(position=Point(x=startx - 4, y=4, z=zplacement-3 + slab), type=STONE_SLAB, orientation=NORTH)) # has a tail now
        next_gen_switch.append(Block(position=Point(x=startx - 5, y=4, z=zplacement-4 + slab), type=STONE_SLAB, orientation=NORTH))
        next_gen_switch.append(Block(position=Point(x=startx - 6, y=4, z=zplacement-4 + slab), type=EMERALD_BLOCK, orientation=NORTH))
        next_gen_switch.append(Block(position=Point(x=startx - 5 + slab, y=4, z=zplacement- 1), type=EMERALD_BLOCK, orientation=NORTH)) # makes the tail less noticeable

    
    next_gen_switch.append(Block(position=Point(x=startx - 6, y=4, z=zplacement-5), type=LEVER, orientation=UP))
    next_gen_switch.append(Block(position=Point(x=startx - 6, y=1, z=zplacement-3), type=COBBLESTONE, orientation=NORTH))
    next_gen_switch.append(Block(position=Point(x=startx - 6, y=2, z=zplacement-4), type=COBBLESTONE, orientation=NORTH))
    next_gen_switch.append(Block(position=Point(x=startx - 4, y=1, z=zplacement-3), type=REDSTONE_WIRE, orientation=NORTH))
    next_gen_switch.append(Block(position=Point(x=startx - 5, y=1, z=zplacement-3), type=REDSTONE_WIRE, orientation=NORTH))
    next_gen_switch.append(Block(position=Point(x=startx - 6, y=2, z=zplacement-3), type=REDSTONE_WIRE, orientation=NORTH))
    next_gen_switch.append(Block(position=Point(x=startx - 6, y=3, z=zplacement-4), type=REDSTONE_WIRE, orientation=NORTH))

    # spawn in the switches
    client.spawnBlocks(Blocks(blocks=next_gen_switch))

    return done_block_position

def next_gen_button(pop_size,startx, startz, xrange, client):

    next_gen_button = []

    # stores the positions underneath the piston which indicate
    # if the player wants to see the next generation of structures
    next_block_positions = []

    # z coordinate needs to back away from the shapes if they generate water or lava
    zplacement = startz - 10

    # clear out the hole for the next gen button
    for n in range(pop_size):
        client.fillCube(FillCubeRequest(  
                cube=Cube(
                    min=Point(x=startx + n*(xrange+1) + int(xrange/2) + 1, y=2, z=zplacement-5), 
                    max=Point(x=startx + n*(xrange+1) + int(xrange/2) + 1, y=3, z=zplacement-5)  
                ),
                type=AIR
            ))
    
    # add in the piston amd button
    for p in range(pop_size):
        # stores the position underneath one piston as it loops through
        next_block_position = (startx + p*(xrange+1) + int(xrange/2) + 1,2,zplacement-5)
        next_gen_button.append(Block(position=Point(x=next_block_position[0], y=next_block_position[1]+1, z=next_block_position[2]), type=PISTON, orientation=DOWN))
        next_block_positions.append(next_block_position)
        next_gen_button.append(Block(position=Point(x=startx + p*(xrange+1) + int(xrange/2) + 1, y=4, z=zplacement-5), type=WOODEN_BUTTON, orientation=NORTH))
    
    # spawn in all the switches
    client.spawnBlocks(Blocks(blocks=next_gen_button))

    return next_block_positions
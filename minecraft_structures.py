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

def place_blocks_in_block_list(block_list,client, startx, starty, startz,genome_id):
    blocks_in_list =[]
    rows, cols = (10, 5)
    block_types = [[0]*cols]*rows
    # for i  in range(pop_size):
    x=8
    z=-9
    index=0

    
    while(index<len(block_list)):
        generated_block=(Block(position=Point(x=startx+11*genome_id+x, y=starty-1,z=startz+z), type=block_list[index], orientation=NORTH))
        blocks_in_list.append(generated_block)
        blocks_in_list.append(Block(position=Point(x=startx+11*genome_id+x, y=starty-2,z=startz+z), type=EMERALD_BLOCK, orientation=NORTH))
        if(generated_block.type==LAVA or generated_block.type==WATER):
            blocks_in_list.append(Block(position=Point(x=startx+11*genome_id+x-1, y=starty-1,z=startz+z), type=STONE_BRICK_STAIRS, orientation=EAST))
            blocks_in_list.append(Block(position=Point(x=startx+11*genome_id+x+1, y=starty-1,z=startz+z), type=STONE_BRICK_STAIRS, orientation=WEST))
            blocks_in_list.append(Block(position=Point(x=startx+11*genome_id+x, y=starty-1,z=startz+z+1), type=STONE_BRICK_STAIRS, orientation=NORTH))
            blocks_in_list.append(Block(position=Point(x=startx+11*genome_id+x, y=starty-1,z=startz+z-1), type=STONE_BRICK_STAIRS, orientation=SOUTH))
        x=x-2
        if(x<0):
            z=z+2
        index=index+1

    block_types[genome_id]=blocks_in_list
    client.spawnBlocks(Blocks(blocks=blocks_in_list))
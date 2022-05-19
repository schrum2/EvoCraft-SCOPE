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
        TODO Make sure to explain why using 11 and 7

        Parameters:
        client (TODO): TODO
        startx (int): TODO
        starty (int): TODO
        startz (int): TODO
        xrange (int): TODO
        yrange   (int): Range for y coordinate values
        zrange (int): TODO
        pop_size (int): TODO
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

def player_selection_switches(pop_size):
        """
        Spawns the switches the a player can use to select their preferred
        structures along with the switch that is used to indicate that they are
        done selected. Then it returns the position of all the points
        right below the redstone lamps for both the selection switches and
        the next generation switch

        Parameters:
        pop_size (int): Number of selection switches being selected

        Returns:
        ((int,int,int),[(int,int,int)]): The position of the space below the redstone lamp for the 
                next generation switch and the list of positions right under each of the redstone lamps for
                the selection switches
        """
        switch = []
        # z coordinate needs to back away from the shapes if they generate water or lava
        zplacement = self.startz - 10

        # clear out the section for the redstone part of the swtich
        for n in range(pop_size):
            self.client.fillCube(FillCubeRequest(  
                    cube=Cube(
                            min=Point(x=self.startx + n*(self.xrange+1) + int(self.xrange/2) - 1, y=1, z=zplacement-4), # subject to change
                            max=Point(x=self.startx + n*(self.xrange+1) + int(self.xrange/2) + 1, y=3, z=zplacement-2)  # subject to change (y = 4 is ground level)
                    ),
                    type=AIR
                ))
        
        # Spawn in the button and return the tuple relating to the position of 
        # under the redstone lamp that indicates if the user wants to see the next
        # generation or not
        done = player_next_gen_switch()
        switch.append(done)
        
        # Now spawn in everything for the selection switches

        # list that stores the position of the redstone block 
        # that is moved when the player flicks the switch
        on_block_positions = []

        # add in the piston, redstone block, redstone lamp, lever, cobblestone blocks, and redstone dust to switch
        for p in range(pop_size):
            switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2) + 1, y=0, z=zplacement-4), type=STICKY_PISTON, orientation=UP))
            switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2) + 1, y=1, z=zplacement-4), type=SLIME, orientation=NORTH))

            # this is the position of each redstone block when the lever is switched on
            on_block_position = (self.startx + p*(self.xrange+1) + int(self.xrange/2) + 1, 3, zplacement-4)
            switch.append(Block(position=Point(x=on_block_position[0], y=on_block_position[1] - 1, z=on_block_position[2]), type=REDSTONE_BLOCK, orientation=NORTH))
            # stores the positions from above
            on_block_positions.append(on_block_position)

            # slabs to put around the mechanism
            for slab in range(0,3):
                switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2) + 3, y=4, z=zplacement-4 + slab), type=STONEBRICK, orientation=NORTH))
                switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2) + 2, y=4, z=zplacement-4 + slab), type=STONE_SLAB, orientation=NORTH))
                switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2) + 1, y=4, z=zplacement-4 + slab), type=STONE_SLAB, orientation=NORTH))
                switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2), y=4, z=zplacement-4 + slab), type=STONE_SLAB, orientation=NORTH))
                switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2) - 1, y=4, z=zplacement-4 + slab), type=STONEBRICK, orientation=NORTH))

            # add in the rest of the blocks needed
            switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2) + 1, y=4, z=zplacement-4), type=REDSTONE_LAMP, orientation=NORTH)) # this adds two dirt blocks which don't belong
            switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2) - 1, y=4, z=zplacement-5), type=LEVER, orientation=UP))
            switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2) - 1, y=1, z=zplacement-3), type=COBBLESTONE, orientation=NORTH))
            switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2) - 1, y=2, z=zplacement-4), type=COBBLESTONE, orientation=NORTH))
            switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2) + 1, y=1, z=zplacement-3), type=REDSTONE_WIRE, orientation=NORTH))
            switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2), y=1, z=zplacement-3), type=REDSTONE_WIRE, orientation=NORTH))
            switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2) - 1, y=2, z=zplacement-3), type=REDSTONE_WIRE, orientation=NORTH))
            switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2) - 1, y=3, z=zplacement-4), type=REDSTONE_WIRE, orientation=NORTH))
   
        # spawn in all the switches
        self.client.spawnBlocks(Blocks(blocks=switch))

        return (done, on_block_positions)

def player_next_gen_switch()
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

    # clear out the section for the next gen switch
        self.client.fillCube(FillCubeRequest(  
                    cube=Cube(
                            min=Point(x=self.startx - 6, y=1, z=zplacement-4), 
                            max=Point(x=self.startx - 4, y=3, z=zplacement-2)  
                    ),
                    type=AIR
                ))
        
        # add in all the components for the next gen switch to switch
        next_gen_switch.append(Block(position=Point(x=self.startx - 4, y=0, z=zplacement-4), type=STICKY_PISTON, orientation=UP))
        next_gen_switch.append(Block(position=Point(x=self.startx - 4, y=1, z=zplacement-4), type=SLIME, orientation=UP))
        done_block_position = (self.startx - 4, 3, zplacement-4)
        next_gen_switch.append(Block(position=Point(x=done_block_position[0], y=done_block_position[1] - 1, z=done_block_position[2]), type=REDSTONE_BLOCK, orientation=NORTH))

        for slab in range(0,3):
            next_gen_switch.append(Block(position=Point(x=self.startx - 2, y=4, z=zplacement-4 + slab), type=EMERALD_BLOCK, orientation=NORTH))
            next_gen_switch.append(Block(position=Point(x=self.startx - 3, y=4, z=zplacement-4 + slab), type=STONE_SLAB, orientation=NORTH))
            next_gen_switch.append(Block(position=Point(x=self.startx - 4, y=4, z=zplacement-4 + slab), type=STONE_SLAB, orientation=NORTH))
            next_gen_switch.append(Block(position=Point(x=self.startx - 5, y=4, z=zplacement-4 + slab), type=STONE_SLAB, orientation=NORTH))
            next_gen_switch.append(Block(position=Point(x=self.startx - 6, y=4, z=zplacement-4 + slab), type=EMERALD_BLOCK, orientation=NORTH))

        next_gen_switch.append(Block(position=Point(x=self.startx - 4, y=4, z=zplacement-4), type=REDSTONE_LAMP, orientation=NORTH)) 
        next_gen_switch.append(Block(position=Point(x=self.startx - 6, y=4, z=zplacement-5), type=LEVER, orientation=UP))
        next_gen_switch.append(Block(position=Point(x=self.startx - 6, y=1, z=zplacement-3), type=COBBLESTONE, orientation=NORTH))
        next_gen_switch.append(Block(position=Point(x=self.startx - 6, y=2, z=zplacement-4), type=COBBLESTONE, orientation=NORTH))
        next_gen_switch.append(Block(position=Point(x=self.startx - 4, y=1, z=zplacement-3), type=REDSTONE_WIRE, orientation=NORTH))
        next_gen_switch.append(Block(position=Point(x=self.startx - 5, y=1, z=zplacement-3), type=REDSTONE_WIRE, orientation=NORTH))
        next_gen_switch.append(Block(position=Point(x=self.startx - 6, y=2, z=zplacement-3), type=REDSTONE_WIRE, orientation=NORTH))
        next_gen_switch.append(Block(position=Point(x=self.startx - 6, y=3, z=zplacement-4), type=REDSTONE_WIRE, orientation=NORTH))

        return done_block_position
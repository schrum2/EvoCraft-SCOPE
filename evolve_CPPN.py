"""
Code originally taken from the offline simplified version of Picbreeder
that comes with NEAT-Python. Just wanted a starting point for evolving CPPNs.
Modifying the code to apply to Minecraft.
"""
# Are these still needed?
import math
import os
import pickle

# For CPPNs and NEAT
import neat
import custom_genomes as cg

# for Minecraft
import grpc
import minecraft_pb2_grpc
from minecraft_pb2 import *

USE_ELITISM = False
IN_GAME_CONTROL = False
PRESENCE_THRESHOLD = 0.5
POPULATION_SIZE = 10

class InteractiveStagnation(object):
    """
    This class is used as a drop-in replacement for the default species stagnation scheme.

    A species is only marked as stagnant if the user has not selected one of its output images
    within the last `max_stagnation` generations.
    """

    def __init__(self, config, reporters):
        self.max_stagnation = int(config.get('max_stagnation'))
        self.reporters = reporters

    @classmethod
    def parse_config(cls, param_dict):
        config = {'max_stagnation': 15}
        config.update(param_dict)

        return config

    @classmethod
    def write_config(cls, f, config):
        f.write('max_stagnation       = {}\n'.format(config['max_stagnation']))

    def update(self, species_set, generation):
        result = []
        for s in species_set.species.values():
            # If any member of the species is selected (i.e., has a fitness above zero),
            # mark the species as improved.
            for m in s.members.values():
                if m.fitness > 0:
                    s.last_improved = generation
                    break

            stagnant_time = generation - s.last_improved
            is_stagnant = stagnant_time >= self.max_stagnation
            result.append((s.key, s, is_stagnant))

        return result

def place_number(client,x,y,z,num):
    
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

class MinecraftBreeder(object):
    def __init__(self, xrange, yrange, zrange, block_list):
        """
        :param xrange: range of x-coordinate values rendered
        :param zrange: range of y-coordinate values rendered
        :param xrange: range of z-coordinate values rendered
        """
        self.block_list = block_list

        self.startx = 0
        self.starty = 5
        self.startz = 0
        
        self.generation = 0
        self.xrange = xrange
        self.yrange = yrange
        self.zrange = zrange
        
        # Don't try any multithreading yet
        self.num_workers = 1

        # Connect to Minecraft server
        channel = grpc.insecure_channel('localhost:5001')
        self.client = minecraft_pb2_grpc.MinecraftServiceStub(channel)

        # Place numbers 0-9, use yrange + 2
        for i in range(10):
            place_number(self.client,self.startx+(i*(self.xrange+1))+int(self.xrange/2),self.starty+self.yrange+2,self.startz,i)

    def query_cppn_for_shape(self, genome, config, corner, xrange, yrange, zrange):
        """
        Query CPPN at all voxel coordinates to generate the list of
        blocks that will eventually be rendered in the Minecraft server.

        Parameters:
        genome (DefaultGenome): A CPPN or some class that extends CPPNs
        config (Config): NEAT configurations
        corner (int,int,int): three-tuple of initial x,y,z coordinates
        xrange (int): number of voxel blocks for each shape along x-dimension
        yrange (int): number of voxel blocks for each shape along y-dimension
        zrange (int): number of voxel blocks for each shape along z-dimension

        Returns:
        [Block]:List of Blocks to generate in Minecraft
        """
        net = neat.nn.FeedForwardNetwork.create(genome, config) # Create CPPN out of genome
        shape = []
        for xi in range(xrange):
            x = scale_and_center(xi,xrange)
            for yi in range(yrange):
                y = scale_and_center(yi,yrange)
                for zi in range(zrange):
                    z = scale_and_center(zi,zrange)
                    # math.sqrt(2) is the usual scaling for radial distances in CPPNs
                    output = net.activate([x, y, z, distance((x,y,z),(0,0,0)) * math.sqrt(2), 1.0])
                    
                    # First output determines whether there is a block at all.
                    # If there is a block, argmax determines the max value and places the specified block 
                    # from the list of possible blocks

                    #print(output)
                        
                    if output[0] < PRESENCE_THRESHOLD: 
                        block = Block(position=Point(x=corner[0]+xi, y=corner[1]+yi, z=corner[2]+zi), type=AIR, orientation=NORTH)
                    else:
                        output_val = argmax(output[1:])
                        block = Block(position=Point(x=corner[0]+xi, y=corner[1]+yi, z=corner[2]+zi), type=self.block_list[output_val], orientation=NORTH)
                        

                    shape.append(block)
        
        return shape

    def place_fences(self, pop_size):
        """
        Places a fenced in area around each of the shapes from the population
        that will be rendered in Minecraft. The size of the fenced in areas
        is based off of instance variables, as is the location.

        Parameters:
        pop_size (int): Fenced in areas to generate in a row
        """

        # clear out previous fences
        self.client.fillCube(FillCubeRequest(  
                cube=Cube(
                    min=Point(x=self.startx-1, y=self.starty-1, z=self.startz-1),
                    max=Point(x=self.startx-1 + pop_size*(self.xrange+1)+1, y=self.starty-1, z=self.zrange+2)
                ),
                type=AIR
            ))

        fence = []
        # Make the first row because this is a fence post problem
        # 0 5 0 to 0 5 11
        for first in range(self.zrange+2):
            fence.append(Block(position=Point(x=self.startx-1, y=self.starty-1,z=self.startz-1 + first), type=DARK_OAK_FENCE, orientation=NORTH))

        # Make nested for loops that will make the fence going in the 
        # top and bottom and other column that divides each structure
        for m in range(pop_size): # still don't know how to get it to repeat itself
            for i in range(self.xrange+2): 
                # do the fence in front of player going in the x direction (when facing south)
                fence.append(Block(position=Point(x=self.startx-1 + m*(self.xrange + 1) + i, y=self.starty-1,z=self.startz-1), type=DARK_OAK_FENCE, orientation=NORTH))
            for j in range(self.xrange+2):
                # do the fence in back of the structure going in the x direction (when facing south)
                fence.append(Block(position=Point(x=self.startx-1 + m*(self.xrange + 1) + j, y=self.starty-1,z=self.startz+self.zrange), type=DARK_OAK_FENCE, orientation=NORTH))
            for k in range(self.zrange+2):
                # do the one that divides the structures z changes
                # there is problem with where the divisions are being placed. Each division isn't the same size
                fence.append(Block(position=Point(x=self.startx-1 + (m+1)*(self.xrange + 1), y=self.starty-1,z=self.startz-1 + k), type=DARK_OAK_FENCE, orientation=NORTH)) 

        self.client.spawnBlocks(Blocks(blocks=fence))

    def clear_area(self,pop_size):
        """
        This function clears a large area by using the population
        size to create a large cube that will encompass more than enough area.
        The value 11 is used because it is the value that will clear everything
        in terms of the y direction. Any larger value will clear the number labels.
        The value 7 is used for the x and z direction because the most something will
        spread is 7 blocks in either the x or z direction.

        Parameters:
        pop_size (int): Number of shapes being generated
        """
        # clear out a big area rather than individual cubes
        self.client.fillCube(FillCubeRequest(  
                cube=Cube(
                    min=Point(x=self.startx-7, y=self.starty-1, z=self.startz-7),
                    max=Point(x=self.startx-1 + pop_size*(self.xrange+1)+7, y=self.starty+11, z=self.zrange+7)
                ),
                type=AIR
            ))

    def player_selection_switches(self, pop_size):
        switch = []
        # z coordinate needs to back away from the shapes if they generate water or lava
        zplacement = self.startz - 10

        #clear out the section for the redstone part of the swtich
        for n in range(pop_size):
            self.client.fillCube(FillCubeRequest(  
                    cube=Cube(
                            min=Point(x=self.startx + n*(self.xrange+1) + int(self.xrange/2) - 1, y=1, z=zplacement-4), # subject to change
                            max=Point(x=self.startx + n*(self.xrange+1) + int(self.xrange/2) + 1, y=3, z=zplacement-2)  # subject to change (y = 4 is ground level)
                    ),
                    type=AIR
                ))

        # spawn in everything for the redstone mechanism

        # list that stores the position of the redstone block 
        # that is moved when the player flicks the switch
        on_block_positions = []

        # spawn in the piston, redstone block, redstone lamp, lever, cobblestone blocks, and redstone dust
        for p in range(pop_size):
            switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2) + 1, y=0, z=zplacement-4), type=STICKY_PISTON, orientation=UP))
            switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2) + 1, y=1, z=zplacement-4), type=SLIME, orientation=NORTH))

            # this is the position of each redstone block when the lever is switched on
            on_block_position = (self.startx + p*(self.xrange+1) + int(self.xrange/2) + 1, 3, zplacement-4)
            switch.append(Block(position=Point(x=on_block_position[0], y=on_block_position[1] - 1, z=on_block_position[2]), type=REDSTONE_BLOCK, orientation=NORTH))
            # stores the position from above
            on_block_positions.append(on_block_position)

            switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2) + 1, y=4, z=zplacement-4), type=REDSTONE_LAMP, orientation=NORTH))
            switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2) - 1, y=4, z=zplacement-5), type=LEVER, orientation=UP))
            switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2) - 1, y=1, z=zplacement-3), type=COBBLESTONE, orientation=NORTH))
            switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2) - 1, y=2, z=zplacement-4), type=COBBLESTONE, orientation=NORTH))
            switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2) + 1, y=1, z=zplacement-3), type=REDSTONE_WIRE, orientation=NORTH))
            switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2), y=1, z=zplacement-3), type=REDSTONE_WIRE, orientation=NORTH))
            switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2) - 1, y=2, z=zplacement-3), type=REDSTONE_WIRE, orientation=NORTH))
            switch.append(Block(position=Point(x=self.startx + p*(self.xrange+1) + int(self.xrange/2) - 1, y=3, z=zplacement-4), type=REDSTONE_WIRE, orientation=NORTH))
            
        
        self.client.spawnBlocks(Blocks(blocks=switch))

        return on_block_positions

    def eval_fitness(self, genomes, config):
        """
            This function is expected by the NEAT-Python framework.
            It takes a population of genomes and configuration information,
            and assigns fitness values to each of the genome objects in
            the population.
        """

        self.clear_area(config.pop_size)
        self.place_fences(config.pop_size)
        on_block_positions = self.player_selection_switches(config.pop_size)
        
        selected = []
        shapes = []
        
        # This loop could be parallelized
        for n, (genome_id, genome) in enumerate(genomes):
            # Initially, none are selected
            selected.append(False)
            # See how CPPN fills out the shape
            corner = (self.startx + n*(self.xrange+1), self.starty, self.startz)
            shapes.append(self.query_cppn_for_shape(genome, config, corner, self.xrange, self.yrange, self.zrange))

        # Render shapes in Minecraft world
        for i in range(len(shapes)):
            # fill the empty space with the evolved shape
            self.client.spawnBlocks(Blocks(blocks=shapes[i]))


        if IN_GAME_CONTROL:
            # TODO
              # if the player can switch the lever to pick a structure

            while True:
                # constantly reads the position right below the redstone lamp
                # to see if the player has switched on a lever
                first = on_block_positions[0]
                blocks = self.client.readCube(Cube(
                    min=Point(x=first[0], y=first[1], z=first[2]),
                    max=Point(x=first[0], y=first[1], z=first[2])
                ))

                print(blocks)

        else:
            # Controlled externally by keyboard

            # Creates a string that is the user's input, and the converts it to a list
            vals = input("Select the ones you like:")
            split_vals = vals.split(' ')
            selected_vals = list(map(int,split_vals))

        # Initialize to all False
        selected = [False for i in range(config.pop_size)]
        # Then set to True for the items that are selected
        for ind in selected_vals:
            selected[ind] = True
        
        print("Selected: {}".format(selected))

        for n, (genome_id, genome) in enumerate(genomes):
            if selected[n]:
                genome.fitness = 1.0
            else:
                genome.fitness = 0.0

        if USE_ELITISM:
            # To assure that all selected individuals survive, the elitism setting is changed
            elite_count = int(sum(map(lambda b : 1 if b else 0, selected)))
            print("{} elite survivors".format(elite_count))
            config.reproduction_config.elitism = elite_count

    # End of MinecraftBreeder

# Various functions

def argmax(l):
    """
    Finds the maximum value in a list of values
    :param l a list of numeric elements
    :return index of first maximal element
    """
    f = lambda i: l[i]
    return max(range(len(l)), key=f)

def distance(v, u):
    """
    Euclidean distance between two vectors of the same length.
    :param u a vectors
    :param v other vector
    :return distance between vectors
    """
    d = 0
    for i in range(len(u)):
        d += (u[i] - v[i])**2
    return math.sqrt(d)

def scale_and_center(index, top):
    """
    This scales the block index to the range [-1,1]
    
    :param index: index of block along a given dimension
    :param top: number of blocks along the given dimension
    """
    return -1.0 + 2.0 * index / (top - 1)

def run():
    # Contains all possible blocks that could be placed
    # block_list = [REDSTONE_BLOCK,QUARTZ_BLOCK,EMERALD_BLOCK,GOLD_BLOCK,DIAMOND_BLOCK,REDSTONE_LAMP]
    block_list = [REDSTONE_BLOCK,PISTON,WATER, LAVA]

    mc = MinecraftBreeder(10,10,10,block_list)

    # Determine path to configuration file.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'cppn_minecraft_config')

    # Note that we provide the custom stagnation class to the Config constructor.
    config = neat.Config(cg.CustomBlocksGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, InteractiveStagnation,
                         config_path)

    config.pop_size = POPULATION_SIZE
    # Changing the number of CPPN outputs after initialization. Could cause problems.
    config.genome_config.num_outputs = len(block_list)+1
    config.genome_config.output_keys = [i for i in range(config.genome_config.num_outputs)]

    pop = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    while 1:
        mc.generation = pop.generation + 1
        pop.run(mc.eval_fitness, 1)


if __name__ == '__main__':
    run()

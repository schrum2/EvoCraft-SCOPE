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

# for Minecraft
import grpc
import minecraft_pb2_grpc
from minecraft_pb2 import *

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


class MinecraftBreeder(object):
    def __init__(self, xrange, yrange, zrange):
        """
        :param xrange: range of x-coordinate values rendered
        :param zrange: range of y-coordinate values rendered
        :param xrange: range of z-coordinate values rendered
        """
        
        self.startx = 0
        self.starty = 0
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

    def query_cppn_for_shape(self, genome, config, corner, xrange, yrange, zrange):
        """
            Query CPPN at all voxel coordinates to generate the list of
            blocks that will eventually be rendered in the Minecraft server.
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
                    output = net.activate([x, y, z, distance((x,y,z),(0,0,0)) * math.sqrt(2)])
                    
                    # First output determines whether there is a block at all.
                    # The next two outputs favor one block or the other: redstone or quartz.
                    # Only if a block is present, then the max of the two available choices is used.
                    if output[0] < 0.5: 
                        block = Block(position=Point(x=corner[0]+xi, y=corner[1]+yi, z=corner[2]+zi), type=AIR, orientation=NORTH)
                    elif output[1] > output[2]:
                        block = Block(position=Point(x=corner[0]+xi, y=corner[1]+yi, z=corner[2]+zi), type=REDSTONE_BLOCK, orientation=NORTH)
                    else:
                        block = Block(position=Point(x=corner[0]+xi, y=corner[1]+yi, z=corner[2]+zi), type=QUARTZ_BLOCK, orientation=NORTH)
                        
                    shape.append(block)
        
        return shape

    def eval_fitness(self, genomes, config):
        """
            This function is expected by the NEAT-Python framework.
            It takes a population of genomes and configuration information,
            and assigns fitness values to each of the genome objects in
            the population.
        """
        selected = []
        placements = []
        shapes = []
        
        # This loop could be parallelized
        for n, (genome_id, genome) in enumerate(genomes):
            selected.append(False)
            # These are the 3D regions where each evolved shape will be placed
            corner = (self.startx + n*(self.xrange+1), self.starty, self.startz)
            placements.append( corner )
            # See how CPPN fills out the shape
            shapes.append(self.query_cppn_for_shape(genome, config, corner, self.xrange, self.yrange, self.zrange))

        # Render shapes in Minecraft world
        for i in range(len(placements)):
            space = placements[i]
            # Clear a space for the shape
            self.client.fillCube(FillCubeRequest(  
                cube=Cube(
                    min=Point(x=space[0], y=space[1], z=space[2]),
                    max=Point(x=space[0]+self.xrange, y=space[1]+self.yrange, z=space[2]+self.zrange)
                ),
                type=AIR
            ))
            # fill the empty space with the evolved shape
            self.client.spawnBlocks(Blocks(blocks=shapes[i]))

        # TODO: Figure out how to specify which items are or are not selected (ideally via in-game interaction)
        input() # For now, just pause the algorithm to get user input

        for n, (genome_id, genome) in enumerate(genomes):
            if selected[n]:
                genome.fitness = 1.0
            else:
                genome.fitness = 0.0

def distance(v, u):
    """
    Euclidean distance between two vectors of the same length.
    :param u: a vectors
    :param v: other vector
    """
    d = 0;
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
    mc = MinecraftBreeder(10,10,10)

    # Determine path to configuration file.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'cppn_minecraft_config')

    # Note that we provide the custom stagnation class to the Config constructor.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, InteractiveStagnation,
                         config_path)

    config.pop_size = 10
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

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

class MinecraftBreeder(object):
    def __init__(self, xrange, yrange, zrange):
        """
        :param xrange: range of x-coordinate values rendered
        :param zrange: range of y-coordinate values rendered
        :param xrange: range of z-coordinate values rendered
        """
        
        self.startx = 0
        self.starty = 0
        self.startx = 0
        
        self.generation = 0
        self.xrange = xrange
        self.yrange = yrange
        self.zrange = zrange
        
        # Don't try any multithreading yet
        self.num_workers = 1

    def query_cppn_for_shape(genome, config, xrange, yrange, zrange):
        """
            Query CPPN at all voxel coordinates to generate the list of
            blocks that will eventually be rendered in the Minecraft server.
        """
        net = neat.nn.FeedForwardNetwork.create(genome, config) # Create CPPN out of genome
        shape = []
        for xi in range(xrange):
            x = scale_and_center(xi,xrange)
            row = []
            for yi in range(yrange):
                y = scale_and_center(yi,yrange)
                for zi in range(zrange):
                    z = scale_and_center(zi,zrange)
                
                    output = net.activate([x, y, z, distance((x,y,z),(0,0,0))])
                    red = int(round((output[0] + 1.0) * 255 / 2.0))
                    green = int(round((output[1] + 1.0) * 255 / 2.0))
                    blue = int(round((output[2] + 1.0) * 255 / 2.0))
                    red = max(0, min(255, red))
                    green = max(0, min(255, green))
                    blue = max(0, min(255, blue))
                    row.append((red, green, blue))
                shape.append(row)
        
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
        for n, (genome_id, genome) in enumerate(genomes):
            selected.append(False)
            # These are the 3D regions where each evolved shape will be placed
            placements.append( (self.startx + n*self.xrange, self.starty, self.startz) )

        # TODO: Loop through and render all shapes in Minecraft server

        # TODO: Figure out how to specify which items are or are not selected (ideally via in-game interaction)

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

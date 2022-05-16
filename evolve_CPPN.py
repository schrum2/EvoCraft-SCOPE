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

    def make_image_from_data(self, image_data, width, height):
        # For mono and grayscale, we need a palette because the evaluation function
        # only returns a single integer instead of an (R, G, B) tuple.
        if self.scheme == 'color':
            image = pygame.Surface((width, height))
        else:
            image = pygame.Surface((width, height), depth=8)
            palette = tuple([(i, i, i) for i in range(256)])
            image.set_palette(palette)

        for r, row in enumerate(image_data):
            for c, color in enumerate(row):
                image.set_at((r, c), color)

        return image

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

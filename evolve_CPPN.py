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

    def make_thumbnails(self, genomes, config):
        img_func = eval_mono_image
        if self.scheme == 'gray':
            img_func = eval_gray_image
        elif self.scheme == 'color':
            img_func = eval_color_image

        with Pool(self.num_workers) as pool:
            jobs = []
            for genome_id, genome in genomes:
                jobs.append(pool.apply_async(img_func, (genome, config, self.thumb_width, self.thumb_height)))

            thumbnails = []
            for j in jobs:
                # TODO: This code currently generates the image data using the multiprocessing
                # pool, and then does the actual image construction here because pygame complained
                # about not being initialized if the pool workers tried to construct an image.
                # Presumably there is some way to fix this, but for now this seems fast enough
                # for the purposes of a demo.
                image_data = j.get()

                thumbnails.append(self.make_image_from_data(image_data, self.thumb_width, self.thumb_height))

        return thumbnails

    def make_high_resolution(self, genome, config):
        genome_id, genome = genome

        # Make sure the output directory exists.
        if not os.path.isdir('rendered'):
            os.mkdir('rendered')

        if self.scheme == 'gray':
            image_data = eval_gray_image(genome, config, self.full_width, self.full_height)
        elif self.scheme == 'color':
            image_data = eval_color_image(genome, config, self.full_width, self.full_height)
        else:
            image_data = eval_mono_image(genome, config, self.full_width, self.full_height)

        image = self.make_image_from_data(image_data, self.full_width, self.full_height)
        pygame.image.save(image, "rendered/rendered-{}-{}.png".format(os.getpid(), genome_id))

        with open("rendered/genome-{}-{}.bin".format(os.getpid(), genome_id), "wb") as f:
            pickle.dump(genome, f, 2)

    def eval_fitness(self, genomes, config):
        selected = []
        rects = []
        for n, (genome_id, genome) in enumerate(genomes):
            selected.append(False)
            row, col = divmod(n, self.num_cols)
            rects.append(pygame.Rect(4 + (self.thumb_width + 4) * col,
                                     4 + (self.thumb_height + 4) * row,
                                     self.thumb_width, self.thumb_height))

        pygame.init()
        screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Interactive NEAT-python generation {0}".format(self.generation))

        buttons = self.make_thumbnails(genomes, config)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_button = -1
                    for n, button in enumerate(buttons):
                        if rects[n].collidepoint(pygame.mouse.get_pos()):
                            clicked_button = n
                            break

                    if event.button == 1:
                        selected[clicked_button] = not selected[clicked_button]
                    else:
                        self.make_high_resolution(genomes[clicked_button], config)

            if running:
                screen.fill((128, 128, 192))
                for n, button in enumerate(buttons):
                    screen.blit(button, rects[n])
                    if selected[n]:
                        pygame.draw.rect(screen, (255, 0, 0), rects[n], 3)
                pygame.display.flip()

        for n, (genome_id, genome) in enumerate(genomes):
            if selected[n]:
                genome.fitness = 1.0
                pygame.image.save(buttons[n], "image-{}.{}.png".format(os.getpid(), genome_id))
                with open("genome-{}-{}.bin".format(os.getpid(), genome_id), "wb") as f:
                    pickle.dump(genome, f, 2)
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

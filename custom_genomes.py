import random

# For CPPNs and NEAT
import neat

# for Minecraft
from minecraft_pb2 import *

LENGTH_OF_BLOCKLIST = 5
MUTATE_CONSTANT = .2

class CustomBlocksGenome(neat.DefaultGenome):
    # Initializes the block list
    def __init__(self, key):
        super().__init__(key)
        self.block_list = []

    # Fills the block list with random block types
    def configure_new(self, config):
        super().configure_new(config)
        self.block_list = random.sample(list(BlockType), LENGTH_OF_BLOCKLIST) #<--

    # Randomly selects one block list from the two genomes (multi-point crossover)
    def configure_crossover(self, genome1, genome2, config):
        super().configure_crossover(genome1, genome2, config)

        index =0
        while(index<len(self.block_list)):
            rand_choice = random.uniform(0.0,1.0)
            if(rand_choice<.5):
                self.block_list.append(genome1.block_list)
            else:
                self.block_list.append(genome2.block_list)
               

    # Based on MUTATE_CONSTANT, selects a random index and replaces it with a new random block
    def mutate(self, config):
        super().mutate(config)
        r = random()
        if(r<MUTATE_CONSTANT):
            random_int = random.randInt(0,len(self.block_list)) #<--
            self.block_list[random_int] = random.choice(list(BlockType))#<--
    
    # Arbitrary value for the difference calculated by inceasing the distance for each difference 
    # in the two lists, will likley change later
    def distance(self, other, config):
        super().distance(other, config)
        block_list_dist = 0
        index =0
        while(index<len(self.block_list)):
            if(self.block_list[index]==other.block_list[index]):
                block_list_dist = block_list_dist + .05
            index = index+1
        return block_list_dist

    def __str__(self):
        return f"Blocks: {self.block_list}\n{super().__str__()}"


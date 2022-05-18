import math
import os
import pickle
import random

# For CPPNs and NEAT
import neat
import CustomBlocksGenome

# for Minecraft
import grpc
import minecraft_pb2_grpc
from minecraft_pb2 import *

LENGTH_OF_BLOCKLIST = 5
MUTATE_CONSTANT = .2

class CustomBlocksGenome(neat.DefaultGenome):
    def __init__(self, key):
        super().__init__(key)
        self.block_list = []

    def configure_new(self, config):
        super().configure_new(config)
        self.block_list = random.sample(list(BlockType), LENGTH_OF_BLOCKLIST) #<--

    def configure_crossover(self, genome1, genome2, config):
        super().configure_crossover(genome1, genome2, config)
        self.block_list = random.choice(genome1.block_list,genome2.block_list)

    def mutate(self, config):
        super().mutate(config)
        r = random()
        if(r<MUTATE_CONSTANT):
            random_int = random.randInt(0,len(self.block_list)-1) #<--
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



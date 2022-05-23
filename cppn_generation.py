# For neat
import neat

# For utility functions
import util

# For simple math functions
import math

# For minecraft
import grpc
import minecraft_pb2_grpc
from minecraft_pb2 import *

def query_cppn_for_shape(genome, config, corner, position_information, args, block_list):
        """
        Query CPPN at all voxel coordinates to generate the list of
        blocks that will eventually be rendered in the Minecraft server.

        Parameters:
        genome (DefaultGenome): A CPPN or some class that extends CPPNs
        config (Config): NEAT configurations
        corner (int,int,int): three-tuple of initial/minimal x,y,z coordinates for shape

        Returns:
        [Block]:List of Blocks to generate in Minecraft
        """
        # If not evolving block list, use the static one specified lower in the code. Otherwise, use the genome's list
        if not args.BLOCK_LIST_EVOLVES:
            block_options = block_list
        else:
            block_options = genome.block_list

        net = neat.nn.FeedForwardNetwork.create(genome, config) # Create CPPN out of genome
        shape = []
        for xi in range(position_information["xrange"]):
            x = util.scale_and_center(xi,position_information["xrange"])
            for yi in range(position_information["yrange"]):
                y = util.scale_and_center(yi,position_information["yrange"])
                for zi in range(position_information["zrange"]):
                    z = util.scale_and_center(zi,position_information["zrange"])
                    # math.sqrt(2) is the usual scaling for radial distances in CPPNs
                    center_dist = util.distance((x,y,z),(0,0,0))
                    output = net.activate([x, y, z, center_dist * math.sqrt(2), 1.0])
                    
                    # First output determines whether there is a block at all.
                    # If there is a block, argmax determines the max value and places the specified block 
                    # from the list of possible blocks
                    presence_threshold = args.PRESENCE_THRESHOLD 
                    
                    if args.DISTANCE_PRESENCE_THRESHOLD:
                        presence_threshold = args.DISTANCE_PRESENCE_MULTIPLIER * center_dist                            

                    # Only generate non-air blocks
                    if output[0] >= presence_threshold: 
                        output_val = util.argmax(output[1:])
                        assert (output_val >= 0 and output_val < len(block_options)),"{} out of bounds: {}".format(output_val,block_options)
                        block = Block(position=Point(x=corner[0]+xi, y=corner[1]+yi, z=corner[2]+zi), type=block_options[output_val], orientation=NORTH)
                        shape.append(block)
        
        if(len(shape) == 0):
            print("Genome at corner {} is empty".format(corner))
        else:
            #print(list(BlockType.items()))
            #print(list(BlockType.keys()))
            print("Genome at corner {} generated {} blocks of these types: {}".format(corner,len(shape),set(map(lambda x: BlockType.keys()[x.type], shape))))

        return shape
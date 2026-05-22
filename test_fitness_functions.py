# for Minecraft
import grpc
import minecraft_pb2_grpc
from minecraft_pb2 import *

# For minecraft structures
import minecraft_structures as ms
import fitness_functions as ff

import pytest
import argparse

def test_type_count():
    
    try:
        channel = grpc.insecure_channel('localhost:5001')
        client = minecraft_pb2_grpc.MinecraftServiceStub(channel)
        
        
        position_information = dict()
        position_information["startx"] = -100
        position_information["starty"] = 5
        position_information["startz"] = 200
        position_information["xrange"] = 10
        position_information["yrange"] = 10
        position_information["zrange"] = 10 

        corners = []
        for n in range(10):
            corner = (position_information["startx"] + n*(position_information["xrange"]+2+1), position_information["starty"], position_information["startz"])
            corners.append(corner)

        x = position_information["startx"]
        y = position_information["starty"]
        z = position_information["startz"]
        ms.clear_area(client, position_information, 10, 1, 5)
        shape1 = [
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
            Block(position=Point(x=x+3, y=y+3,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+5, y=y+3,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+4, y=y+3,  z=z), type=GLOWSTONE, orientation=NORTH),

            Block(position=Point(x=x,   y=y+2,  z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+2,  z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+2,  z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+2,  z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+4,  z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+4,  z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+4,  z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x,   y=y+4,  z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x,   y=y,    z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x,   y=y+1,  z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x,   y=y+3,  z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+3,  z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+5, y=y+3,  z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+4, y=y+3,  z=z+4), type=SLIME, orientation=NORTH),
            
            Block(position=Point(x=x,   y=y+2,  z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+2,  z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+2,  z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+2,  z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+4,  z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+4,  z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+4,  z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x,   y=y+4,  z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x,   y=y,    z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x,   y=y+1,  z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x,   y=y+3,  z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+3,  z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+5, y=y+3,  z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+4, y=y+3,  z=z+1), type=SLIME, orientation=NORTH),
            
            Block(position=Point(x=x,   y=y+2,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+2,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+2,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+2,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+4,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+4,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+4,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+4,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y,    z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+1,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+3,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+3,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+5, y=y+3,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+4, y=y+3,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            
            Block(position=Point(x=x,   y=y+2,  z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+2,  z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+2,  z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+2,  z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+4,  z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+4,  z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+4,  z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+4,  z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y,    z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+1,  z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+3,  z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+3,  z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+5, y=y+3,  z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+4, y=y+3,  z=z+3), type=GLOWSTONE, orientation=NORTH)]

        client.spawnBlocks(Blocks(blocks=shape1))    


        x = position_information["startx"] + position_information["xrange"] + 3
        y = position_information["starty"]
        z = position_information["startz"]
        
        shape2 = []
            
        # fill sides
        for i in range(10):
            for xi in range(position_information["xrange"]):
                shape2.append(Block(position=Point(x=x + xi, y=y, z=z+i), type=RED_GLAZED_TERRACOTTA, orientation=NORTH))
                shape2.append(Block(position=Point(x=x + xi, y=y+2, z=z+i), type=RED_GLAZED_TERRACOTTA, orientation=NORTH))
                shape2.append(Block(position=Point(x=x + xi, y=y+1, z=z+i), type=BLUE_GLAZED_TERRACOTTA, orientation=NORTH))
                shape2.append(Block(position=Point(x=x + xi, y=y+3, z=z+i), type=BLUE_GLAZED_TERRACOTTA, orientation=NORTH))
                shape2.append(Block(position=Point(x=x + xi, y=y+6, z=z+i), type=BLUE_GLAZED_TERRACOTTA, orientation=NORTH))
                shape2.append(Block(position=Point(x=x + xi, y=y+4, z=z+i), type=RED_GLAZED_TERRACOTTA, orientation=NORTH))
                shape2.append(Block(position=Point(x=x + xi, y=y+5, z=z+i), type=RED_GLAZED_TERRACOTTA, orientation=NORTH))
                shape2.append(Block(position=Point(x=x + xi, y=y+8, z=z+i), type=BLUE_GLAZED_TERRACOTTA, orientation=NORTH))
                shape2.append(Block(position=Point(x=x + xi, y=y+7, z=z+i), type=RED_GLAZED_TERRACOTTA, orientation=NORTH))
                shape2.append(Block(position=Point(x=x + xi, y=y+9, z=z+i), type=RED_GLAZED_TERRACOTTA, orientation=NORTH))

        client.spawnBlocks(Blocks(blocks=shape2))


        x = position_information["startx"] + (position_information["xrange"] + 3)*2
        y = position_information["starty"]
        z = position_information["startz"]
        
        shape3 = []
            
        # fill sides
        for i in range(10):
            for xi in range(position_information["xrange"]):
                for yi in range(position_information["yrange"]):
                    shape3.append(Block(position=Point(x=x + xi, y=y+yi, z=z+i), type=IRON_BLOCK, orientation=NORTH))
                
        client.spawnBlocks(Blocks(blocks=shape3))


        x = position_information["startx"] + (position_information["xrange"] + 3)*3
        y = position_information["starty"]
        z = position_information["startz"]
        
        shape4 = []
            
        # fill sides
        for i in range(8):
            for xi in range(6):
                for yi in range(7):
                    shape4.append(Block(position=Point(x=x + xi, y=y+yi, z=z+i), type=NETHER_WART_BLOCK, orientation=NORTH))

        for i in range(7):
            shape4.append(Block(position=Point(x=x+3, y=y + i, z=z+4), type=AIR, orientation=NORTH))
            shape4.append(Block(position=Point(x=x+3, y=y + i, z=z+3), type=AIR, orientation=NORTH))
            shape4.append(Block(position=Point(x=x+2, y=y + i, z=z+4), type=AIR, orientation=NORTH))
            shape4.append(Block(position=Point(x=x+2, y=y + i, z=z+3), type=AIR, orientation=NORTH))
                    
        client.spawnBlocks(Blocks(blocks=shape4))

        test_parser = argparse.ArgumentParser()
        
        def block_int(name):
            """
            Converts the name of a block into its corresponding int value.
            """
            return BlockType.Value(name)
        
        test_parser.add_argument('--DESIRED_BLOCK', type=block_int, default=GLOWSTONE, metavar='',
                            help='The desired block.')
        
        args = test_parser.parse_args()
        
        # number of glow blocks = 42
        assert ff.type_count(client, position_information, corners[0], args) == 42
        
        # 100 * 6 = 600
        args.DESIRED_BLOCK = RED_GLAZED_TERRACOTTA
        assert ff.type_count(client, position_information, corners[1], args) == 600

        # 10^3 = 1000
        args.DESIRED_BLOCK = IRON_BLOCK
        assert ff.type_count(client, position_information, corners[2], args) == 1000

        args.DESIRED_BLOCK = NETHER_WART_BLOCK
        # (8 * 7 * 6) - (7 * 4) = 308  
        assert ff.type_count(client, position_information, corners[3], args) == 308
    except:
        pytest.fail('Currently not connected to a minecraft server.')
        
def test_type_target():
    try:
        channel = grpc.insecure_channel('localhost:5001')
        client = minecraft_pb2_grpc.MinecraftServiceStub(channel)
        
        position_information = dict()
        position_information["startx"] = -100
        position_information["starty"] = 5
        position_information["startz"] = 150
        position_information["xrange"] = 10
        position_information["yrange"] = 10
        position_information["zrange"] = 10 

        corners = []
        for n in range(10):
            corner = (position_information["startx"] + n*(position_information["xrange"]+2+1), position_information["starty"], position_information["startz"])
            corners.append(corner)

        x = position_information["startx"]
        y = position_information["starty"]
        z = position_information["startz"]

        ms.clear_area(client, position_information, 10, 1, 5)
        shape1 = [
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
            Block(position=Point(x=x+3, y=y+3,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+5, y=y+3,  z=z), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+4, y=y+3,  z=z), type=GLOWSTONE, orientation=NORTH),

            Block(position=Point(x=x,   y=y+2,  z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+2,  z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+2,  z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+2,  z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+4,  z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+4,  z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+4,  z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x,   y=y+4,  z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x,   y=y,    z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x,   y=y+1,  z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x,   y=y+3,  z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+3,  z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+5, y=y+3,  z=z+4), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+4, y=y+3,  z=z+4), type=SLIME, orientation=NORTH),
            
            Block(position=Point(x=x,   y=y+2,  z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+2,  z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+2,  z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+2,  z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+4,  z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+4,  z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+4,  z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x,   y=y+4,  z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x,   y=y,    z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x,   y=y+1,  z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x,   y=y+3,  z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+3,  z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+5, y=y+3,  z=z+1), type=SLIME, orientation=NORTH),
            Block(position=Point(x=x+4, y=y+3,  z=z+1), type=SLIME, orientation=NORTH),
            
            Block(position=Point(x=x,   y=y+2,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+2,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+2,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+2,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+4,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+4,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+4,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+4,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y,    z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+1,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+3,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+3,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+5, y=y+3,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+4, y=y+3,  z=z+2), type=GLOWSTONE, orientation=NORTH),
            
            Block(position=Point(x=x,   y=y+2,  z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+2,  z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+2,  z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+2,  z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+4,  z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+2, y=y+4,  z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+1, y=y+4,  z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+4,  z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y,    z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+1,  z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x,   y=y+3,  z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+3, y=y+3,  z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+5, y=y+3,  z=z+3), type=GLOWSTONE, orientation=NORTH),
            Block(position=Point(x=x+4, y=y+3,  z=z+3), type=GLOWSTONE, orientation=NORTH)]

        client.spawnBlocks(Blocks(blocks=shape1))    


        x = position_information["startx"] + position_information["xrange"] + 3
        y = position_information["starty"]
        z = position_information["startz"]
        
        shape2 = []
            
        # fill sides
        for i in range(10):
            for xi in range(position_information["xrange"]):
                shape2.append(Block(position=Point(x=x + xi, y=y, z=z+i), type=RED_GLAZED_TERRACOTTA, orientation=NORTH))
                shape2.append(Block(position=Point(x=x + xi, y=y+2, z=z+i), type=RED_GLAZED_TERRACOTTA, orientation=NORTH))
                shape2.append(Block(position=Point(x=x + xi, y=y+1, z=z+i), type=BLUE_GLAZED_TERRACOTTA, orientation=NORTH))
                shape2.append(Block(position=Point(x=x + xi, y=y+3, z=z+i), type=BLUE_GLAZED_TERRACOTTA, orientation=NORTH))
                shape2.append(Block(position=Point(x=x + xi, y=y+6, z=z+i), type=BLUE_GLAZED_TERRACOTTA, orientation=NORTH))
                shape2.append(Block(position=Point(x=x + xi, y=y+4, z=z+i), type=RED_GLAZED_TERRACOTTA, orientation=NORTH))
                shape2.append(Block(position=Point(x=x + xi, y=y+5, z=z+i), type=RED_GLAZED_TERRACOTTA, orientation=NORTH))
                shape2.append(Block(position=Point(x=x + xi, y=y+8, z=z+i), type=BLUE_GLAZED_TERRACOTTA, orientation=NORTH))
                shape2.append(Block(position=Point(x=x + xi, y=y+7, z=z+i), type=RED_GLAZED_TERRACOTTA, orientation=NORTH))
                shape2.append(Block(position=Point(x=x + xi, y=y+9, z=z+i), type=RED_GLAZED_TERRACOTTA, orientation=NORTH))

        client.spawnBlocks(Blocks(blocks=shape2))


        x = position_information["startx"] + (position_information["xrange"] + 3)*2
        y = position_information["starty"]
        z = position_information["startz"]
        
        shape3 = []
            
        # fill sides
        for i in range(10):
            for xi in range(position_information["xrange"]):
                for yi in range(position_information["yrange"]):
                    shape3.append(Block(position=Point(x=x + xi, y=y+yi, z=z+i), type=IRON_BLOCK, orientation=NORTH))
                
        client.spawnBlocks(Blocks(blocks=shape3))


        x = position_information["startx"] + (position_information["xrange"] + 3)*3
        y = position_information["starty"]
        z = position_information["startz"]
        
        shape4 = []
            
        # fill sides
        for i in range(8):
            for xi in range(6):
                for yi in range(7):
                    shape4.append(Block(position=Point(x=x + xi, y=y+yi, z=z+i), type=NETHER_WART_BLOCK, orientation=NORTH))

        for i in range(7):
            shape4.append(Block(position=Point(x=x+3, y=y + i, z=z+4), type=AIR, orientation=NORTH))
            shape4.append(Block(position=Point(x=x+3, y=y + i, z=z+3), type=AIR, orientation=NORTH))
            shape4.append(Block(position=Point(x=x+2, y=y + i, z=z+4), type=AIR, orientation=NORTH))
            shape4.append(Block(position=Point(x=x+2, y=y + i, z=z+3), type=AIR, orientation=NORTH))
                    
        client.spawnBlocks(Blocks(blocks=shape4))

        test_parser = argparse.ArgumentParser()
        
        def block_int(name):
            """
            Converts the name of a block into its corresponding int value.
            """
            return BlockType.Value(name)
        
        test_parser.add_argument('--DESIRED_BLOCK', type=block_int, default=GLOWSTONE, metavar='',
                            help='The desired block.')
        test_parser.add_argument('--DESIRED_BLOCK_COUNT', type=int, default=0, metavar='',
                            help='The desired block count.')
        
        args = test_parser.parse_args()
        
        # DESIRED_BLOCK_COUNT - abs((DESIRED_BLOCK_COUNT - current_block_count))
        
        # 32 - abs((32 - 42)) = 22
        args.DESIRED_BLOCK_COUNT = 32
        assert ff.type_target(client, position_information, corners[0], args) == 22
        
        # 250 - abs((250 - 600)) = 22
        args.DESIRED_BLOCK = RED_GLAZED_TERRACOTTA
        args.DESIRED_BLOCK_COUNT = 250
        assert ff.type_target(client, position_information, corners[1], args) == -100

        # 875 - abs((875 - 1000)) = 750
        args.DESIRED_BLOCK = IRON_BLOCK
        args.DESIRED_BLOCK_COUNT = 875
        assert ff.type_target(client, position_information, corners[2], args) == 750

        # 250 - abs((250 - 308)) = 42
        args.DESIRED_BLOCK = NETHER_WART_BLOCK
        args.DESIRED_BLOCK_COUNT = 250
        assert ff.type_target(client, position_information, corners[3], args) == 192
    except:
        pytest.fail('Currently not connected to a minecraft server.')
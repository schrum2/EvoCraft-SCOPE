import grpc
import random
import time

import minecraft_pb2_grpc
from minecraft_pb2 import *

channel = grpc.insecure_channel('localhost:5001')
client = minecraft_pb2_grpc.MinecraftServiceStub(channel)

client.fillCube(FillCubeRequest(  # Clear a 20x10x20 working area
    cube=Cube(
        min=Point(x=-2, y=1, z=1),
        max=Point(x=3, y=11, z=11)
    ),
    type=AIR
))

b = [
    Block(position=Point(x=0, y=10, z=4), type=OBSERVER, orientation=SOUTH),
    Block(position=Point(x=0, y=10, z=0), type=SLIME, orientation=SOUTH),
    Block(position=Point(x=-1, y=10, z=0), type=OBSERVER, orientation=NORTH),
    Block(position=Point(x=1, y=10, z=0), type=OBSERVER, orientation=NORTH),
    Block(position=Point(x=0, y=11, z=0), type=OBSERVER, orientation=NORTH),
    Block(position=Point(x=0, y=9, z=0), type=OBSERVER, orientation=NORTH),
    Block(position=Point(x=0, y=10, z=1), type=SLIME, orientation=SOUTH),
    Block(position=Point(x=-1, y=10, z=1), type=PISTON, orientation=SOUTH),
    Block(position=Point(x=1, y=10, z=1), type=PISTON, orientation=SOUTH),
    Block(position=Point(x=0, y=11, z=1), type=PISTON, orientation=SOUTH),
    Block(position=Point(x=0, y=9, z=1), type=PISTON, orientation=SOUTH),
    Block(position=Point(x=-1, y=10, z=2), type=AIR, orientation=SOUTH),
    Block(position=Point(x=-1, y=10, z=3), type=SLIME, orientation=SOUTH),
    Block(position=Point(x=-1, y=10, z=4), type=TNT, orientation=SOUTH),
    Block(position=Point(x=0, y=10, z=3), type=STICKY_PISTON, orientation=NORTH),
    Block(position=Point(x=1, y=10, z=3), type=TNT, orientation=SOUTH),
    Block(position=Point(x=1, y=10, z=4), type=TNT, orientation=SOUTH),
    Block(position=Point(x=0, y=11, z=3), type=TNT, orientation=SOUTH),
    Block(position=Point(x=0, y=11, z=4), type=TNT, orientation=SOUTH),
    Block(position=Point(x=0, y=9, z=3), type=TNT, orientation=WEST),
    Block(position=Point(x=0, y=9, z=4), type=TNT, orientation=SOUTH),
    Block(position=Point(x=-1, y=10, z=5), type=TNT, orientation=SOUTH),
    Block(position=Point(x=1, y=10, z=5), type=TNT, orientation=SOUTH),
    Block(position=Point(x=0, y=11, z=5), type=TNT, orientation=SOUTH),
    Block(position=Point(x=0, y=10, z=8), type=REDSTONE_BLOCK, orientation=SOUTH),
    Block(position=Point(x=0, y=10, z=7), type=QUARTZ_BLOCK, orientation=SOUTH),
    Block(position=Point(x=0, y=10, z=5), type=SAND, orientation=SOUTH),
]

random.shuffle(b)

#for block in b:
#    client.spawnBlocks(Blocks(blocks=[block]))
    
client.spawnBlocks(Blocks(blocks=b))
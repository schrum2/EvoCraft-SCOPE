import grpc

import minecraft_pb2_grpc
from minecraft_pb2 import *

channel = grpc.insecure_channel('localhost:5001')
client = minecraft_pb2_grpc.MinecraftServiceStub(channel)

client.fillCube(FillCubeRequest(  # Clear a 20x10x20 working area
    cube=Cube(
        min=Point(x=-20, y=3, z=-150),
        max=Point(x=20, y=20, z=20)
    ),
    type=AIR
))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=0, y=6, z=0), type=TNT, orientation=WEST),
    Block(position=Point(x=1, y=6, z=0), type=REDSTONE_LAMP, orientation=WEST),
    Block(position=Point(x=2, y=6, z=0), type=OBSERVER, orientation=SOUTH),
    Block(position=Point(x=3, y=6, z=0), type=SLIME, orientation=WEST),
    Block(position=Point(x=4, y=6, z=0), type=SLIME, orientation=WEST),
    Block(position=Point(x=0, y=5, z=0), type=SLIME, orientation=WEST),
    Block(position=Point(x=1, y=5, z=0), type=SLIME, orientation=WEST),
    Block(position=Point(x=2, y=5, z=0), type=STICKY_PISTON, orientation=EAST),
    Block(position=Point(x=4, y=5, z=0), type=SLIME, orientation=WEST),

    Block(position=Point(x=0, y=6, z=1), type=SLIME, orientation=WEST),
    Block(position=Point(x=1, y=6, z=1), type=SLIME, orientation=WEST),
    Block(position=Point(x=2, y=6, z=1), type=STICKY_PISTON, orientation=WEST),
    Block(position=Point(x=3, y=6, z=1), type=STICKY_PISTON, orientation=UP),
    Block(position=Point(x=4, y=6, z=1), type=SLIME, orientation=WEST),
    Block(position=Point(x=0, y=5, z=1), type=SLIME, orientation=WEST),
    Block(position=Point(x=2, y=5, z=1), type=OBSERVER, orientation=UP),
    Block(position=Point(x=3, y=5, z=1), type=SLIME, orientation=WEST),
    Block(position=Point(x=4, y=5, z=1), type=STICKY_PISTON, orientation=EAST),
    Block(position=Point(x=4, y=7, z=1), type=FIRE, orientation=EAST),
]))


blocks = client.readCube(Cube(
    min=Point(x=1, y=5, z=-4),
    max=Point(x=1, y=6, z=1)
))
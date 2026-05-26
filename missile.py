import grpc
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

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=0, y=10, z=5), type=TNT, orientation=SOUTH),
]))

client.spawnBlocks(Blocks(blocks=[
    # Origin slime block
    Block(position=Point(x=0, y=10, z=0), type=SLIME, orientation=SOUTH),

    # Front-facing observers left/right/up/down of origin slime
    Block(position=Point(x=-1, y=10, z=0), type=OBSERVER, orientation=NORTH),  # left
    Block(position=Point(x=1,  y=10, z=0), type=OBSERVER, orientation=NORTH),  # right
    Block(position=Point(x=0,  y=11, z=0), type=OBSERVER, orientation=NORTH),  # up
    Block(position=Point(x=0,  y=9,  z=0), type=OBSERVER, orientation=NORTH),  # down

    # Slime block in front of origin slime
    Block(position=Point(x=0, y=10, z=1), type=SLIME, orientation=SOUTH),

    # Front-facing pistons left/right/up/down of origin slime
    Block(position=Point(x=-1, y=10, z=1), type=PISTON, orientation=SOUTH),  # left
    Block(position=Point(x=1,  y=10, z=1), type=PISTON, orientation=SOUTH),  # right
    Block(position=Point(x=0,  y=11, z=1), type=PISTON, orientation=SOUTH),  # up
    Block(position=Point(x=0,  y=9,  z=1), type=PISTON, orientation=SOUTH),  # down

    # Air, slime, TNT in front of LEFT piston
    Block(position=Point(x=-1, y=10, z=2), type=AIR, orientation=SOUTH),
    Block(position=Point(x=-1, y=10, z=3), type=SLIME, orientation=SOUTH),
    Block(position=Point(x=-1, y=10, z=4), type=TNT, orientation=SOUTH),

    # Back-facing sticky piston behind observer
    Block(position=Point(x=0, y=10, z=3), type=STICKY_PISTON, orientation=NORTH),

    # TNT to the left of sticky piston
    Block(position=Point(x=1, y=10, z=3), type=TNT, orientation=SOUTH),

    # TNT to the left of observer
    Block(position=Point(x=1, y=10, z=4), type=TNT, orientation=SOUTH),

    # TNT above sticky piston
    Block(position=Point(x=0, y=11, z=3), type=TNT, orientation=SOUTH),

    # TNT above observer
    Block(position=Point(x=0, y=11, z=4), type=TNT, orientation=SOUTH),

    # TNT below sticky piston
    Block(position=Point(x=0, y=9, z=3), type=TNT, orientation=SOUTH),

    # TNT below observer
    Block(position=Point(x=0, y=9, z=4), type=TNT, orientation=SOUTH),

    Block(position=Point(x=-1, y=10, z=5), type=TNT, orientation=SOUTH),
    Block(position=Point(x=1, y=10, z=5), type=TNT, orientation=SOUTH),
    Block(position=Point(x=0, y=11, z=5), type=TNT, orientation=SOUTH),
    Block(position=Point(x=0, y=9, z=5), type=TNT, orientation=SOUTH),

    Block(position=Point(x=-1, y=10, z=6), type=TNT, orientation=SOUTH),
    Block(position=Point(x=1, y=10, z=6), type=TNT, orientation=SOUTH),
    Block(position=Point(x=0, y=11, z=6), type=TNT, orientation=SOUTH),
    Block(position=Point(x=0, y=9, z=6), type=TNT, orientation=SOUTH),

    Block(position=Point(x=0, y=10, z=7), type=REDSTONE_BLOCK, orientation=SOUTH),
    Block(position=Point(x=0, y=10, z=6), type=QUARTZ_BLOCK, orientation=SOUTH),
    # Front-facing observer to the left of TNT
    Block(position=Point(x=0, y=10, z=4), type=OBSERVER, orientation=SOUTH),
]))
#blocks = client.readCube(Cube(
#    min=Point(x=1, y=5, z=-4),
#    max=Point(x=1, y=6, z=1)
#))
#time.sleep(0.1)
#time.sleep(2.0)

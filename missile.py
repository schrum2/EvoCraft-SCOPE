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
    Block(position=Point(x=0, y=10, z=4), type=OBSERVER, orientation=SOUTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=0, y=10, z=0), type=SLIME, orientation=SOUTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=-1, y=10, z=0), type=OBSERVER, orientation=NORTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=1, y=10, z=0), type=OBSERVER, orientation=NORTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=0, y=11, z=0), type=OBSERVER, orientation=NORTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=0, y=9, z=0), type=OBSERVER, orientation=NORTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=0, y=10, z=1), type=SLIME, orientation=SOUTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=-1, y=10, z=1), type=PISTON, orientation=SOUTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=1, y=10, z=1), type=PISTON, orientation=SOUTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=0, y=11, z=1), type=PISTON, orientation=SOUTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=0, y=9, z=1), type=PISTON, orientation=SOUTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=-1, y=10, z=2), type=AIR, orientation=SOUTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=-1, y=10, z=3), type=SLIME, orientation=SOUTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=-1, y=10, z=4), type=TNT, orientation=SOUTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=0, y=10, z=3), type=STICKY_PISTON, orientation=NORTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=1, y=10, z=3), type=TNT, orientation=SOUTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=1, y=10, z=4), type=TNT, orientation=SOUTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=0, y=11, z=3), type=TNT, orientation=SOUTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=0, y=11, z=4), type=TNT, orientation=SOUTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=0, y=9, z=3), type=TNT, orientation=WEST),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=0, y=9, z=4), type=TNT, orientation=SOUTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=-1, y=10, z=5), type=TNT, orientation=SOUTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=1, y=10, z=5), type=TNT, orientation=SOUTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=0, y=11, z=5), type=TNT, orientation=SOUTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=0, y=10, z=8), type=REDSTONE_BLOCK, orientation=SOUTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=0, y=10, z=7), type=QUARTZ_BLOCK, orientation=SOUTH),
]))

client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=0, y=10, z=5), type=SAND, orientation=SOUTH),
]))

# client.spawnBlocks(Blocks(blocks=[
#     Block(position=Point(x=0, y=10, z=4), type=OBSERVER, orientation=SOUTH),
# ]))

#blocks = client.readCube(Cube(
#    min=Point(x=1, y=5, z=-4),
#    max=Point(x=1, y=6, z=1)
#))
#time.sleep(0.1)
#time.sleep(2.0)

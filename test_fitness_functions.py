# For CPPNs and NEAT
import neat
import custom_genomes as cg

# for Minecraft
import grpc
import minecraft_pb2_grpc
from minecraft_pb2 import *

# For minecraft structures
import minecraft_structures as ms

# For fitness functions
import pytest

def test_type_count():
    channel = grpc.insecure_channel('localhost:5001')
    client = minecraft_pb2_grpc.MinecraftServiceStub(channel)
        
    print("test")
    
    

def test_type_target():
    print("other test")
import novelty_characterizations as nc
import pytest

import grpc
import minecraft_pb2_grpc
from minecraft_pb2 import *

def test_presence_characterization():
    channel = grpc.insecure_channel('localhost:5001')
    client = minecraft_pb2_grpc.MinecraftServiceStub(channel)

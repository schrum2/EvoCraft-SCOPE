import minecraft_pb2 as mc

def select_possible_block_sets(block_set):
    possible_block_types = []
    if(block_set=='all'):
        for i in range(len(mc.BlockType.values())):
            possible_block_types.append(mc.BlockType.values()[i])
    return possible_block_types
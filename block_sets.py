from minecraft_pb2 import *

def select_possible_block_sets(block_set):
    possible_block_types = []
    if(block_set=='all'):
        possible_block_types = list(BlockType.values())
    elif(block_set=='undroppable'):
        # All blocks that aren't droppable, all doors, plants, torches, wires, levers, 
        # pressure plates, buttons, levers, and shulker boxes are removed
        possible_block_types = [1, 2, 3, 6, 7, 8, 10, 13, 14, 15, 16, 18, 20, 21, 22, 23, 24, 25, 27, 30, 31, 33, 34, 35, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 51, 52, 53, 54, 55, 57, 58, 59, 60, 61, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 83, 84, 85, 86, 87, 88, 89, 91, 92, 93, 94, 95, 96, 98, 100, 101, 103, 104, 105, 106, 108, 109, 110, 112, 113, 114, 116, 117, 118, 119, 120, 122, 125, 127, 128, 129, 130, 131, 132, 133, 135, 136, 138, 140, 141, 142, 143, 144, 145, 147, 148, 149, 150, 151, 152, 154, 155, 157, 160, 161, 163, 164, 165, 166, 168, 170, 171, 172, 173, 174, 175, 176, 177, 179, 180, 181, 185, 187, 188, 189, 190, 193, 194, 195, 196, 198, 199, 201, 202, 203, 204, 205, 206, 208, 209, 210, 211, 212, 213, 216, 217, 218, 219, 222, 223, 224, 225, 226, 228, 230, 231, 235, 236, 240, 242, 244, 249, 250, 252]
    elif(block_set=='machine'):
        possible_block_types = [QUARTZ_BLOCK, SLIME, REDSTONE_BLOCK, PISTON, STICKY_PISTON]
    return possible_block_types
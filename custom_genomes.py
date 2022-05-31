import random

# For CPPNs and NEAT
import neat

# for Minecraft
import minecraft_pb2 as mc
import block_sets

# Must be set in evolution.py
BLOCK_CHANGE_PROBABILITY = 0.0
BLOCK_LIST_LENGTH = 0
POTENTIAL_BLOCK_TYPE_LIST = []
PREVENT_DUPLICATES = False

class CustomBlocksGenome(neat.DefaultGenome):
    def __init__(self, key):
        """ 
        Constructor, Initializes the block list, as well as the rest of the default genome

        Parameters: 
        key (int): Unique identifier for a genome instance
    
        """
        super().__init__(key)
        self.block_list = []

    def configure_new(self, config):
        """
         Fills the block list with random block types as well as the rest of the default genome

         Parameters:
         config (neat.genome.DefaultGenomeConfig): Configuration for the default genome

        """
        super().configure_new(config)
        # The number of blocks in the list is one less than the number of outputs (since the first determines presence)
        # POTENTIAL_BLOCK_TYPE_LIST contains all types of blocks that can be generated and is influenced by the command line parameter
        self.block_list = random.sample(POTENTIAL_BLOCK_TYPE_LIST, BLOCK_LIST_LENGTH)
        # print("genome_id=",self.key)
        # print("newly configured block list: ",self.block_list)
        
    def configure_crossover(self, genome1, genome2, config):
        """
        Randomly selects one block list from the two genomes using multi-point crossover,
        also configues the rest of the default genome. If PREVENT_DUPLICATES is on, it ensures
        no duplicates are added by comparing anything that could be added to the block_list to
        itself to ensure nothing else is added. If both blocks from both genome 1 dn 2 are in 
        the block_list, it generates a new random block until a non-duplicate is added.

        Parameters:
        genome1 (custom_genomes.CustomBlocksGenome): the first genome to take blocks from
        genome2 (custom_genomes.CustomBlocksGenome): the second genome to take blocks from
        config (neat.genome.DefaultGenomeConfig): Configuration for the default genome

        """
        # print("genome_id=",self.key)
        # print("genome_block_list 1: ",genome1.block_list)
        # print("genome_block_list 2: ",genome2.block_list)
        # print()

        super().configure_crossover(genome1, genome2, config)
        index = 0
        while(index<len(genome1.block_list)):
            rand_choice = random.uniform(0.0,1.0)
            if(PREVENT_DUPLICATES):
                if(rand_choice<.5):
                    self.append_block_no_duplicates(genome1, genome2, index)
                else:
                    self.append_block_no_duplicates(genome2, genome1, index)
            else:
                if(rand_choice<.5):
                    self.block_list.append(genome1.block_list[index])
                else:
                    self.block_list.append(genome2.block_list[index])
            index = index + 1

    def append_block_no_duplicates(self, genome_a, genome_b, index):
        """
        Helper method extracted from configure_crossover. Checks if genome a isn't a duplicate
        if it is, then checks genome b. If it also is, then appends a random block that isn't 
        already in the list

        Parameters:
        genome_a (custom_genomes.CustomBlocksGenome): the first genome to take blocks from
        genome_b (custom_genomes.CustomBlocksGenome): the second genome to take blocks from
        index (int): index to take block from 
        """
        if(not genome_a.block_list[index] in self.block_list):
            self.block_list.append(genome_a.block_list[index])
        elif(not genome_b.block_list[index] in self.block_list):
            self.block_list.append(genome_b.block_list[index])
        else:
            random_block = random.choice(POTENTIAL_BLOCK_TYPE_LIST)
            while(random_block in self.block_list):
                random_block = random.choice(POTENTIAL_BLOCK_TYPE_LIST)
            self.block_list.append(random_block)

        # print("New block list: ",self.block_list)
        # print("--------------------------------------------")
               
    def mutate(self, config):
        """
        Based on BLOCK_CHANGE_PROBABILITY, if the random condition is satisfied, selects a random index 
        and replaces it with a new random block. Also mutates the rest of the default genome. If 
        PREVENT_DUPLICATES is on, it first checks that the block list is short enough to allow for 
        duplicates. If it is, it generates a new block, then checks to make sure that block type isn't
        already in the list. Once a lock type is found, it is added to the list

        Parameters:
        config (neat.genome.DefaultGenomeConfig): Configuration for the default genome
        """
        # print("genome_id=",self.key)
        # print("Block_list before mutation:",self.block_list)
        super().mutate(config)
        global BLOCK_CHANGE_PROBABILITY
        r = random.uniform(0.0,1.0) 
        random_int = random.randint(0,len(self.block_list)-1) 
        if(r<BLOCK_CHANGE_PROBABILITY and PREVENT_DUPLICATES and len(self.block_list)<len(POTENTIAL_BLOCK_TYPE_LIST)):
            random_block = random.choice(POTENTIAL_BLOCK_TYPE_LIST)
            while(random_block in self.block_list):
                #print(random_block)
                random_block = random.choice(POTENTIAL_BLOCK_TYPE_LIST)
            self.block_list[random_int] = random_block
        elif(r<BLOCK_CHANGE_PROBABILITY):
            self.block_list[random_int] = random.choice(POTENTIAL_BLOCK_TYPE_LIST)
        # print("Block_list after mutation:",self.block_list)
        # print("--------------------------------------------")

    
    # Arbitrary value for the difference calculated by inceasing the distance for each difference 
    # in the two lists, will likley change later
    def distance(self, other, config):
        """
        Arbitrary value for the difference calculated by inceasing the distance for each difference 
        in the two lists, will likley change later. Also calculates default genomes' distance

        Parameters: 
        other (custom_genomes.CustomBlocksGenome): Another genome than the first one
        config (neat.genome.DefaultGenomeConfig): Configuration for the default genome

        Retruns:
        block_list_dist (double): The calculated distance between the two lists
        """
        super().distance(other, config)
        block_list_dist = 0
        index =0
        while(index<len(self.block_list)):
            if(self.block_list[index]==other.block_list[index]):
                block_list_dist = block_list_dist + .05
            index = index+1
        return block_list_dist

    def __str__(self):
        """
        Prints default genomes's infromation in a string, as well as the newly added block_list
        """
        return f"Blocks: {self.block_list}\n{super().__str__()}"

    


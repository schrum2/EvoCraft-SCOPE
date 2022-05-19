import random

# For CPPNs and NEAT
import neat

# for Minecraft
import minecraft_pb2 as mc

LENGTH_OF_BLOCKLIST = 5
MUTATE_CONSTANT = .2

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
        self.block_list = random.sample(list(mc.BlockType.keys()), LENGTH_OF_BLOCKLIST)
        
    def configure_crossover(self, genome1, genome2, config):
        """
        Randomly selects one block list from the two genomes using multi-point crossover,
        also configues the rest of the default genome

        Parameters:
        genome1 (custom_genomes.CustomBlocksGenome): the first genome to take blocks from
        genome2 (custom_genomes.CustomBlocksGenome): the second genome to take blocks from
        config (neat.genome.DefaultGenomeConfig): Configuration for the default genome

        """
        super().configure_crossover(genome1, genome2, config)
        index = 0
        while(index<len(genome1.block_list)):
            rand_choice = random.uniform(0.0,1.0)
            if(rand_choice<.5):
                self.block_list.append(genome1.block_list[index])
            else:
                self.block_list.append(genome2.block_list[index])
            index = index + 1
               
    def mutate(self, config):
        """
        Based on MUTATE_CONSTANT, if the random condition is satisfied, selects a random index 
        and replaces it with a new random block. Also mutates the rest of the default genome

        Parameters:
        config (neat.genome.DefaultGenomeConfig): Configuration for the default genome
        """
        super().mutate(config)
        r = random.uniform(0.0,1.0) 
        if(r<MUTATE_CONSTANT):
            random_int = random.randint(0,len(self.block_list)-1) 
            self.block_list[random_int] = random.choice(list(mc.BlockType.keys()))#<--
    
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
        Prints defaukt genomes's infromation in a string, as well as the newly added block_list
        """
        return f"Blocks: {self.block_list}\n{super().__str__()}"

    


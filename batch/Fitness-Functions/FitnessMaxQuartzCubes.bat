REM Usage ./FitnessMaxQuartzCubes.bat <seed>
cd..
cd..
python main.py --BASE_DIR=max --EXPERIMENT_PREFIX=quartzcubes --RANDOM_SEED=%1 --POPULATION_SIZE=100 --INTERACTIVE_EVOLUTION=False --SAVE_FITNESS_LOG=True --POTENTIAL_BLOCK_SET=machine --FITNESS_FUNCTION=type_count --DESIRED_BLOCK=QUARTZ_BLOCK --USE_ELITISM=True --EVOLVE_FITNESS=True --SAVE_PARAMETERS=True
 
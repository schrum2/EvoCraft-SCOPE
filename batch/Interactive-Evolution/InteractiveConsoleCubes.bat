REM Usage ./InteractiveConsoleCubes.bat <seed>
cd..
cd..
python main.py --BASE_DIR=console --EXPERIMENT_PREFIX=cubes --RANDOM_SEED=%1 --POPULATION_SIZE=10 --USE_ELITISM=True --INTERACTIVE_EVOLUTION=True --SAVE_PARAMETERS=True
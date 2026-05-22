REM Usage ./InteractiveInGameCubes.bat <seed>
cd..
cd..
python main.py --BASE_DIR=interactive --EXPERIMENT_PREFIX=cubes --RANDOM_SEED=%1 --POPULATION_SIZE=10 --IN_GAME_CONTROL=True --USE_ELITISM=True --INTERACTIVE_EVOLUTION=True --SAVE_PARAMETERS=True
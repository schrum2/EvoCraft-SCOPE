REM Usage ./InteractiveInGameSnakes.bat <seed>
cd..
cd..
python main.py --BASE_DIR=interactive --EXPERIMENT_PREFIX=snakes --RANDOM_SEED=%1 --POPULATION_SIZE=10 --EVOLVE_SNAKE=True --REDIRECT_CONFINED_SNAKES=True --USE_ELITISM=True --IN_GAME_CONTROL=True --INTERACTIVE_EVOLUTION=True --SAVE_PARAMETERS=True
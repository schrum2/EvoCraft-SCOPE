REM Usage ./NoveltySearchLoadRestrictiveMachine.bat <seed>
cd..
cd..
python main.py --BASE_DIR=novelty --EXPERIMENT_PREFIX=basic --LOAD_SAVED_SEED=%1 --POPULATION_SIZE=10 --LOAD_NOVELTY=True --NOVELTY_RANDOM_SCORE=0.1 --EVOLVE_NOVELTY=True --POTENTIAL_BLOCK_SET=restrictive_machine --INTERACTIVE_EVOLUTION=False --NOVELTY_DISTANCE=hamming_distance --NOVELTY_CHARACTER=presence_characterization --XRANGE=2 --YRANGE=1 --ZRANGE=4 --NUM_EVOLVED_BLOCK_LIST_TYPES=2 --SAVE_PARAMETERS=True
REM Usage ./NoveltySearchMachine.bat <seed>
cd..
python main.py --BASE_DIR=novelty --EXPERIMENT_PREFIX=basic --RANDOM_SEED=%1 --POPULATION_SIZE=15 --SAVE_NOVELTY=True --NOVELTY_RANDOM_SCORE=0.1 --EVOLVE_NOVELTY=True --POTENTIAL_BLOCK_SET=machine --INTERACTIVE_EVOLUTION=False --NOVELTY_DISTANCE=hamming_distance --NOVELTY_CHARACTER=presence_characterization --XRANGE=3 --YRANGE=3
REM Usage ./NoveltySearchMachine.bat <seed>
cd..
cd..
python main.py --BASE_DIR=novelty --EXPERIMENT_PREFIX=basic --RANDOM_SEED=%1 --POPULATION_SIZE=10 --SAVE_NOVELTY=True --NOVELTY_RANDOM_SCORE=0.1 --EVOLVE_NOVELTY=True --POTENTIAL_BLOCK_SET=machine --INTERACTIVE_EVOLUTION=False --NOVELTY_DISTANCE=hamming_distance --NOVELTY_CHARACTER=presence_characterization --MAX_NUM_GENERTIONS=1 --XRANGE=3 --YRANGE=3
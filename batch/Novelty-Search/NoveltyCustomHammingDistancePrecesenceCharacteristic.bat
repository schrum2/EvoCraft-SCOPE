REM Usage ./NoveltyCustomHammingDistancePrecesenceCharacteristic.bat <seed>
cd..
cd..
python main.py --BASE_DIR=novelty --EXPERIMENT_PREFIX=basic --RANDOM_SEED=%1 --POPULATION_SIZE=10 --SAVE_NOVELTY=True --NOVELTY_RANDOM_SCORE=0.05 --EVOLVE_NOVELTY=True --POTENTIAL_BLOCK_SET=machine --INTERACTIVE_EVOLUTION=False --NOVELTY_DISTANCE=custom_hamming_distance --NOVELTY_CHARACTER=presence_characterization --SAVE_PARAMETERS=True
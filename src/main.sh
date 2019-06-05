# part 1
python3 pairing.py --clean --save_comb
# part 2 logs are save in test_output/part2.txt
python3 training.py -epochs 4 -batch_size 14 -seed 45 > test_output/part2.txt
import pandas as pd
import numpy as np
import config

import sys

from model import Model
from dataset import Dataset

pair = pd.read_csv(config.PAIR_PATH)

# def get_arg(arg):
# 	if arg in sys.argv:
# 		return int(sys.argv[sys.argv.index(arg)+1])



batch_size = 8
if '-batch_size' in sys.argv:
	batch_size = int(sys.argv[sys.argv.index('-batch_size')+1])

epochs = 5
if '-epochs' in sys.argv:
	epochs = int(sys.argv[sys.argv.index('-epochs')+1])

if __name__ == "__main__":

	dataset = Dataset(x_path = pair[config.DICOM_FILE_TYPE], 
					  y_path = pair[config.MASK_FILE_TYPE])
	model = Model(dataset, batch_size = batch_size)
	for i in range(epochs*batch_size):
		try:
			x, y, j = model.next_batch()
			print(x.shape)
		except TypeError:
			print('end')
			break

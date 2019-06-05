"""Code to build model with dataset"""


import pandas as pd
import numpy as np
import config

import sys

from model import Model
from dataset import Dataset

pair = pd.read_csv(config.PAIR_PATH)

param_list = {'batch_size': 8, 'epochs': 5, 'seed': 63}


def get_arg(param):
	arg = '-' + param
	if arg in sys.argv:
		param_list[param] = int(sys.argv[sys.argv.index(arg)+1])



for param in param_list:
	get_arg(param)


if __name__ == "__main__":

	dataset = Dataset(x_path = pair[config.DICOM_FILE_TYPE], 
					  y_path = pair[config.MASK_FILE_TYPE])
	
	model = Model(dataset, 
		          epochs = param_list['epochs'],
		          batch_size = param_list['batch_size'],
		          seed = param_list['seed'])
	
	while True:
		try:
			x, y = model.next_batch()
		except TypeError:
			print('end of training loop')
			break

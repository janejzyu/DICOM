from parsing import parse_file_list
import config

class Dataset:
	def __init__(self, x_path, y_path):
		assert len(x_path) == len(y_path)
		self.x_path = x_path
		self.y_path = y_path
	
	@property
	def n_dat(self):
		return len(self.x_path)
	
	def get_data(self, ind):
		dicom_path = self.x_path.iloc[ind]
		mask_path =  self.y_path.iloc[ind]
		x = parse_file_list(dicom_path, config.DICOM_FILE_TYPE)
		y = parse_file_list(mask_path, config.MASK_FILE_TYPE)
		return x, y
		
	def preprocess(self, x):
		"""
		standardize the input
		"""
		raise NotImplementedError
		
	def get_preprocessed_data(self, ind):
		"""
		x, y = get_data(ind)
		return preprocess(x), y
		"""
		raise NotImplementedError

	def augment(self, x):
		raise NotImplementedError
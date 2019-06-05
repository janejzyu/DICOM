import numpy as np
import config

class Model():
    """Create a epoch
    """
    def __init__(self, dataset, batch_size = 8, seed = 64):
        self.dataset = dataset
        self.batch_size = batch_size
        self.epoch_generator = self._generate_train_epoch(batch_size)
        self.seed = seed
        np.random.seed(seed)
        
    def _generate_index(self, batch_size):
        n = self.dataset.n_dat
        rand_index = np.random.permutation(n)
        start = 0
        end = start + batch_size
        while start < n:
            yield rand_index[start:end]
            start = end
            end = start + batch_size
    
    def _generate_train_epoch(self, batch_size):
        for ind in self._generate_index(batch_size = batch_size):
            x, y = self.dataset.get_data(ind)
            yield x, y, ind
    
    def next_batch(self):
        try:
            return next(self.epoch_generator)
        except StopIteration:
            print('finished a epoch')
            self.epoch_generator = self._generate_train_epoch(self.batch_size)
            return next(self.epoch_generator)

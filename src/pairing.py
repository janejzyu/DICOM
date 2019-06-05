"""Pairing code for all patients"""


from os import listdir, mkdir, remove
from os.path import join
from shutil import rmtree
import sys

from parsing import parse_contour_file, parse_dicom_file, poly_to_mask

import matplotlib.pyplot as plt
import numpy as np
import config
from PIL import Image
from tqdm import tqdm

def generate_link(link_name = config.LINK_PATH):
	"""Generator of link between patient_id, original_id
	"""
	with open(link_name, 'r') as infile:
		next(infile)
		for line in infile:
			patient_id, original_id = line.strip().split(',')
			yield patient_id, original_id


def plot_dcm_with_mask(dcm_pixel, mask):
	"""Stack mask on top of dicom image 
	"""
	plt.axis('off')
	plt.imshow(dcm_pixel, cmap="gray", alpha = 2)
	plt.imshow(np.invert(mask), cmap='jet', alpha=0.1)
	return plt


def mask_to_image(mask):
	"""Convert boolean mask to gray scale image
	"""
	size = mask.shape[::-1]
	databytes = np.packbits(mask, axis=1)
	img = Image.frombytes(mode='1', size=size, data=databytes)
	return img 

def generate_all_pairing(save_comb = False):
	"""Pair dicom image with its corresponding for all patients

    :param save_comb: whether combined image is saved
    :return: None
    """
	pair_file = open(config.PAIR_PATH, "w+")
	header = config.DICOM_FILE_TYPE + ',' + config.MASK_FILE_TYPE +'\n'
	pair_file.write(header)
	for patient_id, original_id in tqdm(generate_link()):
		cur_contour_path = config.CONTOUR_PATH.format(original_id)
		cur_mask_path = config.MASK_PATH.format(original_id)
		cur_comb_path = config.COMB_PATH.format(original_id)
		try:
			mkdir(cur_mask_path)
		except FileExistsError:
			print("has directory{}".format(cur_mask_path))
		if save_comb:
			try:
				mkdir(cur_comb_path)
			except FileExistsError:
				print("has directory{}".format(cur_comb_path))
		for contour_name in listdir(cur_contour_path):
			contour = parse_contour_file(join(cur_contour_path, contour_name))
			index = str(int(contour_name.split('-')[2]))
			dcm_name = index + config.DCM_EXT
			try:
				dcm_path = join(config.DICOMS_PATH, patient_id, dcm_name)
				dcm = parse_dicom_file(dcm_path) # FileNotFoundError
				if not dcm: # invalid dicom file
					continue
				dcm_pixel = dcm['pixel_data']
				width, height = dcm_pixel.shape
				mask = poly_to_mask(contour, width, height)
                               
				img = mask_to_image(mask)
				mask_path = join(cur_mask_path, index + '.png')
				img.save(mask_path)
				pair_file.write(dcm_path + ',' + mask_path+'\n')
				if save_comb:
					# save comb as image
					plt = plot_dcm_with_mask(dcm_pixel, mask) 
					comb_path = join(cur_comb_path, 'val' + index + '.png')
					plt.savefig(comb_path, bbox_inches='tight', transparent=True, pad_inches=0.0)
			except FileNotFoundError:
				print('no dcm match')	
	pair_file.close()

def clean():
	"""clean all outputs of generate_all_pairing
	"""
	try:
		remove(config.PAIR_PATH)
	except FileNotFoundError:
		print('{} does not exist'.format(config.PAIR_PATH))
	for patient_id, original_id in generate_link():
		cur_mask_path = config.MASK_PATH.format(original_id)
		cur_comb_path = config.COMB_PATH.format(original_id)
		try:
			rmtree(cur_mask_path)
			rmtree(cur_comb_path)
		except FileNotFoundError:
			print('no directory to clean')

if __name__ == "__main__":
	if '--clean' in sys.argv:
		clean()
	
	save_comb = False
	if '--save_comb' in sys.argv:
		save_comb = True
	generate_all_pairing(save_comb)

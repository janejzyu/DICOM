import os
from parsing import parse_contour_file, parse_dicom_file, poly_to_mask


def plot_dcm_with_mask(dcm_pixel, mask):
	raise NotImplementedError

def mask_to_image(mask):
	raise NotImplementedError

def generate_all_pairing(save_comb = False, mask_type):
	"""Pair dicom image with its corresponding for all patients

    :param save_comb: whether combined image is saved
    :param mask_type: as_array or as_image
    :return: None
    """
	# raise NotMatchedError
	raise NotImplementedError

def clean():
	"""clean all outputs of generate_all_pairing
	"""
	raise NotImplementedError

if __name__ == "__main__":
	 clean()
	 generate_all_pairing()

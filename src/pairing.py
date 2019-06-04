import os
from parsing import parse_contour_file, parse_dicom_file, poly_to_mask


def get_patient_id(original_id):
	raise NotImplementedError

def get_original_id(patient_id):
	raise NotImplementedError

def get_dcm(patient_id, index):
	"""Get index.dcm for the given patient

    :param patient_id: filepath to the DICOM file to parse
    :param index: file index
    :return: filepath to the DICOM file
    """
	# raise NotMatchedError
	raise NotImplementedError
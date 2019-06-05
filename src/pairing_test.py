from pairing import *
import sys

def generate_link_test(): 
	#test generate_link
	for patient_id, original_id in generate_link():
	    print('{},{}'.format(patient_id, original_id))


def plot_dcm_with_mask_test(d_test, c_test):
	# test plot_dcm_with_mask method

	contour = parse_contour_file(c_test)
	dcm_test = parse_dicom_file(d_test)['pixel_data'] # FileNotFoundError
	width, height = dcm_test.shape
	mask_test = poly_to_mask(contour, width, height)
	img = plot_dcm_with_mask(dcm_test, mask_test) 


if __name__ == "__main__":
	if '--clean' in sys.argv:
		clean()

	generate_link_test()

	d_test = '../dicoms/SCD0000101/48.dcm'
	c_test = '../contourfiles/SC-HF-I-1/i-contours/IM-0001-0048-icontour-manual.txt'
	plot_dcm_with_mask_test(d_test, c_test)

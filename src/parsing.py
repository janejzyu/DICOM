"""Parsing code for DICOMS and contour files"""

import pydicom
from pydicom.errors import InvalidDicomError

import numpy as np
from PIL import Image, ImageDraw

import config


def parse_contour_file(filename):
    """Parse the given contour filename

    :param filename: filepath to the contourfile to parse
    :return: list of tuples holding x, y coordinates of the contour
    """

    coords_lst = []

    with open(filename, 'r') as infile:
        for line in infile:
            coords = line.strip().split()

            x_coord = float(coords[0])
            y_coord = float(coords[1])
            coords_lst.append((x_coord, y_coord))

    return coords_lst


def parse_dicom_file(filename):
    """Parse the given DICOM filename

    :param filename: filepath to the DICOM file to parse
    :return: dictionary with DICOM image data
    """

    try:
        dcm = pydicom.read_file(filename)
        dcm_image = dcm.pixel_array

        try:
            intercept = dcm.RescaleIntercept
        except AttributeError:
            intercept = 0.0
        try:
            slope = dcm.RescaleSlope
        except AttributeError:
            slope = 0.0

        if intercept != 0.0 and slope != 0.0:
            dcm_image = dcm_image*slope + intercept
        dcm_dict = {'pixel_data' : dcm_image}
        return dcm_dict
    except InvalidDicomError:
        return None

def parse_mask_file(filename):
    """Parse the given mask filename

    :param filename: filepath to the mask file to parse
    :return: dictionary with mask image data
    """   
    img = Image.open(filename)
    width, height = img.size[1], img.size[0]
    mask_image = np.array(img).astype(bool).reshape(width, height)
    mask_dict = {'pixel_data' : mask_image}
    return mask_dict


def parse_file_list(filename_list, file_type):
    """Parse the given filename list

    :param filename_list: list of filepath to parse
    :param file_type
    :return: numpy array of parsed data 
    """ 
    res = []
    for filename in filename_list:
        try:
            if file_type == config.MASK_FILE_TYPE :
                res.append(parse_mask_file(filename)['pixel_data'])
            else:
                assert file_type == config.DICOM_FILE_TYPE
                res.append(parse_dicom_file(filename)['pixel_data'])
        except TypeError:
            pass # None type result from parse_dicom_file
    return np.array(res)


def poly_to_mask(polygon, width, height):
    """Convert polygon to mask

    :param polygon: list of pairs of x, y coords [(x1, y1), (x2, y2), ...]
     in units of pixels
    :param width: scalar image width
    :param height: scalar image height
    :return: Boolean mask of shape (height, width)
    """

    # http://stackoverflow.com/a/3732128/1410871
    img = Image.new(mode='L', size=(width, height), color=0)
    ImageDraw.Draw(img).polygon(xy=polygon, outline=0, fill=1)
    mask = np.array(img).astype(bool)
    return mask

# Challenge

#### Check Challenge_description.pdf for more detailed description of this challenge.

In this challenge, you will download studies of DICOM MRI images and contour files to prepare them for training a convolutional neural network. The inputs to the network will be dicom images and the targets will be the contours encoded as boolean masks (foreground pixels = True; background pixels = False). 


Result can be tested by running **src/main.sh**. Each line is to test each question. Logs from part 2 are save in **test_output/part2.txt**

```bash
# part 1
python3 pairing.py --clean --save_comb
# part 2 logs are save in test_output/part2.txt
python3 training.py -epochs 4 -batch_size 14 -seed 45 > test_output/part2.txt
```


### Definitions
* i-contour: inner contour that separates the left ventricular blood pool from the heart muscle (myocardium)

* o-contour: outer contour that defines the outer border of the left ventricular heart muscle

## Part 1: Parse the DICOM images and Contour Files

Using the functions given above, build a pipeline that will parse the DICOM images and i-contour contour files, making sure to pair the correct DICOM image(s) with the correct contour file. After parsing each i-contour file, make sure to translate the parsed contour to a boolean mask.

Output file systems looks like the following, folders and files that have (*) are outputs from pairing.py:

```bash

contourfiles/
    original_id/
        o-contours/
        i-contours/
            IM-0001-0024-icontour-manual.txt
            IM-0001-0130-icontour-manual.txt
            etc.      
        i-mask/ (*)
            24.png
            130.png
            etc.
        i-comb/ (*)
            val24.png
            val130.png
            etc.       
dicoms/
    patient_id/
        1.dcm
        13.dcm
        24.dcm
        etc.


patient_id,original_id
SCD0000101,SC-HF-I-1
SCD0000201,SC-HF-I-2

pairing.csv (*)
dicom,mask
../dicoms/SCD0000101/24.dcm, ../contourfiles/SC-HF-I-1/i-mask/24.png

```

Since there are less i-contours files than dicom files for a patient, I iterated over files in **i-contours** folders to pair it with the corresponding dicom file. Mask parsed from inner contour files are saved in **i-mask** folders. Pairing of the path between dicom file and mask files are stored in **pairing.csv**

After building the pipeline, please answer the following questions:


#### 1. How did you verify that you are parsing the contours correctly?

I impletmented a function that plot the mask on top of its corresponding dicom image. Results are saved in **i-comb** folders.

To-do: unit test of parsing.py is not implemented yet. Toy contours with lower dimension can be tested to verify the functions.

#### 2. What changes did you make to the code, if any, in order to integrate it into our production code base? 

I didn't change any given code. Further intergration can be made by building a **abstract class/interface** on of the parsing.py file or build a **parser** class with methods in parsing.py.


Note: The function that translates the parsed contours into boolean masks relies on the Pillow library. If you run into any Pillow related issues while using it, please feel free to simply leave the function call in your code, but commented out. We don’t want you to spend too much time (if any) on debugging Pillow issues (as they might be related to environment/install issues).

## Part 2: Model training pipeline

Using the saved information from the DICOM images and contour files, add an additional step to the pipeline that will load batches of data for input into a 2D deep learning model. This pipeline should meet the following criteria:


* Cycles over the entire dataset, loading a single batch (e.g. 8 observations) of inputs (DICOM image data) and targets (boolean masks) at each training step.

* A single batch of data consists of one numpy array for images and one numpy array for targets.

* Within each epoch (e.g. iteration over all studies once), samples from a batch should be loaded randomly from the entire dataset. 


After building the pipeline, please answer the following questions:


#### 1. Did you change anything from the pipelines built in Parts 1 to better streamline the pipeline built in Part 2? If so, what? If not, is there anything that you can imagine changing in the future?

 I added a function in parsing.py to parse a list of files (len = batch_size) and return a ndarray of shape (batch_size, width, height).

```python
def parse_file_list(filename_list, file_type) -> np.ndarray
```

#### 2. How do you/did you verify that the pipeline was working correctly?

x, y is extracted from indexing pairing.csv file. **test_output/part2.txt** contains indices for each epoch and batch. I verified the results by checking
   * indice covers the entire list
   * x, y shape
   * indices are random samples with len = batch_size from the entire epoch
   
#### 3. Given the pipeline you have built, can you see any deficiencies that you would change if you had more time? If not, can you think of any improvements/enhancements to the pipeline that you could build in?


* Paired file path in **pairing.csv** is generated by **generate_all_pairing(save_comb = False)**, which ensures 1:1 matching. **get_data(ind)** can run smoothly if there is no adverserial attacks of any kind, which includes but not limit to:

        * Manual changes to paths in **pairing.csv** file

        * Manual deletion/edition to dicom and/or mask files
Unfortunately, if there is adverserial attack, since x, y is loaded seperately, it can end up having different number of samples for a batch. It'd be nice to assert x, y has to be same size, raise an exception if there is a mismatching.

* I assumed all image shape are the same. In the production pipeline, there should be a step to rescale/crop the image to the same shape at preprocessing phase.

* constants can be saved as enums instand of variables in config.py

* loaded data should be preprocessed/augmented in dataset.py

```python
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
```

* Masks can be saved as run length encoding instead of .png image, which might save storage space. 

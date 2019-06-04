```bash

contourfiles/
    original_id/
        o-contours/
        i-contours/
            IM-0001-0024-icontour-manual.txt
            IM-0001-0130-icontour-manual.txt
            etc.      
        i-mask/
            24.png
            130.png
            etc.
dicoms/
    patient_id/
        1.dcm
        13.dcm
        etc.


patient_id,original_id
SCD0000101,SC-HF-I-1
SCD0000201,SC-HF-I-2

pairing.csv
dimcon_path, i-mask_path
../dicoms/SCD0000101/24.dcm, ../contourfiles/SC-HF-I-1/i-mask/24.png

```
# GTJSONReaderMuret

It generates an image for each symbol defined in a JSON exported from MuRET. 

Change the paths variables in the code at your will (see below)

Created on Tue Sep  3 08:20:50 2019
Modified on Wed Apr 29 18:13:00 2020 David Rizo. 
  
  Option added (-useregionheight) 
  that instead of extracting the symbol given just its bounding box, it extracts it given its width
  and the height of its container region 

@author: Francisco J. Castellanos

@project name: HISPAMUS

==============================================================================

from enum import Enum

import cv2

from CustomJson import CustomJson
        
**-------- PATHS ---------**
str_pathdir_db = "databases/MURET"
str_pathdir_json = str_pathdir_db + "/JSON"
str_pathdir_src = str_pathdir_db + "/SRC"
str_pathdir_samples = str_pathdir_db + "/SAMPLES"
**-----------------------**

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#==============================================================================
"""
Created on Tue Sep  3 08:20:50 2019

@author: Francisco J. Castellanos
@project name: Hispamus

Modified David Rizo June 4
"""
#==============================================================================
import os
from os.path import isdir

from enum import Enum
import cv2

from CustomJson import CustomJson


str_pathdir_db = "databases/MURET"
str_pathdir_json = str_pathdir_db + "/JSON"
str_pathdir_src = str_pathdir_db + "/SRC"
str_pathdir_samples = str_pathdir_db + "/SAMPLES"

assert os.path.isdir(str_pathdir_json), "JSON folder as downloaded from MuRET"
assert os.path.isdir(str_pathdir_src), "Images folder as downloaded from MuRET"

class PropertyType(Enum):
    PROPERTY_TYPE_PAGES,\
    PROPERTY_TYPE_REGIONS,\
    PROPERTY_TYPE_REGION_TYPE,\
    PROPERTY_TYPE_BOUNDING_BOX,\
    PROPERTY_TYPE_APPROXIMATEX,\
    PROPERTY_TYPE_BBOX_FROM_X,\
    PROPERTY_TYPE_BBOX_TO_X,\
    PROPERTY_TYPE_BBOX_FROM_Y,\
    PROPERTY_TYPE_BBOX_TO_Y,\
    PROPERTY_TYPE_STAFF_REGION,\
    PROPERTY_TYPE_SYMBOLS,\
    PROPERTY_TYPE_AGNOSTIC_SYMBOL,\
    PROPERTY_TYPE_POSITION_IN_STAFF\
    = range(13)

    def __str__(self):
        return property_type_keys[self]

    def __repr__(self):
        return self.__str__()

    
    
property_type_keys = {
                    PropertyType.PROPERTY_TYPE_PAGES:                          "pages",\
                    PropertyType.PROPERTY_TYPE_REGIONS:                        "regions",\
                    PropertyType.PROPERTY_TYPE_REGION_TYPE:                    "type",\
                    PropertyType.PROPERTY_TYPE_BOUNDING_BOX:                   "bounding_box",\
                    PropertyType.PROPERTY_TYPE_APPROXIMATEX:                   "approximateX",\
                    PropertyType.PROPERTY_TYPE_BBOX_FROM_X:                    "fromX",\
                    PropertyType.PROPERTY_TYPE_BBOX_TO_X:                      "toX",\
                    PropertyType.PROPERTY_TYPE_BBOX_FROM_Y:                    "fromY",\
                    PropertyType.PROPERTY_TYPE_BBOX_TO_Y:                      "toY",\
                    PropertyType.PROPERTY_TYPE_STAFF_REGION:                   "staff",\
                    PropertyType.PROPERTY_TYPE_SYMBOLS:                        "symbols",\
                    PropertyType.PROPERTY_TYPE_AGNOSTIC_SYMBOL:                "agnostic_symbol_type",\
                    PropertyType.PROPERTY_TYPE_POSITION_IN_STAFF:              "position_in_staff"\
                    }


def redimImage(img, height, width, interpolation = cv2.INTER_LINEAR):
    img2 = img.copy()
    return cv2.resize(img2,(height,width), interpolation=interpolation)


def getBBoxFromDictionary(dictionary):
    assert (type(dictionary) is dict)
    
    fromX = int(dictionary[str(PropertyType.PROPERTY_TYPE_BBOX_FROM_X)])
    toX = int(dictionary[str(PropertyType.PROPERTY_TYPE_BBOX_TO_X)])
    
    fromY = int(dictionary[str(PropertyType.PROPERTY_TYPE_BBOX_FROM_Y)])
    toY = int(dictionary[str(PropertyType.PROPERTY_TYPE_BBOX_TO_Y)])
    
    coord_p1 = (fromY, fromX)
    coord_p2 = (toY, toX)

    return coord_p1, coord_p2

# =============================================================================
# Music symbol
# =============================================================================
class GTSymbol:
    name_label = ""
    position_in_staff = ""
    coord_p1 = (0,0)
    coord_p2 = (0,0)
    region_coord_p1 = (0,0)
    region_coord_p2 = (0,0)

    def __i_integrity(self):
        assert(type(self.name_label) is str)
        assert(self.name_label != "")
        assert(type(self.position_in_staff) is str)
        assert(self.position_in_staff != "")
        assert(type(self.coord_p1) is tuple)
        assert(type(self.coord_p2) is tuple)
        
    def getNameSymbol(self):
        self.__i_integrity()
        return self.name_label

    def __init__(self):
        self.name_label = ""
        self.position_in_staff = ""
        self.coord_p1 = (0,0)
        self.coord_p2 = (0,0)

    def __str__(self):
        self.__i_integrity()
        return self.name_label + ":" + str(self.position_in_staff) + "(" + str(self.coord_p1) + "->" + str(self.coord_p2) + ")"

        
    def __repr__(self):
        self.__i_integrity()
        return self.__str__()


    def isNameInList(self, list_symbol_labels):
        self.__i_integrity()
        assert (type(list_symbol_labels) is list)
        return self.name_label in list_symbol_labels


    def getSRCSample(self, src_image, sample_shape=None, useRegionHeight=False):
        self.__i_integrity()

        fromX = self.coord_p1[1] # it's correct, first coordinate is Y, second X
        if (useRegionHeight):
            fromY = self.region_coord_p1[0]
        else:
            fromY = self.coord_p1[0]

        toX = self.coord_p2[1]
        if (useRegionHeight):
            toY = self.region_coord_p2[0]
        else:
            toY = self.coord_p2[0]

        if len(src_image.shape) == 3:
            #sample = src_image[self.coord_p1[0]:self.coord_p2[0], self.coord_p1[1]:self.coord_p2[1], :]
            sample = src_image[fromY:toY, fromX:toX, :]
        else:
            sample = src_image[fromY:toY, fromX:toX]

        if (sample_shape is not None):
            sample = redimImage(sample, sample_shape[0], sample_shape[1])
            
        return sample
        

    def getNameSymbol(self):
        self.__i_integrity()
        return self.name_label


    def append_label_without_repetitions(self, list_symbol_labels):
        self.__i_integrity()
        assert (type(list_symbol_labels) is list)
        
        if self.name_label not in list_symbol_labels:
            list_symbol_labels.append(self.name_label)
        



    def fromDictionary_bounding_box(self, dictionary):

        self.coord_p1, self.coord_p2 = getBBoxFromDictionary(dictionary)
        

    def fromDictionary(self, dictionary, region_coord_p1, region_coord_p2, dictionary_next_symbol):
        assert (type(dictionary) is dict)
        
        self.region_coord_p1 = region_coord_p1
        self.region_coord_p2 = region_coord_p2
        
        if str(PropertyType.PROPERTY_TYPE_BOUNDING_BOX) in dictionary:
            info_bbox = dictionary[str(PropertyType.PROPERTY_TYPE_BOUNDING_BOX)]
            self.fromDictionary_bounding_box(info_bbox)
        else:
            assert(str(PropertyType.PROPERTY_TYPE_APPROXIMATEX) in dictionary)
            approximate_x1 = dictionary[str(PropertyType.PROPERTY_TYPE_APPROXIMATEX)]

            if dictionary_next_symbol is not None:

                if str(PropertyType.PROPERTY_TYPE_BOUNDING_BOX) in dictionary_next_symbol:
                    bbox_next_symbol = dictionary_next_symbol[str(PropertyType.PROPERTY_TYPE_BOUNDING_BOX)]
                    next_symbol_coord_p1, _ = getBBoxFromDictionary(bbox_next_symbol)
                    approximate_x2 = next_symbol_coord_p1[1]
                else:
                    approximate_x2 = dictionary_next_symbol[str(PropertyType.PROPERTY_TYPE_APPROXIMATEX)]
            else:
                approximate_x2 = region_coord_p2[1]

            self.coord_p1 = (region_coord_p1[0], approximate_x1)
            self.coord_p2 = (region_coord_p2[0], approximate_x2)
        
        self.name_label = dictionary[str(PropertyType.PROPERTY_TYPE_AGNOSTIC_SYMBOL)]
        self.position_in_staff = dictionary[str(PropertyType.PROPERTY_TYPE_POSITION_IN_STAFF)]
        self.__i_integrity()

    def getPositionInStaff(self):
        self.__i_integrity()
        return self.position_in_staff

    
class GTJSONReaderMuret:

    filename = None    
    symbols = []

    def __i_integrity(self):
        assert(self.filename is not None)
        assert(type(self.filename) is str)
        assert(self.symbols is None or type(self.symbols) is list)

    def __init__(self):
        self.filename = None
        self.symbols = []
        
    
    def hasSymbols(self):
        self.__i_integrity()
        if (self.symbols is None):
            return False
        else:
            assert(len(self.symbols) > 0)
            return True
    

    def getFileName(self):
        self.__i_integrity()
        return self.filename
    

    def _i_list_labels(self):
        self.__i_integrity()
        list_labels = []
        
        for symbol in self.symbols:
            symbol.append_label_without_repetitions(list_labels)
        
        return list_labels

    def _i_list_symbols(self):
        self.__i_integrity()
        return self.symbols
        
    def getListLabels(self):
        return self._i_list_labels()

    def getListSymbols(self, list_possible_name_symbols=None):
        self.__i_integrity()

        list_symbols_considered = []
        for symbol in self.symbols:
            if list_possible_name_symbols is None or symbol.isNameInList(list_possible_name_symbols):
                list_symbols_considered.append(symbol)
                
        return list_symbols_considered
        
    def _i_pages_dict_with_regions(self, info_pages):
        for info_page in info_pages:
            if (str(PropertyType.PROPERTY_TYPE_REGIONS) in info_page):
               return True
           
        return False

    def fromDictionary(self, dictionary):
        assert (type(dictionary) is dict)
        
        self.filename = dictionary["filename"]

        if str(PropertyType.PROPERTY_TYPE_PAGES) not in dictionary:
            return

        info_pages = dictionary[str(PropertyType.PROPERTY_TYPE_PAGES)]
        
        self.symbols = []

        if (self._i_pages_dict_with_regions(info_pages)):
            for info_page in info_pages:    
                if (str(PropertyType.PROPERTY_TYPE_REGIONS) in info_page):
                    list_info_regions = info_page[str(PropertyType.PROPERTY_TYPE_REGIONS)]
                    for info_region in list_info_regions:
                        if info_region[str(PropertyType.PROPERTY_TYPE_REGION_TYPE)] == str(PropertyType.PROPERTY_TYPE_STAFF_REGION):
                            info_region_bbox = info_region[str(PropertyType.PROPERTY_TYPE_BOUNDING_BOX)]
                            region_coord_p1, region_coord_p2 = getBBoxFromDictionary(info_region_bbox)

                            if (str(PropertyType.PROPERTY_TYPE_SYMBOLS) in info_region):
                                list_info_symbols = info_region[str(PropertyType.PROPERTY_TYPE_SYMBOLS)]
                                idx = 0
                                for info_symbol in list_info_symbols:
                                    symbol = GTSymbol()

                                    if idx < (len(list_info_symbols)-1):
                                        info_next_symbol = list_info_symbols[idx+1]
                                    else:
                                        info_next_symbol = None

                                    symbol.fromDictionary(info_symbol, region_coord_p1, region_coord_p2, info_next_symbol)
                                    self.symbols.append(symbol)

                                    idx = idx + 1
            
    def load (self, js):
        assert (isinstance(js, CustomJson))
        
        dictionary = js.dictionary
        
        self.fromDictionary(dictionary)
        self.__i_integrity()
    
    
# =============================================================================
#   PRINT  
# =============================================================================
    
    def __str__(self):
        self.__i_integrity()
        return str(self.symbols)
        

        
    def __repr__(self):
        self.__i_integrity()
        return self.__str__()
    


    
def getListsPathfiles(db_names):

    if (db_names is None):
        list_pathfiles_json = FileManager.listFilesRecursive(str_pathdir_json)
        list_pathfiles_src = FileManager.listFilesRecursive(str_pathdir_src)
    else:
        list_pathfiles_json = []
        list_pathfiles_src =  []

        for db_name in db_names:
            list_pathfile_json_db_name = FileManager.listFilesRecursive(str_pathdir_json + "/" + db_name)
            list_pathfile_src_db_name = FileManager.listFilesRecursive(str_pathdir_src + "/" + db_name)

            assert(len(list_pathfile_json_db_name) == len(list_pathfile_src_db_name))
            
            for idx_pathfile in range(len(list_pathfile_json_db_name)):
                pathfile_json = list_pathfile_json_db_name[idx_pathfile]
                pathfile_src = list_pathfile_src_db_name[idx_pathfile]
                
                pathfile_src_to_json_aux = pathfile_src.replace("/SRC/", "/JSON/") + ".json"
                assert(pathfile_src_to_json_aux == pathfile_json)
                list_pathfiles_json.append(pathfile_json)
                list_pathfiles_src.append(pathfile_src)

    return list_pathfiles_src, list_pathfiles_json

if __name__ == "__main__":

    import argparse
    from FileManager import FileManager

    KEY_LABELS = "labels"
    KEY_DBNAME = "dbname"

    parser = argparse.ArgumentParser()
    parser.add_argument('--l', dest=KEY_LABELS, action="append", help='Name of the symbol label to filter extracted samples', required=False, type=str)
    parser.add_argument('--db', dest=KEY_DBNAME, action="append", help='Path of data', required=False, type=str)
    parser.add_argument('--rh', help='Use region/staff the height instead of the height of the symbol bounding box', required=False, action="store_true");

    args = parser.parse_args()
    parsed_args = vars(args)

    if KEY_LABELS in parsed_args or len(parsed_args[KEY_LABELS]) == 0:
        labels = parsed_args[KEY_LABELS]
    else:
        labels = None

    if KEY_DBNAME in parsed_args or len(parsed_args[KEY_DBNAME]) == 0:
        db_names = parsed_args[KEY_DBNAME]
    else:
        db_names = None

    useRegionHeight = args.rh
    if (useRegionHeight):
        print("Using region height to extract symbols instead of the one in the symbols bounding box")

    FileManager.deleteFolder(str_pathdir_samples)
    list_dirs_src, list_dirs_json = getListsPathfiles(db_names)

    #num_src_files = len (list_dirs_src)
    num_json_files = len (list_dirs_json)

    #for idx in range (num_src_files): drizo: Cannot work using a numerical index because there may be a different number files in the images and json folders
    for i in range (num_json_files):
        #str_path_file_src = list_dirs_src[idx]
        str_path_file_json = list_dirs_json[i]
        #print(">>> ", str_path_file_json)
        print(".", end=' ', flush=True)

        # From the JSON file name get the equivalent JPG image path
        image_name = os.path.basename(str_path_file_json).replace('.json', "")
        image_path = os.path.dirname(str_path_file_json).replace('JSON', "SRC") + "/masters"
        str_path_file_src = image_path + "/" + image_name
        #print("---> ", str_path_file_src)
        assert os.path.isfile(str_path_file_src), "JPG for JSON file " + str_path_file_json

        #str_path_file_gt_out = str_path_file_src.replace("/SRC/", "/SAMPLES/")
        str_path_file_gt_out = str_path_file_json.replace("databases/MURET/JSON", "SAMPLES")
        #str_path_file_src = str_path_file_json.replace("databases/MURET/JSON", "databases/MURET/SRC/")

        src_image = FileManager.loadImage(str_path_file_src, True)

        js = CustomJson()
        js.loadJson(str_path_file_json)

        gt_symbols = GTJSONReaderMuret()
        gt_symbols.load(js)

        #print ("\n")
        #print ('-'*80)
        #print (gt_symbols.getFileName())
        #print ('*'*80)
        #print (*gt_symbols._i_list_symbols(),sep='\n')
        #print ('-'*80)

        list_symbols = gt_symbols.getListSymbols(list_possible_name_symbols=labels)

        idx = 1
        for symbol in list_symbols:
            symbol_src = symbol.getSRCSample(src_image=src_image, sample_shape=None, useRegionHeight=useRegionHeight)

            name_symbol = symbol.getNameSymbol().replace(".", "_")
            [pathdir, filename_with_ext] = FileManager.separateDirectoryAndFilename(str_path_file_gt_out)
            filename = FileManager.nameOfFile(filename_with_ext)
            str_path_file_gt_out_symbol = pathdir + "/" + filename + "/" + name_symbol + "/"+ str(idx) + ".png"
            FileManager.saveImageFullPath(symbol_src, str_path_file_gt_out_symbol)
            idx = idx + 1




    print ("Ended")

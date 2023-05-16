# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 15:18:19 2022

@author: Jari.Perakyla
"""

import pandas as pd

def read_input_file(file_name, file_type):

    # .csv file with 'key' and 'input1' colunms. If other columns are present,
    # they are ignored.
    if file_type == "ner_key_input1_csv":
        texts = pd.read_csv(
            file_name,
            escapechar="\\",
            #index_col=False,
            dtype={"key": str, "input1": str}
        )
        
        if not "input1" in texts.columns:
            print('Error: NER input file is expected to have a column named "input1" with documents to be pre-annotated.')
            texts = None

    # Result .csv file from Annotation Platform with columns 'key' and
    # 'output1' or 'input1' present. We keep the same key as in result file.
    #  Other columns are ignored.
    elif file_type == "pii_content_csv":
        texts = pd.read_csv(file_name, index_col=False, escapechar="\\")
        
        if not ("output1" in texts.columns or "input1" in texts.columns):
            print('Error: PII input file is expected to have a column named "input1" or "output1" with documents to be pre-annotated.')
            texts = None
            
        if "output1" in texts.columns:
            texts = texts.rename(columns={"output1": "input1"})
            
        texts = texts[texts["input1"].notnull()]
        
    else:
        print("Error: file_type not recognized.")
        texts = None

    if texts is not None:
        texts = texts[["key", "input1"]]
        
    return texts

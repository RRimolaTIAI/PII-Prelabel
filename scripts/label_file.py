# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 13:52:23 2022

@author: Jari.Perakyla
"""

import json
import pandas as pd
import sys


def extract_labels(result_file_name, project_type, expected_labels):

    with open(result_file_name, encoding='utf-8') as f:
        j = json.load(f)

    label_custom_id_error = False
    labels = pd.DataFrame(
        columns=['label_custom_id', 'label_id', 'label_text'])
    for item in j:
        outputs = item['outputs']
        if outputs:
            for o in outputs:
                annotations = o['annotations']
                if len(annotations) > 0:
                    for annotation in annotations:
                        if not annotation['label_custom_id'] and annotation['label_text']:
                            if not label_custom_id_error:
                                print('    Warning: Custom Key (label_custom_id) is empty, using Class Name (label_text) as class ID. \n             It is recommended to use standardized Custome Key and localized Class Name.')
                                label_custom_id_error = True
                            annotation['label_custom_id'] = annotation['label_text']
                        elif annotation['label_custom_id'] is None:
                            exit('label_custom_id is empty. ')
                        labels = pd.concat([labels,
                                            pd.DataFrame({
                                                'label_custom_id': [annotation['label_custom_id']],
                                                'label_id': [annotation['label_id']],
                                                'label_text': [annotation['label_text']]})],
                                           ignore_index=True, axis=0)

    # Keep only unique labels
    labels_unique = labels.drop_duplicates(subset = ['label_custom_id'])

    # Check that there is information for all expected labels
    label_custom_ids = labels_unique['label_custom_id'].to_list()
    if not all(item in label_custom_ids for item in expected_labels):
        print('    Warning: Label file does not contain all the expected labels - are some labels possibly missing?')
        print('             Expected labels:', expected_labels)
        print('             Detected labels:', label_custom_ids)
        
    # if project_type == 'ner':
    #     labels_unique.set_index('label_text', drop=False, inplace=True)
    # elif project_type == 'pii':
    #     labels_unique.set_index('label_custom_id', drop=False, inplace=True)
    # else:
    #     sys.exit('Cannot recognize project_type:', project_type)

    labels_unique.set_index('label_custom_id', drop=False, inplace=True)
    labels_unique.to_csv('labels.csv')

    return(labels_unique)

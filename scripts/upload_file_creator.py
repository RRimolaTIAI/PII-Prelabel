# -*- coding: utf-8 -*-
"""
This module receives a list of Spacy documents and creates a 
telusinternational.ai NER project compatible upload file for
the specific NER projects.

Created on Wed Apr 13 10:13:40 2022

@author: Jari.Perakyla
"""

import uuid
import json
import time

from scripts.language_configuration import align_entity_label


# Create Annotation Platform annotations and save in upload file
def create_upload_file(pre_annotations, upload_file_name, labels, project_type):

    # To avoid key conflicts, use current numeric UTC time as a starting value for a key
    key_base = int(time.time())

    upload_items = []
    for idx, doc in enumerate(pre_annotations["doc"]):
        upload_items.append(
            create_upload_item(doc, "text" + str(key_base + idx), labels, project_type)
        )
    with open(upload_file_name, "w") as outfile:
        json.dump(upload_items, outfile)


# Construct annotations for a single item
def create_upload_item(doc, key, labels, project_type):

    annotations = []

    for ent in doc.ents:
        ent.label_ = align_entity_label(ent.label_, project_type)
        annotations.append(
            {
                "comment": None,
                "quote": ent.text,
                "start": ent.start_char,
                "end": ent.end_char,
                "label_custom_id": ent.label_,
                #"label_custom_id": align_entity_label(ent.label_, project_type),
                "label_id": labels.at[ent.label_, "label_id"],
                "label_text": labels.at[ent.label_, "label_text"],
                "uuid": str(uuid.uuid1()),
            }
        )

    # Construct item
    item = {
        "key": key,
        "inputs": [{"text": doc.text}],
        "outputs": [{"annotations": annotations}],
    }

    return item

# -*- coding: utf-8 -*-
"""
Languge configuration.

* Lists spaCy and Oracle NER (oner) entity types for 
  each project type (ner/pii) and each language. 

  For spaCy types use actual spaCy entity names, 
  for Oracle NER use Oracle entity names.

* Utility functions for handling entities

Entity names used by Oracle:
PII : DATE_TIME, PERSON; AGE, ADDRESS; EMAIL (in square barackets)
NER : DATE, TIME, DATETIME, DURATION, INTERVAL, RECURRING
      CURRENCY, PERCENTAGE, NUMBER, DIMENSION, AGE, TEMPERATURE, QUANTITY,
      PERSON, GPE, NON_GPE, FACILITY, ORGANIZATION, NORP, PRODUCT, EVENT
                                 
More Entity details in https://docs.google.com/spreadsheets/d/1ra1LThT06k1ASod3HNqO4Xh_TXrZQps02zNRKn__HF0/edit#gid=0
    
Created on Tue Oct 11 16:58:59 2022
@author: jari.perakyla

"""

import pandas as pd
import sys

language_conf = {
    # Language models
    "language_models": {
        "english": {
            "spacy_model": "en_core_web_trf",
            "oner_model": "en_oner_trf_20220830",
        },
        "spanish": {
            "spacy_model": "es_core_news_lg",
            "oner_model": "es_oner_t2v_20220616",
        },
        "portuguese": {"spacy_model": "pt_core_news_lg", "oner_model": ""},
        "dutch": {"spacy_model": "nl_core_news_lg", "oner_model": ""},
        "german": {"spacy_model": "de_core_news_lg", "oner_model": ""},
        "french": {"spacy_model": "fr_core_news_lg", "oner_model": ""},
    },
    # NER
    "ner": {
        # English
        "english": {
            "spacy_entities": [
                "QUANTITY",
                "PERCENT",
                "MONEY",
                "DATE",
                "TIME",
                "PERSON",
                "GPE",
                "FAC",
                "LOC",
                "ORG",
                "PRODUCT",
            ],
            "oner_entities": ["AGE", "TEMPERATURE"],
        },
        # Spanish
        "spanish": {
            "spacy_entities": ["PER", "LOC", "ORG"],
            "oner_entities": [
                "AGE",
                "TEMPERATURE",
                "DIMENSION",
                "DATE",
                "TIME",
                "CURRENCY",
                "PERCENTAGE",
                "GPE",
                "FACILITY",
                "PRODUCT"
            ],
        },
        "portuguese": {
            "spacy_entities": ["PER", "LOC", "ORG"],
            "oner_entities": [],
        },
        "dutch": {
            "spacy_entities": [
                "DATE",
                "FAC",
                "GPE",
                "LOC",
                "MONEY",
                "ORG",
                "PERCENT",
                "PERSON",
                "QUANTITY",
                "TIME",
                "PRODUCT"
            ],
            "oner_entities": [],
        },
        "german": {
            "spacy_entities": ["PER", "LOC", "ORG"],
            "oner_entities": [],
        },
        "french": {
            "spacy_entities": ["PER", "ORG", "LOC"],
            "oner_entities": [],
        },
    },
    # PII
    "pii": {
        
        "english": {
            "spacy_entities": [
                "DATE",
                "TIME",
                "PERSON",
                "EMAIL"
            ],
            "oner_entities": ["AGE", "ADDRESS"],
        },
        
        "spanish": {
            "spacy_entities": [
                "DATE",
                "TIME",
                "PER",
                "EMAIL"
            ],
            "oner_entities": ["AGE", "ADDRESS"],
        },
        
        "portuguese": {
            "spacy_entities": ["PER", "EMAIL"],
            "oner_entities": [],
        },
        "dutch": {
            "spacy_entities": ["TIME", "DATE", "PERSON", "EMAIL"],
            "oner_entities": [],
        },
        "french": {
            "spacy_entities": ["PER", "EMAIL"],
            "oner_entities": [],
        },
        "german": {
            "spacy_entities": ["PER", "EMAIL"],
            "oner_entities": [],
        },
    }
}



entity_map = pd.read_csv(
    "entity_mapping.csv", sep="\\s+", engine="python", dtype="string"
)


def align_entity_label(label, project_type):


    oracle_label = entity_map[
        (entity_map["type"] == project_type)
        & (entity_map["spacy_entity"] == label)
    ]["oracle_entity"].tolist()
    if len(oracle_label) == 0:
        # Return original label if there is no match
        oracle_label = label
    elif len(oracle_label) == 1:
        oracle_label = oracle_label[0]
    else:
        print(project_type, label)
        print(oracle_label)
        print(len(oracle_label))
        sys.exit("Multiple matches")

    # PII projects have square brackets in the labels
    if project_type == "pii":
        oracle_label = f"[{oracle_label}]"

    return oracle_label

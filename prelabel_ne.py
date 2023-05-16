# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 10:44:12 2022

@author: Jari.Perakyla
"""

import sys

# import argparse

from os.path import exists
from time import time
from gooey import Gooey, GooeyParser

from scripts.ner import ner
from scripts.input_file_reader import read_input_file
from scripts.upload_file_creator import create_upload_file
from scripts.label_file import extract_labels

from scripts.language_configuration import language_conf


def filter_entities(docs, ents_to_keep, project_type):

    for doc in docs:
        filtered_ents = []
        for ent in doc.ents:
            if ent.label_ in ents_to_keep:
                # ent.label_ = align_entity_label(ent.label_, project_type)
                filtered_ents.append(ent)
        doc.ents = filtered_ents

    return docs


def process_ner(
    input_file_name, label_file_name, output_file_name, project_type, language
):

    # NER projects
    # TODO: ... see GSheet

    print("\nOracle NER/PII Pre-Labeling\n=============================\n")
    print("Language:\t", language)
    print("Project type:\t", project_type)
    print("Input file:\t", input_file_name)
    print("Label file:\t", label_file_name)
    print("Output file:\t", output_file_name)

    if not exists(input_file_name):
        print(f'Error: Cannot find input file "{input_file_name}".')
        sys.exit(0)

    if not exists(label_file_name):
        print(f'Error: Cannot find label file "{label_file_name}".')
        sys.exit(0)

    if not project_type in ["ner", "pii"]:
        print(
            f'Error: Project type "{project_type}" not recognized. Supported project types are "ner" and "pii"'
        )
        sys.exit(0)

    if not language in list(language_conf["language_models"].keys()):
        print(
            f'Error: Languge {language} not recognized. Supported languages are {list(language_conf["language_models"].keys())}.'
        )
        sys.exit(0)

    # Load language model and texts to be annotated
    print("\nLoading language model ...")
    ner_processor = ner(language)
    print("  Pipeline:\t", ner_processor.component_names())

    # Entities to recognize
    if project_type == "ner":

        input_file_type = "ner_key_input1_csv"
        ents_to_keep = (
            language_conf["ner"][language]["spacy_entities"]
            + language_conf["ner"][language]["oner_entities"]
        )

    elif project_type == "pii":

        input_file_type = "pii_content_csv"
        ents_to_keep = (
            language_conf["pii"][language]["spacy_entities"]
            + language_conf["pii"][language]["oner_entities"]
        )

    else:
        sys.exit("Unknown project type (" + project_type + ")")

    # Convert Spacy labels to project labels. Keep only distinct items.
    #expected_labels = [align_entity_label(spacy_ent, project_type) for spacy_ent in ents_to_keep]
    expected_labels = ents_to_keep
    expected_labels = list(set(expected_labels))
    print("  Entity types:\t", expected_labels, "\n")

    print("Loading input file ...")
    documents = read_input_file(input_file_name, input_file_type)

    # Extract label information from label file (AP result file with example tags)
    print("Extracting labels ...")
    labels = extract_labels(label_file_name, project_type, expected_labels)

    # Tag entities with spacy pipeline tags
    documents = ner_processor.process(documents)

    print("\nGenerating upload file ...")

    # Keep only tags of interest & Create upload file
    documents["doc"] = filter_entities(
        documents["doc"], ents_to_keep, project_type
    )
    create_upload_file(documents, output_file_name, labels, project_type)

    print("\nPre-labeling completed.")


@Gooey(default_size=(800, 800),
       use_cmd_args = True,
       clear_before_run = True,
       show_success_modal = False)
def main():

    start_time = time()

    # parser = argparse.ArgumentParser(description='Oracle NER pre-labeller.')
    parser = GooeyParser(
        description='Oracle NER pre-labeller for "NER" and "PII" projects.'
    )
    parser.add_argument(
        "input_file", help="Name of the input file.", widget="FileChooser"
    )
    parser.add_argument(
        "label_file", help="Name of the label file.", widget="FileChooser"
    )
    parser.add_argument(
        "-upload_file",
        default="upload.json",
        widget="FileChooser",
        help='Name of the uplaod JSON file. Default = "upload.json"',
    )
    parser.add_argument(
        "-project_type",
        choices=["ner", "pii"],
        default="ner",
        widget="Dropdown",
        help='Project type, "pii" or "ner". Default = "ner".',
    )
    parser.add_argument(
        "-language",
        choices=list(language_conf["language_models"].keys()),
        default="english",
        widget="Dropdown",
        help=f'Language, {list(language_conf["language_models"].keys())}. Default = "english".',
    )
    args = parser.parse_args()

    process_ner(
        args.input_file,
        args.label_file,
        args.upload_file,
        args.project_type,
        args.language,
    )

    execution_time = divmod((time() - start_time), 60)
    print(
        f"Execution time: {int(round(execution_time[0], 0))}:{int(round(execution_time[1], 0))}."
    )


if __name__ == "__main__":
    main()

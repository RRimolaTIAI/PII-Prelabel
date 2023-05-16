# PII-Prelabel
prelabel_ne.py 
==============
version 0.2.1
date: 2022-12-05


Change history
==============
0.2.1
-----
* Added PII Spanish, which was missing in the previous version(s)
* Changed PII project so that it accepts also NER input file format (key, input1)
* NOTE: there are still issues in oner entity types for English due to error in training.

0.2.0
-----
* Modified language configuration architecture for easier addition of new languages (language_configuration.py) 
* Added new languages: nl, pt, de, fr
* Added graphical user interface (GUI)
* Refactored test cases
* NOTE: there are still issues in oner entity types for English due to error in training.

0.1.6
-----
* Added "PERCENTAGE" and "DIMENSION" tags for Spanish. Training data had previously
  percentage tag in Spanish ("PORCENTAJE") and a spelling mistake in 
  "DIMENSION" tag with additional "S" at the end ("DIMENSIONS").


Prerequisites:
==============
* Python has been installed and can be found in path
* Poetry has been installed and can be found in path


Installation:
=============
1. Extract the package to a folder of your choice.
2. Double click "setup.bat". Setup.bat will 
	a) open windows command prompt (CMD),
	b) create a poetry environment, 
	c) install python dependencies in the newly created environment, 
	d) download Spacy language models and 
	e) finally run the command "poetry run python prelabel_ne.py", which should show the standard help text 
       indicating successful installation (+ a note about missing input file and label file). 
	   
There will be lot of text in the sceen during the installation and the installation script will downloaded 
base language models from the net. 


Usage: 
======
    poetry run python prelabel_ne.py <input_text_file> <label_file> 
	                                 [-project_type <ner/pii; default = "ner"> 
									  -language <english/spanish; default="english"> 
									  -upload_file <upload_file_name; default = "upload.json">]
									  --ignore-gooey
									  
	OR just
	
	poetry run python prelabel_ne.py

The command does NER labeling and saves results in upload.json (default name) file to be uploaded into AP project. 
In default more GUI is always launched. If GUI is not desired, use --ignore-gooey command line parameter.


Supported Languages and Entity Types
====================================

English		QUANTITY, PERCENTAGE (PERCENT), MONEY, DATE, TIME, PERSON, 
            GPE, FAC, NON_GPE (LOC), ORGANIZATION (ORG), NORP, PRODUCT (en_core_web_lg) 
            EMAIL, AGE, ADDRESS, TEMPERATURE (en_oner_t2v_20220530)

Spanish		NON_GPE (LOC), ORGANIZATION (ORG), PERSON (PER) (es_core_news_lg)
            PRODUCT, DATE, GPE, FACILITY, CURRENCY, TIME, AGE, TEMPERATURE (es_oner_t2v_20220601)
			
Dutch		FAC, DATE, TIME, GPE, PERCENT, NON_GPE (LOC), PERSON, QUANTITY, ORGANIZATION (ORG), PRODUCT, MONEY, EMAIL (nl_core_news_lg)

German		PERSON (PER), NON_GPE (LOC), ORGANIZATION (ORG), EMAIL (de_core_news_lg)

French		PERSON (PER), NON_GPE (LOC), ORGANIZATION (ORG), EMAIL (fr_core_news_lg)

Potuguese	PERSON (PER), NON_GPE (LOC), ORGANIZATION (ORG), EMAIL (pt_core_news_lg)


# -*- coding: utf-8 -*-
"""
NER
"""

import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span
from spacy.language import Language

import warnings
from tqdm.contrib.concurrent import thread_map
from tqdm import tqdm
import psutil
from scripts.language_configuration import language_conf

# We want to suppress "UserWarning: User provided device_type of 'cuda', but CUDA is not available. Disabling"
warnings.filterwarnings("ignore", category=UserWarning)

# 
@Language.factory("email_matcher")
def create_email_matcher(nlp, name):
    return EmailMatcher(nlp.vocab)


class EmailMatcher:
    
    def __init__(self, vocab):
        pattern_email = [{'LIKE_EMAIL': True}]
        self.matcher = Matcher(vocab)
        self.matcher.add("EMAIL", [pattern_email])

    def __call__(self, doc):
        # This method is invoked when the component is called on a Doc
        matches = self.matcher(doc)
        for match_id, start, end in matches:
            entity = Span(doc, start, end, label="EMAIL")
            try:
                doc.ents += (entity,) # Needs to be tupple
            except ValueError as e:
                pass        
        return(doc)

class ner:
    
    def __init__(self, language):

        # Load base language model and Oracle language model.
        base_lang_mod_name = language_conf["language_models"][language][
            "spacy_model"
        ]
        oracle_lang_mod_name = (
            "language_models/"
            + language_conf["language_models"][language]["oner_model"]
        )
        print("  Base model:\t", base_lang_mod_name)
        if oracle_lang_mod_name != "language_models/":
            print("  Oracle model:\t", oracle_lang_mod_name)
        else:
            print("  Oracle model:\t (not defined)")

        self.nlp = spacy.load(base_lang_mod_name)
        if oracle_lang_mod_name != "language_models/":
            self.nlp_oner = spacy.load(oracle_lang_mod_name)
        else:
            self.nlp_oner = None

        # Create matcher to dectet email addresses
        #self.email_matcher = Matcher(self.nlp.vocab)
        #pattern_email = [{'LIKE_EMAIL': True}]
        #self.email_matcher.add("email", [pattern_email], on_match = self._add_email_ent)

        # Combine email matcher, base- and oracle ner components
        self.nlp.add_pipe("email_matcher", before="ner")
        if oracle_lang_mod_name != "language_models/":
            self.nlp.add_pipe("oner", source=self.nlp_oner, before="ner")

        # Remove processing pipeline components not needed to speed up processing
        components_to_remove = list(self.nlp.component_names)
        if "transformer" in components_to_remove:
            components_to_remove.remove(
                "transformer"
            )  # do not remove transformer
        if "tok2vec" in components_to_remove:
            components_to_remove.remove("tok2vec")  # do not remove tok2vec            
        if "ner" in components_to_remove:
            components_to_remove.remove("ner")  # do not remove ner
        if "oner" in components_to_remove:
            components_to_remove.remove("oner")  # do not remove email_matcher
        if "email_matcher" in components_to_remove:
            components_to_remove.remove("email_matcher")  # do not remove oner

        for component in components_to_remove:
            self.nlp.remove_pipe(component)

    def _add_email_ent(self, matcher, doc, i, matches):
        # Get the current match and create tuple of entity label, start and end.
        # Append entity to the doc's entity. (Don't overwrite doc.ents!)
        match_id, start, end = matches[i]
        entity = Span(doc, start, end, label="EMAIL")
        try:
            doc.ents += (entity,) # Needs to be tupple
        except ValueError as e:
            #print("\nValueError while adding email address: ", entity, "\n", e)
            #for ent in doc.ents:
            #    print(ent.text, ent.start_char, ent.end_char, ent.label_)
            pass

    # def _tag_email_addresses(self, doc):
        
    #     self.email_matcher(doc)
    #     #for ent in doc.ents:
    #     #    if(ent.label_ == 'EMAIL'):
    #     #        print(ent.text, ent.start_char, ent.end_char, ent.label_)
        
        return(doc)

    def process(self, documents):

        tqdm.pandas()

        # tqdm & Gooey: https://gist.github.com/GenevieveBuckley/02d6e8299b2210cdd80336a5b44a42c5
        # https://github.com/JAckMcKew/Gooey
        # Still not working ...
        documents["doc"] = thread_map(
            self.nlp,
            documents["input1"],
            max_workers=psutil.cpu_count(logical=False) - 1,
            chunksize=512
        )
        
        #documents["doc"] = documents["doc"].progress_map(lambda x: self._tag_email_addresses(x))

        return documents

    def component_names(self):
        return self.nlp.component_names



        
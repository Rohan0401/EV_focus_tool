from typing import Dict, List
import spacy
from spacy.language import Language

class SpacyExtractor:
    """class SpacyExtractor encapsulate logic to pipe Records with an id and text body
    through a spacy model and return entities seperated by Entity Type
    """

    def __init__(
        self, nlp : Language, input_id_col : str = "id" ,input_text_col : str = "text"

    ): 
    """Initialize the SpacyExtractor pipeline. 
    nlp(spacy.langauge.Language) : pre-loaded spacy language model langauge model
    input_text_col (str) : property on each document to run the model om 
    input_id_col (str) : property on each document to correlate with request"""
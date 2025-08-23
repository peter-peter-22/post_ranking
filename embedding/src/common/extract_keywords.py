from keybert import KeyBERT
from src.common.generate_embeddings import Vector,model
from typing import List
import numpy as np

kw_model = KeyBERT(model=model)

def extract_keywords(texts:List[str], embeddings:List[Vector])->List[str]:
    """Extract keywords from the given texts using keybert model"""
    # Prepare the embeddings. Keybert only accepts numpy arrays. 
    np_embeddings=[np.array(vector) for vector in embeddings]
    # Extract top keywords and their scores
    keyword_scores=kw_model.extract_keywords(
        texts,
        stop_words='english',
        top_n=10,
        keyphrase_ngram_range=(1, 2),
        doc_embeddings=np_embeddings
    )
    # Make sure that keyword_scores is a list.
    if len(embeddings)==1:
        keyword_scores=[keyword_scores]

    # Return only the keywords
    return [[keywords for keywords,_ in keyword_scores_of_text] for keyword_scores_of_text in keyword_scores]
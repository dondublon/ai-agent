from os import getenv

import numpy as np  
from text_prcessor import TextProcessor
import joblib
from rank_bm25 import BM25Okapi
from logging_config import logger   
class TextProcessorBM25(TextProcessor):
    def __init__(self,*,text="",file="",threshold=1):
        super().__init__(text=text, file=file)
        self.threshold = threshold
    def create_model(self,text):
        text_arr = text.split('.')
        self.cleaned_text_arr = [res for sentence in text_arr if (res := sentence.strip())]
        tokenized_corpus = [doc.split() for doc in self.cleaned_text_arr]
        self.bm25 = BM25Okapi(tokenized_corpus)
        logger.debug(f"Created BM25 model with {len(self.cleaned_text_arr)} sentences.")    
    def load_model(self,file):   
        data = joblib.load(file)
        self.cleaned_text_arr = data['cleaned_text_arr']
        self.bm25 = data['bm25']
        logger.debug(f"Loaded BM25 model from {file} with {len(self.cleaned_text_arr)} sentences.")
    def save_model(self,file):
        data = {
            'cleaned_text_arr': self.cleaned_text_arr,
            'bm25': self.bm25
        }
        joblib.dump(data, file) 
        logger.debug(f"Saved BM25 model to {file} with {len(self.cleaned_text_arr)} sentences.")
    def get_answer(self, query):  
        tokenized_query = query.split(" ")
        doc_scores = np.array(self.bm25.get_scores(tokenized_query))
        sorted_indices = np.argsort(doc_scores)[::-1]
        n_scores_for_logging = min(10, len(doc_scores))
        logger.debug(f"BM25 scores for top {n_scores_for_logging} are: {doc_scores[sorted_indices[:n_scores_for_logging]]}")
        sentenceInd = sorted_indices[0]
        return self.cleaned_text_arr[sentenceInd] if doc_scores[sentenceInd] >= self.threshold else None
    @staticmethod
    def createTextProcessor():
        '''Factory method to create a TextProcessorBM25 instance based on environment variable.
        Expects BM25_MODEL_FILE environment variable to be set for loading the model.
        '''
        fileName = getenv("BM25_MODEL_FILE")
        if not fileName:
            raise ValueError("BM25_MODEL_FILE environment variable is not set.")
        textProcessor = TextProcessorBM25(file=fileName, threshold=float(getenv("BM25_THRESHOLD", 1)))
        return textProcessor
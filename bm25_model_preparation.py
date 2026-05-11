from pathlib import Path

from config import MODEL_FILE_NAME, TRAVEL_AGENCY_POLICY_FILE
from text_processor_bm25 import TextProcessorBM25
def main():
    text = TRAVEL_AGENCY_POLICY_FILE.read_text()
    textProcessor = TextProcessorBM25(text=text)
    textProcessor.save_model(MODEL_FILE_NAME)

if __name__ == "__main__":
    main()

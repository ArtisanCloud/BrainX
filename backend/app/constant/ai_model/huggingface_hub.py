from enum import Enum


class HuggingFaceHubModelID(Enum):
    SENTENCE_TRANSFORMERS = "sentence-transformers"
    SHIBING624_TEXT2VEC_BASE_CHINESE = "shibing624_text2vec-base-chinese"
    UNIVERSAL_SENTENCE_ENCODER = "universal-sentence-encoder"
    BERT = "bert"
    BERT_BASE_UNCASED = "bert-base-uncased"
    GPT2 = "gpt2"
    ROBERTA = "roberta"
    BLOOM = "bloom"
    T5 = "t5"
    DISTILBERT = "distilbert"
    ALBERT = "albert"
    XLNET = "xlnet"
    FLAIR = "flair"
    DEBERTA = "deberta"
    GPT_J = "gpt-j"
    GPT_NEO = "gpt-neo"

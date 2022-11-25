from typing import List
from utils import normalize
import kenlm


def pp(log_score, length):
    return 10.0 ** (-log_score / length)


def preplexity(docs: List[str], model_path: str) -> float:
    model = kenlm.Model(model_path)
    doc_log_score, doc_length = 0, 0

    for doc in docs:
        line = doc
        line = normalize(line, case=False, numbers=False, punct=1, code_breaking=1)
        line = tokenizer_char(line)
        log_score = model.score(line, bos=True, eos=True)
        length = len(line.split()) + 1

        # log space
        doc_log_score += log_score
        doc_length += length

    return round(pp(doc_log_score, doc_length), 1)


print(preplexity(docs=["امیر"], model_path='./models/fa_model.arpa'))

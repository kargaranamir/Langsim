import os

lmplz_add = "../kenlm/build/bin/lmplz"
char_add = "../oscar-small/data_char_case_numbers_punct1_code1"
model_add = "./models"
ngram_param = "7"
lang = "fa"

command = ' '.join([f"{lmplz_add}", f"-o {ngram_param}", f"<{char_add}/{lang}_char_train", f">{model_add}/{lang}_model.arpa"])

os.system(command)

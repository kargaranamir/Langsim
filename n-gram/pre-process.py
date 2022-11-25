from utils import split_file2char
from tqdm import tqdm
import glob

lang_paths = glob.glob("../oscar-small/data/*")
lang_paths = ["../oscar-small/data/fa"]

for path in tqdm(lang_paths):
    print(path)
    with open(path) as f:
        data = [line.rstrip('\n') for line in f]
        data = [d for d in data if len(d) != 0]

    path_output = path.replace('data', 'data_char_case_numbers_punct1_code1')
    split_file2char(data, path_output)

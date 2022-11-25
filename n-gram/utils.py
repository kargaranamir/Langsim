import re
from typing import Dict, List
import random
import regex
import unicodedata
from unidecode import unidecode
from emoji import UNICODE_EMOJI

unicode_punct: Dict[str, str] = {
    "，": ",",
    "。": ".",
    "、": ",",
    "„": '"',
    "”": '"',
    "“": '"',
    "«": '"',
    "»": '"',
    "」": '"',
    "「": '"',
    "《": '"',
    "》": '"',
    "´": "'",
    "∶": ":",
    "：": ":",
    "？": "?",
    "！": "!",
    "（": "(",
    "）": ")",
    "；": ";",
    "–": "-",
    "—": " - ",
    "．": ". ",
    "～": "~",
    "’": "'",
    "…": "...",
    "━": "-",
    "〈": "<",
    "〉": ">",
    "【": "[",
    "】": "]",
    "％": "%",
    "►": "-",
}

digit_re: re.Pattern = re.compile(r"\d")

non_printing_chars_re = re.compile(
    f"[{''.join(map(chr, list(range(0, 32)) + list(range(127, 160))))}]"
)

unicode_punct_re = re.compile(f"[{''.join(unicode_punct.keys())}]")


def replace_unicode_punct(text: str) -> str:
    return "".join(unicode_punct.get(c, c) for c in text)


def remove_unicode_punct(text: str) -> str:
    """More aggressive version of replace_unicode_punct but also faster."""
    return unicode_punct_re.sub("", text)


def remove_non_printing_char(text: str) -> str:
    return non_printing_chars_re.sub("", text)


def remove_accent_chars_regex(x: str):
    return regex.sub(r'\p{Mn}', '', unicodedata.normalize('NFKD', x))


def remove_substrings(text, to_replace, replace_with=""):
    if isinstance(to_replace, str):
        to_replace = [to_replace]

    result = text
    for x in to_replace:
        result = result.replace(x, replace_with)
    return result


def remove_emoji(text):
    return remove_substrings(text, UNICODE_EMOJI["en"])


def normalize(line, case: bool = True, numbers: bool = True, punct: int = 1, code_breaking: int = 1) -> str:

    # remove emoji
    line = remove_emoji(line)

    # strip
    line = line.strip()

    if code_breaking == 1:
        # remove accent
        line = remove_accent_chars_regex(line)
    elif code_breaking == 2:
        # transliteration
        line = unidecode(line)
    elif code_breaking == 3:
        # first remove accents then transliteration. transliteration try to translate accents as well, e.g., in arabic.
        line = remove_accent_chars_regex(line)
        line = unidecode(line)

    if case:
        line = line.lower()

    if numbers:
        line = digit_re.sub("0", line)

    if punct == 1:
        # 1 for replace
        line = replace_unicode_punct(line)
    elif punct == 2:
        # 2 for remove
        line = remove_unicode_punct(line)

    line = remove_non_printing_char(line)
    return line


# convert setntence to characters
def tokenizer_char(sentence: str) -> str:
    if sentence == "":
        return ""
    elif sentence.strip() == "":
        return "<sp>"
    else:
        s = ' '.join(list(sentence))
        # replace space with <space> token
        s = re.sub(r"\s\s+", ' <sp> ', s)
        return s.strip()


# convert file to character lines
def file2char(data: List[str], output_path: str) -> None:
    output_data = []
    # pre-process
    for line in data:
        s = line
        s = normalize(s, case=True, numbers=True, punct=1, code_breaking=1)
        s = tokenizer_char(s)
        output_data.append(s + '\n')

    # write file
    with open(output_path, "w") as fh:
        fh.write(''.join(output_data))


def split_file2char(data: List[str], output_path: str) -> None:
    # shuffle data
    random.shuffle(data)

    train_size = int(0.9 * len(data))
    train_data = data[:train_size]
    test_data = data[train_size:]

    # write train
    file2char(data=train_data, output_path=output_path + '_char_train')

    # write test file
    with open(output_path + '_test', "w") as fh:
        fh.write('\n'.join(test_data))

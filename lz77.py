import math
import sys

def get_entropy(text):

        # Char probability.
        prob = [ float(text.count(c)) / len(text) for c in dict.fromkeys(list(text)) ]
        entropy = - sum([ p * math.log(p) / math.log(2.0) for p in prob ])

        return entropy

def find_match(buffer, dictionary):
    offset = len(dictionary)
    substring = ""

    # Find characters from buffer in dictionary.
    for character in buffer:
        substring_tmp = substring + character
        offset_tmp = dictionary.rfind(substring_tmp)

        # No match.
        if offset_tmp < 0:
            break

        # Save found match.
        substring = substring_tmp
        offset = offset_tmp

    # legth of match and offset index.
    return len(substring), len(dictionary) - offset

def compress(text, buffer_size = 16, dictionary_size = 4096):
    dictionary = ""
    buffer = text[:buffer_size]

    result = []
    # loop until we have characters to match.
    while len(buffer) != 0:
        # get match length and offset index.
        size, offset = find_match(buffer, dictionary)

        # add found match into dict.
        dictionary += text[:size + 1]
        # slide dictionary.
        dictionary = dictionary[-dictionary_size:]

        # slide text.
        text = text[size:]
        last_character = text[:1]
        text = text[1:]

        # slide buffer, and add results.
        buffer = text[:buffer_size]
        result.append((offset, size, last_character))
    return result

def decompress(compressed_text):
    text = ""
    for part in compressed_text:
        offset, size, character = part
        text = text + text[-offset:][:size] + character
    return text

# Example from presentation.
example_text = 'abbabbbabaa'
# print(compress(example_text))

paths = [
    ".\Data\czech.txt", 
    ".\Data\english.txt", 
    ".\Data\german.txt", 
    ".\Data\\french.txt", 
    ".\Data\hungarian.txt"]

lens = [16,4096]

for i in range(0, len(paths)):
    f = open(paths[i], 'r', encoding = 'utf-8')
    text = f.read()
    triplet_size = 24

    compressed = compress(text, lens[0], lens[1])
    triplets_count = len(compressed)
    file_size = len(text.encode('utf-8'))
    enc_size = triplets_count * triplet_size
    bps = enc_size / file_size
    print("{0}, triplets: {1}, window size: {2}, max match: {3}, file size: {4}, enc. size: {5}, bps: {6}".format(paths[i], triplets_count, lens[1], lens[0], file_size,  enc_size, bps))

    compressed = compress(text, lens[0] * 4, lens[1] * 2)
    triplets_count = len(compressed)
    file_size = len(text.encode('utf-8'))
    enc_size = triplets_count * triplet_size
    bps = enc_size / file_size
    print("{0}, triplets: {1}, window size: {2}, max match: {3}, file size: {4}, enc. size: {5}, bps: {6}".format(paths[i], triplets_count, lens[1] * 4, lens[0] * 2, file_size,  enc_size, bps))

    compressed = compress(text, lens[0] * 8, lens[1] * 4)
    triplets_count = len(compressed)
    file_size = len(text.encode('utf-8'))
    enc_size = triplets_count * triplet_size
    bps = enc_size / file_size
    print("{0}, triplets: {1}, window size: {2}, max match: {3}, file size: {4}, enc. size: {5}, bps: {6}".format(paths[i], triplets_count, lens[1] * 8, lens[0] * 4, file_size,  enc_size, bps))
    





import os
import re
import sys

PHRASE_THRESHOLD = 2
SANITIZE_RE = re.compile(r'[^a-z0-9 -]')
RED = "\033[31m"
RESET = "\033[0m"

def get_vocabulary(file):
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
        vocabulary = text.split('\n')
        return vocabulary
    return []

def get_files(directory):
    files = []
    print(f"trancribe dir: {directory}")
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)) and filename.endswith('.mp3'):
            files.append(filename)
    return files

def get_codrivers():
    codriver_dir = './codrivers'
    return [os.path.join(codriver_dir, d) for d in os.listdir(codriver_dir) if os.path.isdir(os.path.join(codriver_dir, d))]

def sanitize_phrase(phrase):
    name = phrase.lower()
    name = SANITIZE_RE.sub("", name)
    return name.strip()


def get_file_phrase(filename):
    parts = filename.split("-")
    phrase = parts[0].strip()
    return sanitize_phrase(phrase)


def check_codriver(codriver_dir, vocabulary):
    files = get_files(codriver_dir)
    print(f"  files: {len(files)} phrases: {len(vocabulary)}")
    phrase_count = {}
    deficient = 0
    missing = 0
    for filename in files:

        phrase = get_file_phrase(filename)

        if phrase not in phrase_count:
            phrase_count[phrase] = 0
        phrase_count[phrase] += 1

    for phrase in vocabulary:
        sanitized = sanitize_phrase(phrase)
        if sanitized not in phrase_count or phrase_count[sanitized] < PHRASE_THRESHOLD:
            count = 0
            if sanitized in phrase_count:
                count = phrase_count[sanitized]
            deficient += 1
            if count == 0:
                missing += 1
            prefix = ""
            if count == 0:
                prefix = RED
            print(f"    {prefix}({count}): {phrase}{RESET}")

    print(f"  Number of deficient phrases: {deficient} {(100 * deficient / len(vocabulary)):.2f}%")
    print(f"  Number of missing   phrases: {missing} {(100 * missing / len(vocabulary)):.2f}%")

def main():
    codrivers = get_codrivers()
    print(codrivers);

    vocabulary = []
    vocabulary += get_vocabulary('./vocabulary.txt')
    vocabulary += get_vocabulary('./vocabulary-supplemental.txt')

    for codriver in codrivers:
        print(f">>> {codriver}:")
        check_codriver(codriver, vocabulary)

if __name__ == "__main__":
    main()
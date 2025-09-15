import argparse
import sys
import os.path
import json
import jsbeautifier
import re

def sorted_nicely( to_sort ):
    """ Sort the given iterable in the way that humans expect."""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(to_sort, key = alphanum_key)

# Ordered list of token regexes from most specific/longest to shortest
regex_patterns = [
    r"\b(tightens (one|two|three|four|five|six|square|hairpin|open hairpin)( sharp)?)",
    r"\b(tightens )?(((acute |open )?hairpin )|square |one |two |three |four |five |six |slight )?(right|left)",
    r"\b((through|over|past|around|at|onto|into|straight)\s)?(big jump|small jump|jumps|jump|crest|big crest|small crest|bales|bale|bridge|bumpy|bumps|bad bump|bump|bush|fence|junction|roundabout|sign|gate|tree|house|wall|posts|post|rocks|rock|logs|log|tunnel|bad dip|rough|dip|finish|starts|start|into stop|to stop|left entry chicane|stump|right entry chicane|water splash|twisty|patchy now|ice now|dry now|gravel|tarmac|cobbles|negative camber|good luck)( inside| outside)?",
    r"\b(don't cut|small cut|big cut|cut|uphill|downhill|keep (in|left|middle|out|right))",
    r"\b((hold|care|neat|double caution|triple caution|caution|brake|slowing))",
    r"\b(opens (one|two|three|four|five|six))",
    r"\b((narrows|tightens|opens|widens|opens and tightens|tightens and opens))",
    r"\b((very |extra |half )?long|short)",
    r"\b(unseen|and|into|sudden|early|late|turn|straight|through|sharp)",
    r"\b(one|two|three|four|five|six)\s(left|right)?",
    r"\b[0-9]+",
]

# Compile all patterns
compiled_patterns = [re.compile(p) for p in regex_patterns]

def tokenize(text):
    tokens = []
    pos = 0
    while pos < len(text):
        match = None
        for pattern in compiled_patterns:
            m = pattern.match(text, pos)
            if m:
                if not match or len(m.group(0)) > len(match.group(0)):
                    match = m  # take longest match
        if match:
            tokens.append(match.group(0).strip())
            pos = match.end()
            # Skip any spaces
            while pos < len(text) and text[pos].isspace():
                pos += 1
        else:
            # If nothing matches, skip one character (or raise error if strict)
            pos += 1
    return tokens

def getPaceNoteFiles():
    stages = []
    dirs = ['pacenotes']
    for dirn in dirs:
        for file in os.listdir(f"./{dirn}"):
            stages.append(os.fsdecode(f"./{dirn}/{file}"))
    return stages

def getPaceNoteData(file):
    with open(file, 'r', encoding='utf-8') as f:
        try:
            pacenotes = json.load(f)
            return pacenotes
        except:
            print(f"Error reading json in {file}")
            sys.exit()
    print(f"Error in getPaceNoteData: {file}")
    sys.exit()

def writePaceNoteData(file, data):
    lines = []
    lines.append("[");
    for i, note in enumerate(data):
        if i + 1 < len(data):
            lines.append(f"  {json.dumps(note)},")
        else:
            lines.append(f"  {json.dumps(note)}")
    lines.append("]");
    with open(file, 'w', encoding='utf-8') as f:
        print("\n".join(lines), file=f)

def adjust_calls(calls):
    phrase = " ".join(calls)
    return tokenize(phrase)

def main():
    files = getPaceNoteFiles()
    unique = []

    for file in files:
        pacenotes = getPaceNoteData(file)

        for note in pacenotes:
            calls = note[1]
            note[1] = adjust_calls(calls)

            for call in note[1]:
                if call not in unique:
                    unique.append(call)

            if " ".join(calls) != " ".join(note[1]):
                print(f">>>>>>>>>>>>>>>>>>>>")
                print(calls);
                print(f"ERROR DOES NOT MATCH")
                print(note[1])
                sys.exit()

        writePaceNoteData(file, pacenotes)

    # Display the result
    output = sorted_nicely(unique)
    options = jsbeautifier.default_options()
    options.indent_size = 2
    print(json.dumps(output, indent=2))
    print(f"unique: {len(output)}")

if __name__ == "__main__":
    main()

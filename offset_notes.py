import argparse
import sys
import os.path
import json
import jsbeautifier

def getPaceNotes(file):
    with open(os.path.join(file), 'r') as f:
        try:
            pacenotes = json.load(f)
        except:
            print(f"Error reading json in {file}")
            sys.exit()
    return pacenotes

def adjustNotes(pacenotes, offset):
    newNotes = []
    for note in pacenotes:
        newDistance = note[0] + offset;
        if newDistance < 0:
            newDistance = 0
        newNotes.append([newDistance, note[1]])
    return newNotes

def main():
    if len(sys.argv) == 3:
        file = sys.argv[1]  # Get the first command line argument
        offset = int(sys.argv[2])

        pacenotes = getPaceNotes(file);
        adjusted = adjustNotes(pacenotes, offset)
        print("[")


        for i, note in enumerate(adjusted):
            comma = ","
            if i == len(adjusted) - 1:
                comma = ""

            if len(note) == 3:
                print(f"  [{note[0]}, {json.dumps(note[1])}, {json.dumps(note[2])}]{comma}")
            else:
                print(f"  [{note[0]}, {json.dumps(note[1])}]{comma}")

        print("]")
    else:
        print("No parameter provided.")
        print("provide a filename and then the offset value +/-")
        print(json.dumps(sys.argv, indent=2))

if __name__ == "__main__":
    main()
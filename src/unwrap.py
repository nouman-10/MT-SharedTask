import argparse
import sys
import re

def unwrap(args):
    if args.input == None:
        lines = sys.stdin
    else:
        with open(args.input, 'r') as f:
            lines = f.readlines()

    processed_text = ""
    join_with_space = True

    for line in lines:
        line = line.strip()

        if len(line) == 0:
           continue

        line = re.sub('\s{3,}', '', line)

        # Skipping lines with digits only, since they are most likely page numbers
        if str.isdigit(line):
            continue

        if len(line) == 1:
            processed_text += ' ' + line
            join_with_space = False
            continue

        # Replacing — with -
        line = line.replace('—', '-')
        
        # Replacing « » quotation marks with ""
        line = line.replace('»', '\"')
        line = line.replace('«', "\"")

        # Replacing “ and ” with ""
        line = line.replace('“', '"')
        line = line.replace('”', '"')

        # If the line ends with the character `-` then 
        # it's probably the case that the word has been
        # wrapped to the next line.
        if line.endswith('-'):
            if join_with_space:
                processed_text += ' '
            
            processed_text += line[:-1]
            
            join_with_space = False
        else:
            if join_with_space:
                processed_text += ' '
            
            processed_text += line
            join_with_space = True
    
    if args.output == None:
        pass
        print(processed_text)
    else:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(processed_text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', type=str, default=None, help='Input .txt file. If not provided, the input is expected through stdin')
    parser.add_argument('--output', type=str, default=None, help='Output .txt file. If not provided, the output is printed to stdout')
    args = parser.parse_args()

    unwrap(args)


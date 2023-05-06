import argparse
import sys
import re

def is_roman_numeral(num):
    pattern = re.compile(r"""   
                                ^M{0,3}
                                (CM|CD|D?C{0,3})?
                                (XC|XL|L?X{0,3})?
                                (IX|IV|V?I{0,3})?$
            """, re.VERBOSE)

    if re.match(pattern, num):
        return True

    return False

def is_paragraph_beginning(line):
    if re.match('Art\.?.+\d+', line):
        return True
    
    if re.match('Art\.?.?\s\d+', line):
        True
    
    if re.match('Artículo\.? \d+', line):
        return True
    
    if re.match('^\d+\.? nik[i]?', line):
        return True
    
    if re.match('^[a-z]\)', line):
        return True

    return False

def unwrap(args):
    paragraphs = []
    current_paragraph = ""

    if args.input == None:
        lines = sys.stdin
    else:
        with open(args.input, 'r') as f:
            lines = f.readlines()

    join_with_space = True

    for line in lines:
        line = line.strip()

        if len(line) == 0:
           continue

        if is_paragraph_beginning(line):
            # start new paragraph
            paragraphs.append(current_paragraph)
            current_paragraph = ""

        # if curr_empty_line_count >= args.paragraph_del_len:
        #     # start new paragraph as we reach the number of empty lines
        #     # which represents the paragraph delimitation
        #     paragraphs.append(current_paragraph)
        #     current_paragraph = ""
        #     curr_empty_line_count = 0

        line = re.sub('\s{3,}', '', line)

        # Skipping lines with digits only, since they are most likely page numbers
        if str.isdigit(line):
            continue

        if len(line) == 1:
            current_paragraph += ' ' + line
            join_with_space = False
            continue

        # Replacing « » quotation marks with ""
        line = line.replace('»', '\"')
        line = line.replace('«', "\"")

        # Replacing “ and ” with ""
        line = line.replace('“', '"')
        line = line.replace('”', '"')

        line = line.replace('–', '-')
        line = line.replace('.-', '.')
        line = line.replace('-.', '.')

        line = line.replace('', '')

        # curr_line = line
        # for i, c in enumerate(curr_line):
        #     if c == '.' and i + 1< len(curr_line) and curr_line[i+1] != ' ' and curr_line[i+1] != '.' and curr_line[i+1] != '\n':
        #         print(line)

        # If the line ends with the character `-` then 
        # it's probably the case that the word has been
        # wrapped to the next line.
        if line.endswith('-'):
            if join_with_space:
                current_paragraph += ' '
            
            current_paragraph += line[:-1]
            
            join_with_space = False
        else:
            if join_with_space:
                current_paragraph += ' '
            
            current_paragraph += line
            join_with_space = True
    
    paragraphs.append(current_paragraph)

    if args.output == None:
        pass
        for p in paragraphs:
            p = p.strip()
            if len(p) == 0:
                continue
            print(p)
    else:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(paragraphs)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', type=str, default=None, help='Input .txt file. If not provided, the input is expected through stdin')
    parser.add_argument('--output', type=str, default=None, help='Output .txt file. If not provided, the output is printed to stdout')
    parser.add_argument('--paragraph_del_len', type=str, default=3, help='Number of empty lines that represent a paragraph delimitation')
    args = parser.parse_args()

    unwrap(args)


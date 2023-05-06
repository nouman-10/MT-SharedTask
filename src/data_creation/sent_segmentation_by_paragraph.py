import argparse
import sys
import nltk
import spacy
import stanza
import string

def segment_paragraph(paragraph, args, model):
    if args.segmenter == 'spacy':
        doc = model(paragraph)
        for sent in doc.sents:
           print(sent)

    elif args.segmenter == 'nltk':
        for sent in model.tokenize(paragraph):
            print(sent)
    
    elif args.segmenter == 'stanza':
        doc = model(paragraph)
        for sent in doc.sentences:
            print(sent.text)

def segmentation(args):
    if args.input == None:
        lines = sys.stdin
    else:
        with open(args.input, 'r') as f:
            lines = f.readlines()

    model = None
    if args.segmenter == 'spacy':
        model = spacy.load(args.model) # Load the spaCy Model
    elif args.segmenter == 'stanza':
        model = stanza.Pipeline(lang=args.model, processors='tokenize')
    else:
        model = nltk.data.load(f'tokenizers/punkt/{args.model}.pickle')
        model._params.abbrev_types.update(['art'])

    for line in lines:
        segment_paragraph(line, args, model)
        print(args.paragraph_delim)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', type=str, default=None, help='Input .txt file. If not provided, the input is expected through stdin')
    parser.add_argument('--segmenter', type=str, default='spacy', help='Sentence segmenter to use. spacy or nltk')
    parser.add_argument('--model', type=str, default='en_core_web_sm', help='Model to use (default en_core_web_sm)')
    parser.add_argument('--paragraph_delim', type=str, default='<p>', help='Paragraph delimiter')
    args = parser.parse_args()

    segmentation(args)


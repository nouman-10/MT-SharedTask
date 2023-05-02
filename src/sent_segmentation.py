import argparse
import sys
import nltk
import spacy
import stanza

def sentence_segmentation(args):
    if args.input == None:
        lines = sys.stdin
    else:
        with open(args.input, 'r') as f:
            lines = f.readlines()

    full_text = ""
    for line in lines:
        line = line.strip()
        full_text += line

    if args.segmenter == 'spacy':
        nlp = spacy.load(args.model) # Load the spaCy Model
        doc = nlp(full_text)
        for sent in doc.sents:
           print(sent)

    elif args.segmenter == 'nltk':
        for sent in nltk.sent_tokenize(full_text):
            print(sent)
    
    elif args.segmenter == 'stanza':
        nlp = stanza.Pipeline(lang=args.model, processors='tokenize')
        doc = nlp(full_text)
        for sent in doc.sentences:
            print(sent.text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', type=str, default=None, help='Input .txt file. If not provided, the input is expected through stdin')
    parser.add_argument('--segmenter', type=str, default='spacy', help='Sentence segmenter to use. spacy or nltk')
    parser.add_argument('--model', type=str, default='en_core_web_sm', help='Model to use (i.e. "es_core_web_sm" for spaCy, "es" for stanza)')
    args = parser.parse_args()

    sentence_segmentation(args)



# Intro

Run the script `tools_setup.sh` to download and build hunalign and pdftotext tools.

# .pdf to .txt

We will use pdftotext from xpdf package of tools:

```
src/xpdf/bin64/pdftotext -layout -enc UTF-8 parallel-data/extra/little_prince/LittlePrince.spa.pdf parallel-data/extra/little_prince/LittlePrince.spa.txt
```

# Unwrapping 

To do the unwrapping, use the script `unwrap.py` like so:

```
usage: unwrap.py [-h] [--input INPUT] [--output OUTPUT]

optional arguments:
  -h, --help       show this help message and exit
  --input INPUT    Input .txt file. If not provided, the input is expected through stdin
  --output OUTPUT  Output .txt file. If not provided, the output is printed to stdout
```

Example usage: 

```
python src/unwrap.py --input input_file.txt --output output_file.txt
```

or 

```
cat parallel_data/extra/little_prince/LittlePrince.que.txt | python src/unwrap.py > LittlePrince.que.unwrapped.txt
```

# Sentence segmentation

To do the sentence segmentation, use the script `sentence_segmentation.py`:
```
usage: sent_segmentation.py [-h] [--input INPUT] [--segmenter SEGMENTER] [--model MODEL]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         Input .txt file. If not provided, the input is expected through stdin
  --segmenter SEGMENTER
                        Sentence segmenter to use. spacy or nltk
  --model MODEL         Model to use (i.e. "es_core_web_sm" for spaCy, "es" for stanza)
```

Here are a few examples:
```
python src/sentence_segmentation.py --input LittlePrince.que.unwrapped.txt --segmenter spacy --model es_core_web_sm
python src/sentence_segmentation.py --input LittlePrince.que.unwrapped.txt --segmenter nltk
python src/sentence_segmentation.py --input LittlePrince.que.unwrapped.txt --segmenter stanza --model es
```

# Sentence alignment

Consider adding an alias for hunalign:
```
alias hunalign="<your_path_to_repo>/src/hunalign-1.1/src/hunalign/hunalign 
```

Then, it can be used like so:
```
hunalign americasnlp_dict.txt LittlePrince.que.segmented.txt LittlePrince.spa.segmented.txt -text -utf -realign -autodict=output_dict.txt > LittlePrince.aligned.txt
```

Then, optionally, you can filter only the aligned sentence above a given score, using the script `hunalign_threshold_filter.py`:
```
cat LittlePrince.aligned.txt | python hunalign_threshold_filter.py 0.1
```

where `0.1` is the threshold value for hunalign scores.


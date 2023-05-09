import sys

src_sentences = []
tgt_sentences = []

with open(sys.argv[1], "r", encoding="utf-8") as f:
    for line in f.readlines():
        line = line.strip()
        parts = line.split("\t")
        src_sentence = parts[0]
        tgt_sentence = parts[1]
        if src_sentence == "<p>" and tgt_sentence == "<p>":
            continue

        if len(src_sentence) == 0 or len(tgt_sentence) == 0:
            continue

        src_sentence = src_sentence.replace(" ~~~ ", " ")
        tgt_sentence = tgt_sentence.replace(" ~~~ ", " ")

        src_sentences.append(src_sentence)
        tgt_sentences.append(tgt_sentence)

with open(sys.argv[2] + ".spa", "w", encoding="utf-8") as f:
    for s in src_sentences:
        f.write(s + "\n")

with open(sys.argv[2] + ".que", "w", encoding="utf-8") as f:
    for s in tgt_sentences:
        f.write(s + "\n")

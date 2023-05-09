import sys

if len(sys.argv) < 2:
    print("Threshold value required as an argument")
    exit()

threshold = float(sys.argv[1])
for line in sys.stdin:
    parts = line.split("\t")
    src = parts[0]
    tgt = parts[1]
    if src == "<p>" and tgt == "<p>":
        continue

    score = float(parts[2])

    if score >= threshold:
        print(line.rstrip())

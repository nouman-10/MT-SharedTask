# Data Description

## Original Data (Provided in the shared task)

- JW300: Jehovah Witness Texts (Both in Quechua Cuzco (quz) and Quechua Ayacucho (quy))

  - Quz: parallel-data/quz/jw300
  - Quy: parallel-data/original/jw300

- MINEDU (quy): Sentences extracted from the the official dictionary of the Minister of Education (MINEDU) in Peru for Quechua Ayacucho.

  - Quy: parllel-data/original/minedu

- Dict_misc (quy): Dictionary entries and samples collected by Diego Huarcaya.
  - Quy: parallel-data/original/dict_misc

## Extra Data

### Helsinki-NLP (https://github.com/Helsinki-NLP/americasnlp2021-st)

- Peruvian Constitution: parallel-data/extra/per_const
- Bolivian Constitution: parallel-data/extra/bol_const
- Tatoeba (OPUS): parallel-data/extra/tatoeba

### REPUcs-AmericasNLP2021 (https://github.com/Ceviche98/REPUcs-AmericasNLP2021)

- WebMisc- Additional sentences at http://quechua-ayacucho.org/es/index_es.php and a few poems at https://lyricstranslate.com/ : parallel-data/extra/web_misc
- Lexicon - Vocabulary available at http://quechua-ayacucho.org/es/index_es.php was extracted and transformed manually into parallel corpora: parallel-data/extra/lexicon
- Handbook - translations from the Quechua educational handbook (Iter and Cárdenas, 2019. (no link, didn't do much research to find either haah) were manually aligned to obtain a parallel corpus: parallel-data/extra/handbook

- Peruvian Constitution (but in Quz): parallel-data/quz/per_const
- Regulation of the Amazon Parliament (but in Quz): parallel-data/quz/reglamento

### Bible Corpus (https://github.com/christos-c/bible-corpus/blob/master/bibles/Quichua-NT.xml)

Built a small script to align the Quechua translation with Spanish using ids in the xml

- Bible Corpus: parallel-data/extra/bible

## Data Counts:

| **Dataset**           | **Variant** | **Original Count**    | **Final Count** |
| --------------------- | ----------- | --------------------- | --------------- |
| JW300                 | Quy         | 125008                | 121064          |
| Dict Misc             | Quy         | 9000                  | 8998            |
| Minedu                | Quy         | 643                   | 643             |
| Bible                 | Quy         | 7937 (Qu), 23805 (Es) | 7935\*          |
| Bolivian Constitution | Quy         | 2193                  | 2193            |
| Peruvian Constitution | Quy         | 1276                  | 1276            |
| Lexicon               | Quy         | 6161                  | 6161            |
| Handbook              | Quy         | 2297                  | 2296            |
| Web Misc              | Quy         | 985                   | 985             |
| Tatoeba               | Quy         | 163                   | 163             |
| JW300                 | Quz         | 136589                | 131233          |
| Peruvian Constitution | Quz         | 999                   | 999             |
| Reglamento            | Quz         | 287                   | 287             |

\* The original count refers to the count in xml files and final refers to the count after the mapping

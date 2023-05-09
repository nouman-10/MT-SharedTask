# Data Description

## Original Data (Provided in the shared task)

- JW300: Jehovah Witness Texts (Both in Quechua Cuzco (quz) and Quechua Ayacucho (quy))

  - Quz: `./data/parallel-data/quechua-spanish/original/jw300_quz/`
  - Quy: `./data/parallel-data/quechua-spanish/original/jw300_quy/`

- MINEDU (quy): Sentences extracted from the the official dictionary of the Minister of Education (MINEDU) in Peru for Quechua Ayacucho.

  - Quy: `./data/parallel-data/quechua-spanish/original/minedu_quy/`

- Dict_misc (quy): Dictionary entries and samples collected by Diego Huarcaya.
  - Quy: `./data/parallel-data/quechua-spanish/original/dict_misc_quy/`

## Extra Data

### Helsinki-NLP (https://github.com/Helsinki-NLP/americasnlp2021-st)

- Peruvian Constitution: `./data/parallel-data/quechua-spanish/extra/per_const_quy/`
- Bolivian Constitution: `./data/parallel-data/quechua-spanish/extra/bol_const_quy/`
- Tatoeba (OPUS): `./data/parallel-data/quechua-spanish/extra/tatoeba_quy/`
- Bibles: `./data/parallel-data/quechua-spanish/extra/bible_quy/`

### REPUcs-AmericasNLP2021 (https://github.com/Ceviche98/REPUcs-AmericasNLP2021)

- WebMisc- Additional sentences at http://quechua-ayacucho.org/es/index_es.php and a few poems at https://lyricstranslate.com/
  - `./data/parallel-data/quechua-spanish/extra/web_misc_quy/`
- Lexicon - Vocabulary available at http://quechua-ayacucho.org/es/index_es.php was extracted and transformed manually into parallel corpora
  - `./data/parallel-data/quechua-spanish/extra/lexicon_quy/`
- Handbook - translations from the Quechua educational handbook (Iter and Cárdenas, 2019. (no link, didn't do much research to find either haah) were manually aligned to obtain a parallel corpus
  - `./data/parallel-data/quechua-spanish/extra/handbook_quy/`

- Peruvian Constitution (but in Quz): `./data/parallel-data/quechua-spanish/extra/per_const_quz/`
- Regulation of the Amazon Parliament (but in Quz): `./data/parallel-data/quechua-spanish/extra/reglamento_const/`

### https://github.com/a-rios/squoia

Multiple parallel corpuses (not big, like 300-600 sentences each). Most of them are nearly aligned but some of them have huge differences in length, so can't be aligned and are skipped. We did have to manually align the nearly aligned ones but this majorly included line breaks in one corpus and not the other, so not major differences

- Fundacion (in Quz): `./data/parallel-data/quechua-spanish/extra/fundacion_quz/`
- DW (in Quz): `./data/parallel-data/quechua-spanish/extra/dw_quz/`
- Cosude (in Quz): `./data/parallel-data/quechua-spanish/extra/cosude_quz/`


## Data Counts:

| **Dataset**           | **Variant** | **Original Count**    | **Final Count** |
| --------------------- | ----------- | --------------------- | --------------- |
| JW300                 | Quy         | 125008                | 121064          |
| Dict Misc             | Quy         | 9000                  | 8998            |
| Minedu                | Quy         | 643                   | 643             |
| Bible                 | Quy         | 34831                 | 31102           |
| Bolivian Constitution | Quy         | 2193                  | 2193            |
| Peruvian Constitution | Quy         | 1276                  | 1276            |
| Lexicon               | Quy         | 6161                  | 6161            |
| Handbook              | Quy         | 2297                  | 2296            |
| Web Misc              | Quy         | 985                   | 985             |
| Tatoeba               | Quy         | 163                   | 163             |
| JW300                 | Quz         | 136589                | 131233          |
| Peruvian Constitution | Quz         | 999                   | 999             |
| Reglamento            | Quz         | 287                   | 287             |
| Fundacion             | Quz         | 440                   | 440             |
| DW                    | Quz         | 856                   | 856             |
| Cosude                | Quz         | 529                   | 529             |


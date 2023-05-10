### Install requirements

Install the required libraries by running `pip install -r requirements.txt`

## Train the model


### Training
To run the model, using the Quechua data used for the best model, including the Cuzco variant (but including the same data in both variants only once), run the following command:

```
python mt_model.py --checkpoint Helsinki-NLP/opus-mt-es-fi --out_model_name es_fi_quz --extra_data_codes quy quz --epochs 20
```
Note: In order to push the model to the Huggingface hub, make sure you login first using `huggingface-cli login` before training the model.
### Arguments

```
usage: mt_model.py [-h] --checkpoint CHECKPOINT --out_model_name OUT_MODEL_NAME [--metric METRIC] [--epochs EPOCHS] [--is_prompt | --no-is_prompt]
                   [--extra_data_codes [EXTRA_DATA_CODES ...]] [--is_multilingual | --no-is_multilingual] [--with_dups | --no-with_dups]
                   [--push_to_hub | --no-push_to_hub]

options:
  -h, --help            show this help message and exit
  --checkpoint CHECKPOINT
                        Name of model checkpoint to load from HuggingFace
  --out_model_name OUT_MODEL_NAME
                        Output Model Name
  --metric METRIC       Metric to choose the best model on (Default: 'chrf') (Other: 'bleu')
  --epochs EPOCHS       Number of epochs to train the model for (Default: 10)
  --is_prompt, --no-is_prompt
                        Some models require a checkpoint (Default: False)
  --extra_data_codes [EXTRA_DATA_CODES ...]
                        Extra data to load for quechua (Default: []) (Options: 'quy', 'quz', 'que', 'bcktr', 'copied')
  --is_multilingual, --no-is_multilingual
                        Whether to train a multilingual model or just on Quechua (Default: False)
  --with_dups, --no-with_dups
                        Whether to include duplicate data but different dialect for Quechua (Default: False)
  --push_to_hub, --no-push_to_hub
                        Whether to push the model to the hub or not (Default: False)
```

## Test the model

### Generate Predictions

To generate the predictions, using the trained model, run the following command (for the dev set):

```
python generate_translations.py --model_name es_fi_quz --src_file ./../../data/parallel-data/quechua-spanish/dev/dev.es --tgt_file translations/quechua/dev.txt
```
The `--tgt_file` represents the file path to save the translations to. And `--model_name` could be your local path to a model or a huggingface model as well.

### Evaluating Predictions
To evaluate your predictions (chrF and bleu) against true translations, run the following command:
```
python evaluate.py --system_output translations/quechua/dev.txt --gold_reference ./../../data/parallel-data/quechua-spanish/dev/dev.quy
```

### Install requirements

Install the required libraries by running `pip install -r requirements.txt`

### Sample Run

To run the model, using all Quechua data, including the Cuzco variant (but including the same data in both variants only once), run the following command:

```
python hf_model.py --checkpoint Helsinki-NLP/opus-mt-es-fi --out_model_name es_fi_quz --extra_data_codes quy quz que bcktr
```

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
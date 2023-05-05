### Install requirements

Install the required libraries by running `pip install -r requirements.txt`

### Sample Run

To run the model, using all Quechua data, including the Cuzco variant (but including the same data in both variants only once), run the following command:

```
python hf_model.py --tgt_lang quechua --checkpoint Helsinki-NLP/opus-mt-es-fi --out_model_name /scratch/s4992113/americas_nlp/hels_es_fi_quy --epochs 20 --is_prompt 0
```

Parameters:
- `tgt_lang`: name of the target language (required)
- `checkpoint`: the model that you want to fine-tune (could be a pretrained one) (required)
- `out_model_name`: where to save the fine-tuned model (required)
- `epochs`: number of epochs (default=10)
- `is_prompt`: whether to add a prompt when tokenizing (required for models based on t5 architecture) (default=1)
- `metric`: which metric to chose the best model on (`chrf` or `bleu`) (default=`chrf`)

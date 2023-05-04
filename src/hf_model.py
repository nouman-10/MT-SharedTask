# Some helper functions for training the models
from transformers import AutoTokenizer, DataCollatorForSeq2Seq
import evaluate
import numpy as np
from transformers import AutoModelForSeq2SeqLM, Seq2SeqTrainingArguments, Seq2SeqTrainer
from constants import QUECHUA_DATA_PATHS, QUECHUA_DUPLICATES
from helper_funcs import read_data_into_hf

bleu_metric = evaluate.load("sacrebleu")
chrf_metric = evaluate.load("chrf")

def load_dataset_from_hf(ds_name):
  return load_dataset(ds_name)


def load_pre_trained_tokenizer(checkpoint):
  if "mbart" in checkpoint.lower():
    return AutoTokenizer.from_pretrained(checkpoint, src_lang="es_XX", tgt_lang="en_XX")
  return AutoTokenizer.from_pretrained(checkpoint)

def preprocess_function(examples, tokenizer, source_lang="es", target_lang="quy", prefix="translate Spanish to Quechua", is_prompt=True):
    if is_prompt:
      inputs = [prefix + example[source_lang] for example in examples["translation"]]
      targets = [example[target_lang] for example in examples["translation"]]
      model_inputs = tokenizer(inputs, text_target=targets, max_length=128, truncation=True)
      return model_inputs
    else:
      inputs = [ex[source_lang] for ex in examples["translation"]]
      targets = [ex[target_lang] for ex in examples["translation"]]
      model_inputs = tokenizer(
          inputs, text_target=targets, max_length=128, truncation=True
      )
      return model_inputs

def get_data_collator(tokenizer, checkpoint):
  return DataCollatorForSeq2Seq(tokenizer=tokenizer, model=checkpoint)

def postprocess_text(preds, labels):
    preds = [pred.strip() for pred in preds]
    labels = [[label.strip()] for label in labels]

    return preds, labels

def prepare_compute_metrics(tokenizer):
  def compute_metrics(eval_preds):
      nonlocal tokenizer
      preds, labels = eval_preds
      if isinstance(preds, tuple):
          preds = preds[0]
      decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)

      labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
      decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

      decoded_preds, decoded_labels = postprocess_text(decoded_preds, decoded_labels)

      result_bleu = bleu_metric.compute(predictions=decoded_preds, references=decoded_labels)
      result_chrf = chrf_metric.compute(predictions=decoded_preds, references=decoded_labels)
      result = {"bleu": result_bleu["score"], "chrf": result_chrf["score"]}
      

      prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) for pred in preds]
      result["gen_len"] = np.mean(prediction_lens)
      result = {k: round(v, 4) for k, v in result.items()}
      return result
  return compute_metrics

def load_pretrained_model(checkpoint):
  return AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

def get_training_args(model_name, epochs=3, metric="chrf"):
  return Seq2SeqTrainingArguments(
    output_dir=model_name,
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    weight_decay=0.01,
    save_total_limit=3,
    num_train_epochs=epochs,
    predict_with_generate=True,
    fp16=True,
    metric_for_best_model=metric,
  )

def get_trainer(model, training_args, dataset, tokenizer, data_collator):
  return Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["dev"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=prepare_compute_metrics(tokenizer),
  )


def train_model(tgt_lang_code, checkpoint, out_model_name, metric="chrf", epochs=3, is_prompt=True):
  dataset = read_data_into_hf(tgt_lang_code, data_paths=QUECHUA_DATA_PATHS, duplicates=QUECHUA_DUPLICATES)
  tokenizer = load_pre_trained_tokenizer(checkpoint)

  tokenized_dataset = dataset.map(preprocess_function, fn_kwargs={"tokenizer": tokenizer, "is_prompt":is_prompt}, batched=True)
  data_collator = get_data_collator(tokenizer, checkpoint)

  model = load_pretrained_model(checkpoint)
  training_args = get_training_args(out_model_name, metric=metric, epochs=epochs)

  trainer = get_trainer(model, training_args, tokenized_dataset, tokenizer, data_collator)
  trainer.train()




if __name__ == "__main__":
  import argparse
  from datasets import load_dataset
  parser = argparse.ArgumentParser()
  parser.add_argument("--tgt_lang_code", type=str, required=True)
  parser.add_argument("--checkpoint", type=str, required=True)
  parser.add_argument("--out_model_name", type=str, required=True)
  parser.add_argument("--metric", type=str, required=True)
  parser.add_argument("--epochs", type=int, required=True)
  parser.add_argument("--is_prompt", type=int, default=1)

  args = parser.parse_args()

  train_model(args.tgt_lang_code, args.checkpoint, args.out_model_name, args.metric, args.epochs, args.is_prompt)

# Some helper functions for training the models
from transformers import AutoTokenizer, DataCollatorForSeq2Seq
import evaluate
import numpy as np
from transformers import AutoModelForSeq2SeqLM, Seq2SeqTrainingArguments, Seq2SeqTrainer
from constants import ORIGINAL_DATA_PATHS, EXTRA_DATA_PATHS, QUECHUA_DUPLICATES
from helper_funcs import read_data_into_hf
import sacrebleu
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
      model_inputs = tokenizer(inputs, text_target=targets, max_length=200, truncation=True)
      return model_inputs
    else:
      inputs = [ex[source_lang] for ex in examples["translation"]]
      targets = [f"{prefix.split()[-1]}" + " " + ex[target_lang] for ex in examples["translation"]]
      model_inputs = tokenizer(
          inputs, text_target=targets, padding=True, truncation=True
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

      result_bleu = sacrebleu.corpus_bleu(decoded_preds, decoded_labels)
      result_chrf = sacrebleu.corpus_chrf(decoded_preds, decoded_labels)
      result = {"bleu": result_bleu.score, "chrf": result_chrf.score}

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
    evaluation_strategy="steps",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    weight_decay=0.01,
    save_total_limit=1,
    load_best_model_at_end=True,
    num_train_epochs=epochs,
    predict_with_generate=True,
    fp16=True,
    metric_for_best_model=metric,
    push_to_hub=True
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


def train_model(tgt_lang, checkpoint, out_model_name, metric, epochs, is_prompt, prefix, extra_data_codes, with_dup):
  data_paths = ORIGINAL_DATA_PATHS
  for code in extra_data_codes:
    data_paths.extend(EXTRA_DATA_PATHS[code])
  duplicate_paths = [] if with_dup else QUECHUA_DUPLICATES
  dataset = read_data_into_hf(tgt_lang, data_paths=data_paths, duplicates=duplicate_paths)
  tokenizer = load_pre_trained_tokenizer(checkpoint)

  tokenized_dataset = dataset.map(preprocess_function, fn_kwargs={"tokenizer": tokenizer, "is_prompt":is_prompt, "prefix":prefix}, batched=True)
  data_collator = get_data_collator(tokenizer, checkpoint)

  model = load_pretrained_model(checkpoint)
  training_args = get_training_args(out_model_name, metric=metric, epochs=epochs)

  trainer = get_trainer(model, training_args, tokenized_dataset, tokenizer, data_collator)
  trainer.train()
  trainer.push_to_hub(out_model_name)



if __name__ == "__main__":
  import argparse
  from datasets import load_dataset
  parser = argparse.ArgumentParser()
  parser.add_argument("--tgt_lang", type=str, required=True)
  parser.add_argument("--checkpoint", type=str, required=True)
  parser.add_argument("--out_model_name", type=str, required=True)
  parser.add_argument("--metric", type=str, required=False, default='chrf')
  parser.add_argument("--epochs", type=int, required=False, default=10)
  parser.add_argument("--is_prompt", type=int, default=1)
  parser.add_argument("--prefix", type=str, default="traducir español a quechua")
  parser.add_argument("--extra_data_codes", nargs"*", type=str, default=[])
  parser.add_argument("--with_dup", type=int, default=0)

  args = parser.parse_args()

  train_model(args.tgt_lang, args.checkpoint, args.out_model_name, args.metric, args.epochs, args.is_prompt, args.prefix, args.extra_data_codes, args.with_dup)

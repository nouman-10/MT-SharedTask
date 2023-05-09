import argparse
from typing import Dict, Iterable, List, Tuple

import numpy as np
import sacrebleu
from datasets import DatasetDict, concatenate_datasets
from transformers import (AutoModelForSeq2SeqLM, AutoTokenizer,
                          DataCollatorForSeq2Seq, EarlyStoppingCallback,
                          Seq2SeqTrainer)

import helper_funcs as f


class MT_Model:
    def __init__(
        self,
        checkpoint: str,
        out_model_name: str,
        que_data_codes: List[str] = ["orig"],
        is_multilingual: bool = False,
        epochs: int = 10,
        is_prompt: bool = False,
        push_to_hub: bool = False,
        metric: str = "chrf",
        with_dups: bool = False,
    ):
        self.checkpoint = checkpoint
        self.out_model_name = out_model_name

        self.que_data_codes = ["orig"] + que_data_codes if que_data_codes else ["orig"]
        self.is_multilingual = is_multilingual
        self.epochs = epochs
        self.is_prompt = is_prompt
        self.push_to_hub = push_to_hub
        self.metric = metric

        datasets = f.load_dataset(is_multilingual, self.que_data_codes, with_dups)
        self.load_pretrained_tokenizer()
        self.get_data_collator()
        self.load_pretrained_model()

        self.tokenize(datasets)

    def load_pretrained_tokenizer(self):
        """Load a pre-trained tokenizer from HuggingFace"""
        self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint)

    def get_data_collator(self):
        """Get the data collator for the trainer"""
        self.data_collator = DataCollatorForSeq2Seq(tokenizer=self.tokenizer, model=self.checkpoint)

    def load_pretrained_model(self):
        """Load a pre-trained model from HuggingFace"""
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.checkpoint)

    def tokenize(self, datasets: Dict[str, DatasetDict]):
        """Tokenize the datasets

        Args:
            datasets (Dict[str, DatasetDict]): The datasets to tokenize
        """
        datasets = [
            dataset.map(
                f.preprocess_function,
                fn_kwargs={
                    "tokenizer": self.tokenizer,
                    "is_prompt": False,
                    "prefix": f"translate Spanish to {lang}: ",
                    "is_multilingual": self.is_multilingual,
                },
                batched=True,
            )
            for lang, dataset in datasets.items()
        ]

        self.tokenized_dataset = DatasetDict(
            {
                "train": concatenate_datasets([dataset["train"] for dataset in datasets]),
                "dev": concatenate_datasets([dataset["dev"] for dataset in datasets]),
            }
        )

    def compute_metrics(self, eval_preds: Tuple[Iterable[int], Iterable[int]]) -> Dict[str, float]:
        """Compute metrics while training the model

        Args:
            eval_preds (Tuple[Iterable[int], Iterable[int]]): Tuple containing input ids for predictions and true labels

        Returns:
            Dict[str, float]: Dictionary containing the computed metrics, namely bleu and chrf (also avg generated length)
        """
        preds, labels = eval_preds
        if isinstance(preds, tuple):
            preds = preds[0]
        decoded_preds = self.tokenizer.batch_decode(preds, skip_special_tokens=True)

        labels = np.where(labels != -100, labels, self.tokenizer.pad_token_id)
        decoded_labels = self.tokenizer.batch_decode(labels, skip_special_tokens=True)

        decoded_preds, decoded_labels = f.postprocess_text(decoded_preds, decoded_labels)

        result_bleu = sacrebleu.corpus_bleu(decoded_preds, [decoded_labels])
        result_chrf = sacrebleu.corpus_chrf(decoded_preds, [decoded_labels])
        result = {"bleu": result_bleu.score, "chrf": result_chrf.score}

        prediction_lens = [np.count_nonzero(pred != self.tokenizer.pad_token_id) for pred in preds]
        result["gen_len"] = np.mean(prediction_lens)
        result = {k: round(v, 4) for k, v in result.items()}
        return result

    def get_trainer(self) -> Seq2SeqTrainer:
        """Returns a trainer using the loaded dataset and model

        Returns:
            Seq2SeqTrainer: The trainer
        """
        return Seq2SeqTrainer(
            model=self.model,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=5)],
            args=self.training_args,
            train_dataset=self.tokenized_dataset["train"],
            eval_dataset=self.tokenized_dataset["dev"],
            tokenizer=self.tokenizer,
            data_collator=self.data_collator,
            compute_metrics=self.compute_metrics,
        )

    def train(self):
        """Load the training arguments and start the training"""
        self.training_args = f.get_training_args(
            out_model_name=self.out_model_name,
            epochs=self.epochs,
            metric=self.metric,
            push_to_hub=self.push_to_hub,
            is_multilingual=self.is_multilingual,
        )
        self.trainer = self.get_trainer()
        self.trainer.train()

        if self.push_to_hub:
            self.trainer.push_to_hub(self.out_model_name)


def get_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, required=True, help="Name of model checkpoint to load from HuggingFace")
    parser.add_argument("--out_model_name", type=str, required=True, help="Output Model Name")
    parser.add_argument("--metric", type=str, required=False, default="chrf", help="Metric to choose the best model on (Default: 'chrf') (Other: 'bleu')")
    parser.add_argument("--epochs", type=int, required=False, default=10, help="Number of epochs to train the model for (Default: 10)")
    parser.add_argument("--is_prompt", default=False, action=argparse.BooleanOptionalAction, help="Some models require a checkpoint (Default: False)")
    parser.add_argument("--extra_data_codes", nargs="*", type=str, default=[], help="Extra data to load for quechua (Default: []) (Options: 'quy', 'quz', 'que', 'bcktr', 'copied')")
    parser.add_argument("--is_multilingual", default=False, action=argparse.BooleanOptionalAction, help='Whether to train a multilingual model or just on Quechua (Default: False)')
    parser.add_argument("--with_dups", default=False, action=argparse.BooleanOptionalAction, help="Whether to include duplicate data but different dialect for Quechua (Default: False)")
    parser.add_argument("--push_to_hub", default=False, action=argparse.BooleanOptionalAction, help="Whether to push the model to the hub or not (Default: False)")

    return parser

if __name__ == "__main__":

    parser = get_argument_parser()
    args = parser.parse_args()

    mt_model = MT_Model(
        checkpoint=args.checkpoint,
        out_model_name=args.out_model_name,
        que_data_codes=args.extra_data_codes,
        is_multilingual=args.is_multilingual,
        epochs=args.epochs,
        is_prompt=args.is_prompt,
        metric=args.metric,
        push_to_hub=args.push_to_hub,
        with_dups=args.with_dups,
    )
    mt_model.train()

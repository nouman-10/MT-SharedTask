from typing import List

from datasets import Dataset
from transformers import pipeline
from transformers.pipelines.pt_utils import KeyDataset


def generate_translations(model_checkpoint: str, texts: List[str]) -> List[str]:
    """Genrate translations using a HuggingFace model

    Args:
        model_checkpoint (str): The name of the model to use
        texts (List[str]): The texts to translate
    Returns:
        List[str]: Generated translations
    """

    dataset = Dataset.from_dict({"es": texts})
    pipe = pipeline("translation", model=model_checkpoint)
    translations = []
    for rows in pipe(KeyDataset(dataset, "es"), batch_size=16):
        translations.extend([row['translation_text'].strip() for row in rows])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, required=True, help="Name of model to use")
    parser.add_argument("--src_file", type=str, required=True, help="Path of the file with source sentences")
    parser.add_argument("--tgt_file", type=str, required=True, help="Filename to save the translations to")

    args = parser.parse_args()
    src_texts = open(args.src_file, "r").readlines()

    translations = generate_translations(args.model_name, src_texts)

    with open(args.tgt_file, "w") as f:
        f.write("\n".join(translations))

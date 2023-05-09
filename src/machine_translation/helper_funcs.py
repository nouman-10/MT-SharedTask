import os
from typing import Any, Dict, Iterable, List, Tuple

from datasets import Dataset, DatasetDict
from transformers import PreTrainedTokenizer, Seq2SeqTrainingArguments

from constants import (DATA_CODES, QUECHUA_DATA_PATHS, QUECHUA_DUPLICATES,
                       SRC_LANG, SRC_LANG_CODE, MAIN_FOLDER_PATH)


def preprocess_function(
    examples: Iterable[Dict[str, Any]],
    tokenizer: PreTrainedTokenizer,
    prefix: str = "translate Spanish to Quechua: ",
    is_prompt: bool = True,
    is_multilingual: bool = False,
):
    """Preprocess and tokenize the data.

    Args:
        examples (Iterable[Dict[str, Any]]): The input examples containing the source and target text.
        tokenizer (PreTrainedTokenizer): The tokenizer to use.
        prefix (_type_, optional): Some models require prefix. Defaults to "translate Spanish to Quechua: ".
        is_prompt (bool, optional): Whether the prefix should be added or not. Defaults to False.
        is_multilingual (bool, optional): Whether a multilingual model is being trained or not. Defaults to False.

    Returns:
        _type_: _description_
    """
    if is_prompt:
        inputs = [prefix + example["src"] for example in examples["translation"]]
    else:
        if is_multilingual:
            inputs = [ex["src"] + f" {prefix.split()[-1]}" for ex in examples["translation"]]
        else:
            inputs = [ex["src"] for ex in examples["translation"]]

    targets = [example["tgt"] for example in examples["translation"]]
    model_inputs = tokenizer(inputs, text_target=targets, padding=True, truncation=True)
    return model_inputs


def postprocess_text(preds: List[str], labels: List[str]) -> Tuple[List[str], List[str]]:
    """Postprocess the predictions and labels for computation of metrics.

    Args:
        preds (List[str]): Predictions.
        labels (List[str]): Labels.

    Returns:
        Tuple[List[str], List[str]]: The postprocessed predictions and labels.
    """
    preds = [" ".join(pred.strip().split()[1:]) for pred in preds]
    labels = [" ".join(label.strip().split()[1:]) for label in labels]

    return preds, labels


def get_training_args(
    out_model_name: str, epochs: int = 10, metric: str = "chrf", is_multilingual: bool = False, push_to_hub: bool = True
) -> Seq2SeqTrainingArguments:
    """Get the training arguments for the trainer.

    Args:
        out_model_name (str): The name of the model to save.
        epochs (int, optional): Number of epochs. Defaults to 10.
        metric (str, optional): Metric to choose the best model for (chrf or bleu). Defaults to "chrf".
        eval_steps (int, optional): Number of steps after which evaluation should be done. Defaults to 1000.
        save_steps (int, optional): Number of steps after which the model should be saved. Defaults to 1000.
        push_to_hub (bool, optional): Whether the model should be pushed to huggingface hub or not. Defaults to True.

    Returns:
        Seq2SeqTrainingArguments: The training arguments.
    """
    eval_steps = (
        10000 if is_multilingual else 1000
    )  # It takes a lot of time to evaluate the multilingual model so less evaluation steps
    return Seq2SeqTrainingArguments(
        output_dir=out_model_name,
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
        eval_steps=eval_steps,
        save_steps=eval_steps,
        metric_for_best_model=metric,
        push_to_hub=push_to_hub,
    )


def load_dataset(
    is_multilingual=False, que_data_codes=["orig"], with_dup: bool = False
) -> DatasetDict | Dict[str, DatasetDict]:
    """Load the dataset from local files

    Args:
        is_multilingual (bool, optional): Whether multilingual data should be loaded. Defaults to False.
        que_data_codes (list, optional): Which quechua data to load, default loads only the original task's data. Defaults to ["orig"].
        with_dup (bool, optional): Whether to load the duplicate data or not. Defaults to False.

    Returns:
        Dict[str, DatasetDict]: returns a dictionary with the datasets for each language
    """
    if is_multilingual:
        return load_multilingual_data(que_data_codes, with_dup)
    else:
        return load_quechua_data(que_data_codes, with_dup)


def load_quechua_data(data_codes: List[str] = ["orig"], with_dup: bool = False) -> Dict[str, DatasetDict]:
    """Load the quechua data from local files

    Args:
        data_codes (list, optional): Which quechua data to load, default loads only the original task's data. Defaults to ["orig"].
        with_dup (bool, optional): Whether to load the duplicate data or not. Defaults to False.
    Returns:
        Dict[str, DatasetDict]: returns a dictionary with the datasets for quechua
    """
    data_paths = []
    for code in data_codes:
        data_paths.extend(QUECHUA_DATA_PATHS[code])

    return {"quechua": read_data_into_hf("quechua", data_paths, [] if with_dup else QUECHUA_DUPLICATES)}


def load_multilingual_data(que_data_codes: List[str] = ["orig"], with_dup: bool = False) -> Dict[str, DatasetDict]:
    """Load the multilingual data from local files

    Args:
        que_data_codes (list, optional): Which quechua data to load, default loads only the original task's data. Defaults to ["orig"].
        with_dup (bool, optional): Whether to load the duplicate data or not. Defaults to False.
    Returns:
        Dict[str, DatasetDict]: returns a dictionary with the datasets for each language
    """
    datasets = {tgt_lang: read_data_into_hf(tgt_lang) for tgt_lang in DATA_CODES if tgt_lang != "quechua"}
    datasets["quechua"] = load_quechua_data(que_data_codes, with_dup)["quechua"]
    return datasets


def create_data_sample(src_text: str, tgt_text: str) -> Dict[str, Dict[str, str]]:
    """Create a data sample in the format required by the HF datasets library for MT systems

    Args:
        src_text (str): Source text
        tgt_text (str): Target text

    Returns:
        Dict[str, Dict[str, str]]: The data sample
    """
    return {"translation": {"src": src_text, "tgt": tgt_text}}


def create_sub_folder_data_path(tgt_lang: str, src_lang: str = SRC_LANG) -> str:
    """Create the path to the subfolder containing the data for the given language pair

    Args:
        tgt_lang (str): Target language
        src_lang (str, optional): Source language. Defaults to SRC_LANG ("spanish").

    Returns:
        str: The path to the subfolder containing the data for the given language pair
    """
    sub_folder = f"{tgt_lang}-{src_lang}"
    data_path = os.path.join(MAIN_FOLDER_PATH, sub_folder)
    return data_path


def read_data(
    data_path: str, subfolder: str, file_name: str, tgt_code: str, src_code: str = SRC_LANG_CODE
) -> Tuple[List[str], List[str]]:
    """Read the data for the given language pair from the given path

    Args:
        data_path (str): Folder containing the data
        subfolder (str): Subfolder containing the data for the given language pair
        file_name (str): Name of the file containing the data
        tgt_code (str): Target language code (for the extension of the file)
        src_code (str, optional): Source language code (for the extension of the file). Defaults to SRC_LANG_CODE ("es").

    Returns:
        Tuple[List[str], List[str]]: The target and source data
    """
    tgt_lang_path = os.path.join(data_path, subfolder, f"{file_name}.{tgt_code}")
    src_lang_path = os.path.join(data_path, subfolder, f"{file_name}.{src_code}")

    tgt_data = open(tgt_lang_path, "r").readlines()
    src_data = open(src_lang_path, "r").readlines()

    tgt_data = [line.strip() for line in tgt_data]
    src_data = [line.strip() for line in src_data]
    return tgt_data, src_data


def convert_data_into_hf(
    tgt_data: List[str], src_data: List[str]
) -> Dataset:
    """Convert the data into the format required by the HF datasets library for MT systems

    Args:
        tgt_data (List[str]): Target data
        src_data (List[str]): Source data
    Returns:
        Dataset: The dataset in the format required by the HF datasets library for MT systems
    """
    data = []
    for tgt_row, src_row in zip(tgt_data, src_data):
        if tgt_row and src_row:
            data.append(
                create_data_sample(
                    src_text=src_row,
                    tgt_text=tgt_row,
                )
            )
    return Dataset.from_list(data)


def read_data_into_hf(
    tgt_lang: str, data_paths: List[str] | None = None, duplicates: List[str] | None = None
) -> DatasetDict:
    """Read the data for the given language pair into the format required by the HF datasets library for MT systems

    Args:
        tgt_lang (str): Target language
        data_paths (List[str] | None, optional): Specific data paths (especially for data other than original training). Defaults to None.
        duplicates (List[str] | None, optional): Duplicates (data to exclude). Defaults to None.

    Returns:
        DatasetDict: The dataset in the format required by the HF datasets library for MT systems (both train and dev)
    """
    tgt_code = DATA_CODES[tgt_lang]
    lang_data_path = create_sub_folder_data_path(tgt_lang)

    train_tgt_data, train_src_data = [], []

    if data_paths is None:
        train_tgt_data, train_src_data = read_data(os.path.join(lang_data_path, "original"), "train", "train", tgt_code)
    else:
        for path in data_paths:
            if path in duplicates:
                continue
            else:
                file_name = "_".join(path.split("/")[-1].split("_")[:-1])
                tgt_data, src_data = read_data(lang_data_path, path, file_name, tgt_code)
                train_tgt_data.extend(tgt_data)
                train_src_data.extend(src_data)
                print(f"Data read from {path} | Count: {len(tgt_data)} | {len(src_data)}")

    dev_tgt_data, dev_src_data = read_data(lang_data_path, "dev", "dev", tgt_code)

    print(f"Lang: {tgt_lang.capitalize()} | Train Count: {len(train_tgt_data)} | Dev Count: {len(dev_tgt_data)}")
    return DatasetDict(
        {
            "train": convert_data_into_hf(train_tgt_data, train_src_data),
            "dev": convert_data_into_hf(dev_tgt_data, dev_src_data),
        }
    )

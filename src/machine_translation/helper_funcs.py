import os
from constants import DATA_CODES, SRC_LANG, SRC_LANG_CODE, MAIN_FOLDER_PATH
from datasets import Dataset, DatasetDict

TGT_LANG_CODE = "quy"

def create_data_sample(src_text, tgt_text, src_code=SRC_LANG_CODE, tgt_code=TGT_LANG_CODE):
  return {
      "translation": {
          src_code: src_text,
          tgt_code: tgt_text
      }
  }

def create_sub_folder_data_path(tgt_lang, src_lang=SRC_LANG):
  sub_folder = f"{tgt_lang}-{src_lang}"
  data_path = os.path.join(MAIN_FOLDER_PATH, sub_folder)
  return data_path


def read_data(data_path, subfolder, file_name, tgt_code, src_code=SRC_LANG_CODE):
  tgt_lang_path = os.path.join(data_path, subfolder, f"{file_name}.{tgt_code}")
  src_lang_path = os.path.join(data_path, subfolder, f"{file_name}.{src_code}")

  tgt_data = open(tgt_lang_path, "r").readlines()
  src_data = open(src_lang_path, "r").readlines()

  tgt_data = [line.strip() for line in tgt_data]
  src_data = [line.strip() for line in src_data]
  return tgt_data, src_data


def convert_data_into_hf(tgt_data, src_data, tgt_code=TGT_LANG_CODE, src_code=SRC_LANG_CODE):
  data = []
  for tgt_row, src_row in zip(tgt_data, src_data):
      if tgt_row and src_row:
          data.append(create_data_sample(
              src_text=src_row,
              tgt_text=tgt_row,
              src_code=src_code,
              tgt_code=tgt_code,
          ))
  return Dataset.from_list(data)


def read_data_into_hf(tgt_lang, data_paths=None, duplicates=None):
  tgt_code = DATA_CODES[tgt_lang]
  lang_data_path = create_sub_folder_data_path(tgt_lang)

  train_tgt_data, train_src_data = [], []
  if data_paths is None:
      train_tgt_data, train_src_data = read_data(lang_data_path, "train", "train", tgt_code)
  else:
    for path in data_paths:
      if path in duplicates:
        continue
      else:
        file_name = "_".join(path.split("/")[-1].split("_")[:-1])
        tgt_data, src_data = read_data(lang_data_path, path, file_name, tgt_code)
        train_tgt_data.extend(tgt_data)
        train_src_data.extend(src_data)

        print(f"{path} {len(tgt_data)} {len(src_data)}")
        
  dev_tgt_data, dev_src_data = read_data(lang_data_path, "dev", "dev", tgt_code)

  return DatasetDict({
      "train": convert_data_into_hf(train_tgt_data, train_src_data),
      "dev": convert_data_into_hf(dev_tgt_data, dev_src_data)
  })
    



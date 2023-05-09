
MAIN_FOLDER_PATH = "/home2/s4992113/MT-Project/MT-SharedTask/data/parallel-data/"
DATA_CODES = {
    "ashaninka": "cni",
    "aymara": "aym",
    "bribri": "bzd",
    "chatino": "czn",
    "guarani": "gn",
    "hñähñu": "oto",
    "nahuatl": "nah",
    "raramuri": "tar",
    "shipibo_konibo": "shp",
    "wixarika": "hch",
    "quechua": "quy"
}


ORIGINAL_DATA_PATHS = [
    "original/jw300_quy",
    "original/dict_misc_quy",
    "original/minedu_quy",
    "original/jw300_quz/",
]

EXTRA_DATA_PATHS = {
    "quy": [
        "extra/bible_quy",
        "extra/bol_const_quy",
        "extra/per_const_quy",
        "extra/lexicon_quy",
        "extra/handbook_quy",
        "extra/web_misc_quy",
        "extra/tatoeba_quy"
    ],
    "quz": [
        "extra/per_const_quz",
        "extra/reglamento_quz",
        "extra/cosude_quz",
        "extra/dw_quz",
        "extra/fundacion_quz"
    ],
    "que": [
        "extra/ley_consumo_drogas_que",
        "extra/ley_organica_alimentacion_que",
        "extra/ley_soberania_alimentaria_que",
        "extra/un_human_rights_que",
        "extra/ec_const_que",
        "extra/little_prince_que"
    ],
    "copy": [       
        "copied/llamacha_quy",
        "copied/wiki_quy",
        "copied/cc_qu_quy"
    ],
    "bcktr": [
        "backtranslation/comentarios_reales_quy",
        "backtranslation/cronica_del_peru_quy",
        "backtranslation/nueva_coronica_y_buen_gobierno_quy"
    ],
    "aymara": [
        "aymara/aymara_quy"
    ]
}

QUECHUA_DUPLICATES = [
    "original/jw300_quz/",
    "extra/per_const_quz",
]

SRC_LANG = "spanish"
SRC_LANG_CODE = "es"

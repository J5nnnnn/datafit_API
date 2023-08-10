import sys
import pandas as pd
import sklearn
import platform
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


import tensorflow as tf
# print(tf.__version__)
import tensorflow_hub as hub
import tensorflow_text as text
import tensorflow.keras


from tqdm.auto import tqdm
import transformers
from transformers import AutoTokenizer,TFDistilBertModel, DistilBertConfig, BertTokenizer
from transformers import TFAutoModel
# from google.colab import files
import io
from transformers import TFAutoModelForSequenceClassification
from sklearn import preprocessing


from datasets import load_dataset
from datasets import Dataset, DatasetDict

from transformers import DefaultDataCollator
from transformers import BertTokenizer

import time


# TODO num_labels need to updated with new dataset
params = {
    "bert": "cahya/bert-base-indonesian-522M",
    "num_labels": 42,
    "return_tensors": "tf",
    "batch_size": 32,
    "epochs": 10,
    "padding": "max_length",
    "max_length": 100,
    "truncation": True
}

params_sub = {
    "bert": "distilbert-base-multilingual-cased",
    "num_labels": 185,
    "return_tensors": "tf",
    "batch_size": 32,
    "epochs": 5,
    "padding": "max_length",
    "max_length": 100,
    "truncation": True
}


def load_model():
    new_model = TFAutoModelForSequenceClassification.from_pretrained(params['bert'], num_labels=params['num_labels'])
    new_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=5e-5),loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),metrics=tf.metrics.SparseCategoricalAccuracy(),)

    new_model.load_weights('./checkpoints/my_checkpoint')
    return new_model


def load_model_sub():
    new_model_sub = TFAutoModelForSequenceClassification.from_pretrained(params_sub['bert'], num_labels=params_sub['num_labels'])
    new_model_sub.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=5e-5),loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),metrics=tf.metrics.SparseCategoricalAccuracy(),)

    new_model_sub.load_weights('./Checkpoints_subcat/my_checkpoint')
    return new_model_sub


def tokenize_function(examples):
    tokenizer = BertTokenizer.from_pretrained(params['bert'])
    return tokenizer(examples["name"], padding=params["padding"], truncation=params["truncation"], max_length= params["max_length"])


def tokenize_function_sub(examples):
    tokenizer = AutoTokenizer.from_pretrained(params_sub['bert'])
    return tokenizer(examples["name"], padding=params_sub["padding"], truncation=params_sub["truncation"], max_length= params_sub["max_length"])



def payload_preprocessing(new_model, sub_model, payload):
    # just process current given input
    t1 = time.time()
    df = pd.read_csv('product_category_data.csv')

    t2 = time.time()

    label_encoder = preprocessing.LabelEncoder()
    ## Encode labels in column 'top_category'
    label_encoder.fit_transform(df['top_category'])

    label_encoder_sub = preprocessing.LabelEncoder()
    label_encoder_sub.fit_transform(df['sub_category'])

    t3 = time.time()

    pred_df = pd.DataFrame(payload, columns=["name"])

    pred_dict = {
        'pred': Dataset.from_pandas(pred_df)
    }
    pred_dataset = DatasetDict(pred_dict)
    # pred_dataset['pred'] = pred_dataset['pred'].remove_columns('__index_level_0__')

    tokenized_pred_datasets = pred_dataset['pred'].map(tokenize_function)
    tokenized_pred_datasets_sub = pred_dataset['pred'].map(tokenize_function_sub)

    data_collator = DefaultDataCollator(return_tensors=params['return_tensors'])
    tf_pred_dataset = tokenized_pred_datasets.to_tf_dataset(
        columns=["attention_mask", "input_ids", "token_type_ids"],
        label_cols=None,
        shuffle=False,
        collate_fn=data_collator,
        batch_size=params['batch_size'],)
    
    tf_pred_dataset_sub = tokenized_pred_datasets_sub.to_tf_dataset(
        columns=["attention_mask", "input_ids"],
        label_cols=None,
        shuffle=False,
        collate_fn=data_collator,
        batch_size=params['batch_size'],)

    t4 = time.time()
    pred_logits = new_model.predict(tf_pred_dataset).logits
    pred_logits_sub = sub_model.predict(tf_pred_dataset_sub).logits
    t5 = time.time()
    res = np.argmax(pred_logits, axis=-1)
    res_sub = np.argmax(pred_logits_sub, axis=-1)

    predicted_label = label_encoder.inverse_transform(res)
    predicted_label_sub = label_encoder_sub.inverse_transform(res_sub)

    t6 = time.time()
    print(predicted_label_sub)

    print("load csv: ", t2 - t1, " s")
    print("label encoder: ", t3 - t2, " s")
    print("tokonize: ", t4 - t3, " s")
    print("model predict: ", t5 - t4, " s")
    print("inverse transform: ", t6 - t5, " s")

    top = predicted_label.tolist()
    sub = predicted_label_sub.tolist()

    return convert_json(top, sub)


def convert_json(l1, l2):
    res = dict()
    res["sub"] = l2
    res['top'] = l1

    return res

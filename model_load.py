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


def load_model():
    new_model = TFAutoModelForSequenceClassification.from_pretrained(params['bert'], num_labels=params['num_labels'])
    new_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=5e-5),loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),metrics=tf.metrics.SparseCategoricalAccuracy(),)

    new_model.load_weights('./checkpoints/my_checkpoint')
    return new_model


def tokenize_function(examples):
    tokenizer = BertTokenizer.from_pretrained(params['bert'])
    return tokenizer(examples["name"], padding=params["padding"], truncation=params["truncation"], max_length= params["max_length"])


def payload_preprocessing(new_model, payload):
    # just process current given input
    df = pd.read_csv('product_category_data.csv')

    label_encoder = preprocessing.LabelEncoder()
    ## Encode labels in column 'top_category'
    label_encoder.fit_transform(df['top_category'])

    pred_df = pd.DataFrame(payload, columns=["name"])

    pred_dict = {
        'pred': Dataset.from_pandas(pred_df)
    }
    pred_dataset = DatasetDict(pred_dict)
    # pred_dataset['pred'] = pred_dataset['pred'].remove_columns('__index_level_0__')

    tokenized_pred_datasets = pred_dataset['pred'].map(tokenize_function)

    data_collator = DefaultDataCollator(return_tensors=params['return_tensors'])
    tf_pred_dataset = tokenized_pred_datasets.to_tf_dataset(
        columns=["attention_mask", "input_ids", "token_type_ids"],
        label_cols=None,
        shuffle=False,
        collate_fn=data_collator,
        batch_size=params['batch_size'],)

    pred_logits = new_model.predict(tf_pred_dataset).logits
    res = np.argmax(pred_logits, axis=-1)

    predicted_label = label_encoder.inverse_transform(res)

    return predicted_label.tolist()


# def main():
#     model = load_model()

#     print(payload_preprocessing(model))


# if __name__ == "__main__":
#     main()

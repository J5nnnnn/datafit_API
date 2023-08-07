import time

import pandas as pd
import tensorflow as tf
import numpy as np

from sklearn import preprocessing


def load_model():
    new_model = tf.keras.models.load_model('saved_model_rnn/lstm_model')
    return new_model


def payload_preprocessing(new_model, payload):
    # just process current given input
    t1 = time.time()
    df = pd.read_csv('product_category_data.csv')

    t2 = time.time()

    label_encoder = preprocessing.LabelEncoder()
    ## Encode labels in column 'top_category'
    label_encoder.fit_transform(df['top_category'])

    t3 = time.time()

    input_tensor = tf.constant(payload)

    t4 = time.time()
    pred_logits = new_model.predict(input_tensor)
    t5 = time.time()
    res = np.argmax(pred_logits, axis=-1)

    predicted_label = label_encoder.inverse_transform(res)

    t6 = time.time()

    print("load csv: ", t2 - t1, " s")
    print("label encoder: ", t3 - t2, " s")
    print("input conversion: ", t4 - t3, " s")
    print("model predict: ", t5 - t4, " s")
    print("inverse transform: ", t6 - t5, " s")
    return predicted_label.tolist()

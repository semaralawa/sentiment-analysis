import re
import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification

# load model
model = TFBertForSequenceClassification.from_pretrained(
    "indobenchmark/indobert-base-p2")
# load tokenizer
tokenizer = BertTokenizer.from_pretrained("indobenchmark/indobert-base-p2")
# compile model
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=3e-5, epsilon=1e-08, clipnorm=1.0),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(
    from_logits=True),
    metrics=[tf.keras.metrics.SparseCategoricalAccuracy('accuracy')])
# load weight
model.load_weights('model/weight/test')


def preprocess(data):
    # Defining regex patterns.
    url_pattern = r"((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]*)"
    user_pattern = '@[^\s]+'
    alpha_pattern = "[^a-zA-Z0-9]"
    sequence_pattern = r"(.)\1\1+"
    seq_replace_pattern = r"\1\1"

    data = data.lower()
    # Replace all URls with 'URL'
    data = re.sub(url_pattern, ' URL', data)
    # Replace @USERNAME to 'USER'.
    data = re.sub(user_pattern, ' USER', data)
    # Replace all non alphabets.
    data = re.sub(alpha_pattern, " ", data)
    # Replace 3 or more consecutive letters by 2 letter.
    data = re.sub(sequence_pattern, seq_replace_pattern, data)
    # save to list
    data = data.strip()

    return data


def predict(input):
    input = preprocess(input)
    # start predicting
    tf_batch = tokenizer(input, max_length=128, padding=True,
                         truncation=True, return_tensors='tf')
    # print(tf_batch)
    tf_outputs = model(tf_batch)
    tf_predictions = tf.nn.softmax(tf_outputs[0], axis=-1)
    # print()
    labels = ['Positive', 'netral', 'Negative']
    label = tf.argmax(tf_predictions, axis=1)
    # print(label)
    label = label.numpy()

    print(labels[label[0]])
    return (labels[label[0]], tf_predictions.numpy()[0][label[0]])


def testa(input):
    return ('negative', 50)

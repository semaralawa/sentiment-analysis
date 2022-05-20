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
model.load_weights('model/test')


def predict(input):
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

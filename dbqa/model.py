from keras.models import Model
from keras.layers import *
from keras import backend as K
from keras.preprocessing.sequence import pad_sequences
from embedding import *


def padding_dataset(dataset, max_len = None):
    for i in xrange(len(dataset)):
        # if dataset[i] is None or len(dataset[i]) == 0:
        #     dataset = [0.0]
        dataset[i] = numpy.asarray(dataset[i], dtype='float32')+1 # 0 could not be used, because 0 is <padding>

    if max_len is None:
        dataset = pad_sequences(dataset, value=0)
        max_len = len(dataset[0])
    else:
        dataset = pad_sequences(dataset, value=0, maxlen=max_len)
    print('     max sentence length after padding: %d'%len(dataset[0]))
    return numpy.asarray(dataset), max_len


def build_mdl(len_words, embed_dim, embeds, len_sent1, len_sent2):
    embeds.insert(0, np.zeros(embeds[0].shape, dtype='float32'))  # for padding

    input_q = Input(shape=(len_sent1,), dtype='int32')
    input_a = Input(shape=(len_sent2,), dtype='int32')
    embed = Embedding(mask_zero=True, input_dim=len_words+1, output_dim=embed_dim,
                      weights=[np.array(embeds)], dropout=0.2)
    x_q = embed(input_q)
    x_a = embed(input_a)
    rnn_q = LSTM(64, input_dim=embed_dim, return_sequences=False, input_length=len_sent1)(x_q)
    rnn_a = LSTM(64, input_dim=embed_dim, return_sequences=False, input_length=len_sent2)(x_a)
    dense_q = Dense(32)(rnn_q)
    dense_a = Dense(32)(rnn_a)

    def cosine(x):
        axis = len(x[0]._keras_shape) - 1
        dot = lambda a, b: K.batch_dot(a, b, axes=axis)
        return dot(x[0], x[1]) / K.sqrt(dot(x[0], x[0]) * dot(x[1], x[1]))

    # https://github.com/fchollet/keras/issues/2299
    cosine_sim = merge([dense_q, dense_a], mode=cosine, output_shape=(1,))
    model = Model(input=[input_q, input_a], output=[cosine_sim])
    model.compile(optimizer='rmsprop', loss='mse')
    return model

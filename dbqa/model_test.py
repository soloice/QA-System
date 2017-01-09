from model import *
from preprocess import *
import time


def dump(arr, info):
    tm = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    fh = open('../../data/res/dbqa/' + info + '-' + tm + '.npy', 'w')
    np.save(fh, arr)
    fh.close()


fold = 10.0  # 1/10 of the whole training data will be removed from
# training_xxx and used as fake test data after model.fit()
validation_split = 0.1 # 0.1 of will be used as develop set when fitting

if __name__ == '__main__':

    print('... loading embedding')
    p = Preprocessor()
    p.load_dictionary(dict_name='../../data/dbqa.word2vec.wordlist.txt')

    print('... loading data')
    p.load_training_data(cut_off=200) # from pkl
    # data_size = int(len(p.labels_training) * (fold-1) / fold) # train size + validation size
    # data_size = 10
    # print('     %d for training, %d for testing'%(data_size, len(p.labels_training)-data_size))

    # padding
    p.questions_training, sent_len1 = padding_dataset(p.questions_training)
    p.answers_training, sent_len2 = padding_dataset(p.answers_training)

    print('... building model')
    wordlist, embeds, len_words, embed_dim = get_word2vec()
    model = build_mdl(len_words, embed_dim, embeds, sent_len1, sent_len2)

    print('... fitting')
    for i in xrange(20):
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print 'Epoch', i
        model.fit([p.questions_training, p.answers_training], p.labels_training,
                  batch_size=100, nb_epoch=1, validation_split=0.1, shuffle=True, verbose=True)
        pred = model.predict([p.questions_training, p.answers_training], verbose=1)
        # print pred.ravel()
        dump(pred.ravel(), 'train-epoch' + str(i))

    # print('... fitting')
    # for i in xrange(20):
    #     print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    #     print 'Epoch', i
    #     model.fit([p.questions_training[:data_size], p.answers_training[:data_size]], p.labels_training[:data_size],
    #               batch_size=100, nb_epoch=1, validation_split=0.1, shuffle=True, verbose=True)
    #     pred = model.predict([p.questions_training[:data_size], p.answers_training[:data_size]], verbose=1)
    #     # print pred.ravel()
    #     dump(pred.ravel(), 'train-epoch' + str(i))

    # TODO: may add dumping step

    print('... predicting on real test set')
    print('Current time:')
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    p.load_testing_data(cut_off=200) # load from pkl
    p.questions_testing, _ = padding_dataset(p.questions_testing, max_len=sent_len1)
    p.answers_testing, _ = padding_dataset(p.answers_testing, max_len=sent_len2)
    pred = model.predict([p.questions_testing, p.answers_testing], verbose=1)

    # TODO: add output module
    dump(pred, 'test')
    print('done')


'''python model_test.py
Using Theano backend.
... loading embedding
... loading data
     10 for training, 181872 for testing
     max sentence length after padding: 37
     max sentence length after padding: 2077
... building model
... fitting
Train on 9 samples, validate on 1 samples
Epoch 1/10
9/9 [==============================] - 1s - loss: 0.0343 - val_loss: 0.0050
Epoch 2/10
9/9 [==============================] - 1s - loss: 0.0054 - val_loss: 0.0047
Epoch 3/10
9/9 [==============================] - 1s - loss: 0.0183 - val_loss: 9.5107e-04
Epoch 4/10
9/9 [==============================] - 1s - loss: 0.0122 - val_loss: 2.5545e-06
Epoch 5/10
9/9 [==============================] - 1s - loss: 0.0044 - val_loss: 1.4764e-04
Epoch 6/10
9/9 [==============================] - 1s - loss: 0.0041 - val_loss: 5.2885e-04
Epoch 7/10
9/9 [==============================] - 1s - loss: 0.0028 - val_loss: 7.3046e-04
Epoch 8/10
9/9 [==============================] - 1s - loss: 0.0294 - val_loss: 4.3623e-07
Epoch 9/10
9/9 [==============================] - 1s - loss: 0.0026 - val_loss: 7.4439e-05
Epoch 10/10
9/9 [==============================] - 1s - loss: 0.0129 - val_loss: 0.0013
... predicting on fake test set
... statistic
0 - -0.06 = 0.06
0 - 0.14 = -0.14
0 - 0.10 = -0.10
0 - 0.18 = -0.18
1 - -0.08 = 1.08
0 - 0.10 = -0.10
0 - 0.07 = -0.07
0 - 0.13 = -0.13
1 - 0.08 = 0.92
0 - 0.14 = -0.14
avrg_error: 0.1216
... predicting on real test set
     max sentence length after padding: 37
     max sentence length after padding: 2077
done'''


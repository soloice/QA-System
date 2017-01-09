# coding=utf-8
import sys
import gl
import codecs
# import jieba.posseg as pseg
# import jieba
import numpy as np
import pickle
reload(sys)
sys.setdefaultencoding('utf-8')


__author__ = 'soloice'


class Preprocessor:
    def __init__(self):
        self.questions_training, self.questions_testing = [], []
        self.answers_training, self.answers_testing = [], []
        self.labels_training, self.labels_testing, self.labels_dev = [], [], []
        self.unknown_word = ['<UNKNOWN>', '<DIGITS>', '<ALPHA>', '<ALPHA_NUM>']
        self.index_to_word, self.word_to_index = {}, {}
        for i, word in enumerate(self.unknown_word):
            self.index_to_word[i] = word
            self.word_to_index[word] = i
        self.vocab_size = len(self.unknown_word)

    def clear_data(self):
        self.questions_training, self.questions_testing = [], []
        self.answers_training, self.answers_testing = [], []
        self.labels_training, self.labels_testing = [], []

    def special_words(self, w):
        if w.isdigit():
            return 1  # '<DIGITS>'
        elif sum([(0 if c in 'qwertyuiopasdfghjklzxcvbnm' else 1) for c in w.lower()])==0:
            return 2  # '<ALPHA>'
        elif sum([(0 if c in 'qwertyuiopasdfghjklzxcvbnm01234567890' else 1) for c in w.lower()])==0:
            return 3  # '<ALPHA_NUM>'
        else:
            return 0  # '<UNKNOWN>'

    def word_list_to_index_list(self, sentence, insert_new_word_into_dict=False):
        def get_index(w):
            if w in self.word_to_index:
                return self.word_to_index.get(w, self.special_words(w))
            else:
                return self.special_words(w)

        if insert_new_word_into_dict:
            for word in sentence:
                if word not in self.word_to_index:
                    self.word_to_index[word] = self.vocab_size
                    self.index_to_word[self.vocab_size] = word
                    self.vocab_size += 1

        return map(get_index, sentence)

    def index_list_to_word_list(self, sentence):
        return map(lambda index: self.index_to_word.get(index, self.unknown_word[0]), sentence)

    # def fit_on_corpus(self, corpus_file_name=gl.training_data_file_name, insert_new_word_into_dict = True):
    #     fh = codecs.open(corpus_file_name, 'r', encoding='utf-8')
    #     for i, line in enumerate(fh.readlines()):
    #         question, answer, label = self.replace_line(line).strip().split('\t')
    #         question = [word for word in jieba.cut(question)]
    #         answer = [word for word in jieba.cut(answer)]
    #         question = self.word_list_to_index_list(question, insert_new_word_into_dict)
    #         answer = self.word_list_to_index_list(answer, insert_new_word_into_dict)
    #         label = float(label)
    #         # words = pseg.cut(question)
    #         # print type(words)
    #         # for word, pos in words:
    #         #     print word, pos
    #         self.questions_training.append(question)
    #         self.answers_training.append(answer)
    #         self.labels_training.append(label)
    #         # if i < 10:
    #         #     print '/'.join(self.index_list_to_word_list(question)), \
    #         #         '/'.join(self.index_list_to_word_list(answer)), label
    #         if i % 10000 == 0:
    #             print 'Processed', i, 'lines...'
    #     fh.close()
    #     self.labels_training = np.array(self.labels_training)
    #     print 'Finish processing!'

    def replace_line(self,line):
        return line.replace('，', ',').replace('。', '.')\
            .replace('！', '!').replace('？', '?')\
            .replace('“', '"').replace('”', '"')

    # def load_test_data(self, corpus_file_name=gl.testing_data_file_name, label_available=False):
    #     fh = codecs.open(corpus_file_name, 'r', encoding='utf-8')
    #     for i, line in enumerate(fh.readlines()):
    #         line = self.replace_line(line)
    #         if label_available:
    #             question, answer, label = line.strip().split('\t')
    #             self.labels_testing.append(float(label))
    #         else:
    #             qa = line.split('\t')
    #             question = qa[0].strip()
    #             answer = qa[1].strip() # maybe empty!!!
    #
    #         question = [word for word in jieba.cut(question)]
    #         answer = [word for word in jieba.cut(answer)]
    #         question = self.word_list_to_index_list(question)
    #         answer = self.word_list_to_index_list(answer)
    #         self.questions_testing.append(question)
    #         self.answers_testing.append(answer)
    #         if i < 30:
    #             print '/'.join(self.index_list_to_word_list(question)), \
    #                 '/'.join(self.index_list_to_word_list(answer))
    #         if i % 10000 == 0:
    #             print 'Processed', i, 'lines...'
    #     fh.close()
    #     print 'Finish processing!'

    def load_dictionary(self, dict_name='../../data/my_dict.txt'):
        self.index_to_word, self.word_to_index = {}, {}
        fh = codecs.open(dict_name, 'r', encoding='utf-8')
        for i, line in enumerate(fh.readlines()):
            index, word = line.rstrip('\r\n').split('\t')
            index = int(index)
            self.word_to_index[word] = index
            self.index_to_word[index] = word
        self.vocab_size = len(self.word_to_index)
        fh.close()

    def save_dictionary(self, dict_name='../../data/my_dict.txt'):
        fh = codecs.open(dict_name, 'w', encoding='utf-8')
        assert self.vocab_size == len(self.index_to_word)
        assert self.vocab_size == len(self.word_to_index)
        for i in xrange(self.vocab_size):
            fh.write(str(i) + '\t' + self.index_to_word[i] + '\n')
        fh.close()

    def get_training_data(self):
        return self.questions_training, self.answers_training, self.labels_training

    def get_testing_data(self):
        return self.questions_testing, self.answers_testing, self.labels_testing

    def load_training_data(self, cut_off=None):
        # cut_off: whether to cut off too long sentences.
        with open(gl.train_pkl, 'rb') as pkl:
            self.questions_training, self.answers_training, self.labels_training = pickle.load(pkl)
        if cut_off is not None:
            assert type(cut_off) == int
            for i in xrange(len(self.answers_training)):
                if len(self.answers_training[i]) > cut_off:
                    self.answers_training[i] = self.answers_training[i][:cut_off]
        return self.questions_training, self.answers_training, self.labels_training

    def load_testing_data(self, cut_off=None):
        with open(gl.test_pkl, 'rb') as pkl:
            self.questions_testing, self.answers_testing, self.labels_testing = pickle.load(pkl)
        if cut_off is not None:
            assert type(cut_off) == int
            for i in xrange(len(self.answers_testing)):
                if len(self.answers_testing[i]) > cut_off:
                    self.answers_testing[i] = self.answers_testing[i][:cut_off]
        return self.questions_testing, self.answers_testing, self.labels_testing

    def reset(self):
        self.__init__()

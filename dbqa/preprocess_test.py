# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import jieba
from preprocess import Preprocessor
from embedding import *
import pickle

# Use case examples:
wordlist, embeds, len_words, embed_dim = get_word2vec()
write2word2vec(wordlist)

# Use an out-of-the-box dictionary
sent = u'“年”字有多少笔？	笔顺编号:311212,，?？!！.。>》\、'
sentence = [word for word in jieba.cut(Preprocessor().replace_line(sent))]
p = Preprocessor()
p.load_dictionary(dict_name='../data/dbqa.word2vec.wordlist.txt')
print len(p.word_to_index)
print '/'.join(sentence)
indices = p.word_list_to_index_list(sentence)
print indices
print '/'.join(p.index_list_to_word_list(indices))

# You may also want to fit the dictionary from corpus
#p.reset()
p.fit_on_corpus(insert_new_word_into_dict=False)
#p.save_dictionary()
print 'Vocab size:', p.vocab_size

# questions: list of sentences, where a sentence is a list comprising of word indices
# answers: list of sentences, where a sentence is a list comprising of word indices
# labels: a 1-D numpy array
# These 3 variables should share the same length.
questions, answers, labels = p.get_training_data()
print('writing '+gl.train_pkl)
with open(gl.train_pkl,'wb') as pkl:
    pickle.dump([questions, answers, labels],pkl)
print('done')
# if you want to transfer a sequence of indices into a sequence of words,
# you may want to use:
print '/'.join(p.index_list_to_word_list(questions[0]))
print '/'.join(p.index_list_to_word_list(answers[0]))

''''''

p.load_test_data(label_available=False)
questions, answers, _ = p.get_testing_data()
print('writing '+gl.test_pkl)
with open(gl.test_pkl,'wb') as pkl:
    pickle.dump([questions, answers, _],pkl)
print('done')
print '/'.join(p.index_list_to_word_list(questions[0]))
print '/'.join(p.index_list_to_word_list(answers[0]))

# coding=utf-8
from __future__ import division
import gl
import numpy as np
import codecs


class Similarity:
    def __init__(self, embedding_file_name=gl.embedding_file_name):
        self.word_embedding = {}
        fh = codecs.open(embedding_file_name, 'r', encoding='utf-8')
        for line in fh.readlines():
            tmp = line.split()
            word, embedding = tmp[0], np.array(map(float, tmp[1:]))
            self.word_embedding[word] = embedding
        fh.close()

    def similarity(self, w1, w2, lbda=0.6):
        so, sw = self.similarity_overlap(w1, w2), self.similarity_word_vector(w1, w2)
        return so if sw < 1e-6 else lbda * so + (1 - lbda) * sw

    def similarity_overlap(self, w1, w2):
        s1 = set(w1)
        s2 = set(w2)
        return len(s1 & s2) / len(s1 | s2)

    def similarity_word_vector(self, w1, w2):
        try:
            e1, e2 = self.word_embedding[w1], self.word_embedding[w2]
            cos_sim = np.dot(e1, e2) / (np.linalg.norm(e1) * np.linalg.norm(e2))
            return (cos_sim + 1.0) / 2.0
        except KeyError:
            # At least one of the words is not in the word_embedding file.
            return 0.0

if __name__ == '__main__':
    sim = Similarity()
    w1, w2 = u'我', u'你'
    print w1, w2
    print sim.similarity_word_vector(w1, w2)
    print sim.similarity_overlap(w1, w2)
    print sim.similarity(w1, w2)

    w1, w2 = u'北京大学', u'清华大学'
    print w1, w2
    print sim.similarity_word_vector(w1, w2)
    print sim.similarity_overlap(w1, w2)
    print sim.similarity(w1, w2)

    w1, w2 = u'1913年', u'1917年'
    print w1, w2
    print sim.similarity_word_vector(w1, w2)
    print sim.similarity_overlap(w1, w2)
    print sim.similarity(w1, w2)

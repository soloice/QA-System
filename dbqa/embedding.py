import gl
import numpy


def get_word2vec():
    fin = open(gl.embedding_file_name,'r')
    line = fin.readline().strip().split()

    len_words = int(line[0])
    embed_dim = int(line[1])
    wordlist = []
    embeds = []

    for i in range(len_words):
        line = fin.readline().strip().split()
        word = line[0]
        vector = numpy.array([float(item) for item in line[1:]], dtype='float32')
        embeds.append(vector)
        wordlist.append(word)
    fin.close()

    wordlist = ['<UNKNOWN>','<DIGITS>','<ALPHA>','<ALPHA_NUM>']+wordlist
    embeds.insert(0, numpy.zeros(embeds[0].shape, dtype='float32'))
    embeds.insert(0, numpy.zeros(embeds[0].shape, dtype='float32'))
    embeds.insert(0, numpy.zeros(embeds[0].shape, dtype='float32'))
    embeds.insert(0, numpy.average(embeds, axis=0))
    len_words+=4
    return wordlist, embeds, len_words, embed_dim


def write2word2vec(wordlist):
    with open('../data/dbqa.word2vec.wordlist.txt','w') as fout:
        for id,word in enumerate(wordlist):
            fout.write('%d\t%s\n'%(id, word))


if __name__ == '__main__':
    wordlist, embeds, len_words, embed_dim = get_word2vec()
    write2word2vec(wordlist)

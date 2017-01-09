# coding=utf-8
import codecs
import sys
import gl
import time

reload(sys)
sys.setdefaultencoding('utf-8')


class MentionID:
    def __init__(self):
        self.id_set = {}
        self.mention = {}

    def load_mention_2_id(self, knowledge_base_mention_file_name=gl.knowledge_base_mention_file_name):
        # Typically, it takes ~60s to load this file.
        t1 = time.time()
        fh = codecs.open(knowledge_base_mention_file_name, 'r', encoding='utf-8')
        for line_no, line in enumerate(fh.readlines()):
            try:
                mention, aliases = line.rstrip().split(' ||| ')
            except ValueError:
                # print 'Error at line', line_no
                # print 'Line content:', line.rstrip()
                continue
            aliases_list = aliases.split('\t')
            self.id_set[mention] = set(aliases_list)
            # for alias in aliases_list:
            #     self.mention[alias] = mention
        fh.close()
        t2 = time.time()
        print 'Loading mention2id consumed', t2 - t1, 'seconds'

    def show(self, first_n=20):
        for i, mention in enumerate(self.id_set.keys()):
            print i, mention
            for alias in self.id_set[mention]:
                print 'Possible alias:', alias
            if i > first_n:
                break

    def show_id_set(self, mention):
        if mention in self.id_set:
            print mention, 'in mention2id'
            for some_id in self.id_set[mention]:
                print some_id
            return self.id_set[mention]
        else:
            print 'Unfortunately,' + mention + 'not found!'
            return set([])

    def find_id_set(self, mention):
        if mention in self.id_set:
            return self.id_set[mention]
        else:
            return set([])

if __name__ == '__main__':
    mid = MentionID()
    mid.load_mention_2_id()
    s = u'《 机械 设计 基础 》'
    mid.show_id_set(s)

    while True:
        s = input()
        s = s.decode('utf-8')
        print type(s), s
        t1 = time.time()
        mid.show_id_set(s)
        t2 = time.time()
        print 'Query on string', s, 'consumed', t2 - t1, 'seconds'
        if s == 'EXIT':
            break

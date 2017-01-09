import codecs
import sys
import gl
import time
import mention_id
reload(sys)
sys.setdefaultencoding('utf-8')


class KnowledgeBase:
    def __init__(self):
        self.knowledge_about = {}

    def load_knowledge_base(self, knowledge_file_name=gl.knowledge_base_file_name):
        # Typically, it takes ~130s to load this file.
        t1 = time.time()
        fh = codecs.open(knowledge_file_name, 'r', encoding='utf-8')
        total_line_number, skipped = 0, 0
        for line_no, line in enumerate(fh.readlines()):
            # if line_no > 101840:
            #     print 'line content:', line.rstrip()
            total_line_number += 1
            if line_no % 1000000 == 0:
                print 'Processed', line_no, 'lines'
            try:
                entity1, predicate, entity2 = line.rstrip().split(' ||| ')
            except ValueError:
                skipped += 1
                continue
                # print line.rstrip()
                # print 'Split by |||:'
                # for item in line.rstrip().split('|||'):
                #     print item
                # print 'Split by < >|||< >:'
                # for item in line.rstrip().split(' ||| '):
                #     print item
                # print 'Error at line', line_no
                # exit(1)
            try:
                self.knowledge_about[entity1].append((predicate, entity2))
            except KeyError:
                self.knowledge_about[entity1] = [(predicate, entity2)]
        fh.close()
        print 'total line number:', total_line_number
        print 'skipped:', skipped

        for entity in self.knowledge_about.keys():
            self.knowledge_about[entity] = set(self.knowledge_about[entity])
        t2 = time.time()
        print 'Loading knowledge base consumed', t2 - t1, 'seconds'

    def show(self, first_n=20):
        for i, entity in enumerate(self.knowledge_about.keys()):
            # print entity, len(entity)
            print entity
            for predicate, entity2 in self.knowledge_about[entity]:
                # print predicate, len(predicate), type(predicate), entity2, len(entity2), type(entity2)
                print '\t', predicate, entity2
            if i > first_n:
                break

    def show_entity(self, entity):
        if entity in self.knowledge_about:
            print entity, 'in knowledge base! attributes:'
            for item in self.knowledge_about[entity]:
                predicate, entity2 = item
                print predicate, entity2
            pass
        else:
            print 'Unfortunately,' + entity + 'not found!'

if __name__ == '__main__':
    kb = KnowledgeBase()
    kb.load_knowledge_base()
    mid = mention_id.MentionID()
    mid.load_mention_2_id()
    while True:
        s = input()
        s = s.decode('utf-8')
        print type(s), s
        t1 = time.time()
        possible_ids = {s} | mid.show_id_set(s)
        for pid in possible_ids:
            print 'Possible id:', pid
            kb.show_entity(pid)
        t2 = time.time()
        print 'Query on string', s, 'consumed', t2 - t1, 'seconds'
        if s == 'EXIT':
            break

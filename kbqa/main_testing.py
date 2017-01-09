import codecs
import sys
import gl
import query
import similarity
import time
import mention_id
import knowledge_base
import mention_extractor
reload(sys)
sys.setdefaultencoding('utf-8')


if __name__ == '__main__':
    # Step1: load knowledge base
    kb = knowledge_base.KnowledgeBase()
    kb.load_knowledge_base()

    # Step2: load mention2id
    mid = mention_id.MentionID()
    mid.load_mention_2_id()

    # training phase

    # Step3: load questions
    query_list = query.QueryList()
    query_list.read_query_file(gl.testing_data_split_file_name)
    me = mention_extractor.MentionExtractor()

    fh = codecs.open(gl.testing_data_result_file_name, 'w', encoding='utf-8')

    sim = similarity.Similarity()
    for qid, qry in enumerate(query_list.query_list):
        print 'query id:', qid+1

        # print '||||'.join(qry.tokens)
        entity, rest_token = me.get_entity(qry.tokens, qry.mentions)
        # print 'entity:' + entity + 'len(entity):' + str(len(entity))
        # print 'rest_token:', '----'.join(rest_token)
        # input('Press a digit to continue\n')
        possible_ids = mid.find_id_set(entity)
        # for pid in possible_ids:
        #     print 'possible id:(' + pid + ')' + str(len(pid))
        tokens = ''.join(qry.tokens)
        scores = [(sim.similarity(tokens, pid), pid) for pid in possible_ids]
        scores = sorted(scores, key=lambda s: -s[0])
        # for item in scores:
        #     print 'Score for ' + item[1] + ':', item[0]
        # input('*****************\n')

        if len(scores) == 0:
            scores = [(1.0, entity)]

        pid = scores[0][1]
        try:
            info = kb.knowledge_about[pid]
        except KeyError:
            try:
                info = kb.knowledge_about[entity]
            except KeyError:
                print 'Unfortunately,' + entity + 'not fount in the knowledge base'
                # return something
                fh.write('<question id=' + str(qid + 1) + '>\t')
                fh.write(tokens + '\n')
                fh.write('<answer id=' + str(qid + 1) + '>\t')
                fh.write('[THIS-IS-AN-ANSWER.]\n')
                print qid+1, '[THIS-IS-AN-ANSWER.]'
                fh.write('==================================================\n')
                continue
        best_match, best_match_score = ('[ATTRIBUTE]', '[THIS-IS-AN-ANSWER.]'), 0.0
        for attr, entity2 in info:
            for token in rest_token:  # tokens
                tmp_score = sim.similarity(attr, token)
                # print 'For pair (' + token + ', '+ attr + '), similarity = ', tmp_score
                if tmp_score > best_match_score:
                    best_match_score = tmp_score
                    best_match = (attr, entity2)

        for attr, entity2 in info:
            if attr in rest_token:
                best_match = (attr, entity2)
                break

        fh.write('<question id=' + str(qid + 1) + '>\t')
        fh.write(tokens + '\n')
        fh.write('<answer id=' + str(qid + 1) + '>\t')
        fh.write(best_match[1] + '\n')
        print qid+1, best_match[1]
        fh.write('==================================================\n')

        # print 'After bypath:'
        # print best_match[0], best_match[1]
    fh.close()

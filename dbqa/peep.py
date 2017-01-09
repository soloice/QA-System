# coding=utf-8
import codecs
import jieba
import gl
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def replace_line(line):
    return line.replace('，', ',').replace('。', '.').\
        replace('！', '!').replace('？', '?').replace('“', '"').replace('”', '"')

res = []

fh = codecs.open(gl.training_data_file_name, 'r', encoding='utf-8')
for i, line in enumerate(fh.readlines()):
    _, answer, _ = replace_line(line).strip().split('\t')
    # question = [word for word in jieba.cut(question)]
    answer = [word for word in jieba.cut(answer)]
    res.append(answer)
    if i % 10000 == 0:
        print 'Processed', i, 'lines...'
fh.close()

records_sorted_by_length = sorted(zip(xrange(1, len(res)+1), res), key=lambda x:len(x[1]))
nb_records = len(records_sorted_by_length)

k = 10000
for i in xrange(0, nb_records, k):
    print 'length at', i, ':', len(records_sorted_by_length[i][1])

for i in xrange(170000, nb_records, 1000):
    print 'length at', i, ':', len(records_sorted_by_length[i][1])

for i in xrange(181000, 181500, 100):
    print 'length at', i, ':', len(records_sorted_by_length[i][1])

for i in xrange(181500, nb_records, 10):
    print 'length at', i, ':', len(records_sorted_by_length[i][1])

for i in xrange(181880, nb_records):
    print 'length at', i, ':', len(records_sorted_by_length[i][1])

for item in records_sorted_by_length[0::10000]:
    print ' '.join(item[1])

cut_off = records_sorted_by_length[-10:]
for i in cut_off:
    print 'line number:', i[0], 'content:', ' '.join(i[1])
import gl
import codecs


class Query:
    def __init__(self, query_origin, answer, tokens, mentions):
        self.query_origin = query_origin
        self.answer = answer  
        self.tokens = tokens
        self.mentions = mentions


class QueryList:
    def __init__(self):
        self.query_list = []

    def read_query_file(self, file_name=gl.training_data_split_file_name):
        fh = codecs.open(file_name, 'r', encoding='utf-8')
        lines = fh.readlines()
        for i in range(0, len(lines), 5):
            # print i
            query = lines[i].strip()
            ans = lines[i+1].strip()
            tokens = lines[i+2].strip().split('\t')
            mentions = lines[i+3].strip().split('\t')
            query_tmp = Query(query, ans, tokens, mentions)
            self.query_list.append(query_tmp)
        fh.close()
        return self.query_list

# test
if __name__ == '__main__':
    ql = QueryList()
    ql.read_query_file()
    for i in range(20):
        print ql.query_list[i].query_origin
        print '||||'.join(ql.query_list[i].mentions)
        print '----------------------------------'

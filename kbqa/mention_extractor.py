# coding=utf-8
import query
import copy


class MentionExtractor:
    def __init__(self):
        self.stop_words = ['电视剧', '关于', '怎样', '书', '哪个', '有', '谁', '知道', '大家', '一', '本', '一本',
                           '叫', '到', '你', '比较', '好', '的', '做', '有人', '那', '新', '买', '过', '问', '下',
                           '什么', '了解', '能', '告诉', '我', '没', '没有', '呃', '…', '想', '电影', '游戏', '音乐',
                           '小说', '过', '去', '请教', '一下', '你们', '玩', '给', '大家', '你们', '玩', '给', '怎么',
                           '首', '认识', '还有', '与', '人', '家', '啥', '把', '有人', '请问', '时候', '很', '好奇',
                           '考', '考考', '考你', '是', '记得', '的', '得', '这', '记得']

    def calculate_mention(self, mention_split):
        count = 0
        for i in range(len(mention_split)):
            if mention_split[i] in self.stop_words:
                count += 1
        return count * 1.0 / len(mention_split)

    def get_entity(self, token_list, mention_list):
        best_entity = ''
        best_entity_list = []
        previous_mean_less = True
        for i in range(len(mention_list)):
            mention_split_tmp = mention_list[i].split(' ')
            mention_score = self.calculate_mention(mention_split_tmp)
            if mention_score > 0.5:
                if len(best_entity_list) > 0:
                    break
                previous_mean_less = True
            else:
                if previous_mean_less:
                    best_entity = copy.deepcopy(mention_list[i])
                    # print best_entity
                    best_entity_list = list(mention_split_tmp)
                    previous_mean_less = False
                else:
                    is_contain = True
                    for j in range(len(best_entity_list)):
                        # print '---'.join(mention_split_tmp)
                        if best_entity_list[j] not in mention_split_tmp:
                            is_contain = False
                            break
                    if not is_contain:
                        break
                    else:
                        best_entity = copy.deepcopy(mention_list[i])
                        # print mention_list[i]
                        # print best_entity
                        best_entity_list = list(mention_split_tmp)
                        # print '---'.join(best_entity_list)
                        previous_mean_less = False
        if len(best_entity_list) > 0:
            last_word = best_entity_list[-1]
            try:
                index = token_list.index(last_word)
            except ValueError:
                index = 0
        else:
            return best_entity, token_list
        if index >= len(token_list) - 1:
            return best_entity, token_list
        else:
            return best_entity, token_list[index + 1:-1]


if __name__ == '__main__':
    query_list = query.QueryList()
    query_list.read_query_file()
    entity_list = []
    tokens_list = []
    me = MentionExtractor()
    for ii in range(len(query_list.query_list)):
        print '||||'.join(query_list.query_list[ii].tokens)
        entity, last_token = me.get_entity(query_list.query_list[ii].tokens, query_list.query_list[ii].mentions)
        print entity
        print '---'.join(last_token)

import jieba
import jieba.posseg as pseg


class Tokenizer:
    def __init__(self, user_dicts=None):
        # 加载外部词典
        if user_dicts is not None:
            if type(user_dicts) not in (dict, tuple):
                user_dicts = [user_dicts]
            for dp in user_dicts:
                jieba.load_userdict(dp)

    @staticmethod
    def tokenize(sentence):
        seg = pseg.cut(sentence)
        return [(word, tag)
                for word, tag in seg]


if __name__ == '__main__':
    tokenizer = Tokenizer()
    while True:
        s = input('请输入句子：')
        result = tokenizer.tokenize(s)
        for t in result:
            print(t)

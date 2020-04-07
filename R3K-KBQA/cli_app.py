from query_management import *


if __name__ == '__main__':
    manager = QueryManager(verbose=True)
    print('=====三国小灵通QA系统=====')
    while True:
        ques = input('请输入您的问题：')
        query_note = manager.ask(ques)
        print(query_note['reply'])
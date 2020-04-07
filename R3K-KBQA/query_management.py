import copy
from SPARQLWrapper import SPARQLWrapper, JSON
from slot_recognition import *
from SPARQL_generation import *


class QueryManager:
    def __init__(self, verbose=False):
        self.__conn = SPARQLWrapper(ENDPOINT_URL)
        self.__verbose = verbose

    def set_verbose(self, verbose):
        if type(verbose) == bool:
            self.__verbose = verbose

    def ask(self, ques):
        query_success = True

        sentence = ques.replace('“', '"').replace('”', '"')

        recognition_result = SlotRecognizer.recognize(sentence)

        # 无法理解问题的情况处理
        if recognition_result is None:
            result_value = None
            result_reply = '对不起，我无法理解您的问题，请换种说法问我吧！'
            query_success = False
            if self.__verbose:
                print('*' * 13)
                print('答案内容：', result_value)
                print('答案回复：', result_reply)
                print('*' * 13)
            query_note = {'success': query_success,
                          'question': ques,
                          'result': result_value,
                          'reply': result_reply, }
            return query_note

        tid = recognition_result[0]
        arguments = recognition_result[1]
        template = templates[tid]
        temp_type = template['type']

        sparql = SparqlGenerator.generate_sparql_from_recognition_result(recognition_result)

        query_result = self.query(sparql)
        result_list = self.parse_result(query_result, temp_type)
        result_value = '、'.join(result_list)
        result_arguments = copy.deepcopy(arguments)
        result_arguments['value'] = result_value

        result_reply = None
        # 没有结果的处理
        if (temp_type == 'select' and result_value == '') or \
            (temp_type == 'count' and result_value == '0'):  # 继续跟踪查询是不是事件名等输错
            checks = template['checks']
            checks_note = []
            for check in checks:
                check_template = checks_templates[check]
                check_temp_type = check_template['type']
                check_sparql = SparqlGenerator.generate_sparql_from_check_template(check_template, arguments)
                check_query_result = self.query(check_sparql)
                check_result_list = self.parse_result(check_query_result, check_temp_type)
                check_result_value = '、'.join(check_result_list)
                if (check_temp_type == 'count' and check_result_value == '0') or \
                    (check_temp_type == 'select' and check_result_value == ''):
                    note = check_template['if_none_reply'].format(**arguments)
                    checks_note.append(note)
            checks_reply = '，'.join(checks_note)
            if checks_reply != '':
                checks_reply += '，'
                result_reply = '对不起，没有查询到结果。' + checks_reply + '请检查您的提问是否有误。'
                query_success = False
            else:
                result_reply = template['none_reply'].format(**arguments)
                query_success = True
        else:
            result_reply = template['reply'].format(**result_arguments)

        if self.__verbose:
            print('*' * 13)
            print('问题：', ques)
            print('模板ID：', tid)
            print('槽识别结果：', arguments)
            print('SPARQL：\n', sparql)
            print('请求返回结果：', query_result)
            print('答案内容：', result_value)
            print('答案回复：', result_reply)
            print('*' * 13)

        query_note = {'success': query_success,
                      'question': ques,
                      'template_id': tid,
                      'arguments': arguments,
                      'SPARQL': sparql,
                      'result': result_value,
                      'reply': result_reply, }

        return query_note

    def query(self, sparql, format=JSON):
        self.__conn.setQuery(sparql)
        self.__conn.setReturnFormat(format)
        query_result = self.__conn.query().convert()
        return query_result

    @staticmethod
    def parse_result(query_result, type):
        bindings = query_result['results']['bindings']
        result_list = []
        key_val = 'x'
        if type == 'count':
            key_val = 'callret-0'
        for item in bindings:
            value = item[key_val]['value']
            if type == 'select':
                index = value.find('#')
                value = value[index + 1:]
            result_list.append(value)
        return result_list

import refo


SPARQL_PREFIX = '''
prefix :      <http://ws.nju.edu.cn/tcqa#>
prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix owl:   <http://www.w3.org/2002/07/owl#>
prefix xsd:   <http://www.w3.org/2001/XMLSchema#>
prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
'''


SPARQL_TEMPLATES = {
    'select': '''
        select distinct ?x from <{graph_url}>
        where {{
            {sparql_expression}
        }}
    ''',
    'count': '''
        select count(?x) from <{graph_url}>
        where {{
            {sparql_expression}
        }}
    ''',
}


# 构造常用regex组件
def get_long_literal(text):
    long_literal = refo.Literal(text[0])
    for c in text[1:]:
        long_literal += refo.Literal(c)
    return long_literal


EVENT = get_long_literal('事件')  # refo.Literal('事') + refo.Literal('件')
QM = refo.Literal('"')
CHAP = get_long_literal('章节')  # refo.Literal('章') + refo.Literal('节')
ANY = refo.Star(refo.Any(), greedy=False)
HOWMANY = get_long_literal('几个') | get_long_literal('多少')  # refo.Literal('几') + refo.Literal('个') | refo.Literal('多') + refo.Literal('少')
PERSON = get_long_literal('人物')  # refo.Literal('人') + refo.Literal('物')

event_name = refo.Group(ANY, 'event_name')
person_name = refo.Group(ANY, 'person_name')
force_name = refo.Group(ANY, 'force_name')

ANY_SLOT_0 = refo.Group(ANY, 'ANY_SLOT_0')
ANY_SLOT_1 = refo.Group(ANY, 'ANY_SLOT_1')
ANY_SLOT_2 = refo.Group(ANY, 'ANY_SLOT_2')

templates = {
    1: {
        'name': '事件章节',
        'info': '给出指定事件在书中出现的章节',
        'slot_list': ['event_name'],
        'regex': ANY_SLOT_0 + QM + event_name + QM + ANY + CHAP + ANY,
        'slot_score': {
            'ANY_SLOT_0': {
                '事件': +200,
                '人物': -100,
                '势力': -100,
            }
        },
        'type': 'select',
        'sparql_expression': '''
            ?a rdf:type :事件.
            ?a :事件名 '{event_name}'.
            ?a :章节 ?x.
        ''',
        'reply': '事件“{event_name}”出现在书中的{value}。',
        'none_reply': '没有找到事件“{event_name}”在书中出现的位置。',
        'checks': ['event_name']
    },
    2: {
        'name': '事件人物个数',
        'info': '查询指定事件中涉及到的人物个数',
        'slot_list': ['event_name'],
        'regex': ANY_SLOT_0 + QM + event_name + QM + ANY_SLOT_1 + HOWMANY + ANY + PERSON + ANY,
        'slot_score': {
            'ANY_SLOT_0': {
                '事件': +200,
                '人物': -100,
                '势力': -100,
            },
            'ANY_SLOT_1': {
                '涉及': +200,
            }
        },
        'type': 'count',
        'sparql_expression': '''
            ?a rdf:type :事件.
            ?a :事件名 '{event_name}'.
            ?a :涉及人物 ?x.
            ?x rdf:type :人物.
        ''',
        'reply': '事件“{event_name}”涉及到的人物有{value}人。',
        'none_reply': '事件“{event_name}的涉及人数没有记录”。',
        'checks': ['event_name']
    },
    3: {
        'name': '事件人物',
        'info': '查询指定事件涉及到的人物',
        'slot_list': ['event_name'],
        'regex': ANY_SLOT_0 + QM + event_name + QM + ANY_SLOT_1 + PERSON + ANY_SLOT_2,
        'slot_score': {
            'ANY_SLOT_0': {
                '事件': +200,
                '人物': -100,
                '势力': -100,
            },
            'ANY_SLOT_1': {
                '涉及': +200,
                '多少': -150,
                '几个': -150,
            },
            'ANY_SLOT_2': {
                '多少': -150,
                '几个': -150,
            }
        },
        'type': 'select',
        'sparql_expression': '''
            ?a rdf:type :事件.
            ?a :事件名 '{event_name}'.
            ?a :涉及人物 ?x.
            ?x rdf:type :人物.
        ''',
        'reply': '“事件{event_name}”涉及到的人物有{value}。',
        'none_reply': '没有找到事件“{event_name}”涉及到的人物。',
        'checks': ['event_name']
    },
    4: {
        'name': '人物事件',
        'info': '查询指定人物参与的事件',
        'slot_list': ['person_name'],
        'regex': ANY_SLOT_0 + QM + person_name + QM + ANY + EVENT + ANY,
        'slot_score': {
            'ANY_SLOT_0': {
                '人物': +200,
                '事件': -100,
                '势力': -100,
            },
        },
        'type': 'select',
        'sparql_expression': '''
            ?a rdf:type :人物.
            ?a :姓名 '{person_name}'.
            ?x :涉及人物 ?a.
            ?x rdf:type :事件.
        ''',
        'reply': '人物“{person_name}”参与的事件有：{value}。',
        'none_reply': '在记录中，人物“{person_name}”没有参与的事件。',
        'checks': ['person_name']
    },
    5: {
        'name': '势力效忠人数',
        'info': '查询效忠指定势力的人物数量',
        'slot_list': ['force_name'],
        'regex': ANY_SLOT_0 + QM + force_name + QM + ANY + PERSON + ANY,
        'slot_score': {
            'ANY_SLOT_0': {
                '效忠': +200,
                '势力': +200,
                '政权': +150,
                '人物': -100,
                '事件': -100,
            },
        },
        'type': 'count',
        'sparql_expression': '''
            ?a rdf:type :势力.
            ?a :势力名 '{force_name}'.
            ?x :效忠势力 ?a.
            ?x rdf:type :人物.
        ''',
        'reply': '势力“{force_name}”的效忠者有{value}人。',
        'none_reply': '在记录中，势力“{force_name}”没有效忠的人物。',
        'checks': ['force_name']
    }
}

checks_templates = {
    'event_name': {
        'type': 'count',
        'sparql_expression': '''
            ?x rdf:type :事件.
            ?x :事件名 '{event_name}'.
        ''',
        'if_none_reply': '没有查询到名为“{event_name}”的事件'
    },
    'person_name': {
        'type': 'count',
        'sparql_expression': '''
            ?x rdf:type :人物.
            ?x :姓名 '{person_name}'.
        ''',
        'if_none_reply': '没有查询到名为“{person_name}”的人物'
    },
    'force_name': {
        'type': 'count',
        'sparql_expression': '''
        ?x rdf:type :势力.
        ?x :势力名 '{force_name}'.
    ''',
        'if_none_reply': '没有查询到名为“{force_name}”的势力'
    },
}

import refo
from templates import *


class SlotRecognizer:
    # 输入句子，输出最佳匹配结果，包括模板的id、模板槽的文字、匹配得分
    @staticmethod
    def recognize(sentence):
        matched_results = []  # 存放能够匹配的模板的结果，(template_id, arguments, score)

        for tid in templates.keys():  # 对于每一个模板进行匹配
            template = templates[tid]  # 当前正在匹配的模板
            result = SlotRecognizer.match(sentence, template)  # 匹配一个模板的结果，(True, arguments, score) or (False, )
            if result[0] is True:  # 如果当前模板能够匹配
                matched_results.append((tid, result[1], result[2]))  # 将匹配结果加入到matched_result列表中

        if len(matched_results) == 0:  # 如果没有模板能够匹配，返回None
            return None
        else:  # 如果有模板能够匹配，返回最佳匹配结果
            matched_results = sorted(matched_results, key=lambda x: x[2], reverse=True)  # 匹配的模板按照匹配得分从大到小进行排序
            return matched_results[0][0:2]

    # 输入句子和模板，输出匹配结果
    # 如果当前模板能够匹配句子，则输出(True, arguments, score), 其中arguments是匹配的槽的文字，score是匹配得分
    # 如果当前模板不能匹配句子，则输出(False,)
    @staticmethod
    def match(sentence, template):
        regex = template['regex']
        slot_list = template['slot_list']
        m = refo.search(regex, sentence)

        if m is None:
            return False,
        arguments = {}
        for slot in slot_list:
            m_span = m.span(slot)
            arguments[slot] = sentence[m_span[0]:m_span[1]]

        # 打分
        score = 0
        slots_score = template['slot_score']
        any_slots = list(slots_score.keys())
        for any_slot in any_slots:
            scores_for_slot = slots_score[any_slot]
            m_span = m.span(any_slot)
            matched_words = sentence[m_span[0]:m_span[1]]
            for keyword in scores_for_slot.keys():
                if keyword in matched_words:
                    score += scores_for_slot[keyword]

        return True, arguments, score

from config import *
from templates import *


class SparqlGenerator:
    @staticmethod
    def generate_sparql_from_recognition_result(recognition_result):
        tid = recognition_result[0]
        arguments = recognition_result[1]

        template = templates[tid]
        temp_type = template['type']
        sparql_expression = template['sparql_expression']

        sparql = SparqlGenerator.__generate_sparql(temp_type, sparql_expression, arguments)

        return sparql

    @staticmethod
    def generate_sparql_from_check_template(check_template, arguments):
        temp_type = check_template['type']
        sparql_expression = check_template['sparql_expression']

        sparql = SparqlGenerator.__generate_sparql(temp_type, sparql_expression, arguments)

        return sparql

    @staticmethod
    def __generate_sparql(temp_type, sparql_expression, arguments):
        sparql_template = SPARQL_TEMPLATES[temp_type]
        sparql_expression = sparql_expression.format(**arguments)
        sparql_template = sparql_template.format(graph_url=GRAPH_URL, sparql_expression=sparql_expression)
        sparql = SPARQL_PREFIX + sparql_template

        return sparql

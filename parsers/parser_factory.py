import importlib

class ParserFactory:
    @staticmethod
    def get_parser(parser_name):
        module_name = f'parsers.{parser_name.lower()}'
        class_name = parser_name

        module = importlib.import_module(module_name)
        parser_class = getattr(module, class_name)
        return parser_class()
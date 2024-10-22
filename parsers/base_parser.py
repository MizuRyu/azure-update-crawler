from abc import ABC, abstractclassmethod

class BaseParser(ABC):
    @abstractclassmethod
    def parse(self, html):
        pass
from abc import ABC, abstractmethod
import string


class TextProcessor(ABC):
    @abstractmethod
    def transform(self, text):
        pass


class ConvertCase(TextProcessor):
    def __init__(self, casing='lower'):
        self.casing = casing

    def transform(self, text):
        if self.casing == 'lower':
            return text.lower()
        elif self.casing == 'upper':
            return text.upper()
        elif self.casing == 'title':
            return text.title()


class RemoveDigit(TextProcessor):
    def transform(self, text):
        return ''.join(char if not char.isdigit() else ' ' for char in text)


class RemoveSpace(TextProcessor):
    def transform(self, text):
        return ''.join(text.split())


class RemovePunkt(TextProcessor):
    def transform(self, text):
        return ''.join(filter(lambda char: char in string.punctuation, text))


#then we create the pipe class to put them all together
class TextPipeline:
    def __init__(self, *args):
        self.transformers = args

    def transform(self, text):
        for tf in self.transformers:
            text = tf.transform(text)
        return text

    def __str__(self):
        transformers = '-->'.join([tf.__class__.__name__ for tf in self.transformers])
        return f'Pipeline: [{transformers}]'

import random


class SingleMarcov:
    def __init__(self, text: str = None, file_path: str = None):
        self.model = {}

        if not (text or file_path):
            raise ValueError("学習用のデータを指定してください")

        if text:
            self.text = text
        else:
            with open(file_path, 'r', encoding="utf-8") as f:
                self.text = f.read()

        self._generate_model()

    def _generate_model(self):
        table = str.maketrans({
            '\n': '',
            '\r': '',
            '(': '（',
            ')': '）',
            '[': '［',
            ']': '］',
            '"': '”',
            "'": "’",
        })
        text = self.text.translate(table)

        for i, char in enumerate(text):
            if char not in self.model:
                self.model[char] = []
            if i + 1 < len(text):
                self.model[char].append(text[i + 1])

    def generate_text(self, *, max_length: int = None):
        text = random.choice(list(self.model.keys()))

        while not max_length or len(text) < max_length:
            if len(self.model[text[-1]]) <= 0:
                break
            text += random.choice(self.model[text[-1]])

        return text


if __name__ == '__main__':
    model = SingleMarcov(file_path='webmania_thread.txt')
    print(model.generate_text(max_length=100))

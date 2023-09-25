import re

class ChatFilter:
    def __init__(self):
        with open('bad_words_en.txt', 'r', encoding='utf-8') as f:
            self.SENSITIVE_WORDS_EN = [line.strip().lower() for line in f]
        with open('bad_words_kr.txt', 'r', encoding='utf-8') as f:
            self.SENSITIVE_WORDS_KO = [line.strip().lower() for line in f]
        with open('bad_words_jp.txt', 'r', encoding='utf-8') as f:
            self.SENSITIVE_WORDS_JP = [line.strip().lower() for line in f]

    def filter_sensitive_words(self, text):
        if re.search(r'[가-힣]', text):
            for word in self.SENSITIVE_WORDS_KO:
                if word in text.lower():
                    return "필터링"
        elif re.search(r'[\u3040-\u30ff\u31f0-\u31ff\uff66-\uff9f]', text):
            for word in self.SENSITIVE_WORDS_JP:
                if word in text.lower():
                    return "필터링"
        else:
            for word in self.SENSITIVE_WORDS_EN:
                pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
                if pattern.search(text):
                    return "필터링"
        return text

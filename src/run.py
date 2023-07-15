from pathlib import Path
from collections import Counter
from scr.text_process import (RemoveDigit, RemoveSpace, RemovePunkt, ConvertCase, TextPipeline)
from scr.utils import print_success

class Search:
    def __init__(self, documents_path: str, stop_words: str = None) -> None:

        self.data = self.crawl(documents_path)

        # Load text processor
        self.pipe = TextPipeline(ConvertCase(), RemoveDigit(), RemovePunkt(), RemoveSpace())

        # Load stop words
        self.stop_words = self.load_stop_words(stop_words)

        # index data
        self.index = self.index_data()

    def crawl(self, document_path: str) -> dict:

        data = {}
        for doc_path in Path(document_path).iterdir():
            if doc_path.suffix != '.txt':
                continue

            with open(doc_path) as f:
                doc_name = doc_path.stem.replace('_', ' ').title()
                data[doc_name] = f.read()

        return data

    def load_stop_words(self, stop_words: list) -> list:

        if stop_words is None:
            stop_words = open('data/stop_words.txt').read()
            stop_words = stop_words.split('\n')

        # Process stop words
        stop_words = set(map(self.pipe.transform, stop_words))

        return stop_words

    def index_data(self, ) -> dict:

        index = {}
        for doc_name, doc_content in self.data.items():
            for word in doc_content.split():
                word = self.pipe.transform(word)
                if not word:
                    continue

                if word in self.stop_words:
                    continue

                if word in index:
                    index[word].add(doc_name)
                else:
                    index[word] = {doc_name}

        return index

    def search(self, query: str, top_k: int = 5) -> list:

        query = self.pipe.transform(query)
        search_tokens = query.split()
        docs = []
        for token in search_tokens:
            docs.extend(self.index.get(token, []))

        # Count number of documents
        docs = Counter(docs).most_common(top_k)
        docs = [doc[0] for doc in docs]
        return docs[:top_k]


if __name__ == '__main__':
    searcher = Search('data/documents')

    # Search query
    while True:
        query = input('Search to find a doc (q to quit): ')
        if query.lower() == 'q':
            break

        docs = searcher.search(query, top_k=5)
        for doc_name in docs:
            print_success(f'- {doc_name}')
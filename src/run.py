from pathlib import Path

class Search:
    def __init__(self, documents_path):
        self.data = self.crawl(documents_path)
        self.index = self.index()

    def crawl(self, documents_path):
        data = {}
        for doc_path in Path(documents_path).iterdir():
            if doc_path.suffix != '.txt':
                continue

            with open(doc_path) as f:
                doc_name = doc_path.stem.replace('_', ' ').title()
                data[doc_name] = f.read

        return data

if __name__ == '__main__':
    searcher = Search('data/documents')
import os
import re
import string
import numpy as np
from typing import List, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import json


class DocumentSearchEngine:
    def __init__(self, documents_folder: str):
        """
        Инициализация поисковой модели на основе библиотеки документов.
        :param documents_folder: Путь к папке с .txt файлами электронных книг.
        """
        self.documents_folder = documents_folder
        self.documents: List[str] = []
        self.document_names: List[str] = []
        self.document_metadata: dict[str, dict] = {}
        self.vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
        self.document_vectors = None

        self._load_documents()
        self._vectorize_documents()

    def _load_documents(self):
        """
        Загрузка всех .txt документов из папки в память.
        Также проверяется наличие .meta файлов с метаданными.
        """
        for file_name in os.listdir(self.documents_folder):
            if file_name.endswith('.txt'):
                path = os.path.join(self.documents_folder, file_name)
                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    self.documents.append(content)
                    self.document_names.append(file_name)

                # Попробуем загрузить метаданные
                meta_file = os.path.join(self.documents_folder, file_name.replace('.txt', '.meta.json'))
                if os.path.exists(meta_file):
                    with open(meta_file, 'r', encoding='utf-8') as mf:
                        metadata = json.load(mf)
                        self.document_metadata[file_name] = metadata
                else:
                    self.document_metadata[file_name] = {
                        "title": file_name,
                        "author": "Неизвестен",
                        "tags": []
                    }

    def _vectorize_documents(self):
        """
        Преобразование документов в векторы TF-IDF.
        """
        self.document_vectors = self.vectorizer.fit_transform(self.documents)

    def search(self, query: str, top_n: int = 5) -> List[Tuple[str, float]]:
        """
        Поиск по запросу. Возвращает список документов с наиболее похожими фрагментами.
        :param query: Текст запроса.
        :param top_n: Сколько топ-результатов вернуть.
        :return: Список кортежей (имя_документа, коэффициент_сходства).
        """
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.document_vectors).flatten()

        ranked_indices = np.argsort(similarities)[::-1][:top_n]
        results = [(self.document_names[i], similarities[i]) for i in ranked_indices if similarities[i] > 0.0]

        return results

    def get_snippet(self, doc_name: str, query: str, window: int = 40) -> Optional[str]:
        """
        Извлечение фрагмента из документа с вхождением поискового запроса.
        :param doc_name: Имя файла документа
        :param query: Поисковый запрос
        :param window: Размер контекста вокруг совпадения
        :return: Строка с фрагментом текста
        """
        if doc_name not in self.document_names:
            return None

        index = self.document_names.index(doc_name)
        content = self.documents[index].lower()
        query = query.lower()

        match = re.search(re.escape(query), content)
        if not match:
            return None

        start = max(0, match.start() - window)
        end = min(len(content), match.end() + window)

        return content[start:end].strip()

    def list_all_documents(self) -> List[dict]:
        """
        Получить список всех документов с метаданными.
        :return: Список словарей с информацией о каждом документе.
        """
        all_docs = []
        for name in self.document_names:
            meta = self.document_metadata.get(name, {})
            all_docs.append({
                "filename": name,
                "title": meta.get('title', name),
                "author": meta.get('author', 'Неизвестен'),
                "tags": meta.get('tags', [])
            })
        return all_docs

    def api_search(self, query: str, top_n: int = 5) -> List[dict]:
        """
        Метод для вызова из API — возвращает список документов с совпадениями и фрагментами.
        :param query: Строка запроса.
        :param top_n: Число результатов.
        :return: Список словарей с результатами.
        """
        raw_results = self.search(query, top_n)
        return [
            {
                "filename": name,
                "similarity": float(score),
                "snippet": self.get_snippet(name, query),
                "metadata": self.document_metadata.get(name, {})
            }
            for name, score in raw_results
        ]

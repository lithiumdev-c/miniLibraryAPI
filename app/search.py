from elasticsearch import AsyncElasticsearch
from typing import Any, List, Dict

from app.models.book import Book

class BookSearch:
    INDEX_NAME = 'books'

    def __init__(self, es_client:AsyncElasticsearch):
        self.es = es_client
    
    async def create_index(self):
        if not await self.es.indices.exists(index=self.INDEX_NAME):
            await self.es.indices.create(
                index = self.INDEX_NAME,
                mappings={
                    "properties": {
                        "id": {"type": "integer"},
                        "title": {"type": "text"},
                        "author": {"type": "text"},
                    }
                }
            )
    
    async def index_book(self, book_model: Book):
        await self.es.index(
            index=self.INDEX_NAME,
            id=str(book_model.id),
            document={
                'id': book_model.id,
                'title': book_model.title,
                'author': book_model.author,
            }
        )
    
    async def search_book(self, query:str) -> List[int]:
        response = await self.es.search(
            index=self.INDEX_NAME,
            query={
                'multi-match': {
                    'query': query,
                    'fields': ['title^2', 'author'],
                    'fuzziness': 'AUTO',
                }
            }
        )

        return [int(hit['_id']) for hit in response['hits']['hits']]
    
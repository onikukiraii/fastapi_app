import os
from collections.abc import Generator

from opensearchpy import OpenSearch

OPENSEARCH_URL = os.environ.get("OPENSEARCH_URL", "http://localhost:9205")

client = OpenSearch(
    hosts=[OPENSEARCH_URL],
    use_ssl=False,
    verify_certs=False,
)

INDEX_NAME = "users"


def get_opensearch() -> Generator[OpenSearch]:
    yield client


def ensure_index() -> None:
    """Create users index if it doesn't exist."""
    if not client.indices.exists(index=INDEX_NAME):
        client.indices.create(
            index=INDEX_NAME,
            body={
                "settings": {
                    "analysis": {
                        "analyzer": {
                            "kuromoji_analyzer": {
                                "type": "custom",
                                "tokenizer": "kuromoji_tokenizer",
                            }
                        }
                    }
                },
                "mappings": {
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "text", "analyzer": "kuromoji_analyzer"},
                        "email": {"type": "keyword"},
                        "created_at": {"type": "date"},
                    }
                },
            },
        )


def index_user(user_id: int, name: str, email: str, created_at: str) -> None:
    """Index a user document in OpenSearch."""
    client.index(
        index=INDEX_NAME,
        id=str(user_id),
        body={
            "id": user_id,
            "name": name,
            "email": email,
            "created_at": created_at,
        },
        refresh=True,
    )


def search_users(query: str) -> list[dict]:
    """Search users by name using full-text search."""
    response = client.search(
        index=INDEX_NAME,
        body={
            "query": {
                "match": {
                    "name": {
                        "query": query,
                        "fuzziness": "AUTO",
                    }
                }
            }
        },
    )
    return [hit["_source"] for hit in response["hits"]["hits"]]

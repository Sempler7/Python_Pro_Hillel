from typing import Any

from django.conf import settings
from elasticsearch import Elasticsearch, NotFoundError

from .models import Photo

INDEX_NAME = "photos"


def get_client() -> Elasticsearch:
    """Створює клієнт Elasticsearch."""

    return Elasticsearch(settings.ELASTICSEARCH_URL)


def ensure_index() -> None:
    """Створює індекс фотографій, якщо він ще не існує."""

    client = get_client()

    if client.indices.exists(index=INDEX_NAME):
        return

    client.indices.create(
        index=INDEX_NAME,
        mappings={
            "properties": {
                "caption": {"type": "text"},
                "tags": {"type": "text"},
                "author_id": {"type": "integer"},
                "created_at": {"type": "date"},
            }
        },
    )


def serialize_photo(photo: Photo) -> dict[str, Any]:
    """Перетворює фотографію на документ для Elasticsearch."""

    return {
        "id": photo.id,
        "caption": photo.caption,
        "tags": " ".join(photo.tags or []),
        "author_id": photo.author_id,
        "created_at": photo.created_at.isoformat(),
    }


def index_photo(photo: Photo) -> None:
    """Індексує або оновлює фотографію в Elasticsearch."""

    try:
        ensure_index()
        get_client().index(
            index=INDEX_NAME,
            id=str(photo.id),
            document=serialize_photo(photo),
            refresh=True,
        )
    except Exception as error:
        print(f"Elasticsearch index error: {error}")


def delete_photo_from_index(photo_id: int) -> None:
    """Видаляє фотографію з індексу пошуку."""

    try:
        get_client().delete(
            index=INDEX_NAME,
            id=str(photo_id),
        )
    except NotFoundError:
        return
    except Exception as error:
        print(f"Elasticsearch delete error: {error}")


def search_photo_ids(query: str) -> list[int]:
    """Шукає ID фотографій за описом і тегами."""

    try:
        ensure_index()

        response = get_client().search(
            index=INDEX_NAME,
            query={
                "multi_match": {
                    "query": query,
                    "fields": ["caption^2", "tags"],
                }
            },
        )

        return [int(hit["_id"]) for hit in response["hits"]["hits"]]

    except Exception as error:
        print(f"Elasticsearch search error: {error}")
        print(getattr(error, "info", None))
        return []

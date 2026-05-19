from typing import Callable, Generic, TypeVar
from pydantic import BaseModel

from app.domain.value_objects.pagination import PaginatedResult

T = TypeVar("T")


class PaginatedDto(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool

    @classmethod
    def from_result(cls, result: PaginatedResult, mapper: Callable) -> "PaginatedDto":
        return cls(
            items=[mapper(item) for item in result.items],
            total=result.total,
            page=result.page,
            page_size=result.page_size,
            total_pages=result.total_pages,
            has_next=result.has_next,
            has_previous=result.has_previous,
        )

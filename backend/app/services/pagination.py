from typing import Any
from fastapi import Query


def pagination_params(limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0)) -> tuple[int, int]:
	return limit, offset


def apply_pagination(query: Any, limit: int, offset: int):
	return query.offset(offset).limit(limit)

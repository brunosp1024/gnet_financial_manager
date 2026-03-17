import pytest
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from apps.core.pagination.standard_pagination import StandardPagination


@pytest.fixture
def rf():
    return APIRequestFactory()


def make_request(rf, path="/", params=None):
    return Request(rf.get(path, params or {}))


@pytest.fixture
def pagination():
    return StandardPagination()


class TestStandardPaginationConfig:
    def test_default_page_size(self, pagination):
        assert pagination.page_size == 20

    def test_page_size_query_param(self, pagination):
        assert pagination.page_size_query_param == "page_size"

    def test_max_page_size(self, pagination):
        assert pagination.max_page_size == 100


class TestStandardPaginationBehavior:
    def test_paginates_queryset(self, pagination, rf):
        items = list(range(50))
        request = make_request(rf)
        result = pagination.paginate_queryset(items, request)

        assert result == list(range(20))

    def test_custom_page_size_via_query_param(self, pagination, rf):
        items = list(range(50))
        request = make_request(rf, params={"page_size": "10"})
        result = pagination.paginate_queryset(items, request)

        assert len(result) == 10

    def test_page_size_capped_at_max(self, pagination, rf):
        items = list(range(200))
        request = make_request(rf, params={"page_size": "150"})
        result = pagination.paginate_queryset(items, request)

        assert len(result) == 100

    def test_second_page(self, pagination, rf):
        items = list(range(50))
        request = make_request(rf, params={"page": "2"})
        result = pagination.paginate_queryset(items, request)

        assert result == list(range(20, 40))

    def test_get_paginated_response_contains_count(self, pagination, rf):
        items = list(range(50))
        request = make_request(rf)
        pagination.paginate_queryset(items, request)
        response = pagination.get_paginated_response([])

        assert "count" in response.data
        assert response.data["count"] == 50

    def test_get_paginated_response_contains_next_and_previous(self, pagination, rf):
        items = list(range(50))
        request = make_request(rf)
        pagination.paginate_queryset(items, request)
        response = pagination.get_paginated_response([])

        assert "next" in response.data
        assert "previous" in response.data

import pytest
from rest_framework.test import APIClient

from comments.models import Comment


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def root_comment(db):
    return Comment.objects.create(
        username="Dima", email="dima@test.com", text="Root comment"
    )


@pytest.fixture
def reply_comment(db, root_comment):
    return Comment.objects.create(
        username="Alex",
        email="alex@test.com",
        text="Reply comment",
        parent=root_comment,
    )


@pytest.fixture
def many_comments(db):
    comments = []
    for i in range(5):
        comments.append(
            Comment.objects.create(
                username=f"user{i}", email=f"user{i}@test.com", text=f"text {i}"
            )
        )
    return comments

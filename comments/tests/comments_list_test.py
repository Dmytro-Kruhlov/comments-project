import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_get_comments_empty(api_client):
    url = reverse("comments-list")

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["count"] == 0
    assert response.data["results"] == []


@pytest.mark.django_db
def test_get_comments_with_data(api_client, root_comment):
    url = reverse("comments-list")

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["count"] == 1

    comment = response.data["results"][0]
    assert comment["username"] == "Dima"
    assert comment["text"] == "Root comment"
    assert comment["first_reply"] is None


@pytest.mark.django_db
def test_get_comments_with_first_reply(api_client, root_comment, reply_comment):
    url = reverse("comments-list")

    response = api_client.get(url)

    assert response.status_code == 200

    comment = response.data["results"][0]

    assert comment["first_reply"] is not None
    assert comment["first_reply"]["text"] == "Reply comment"


@pytest.mark.django_db
def test_only_root_comments_returned(api_client, root_comment, reply_comment):
    url = reverse("comments-list")

    response = api_client.get(url)

    assert response.data["count"] == 1

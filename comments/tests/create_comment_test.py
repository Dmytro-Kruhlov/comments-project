import pytest
from django.core.cache import cache
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_create_comment_success():
    client = APIClient()

    captcha_id = "test-id"
    captcha_text = "abc123"

    cache.set(captcha_id, captcha_text)

    data = {
        "username": "testuser",
        "email": "test@test.com",
        "text": "hello world",
        "captcha_id": captcha_id,
        "captcha": captcha_text,
    }

    response = client.post("/api/comments/create/", data)

    assert response.status_code == 201
    assert response.data["username"] == "testuser"


@pytest.mark.django_db
def test_create_comment_invalid_captcha():
    client = APIClient()

    captcha_id = "test-id"
    real_captcha = "abc123"

    cache.set(captcha_id, real_captcha)

    data = {
        "username": "testuser",
        "email": "test@test.com",
        "text": "hello world",
        "captcha_id": captcha_id,
        "captcha": "wrong",
    }

    response = client.post("/api/comments/create/", data)

    assert response.status_code == 400
    assert "invalid" in str(response.data).lower()

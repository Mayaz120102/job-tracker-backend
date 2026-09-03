from fastapi import status


def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "Password123",
            "phone_number": "1234567890",
            "address": "123 Test St",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"message": "user created successfully"}


def test_register_duplicate_user(client):

    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "Password123",
            "phone_number": "1234567890",
            "address": "123 Test St",
        },
    )

    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "Password123",
            "phone_number": "1234567890",
            "address": "123 Test St",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Email or username already registered"}


def test_login_success(client):

    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "Password123",
            "phone_number": "1234567890",
            "address": "123 Test St",
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "Password123",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_failure(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "nonexistent",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED



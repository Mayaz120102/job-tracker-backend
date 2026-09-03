from fastapi import status


def test_create_application(client, auth_headers):
    response = client.post(
        "/applications",
        json={
            "company_name": "Google",
            "job_title": "Backend Intern",
            "status": "applied",
            "applied_date": "2026-01-15",
            "job_url": "https://example.com",
            "notes": "Applied via referral",
        },
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_201_CREATED


def test_user_cannot_see_others_applications(client, auth_headers):
    client.post(
        "/applications",
        json={
            "company_name": "Google",
            "job_title": "Backend Intern",
            "status": "applied",
            "applied_date": "2026-01-15",
            "job_url": "https://example.com",
            "notes": "Applied via referral",
        },
        headers=auth_headers
    )

    client.post("/auth/register", json={
        "email": "userb@example.com",
        "username": "userb",
        "password": "Password123",
        "phone_number": "0987654321",
        "address": "456 Other St",
    })

    login_response = client.post("/auth/login", data={
        "username": "userb",
        "password": "Password123",
    })
    user_b_token = login_response.json()["access_token"]
    user_b_headers = {"Authorization": f"Bearer {user_b_token}"}

    response = client.get("/applications", headers=user_b_headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
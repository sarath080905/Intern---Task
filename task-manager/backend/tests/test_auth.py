# ==============================
# Authentication tests
# ==============================

def test_register(client, user_credentials):
    response = client.post("/register", json=user_credentials)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_credentials["email"]
    assert "id" in data
    assert "hashed_password" not in data


def test_register_duplicate_email(client, user_credentials):
    # Duplicate registration should return a validation error.
    client.post("/register", json=user_credentials)
    response = client.post("/register", json=user_credentials)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login(client, registered_user):
    # Login should return a bearer token when credentials are correct.
    response = client.post(
        "/login",
        data={
            "username": registered_user["email"],
            "password": registered_user["password"],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert "access_token" in data


def test_login_wrong_password(client, registered_user):
    # Invalid password should fail authentication.
    response = client.post(
        "/login",
        data={
            "username": registered_user["email"],
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


def test_me_requires_auth(client):
    # Access to current user endpoint requires a valid token.
    response = client.get("/me")

    assert response.status_code == 401


def test_me_with_token(client, auth_headers):
    response = client.get("/me", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"

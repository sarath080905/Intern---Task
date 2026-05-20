# ==============================
# Task API tests
# ==============================

def test_create_task_unauthorized(client):
    # Protected task creation should reject missing authentication.
    response = client.post(
        "/tasks",
        json={"title": "Unauthorized task", "completed": False},
    )

    assert response.status_code == 401


def test_list_tasks_unauthorized(client):
    # Listing tasks requires authentication.
    response = client.get("/tasks")

    assert response.status_code == 401


def test_create_task(client, auth_headers):
    # Authenticated users can create a new task.
    response = client.post(
        "/tasks",
        json={
            "title": "Write pytest tests",
            "description": "Step 8",
            "completed": False,
        },
        headers=auth_headers,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Write pytest tests"
    assert data["completed"] is False
    assert "id" in data


def test_list_tasks(client, auth_headers):
    # Confirm task list returns all created tasks for the user.
    client.post(
        "/tasks",
        json={"title": "Task A", "completed": False},
        headers=auth_headers,
    )
    client.post(
        "/tasks",
        json={"title": "Task B", "completed": True},
        headers=auth_headers,
    )

    response = client.get("/tasks", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_filter_completed_tasks(client, auth_headers):
    # Task filtering should return only completed items when requested.
    client.post(
        "/tasks",
        json={"title": "Done", "completed": True},
        headers=auth_headers,
    )
    client.post(
        "/tasks",
        json={"title": "Todo", "completed": False},
        headers=auth_headers,
    )

    response = client.get("/tasks?completed=true", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["completed"] is True


def test_update_and_delete_task(client, auth_headers):
    # Update a task and then delete it to verify the full lifecycle.
    create = client.post(
        "/tasks",
        json={"title": "Update me", "completed": False},
        headers=auth_headers,
    )
    task_id = create.json()["id"]

    update = client.put(
        f"/tasks/{task_id}",
        json={"completed": True},
        headers=auth_headers,
    )
    assert update.status_code == 200
    assert update.json()["completed"] is True

    delete = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert delete.status_code == 204

    get = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get.status_code == 404


def test_user_cannot_access_other_users_task(client, user_credentials):
    # Ensure one user cannot access another user's task.
    other = {"email": "other@example.com", "password": "secret123"}
    client.post("/register", json=user_credentials)
    client.post("/register", json=other)

    login_a = client.post(
        "/login",
        data={"username": user_credentials["email"], "password": user_credentials["password"]},
    )
    headers_a = {"Authorization": f"Bearer {login_a.json()['access_token']}"}

    task = client.post(
        "/tasks",
        json={"title": "Private task", "completed": False},
        headers=headers_a,
    )
    task_id = task.json()["id"]

    login_b = client.post(
        "/login",
        data={"username": other["email"], "password": other["password"]},
    )
    headers_b = {"Authorization": f"Bearer {login_b.json()['access_token']}"}

    response = client.get(f"/tasks/{task_id}", headers=headers_b)
    assert response.status_code == 404

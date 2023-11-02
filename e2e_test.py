import requests


API_URL = "http://127.0.0.1:5000/api/users/list"

def test_get_users_list():
    response = requests.get(API_URL)

    assert response.status_code == 200, "Status code is not 200 OK"

    users = response.json()
    assert isinstance(users, list), "Response is not a list"

    for user in users:
        assert "username" in user, "User does not have 'username' field"
        assert "userId" in user, "User does not have 'userId' field"
        assert "firstSeen" in user, "User does not have 'firstSeen' field"

    print("E2E Test Passed!")

if __name__ == "__main__":
    test_get_users_list()

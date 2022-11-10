import json
from config import setting


def test_create_user(client):
    data = {"email": "test2@test.com", "password": "password"}
        # providing dummy data
    response = client.post("/users", json.dumps(data))
        # gives above data in json format
        #now we check the o/p using assert
    assert response.status_code == 200
        # 200 ok aaucha thei ho
    assert response.json()["email"] == "test2@test.com"
        # email match check
    assert response.json()["is_active"] == True
        # is_active bool ho, thei check

import json
from config import setting


def test_create_item(client, token_header):
    data = {"title": setting.TEST_ITEM, "description": setting.TEST_ITEM_DEF}
        # providing dummy data
    response = client.post("/item", json.dumps(data), headers=token_header)
        # gives above data in json format
        #now we check the o/p using assert
    assert response.status_code == 200
        # 200 ok aaucha thei ho
    pass


def test_retrieve_item_by_id(client):
    response = client.get("/item/1")
    assert response.status_code == 200
    assert response.json()["title"] == setting.TEST_ITEM

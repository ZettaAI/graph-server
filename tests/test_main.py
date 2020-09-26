from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# TODO fix tests after bigtable emulator is setup
def test_home():
    from starlette.status import HTTP_200_OK

    response = client.get("/")
    assert response.status_code == HTTP_200_OK
    assert response.json().get("version") != None

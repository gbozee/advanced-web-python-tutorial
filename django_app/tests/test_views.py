def test_home_page(client):
    response = client.get("/")
    assert response.content.decode("utf-8") == "Hello world"


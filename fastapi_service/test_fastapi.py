import pytest
from httpx import AsyncClient
from fastapi import status
from httpx._transports.asgi import ASGITransport
from mongomock import MongoClient
from passlib.context import CryptContext
from main import app
from util import create_user, get_user, get_mongo_clien, create_access_token

pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")

def test_create_user(): # check signup
    result = create_user("test@example.com", "password", "testuser", {"art": 1}, "news", [])
    assert result == 1

def test_authenticate_user(): # check login
    user = get_user("test@example.com")
    assert user is not False

access_token = create_access_token(
    data={"sub": "agash"}, expires_delta=60)

@pytest.mark.asyncio
async def test_news_loader_unauthorized(): # unauthorised news loader
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/news/all")
        assert response.status_code != status.HTTP_200_OK

@pytest.mark.asyncio
async def test_news_loader_authorized(): # authorised news loader
    token = "bearer "+access_token
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/news/all", headers={"Authorization": token})
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_top_news_loader_unauthorized(): # unauthorised top news loader
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/news/top")
        assert response.status_code != status.HTTP_200_OK

@pytest.mark.asyncio
async def test_top_news_loader_authorized(): # authorised top news loader
    token = "bearer "+access_token
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/news/top", headers={"Authorization": token})
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_news_id_unauthorized(): # unauthorised news id 
    token = "bearer "
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/news/id?id=1", headers={"Authorization": token})
        assert response.status_code != status.HTTP_200_OK

@pytest.mark.asyncio
async def test_news_id_authorized(): # authorised news id
    token = "bearer "+access_token
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/news/id?id=1", headers={"Authorization": token})
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_news_watch_unauthorized(): # unauthorised news watch
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/watch/")
        assert response.status_code != status.HTTP_200_OK


@pytest.mark.asyncio
async def test_news_watch_authorized(): # authorised news watch
    token = "bearer "+access_token
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/watch/", headers={"Authorization": token})
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_news_notify_unauthorized(): # unauthorised news notify
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/notify/")
        assert response.status_code != status.HTTP_200_OK


@pytest.mark.asyncio
async def test_news_notify_authorized(): # authorised news notify
    token = "bearer "+access_token
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/notify/", headers={"Authorization": token})
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_profile_view_unauthorized(): # unauthorised profile viewer
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/profile/view")
        assert response.status_code != status.HTTP_200_OK


@pytest.mark.asyncio
async def test_profile_view_authorized(): # authorised profile viewer
    token = "bearer "+access_token
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/profile/view", headers={"Authorization": token})
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_searcher_unauthorized(): # unauthorised searcher
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/search/db?to_search=example")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_searcher_success(): # authorised searcher
    token = "bearer "+access_token
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/search/db?to_search=example", headers={"Authorization": token})
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_searcher_serp_unauthorized(): # unauthorised searcher
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/search/serp?to_search=example")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_searcher_serp_success(): # authorised searcher
    token = "bearer "+access_token
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/search/serp?to_search=example", headers={"Authorization": token})
        assert response.status_code == status.HTTP_200_OK
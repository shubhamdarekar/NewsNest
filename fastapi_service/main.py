from fastapi import FastAPI
from routers import news_loader, profile, search, notifications, news_watch

app = FastAPI()

app.include_router(search.router, tags=['search'], prefix='/search')
app.include_router(news_loader.router, tags=['news'], prefix='/news')
app.include_router(profile.router, tags=['profile'], prefix='/profile')
app.include_router(notifications.router, tags=['notificaitons'], prefix='/notify')
app.include_router(news_watch.router, tags=['news'], prefix='/watch')
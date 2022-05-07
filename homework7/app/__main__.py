import uvicorn
from fastapi import FastAPI

from app.channel import main_channel
from app.redis import redis
from app.routers.history import router as history_router
from app.routers.login import router as login_router
from app.routers.ws import router as ws_router
from settings import cfg

app = FastAPI()
app.include_router(history_router)
app.include_router(login_router)
app.include_router(ws_router)


@app.on_event('startup')
async def startup_event() -> None:
    await redis.init()
    await main_channel.init(cfg.MAIN_CHANNEL_NAME)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8090)

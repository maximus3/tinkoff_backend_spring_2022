import uvicorn
from fastapi import FastAPI

from .routers import tasks

app = FastAPI()

app.include_router(tasks.router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8090)

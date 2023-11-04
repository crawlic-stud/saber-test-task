import uvicorn

from setup import app
from settings import api


if __name__ == "__main__":
    uvicorn.run(app, host=api.APP_HOST, port=api.APP_PORT)

import uvicorn
from fastapi import FastAPI

from settings import get_settings


settings = get_settings()
app = FastAPI()


# @app.on_event('startup')
# def load_data():
#     import data
#     data.main()


@app.get('/')
async def root():
    """Say hello."""
    return {'message': 'Hello FastAPI'}


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.host,
        port=settings.port,
        reload=True,
    )

import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.responses import RedirectResponse
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from database import Session, create_all
from database.models import Movie, Rating, Review, User

from .routers import movies, ratings, reviews, users

create_all()
app = FastAPI()

app.include_router(users.router)
app.include_router(movies.router)
app.include_router(reviews.router)
app.include_router(ratings.router)

flask_app = Flask(__name__)
admin = Admin(
    flask_app, name='Movie Rating Service', template_mode='bootstrap4', url='/'
)
admin.add_view(ModelView(User, Session))
admin.add_view(ModelView(Movie, Session))
admin.add_view(ModelView(Rating, Session))
admin.add_view(ModelView(Review, Session))


@app.get('/')
def root() -> RedirectResponse:
    return RedirectResponse('/movies', status_code=status.HTTP_302_FOUND)


app.mount('/admin', WSGIMiddleware(flask_app))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8090)

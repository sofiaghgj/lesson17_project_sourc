# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')
class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating =fields.Float()

class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)
@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        # all_movies = Movie.query.all()
        # return movies_schema.dump(all_movies), 200
        movies = Movie.query.all()

        if genre_id := request.args.get('genre_id'):
            movies = movies.filter(Movie.genre_id == genre_id)

        if director_id := request.args.get('director_id'):
            movies = movies.filter(Movie.director_id == director_id)

        return movies_schema.dump(movies.all), 200


    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
            db.session.commit()
        return movies_schema.dump(new_movie), 201



@movies_ns.route('/<int:uid>')
class MovieView(Resource):
    def get(self, uid: int):
        movie = Movie.query.get(uid)
        return movies_schema.dump(movie), 200
    def delete(self, uid: int):
        movie = Movie.query.get(uid)
        with db.session.begin():
            db.session.delete(movie)
        return "", 204
    def patch(self, uid):
        movie = Movie.query.get(uid)
        req_json = request.json
        if "title" in req_json:
            movie.title = req_json.get("title")
        if "description" in req_json:
            movie.description = req_json.get("description")
        if "trailer" in req_json:
            movie.trailer = req_json.get("trailer")
        if "year" in req_json:
            movie.year = req_json.get("year")
        if "rating" in req_json:
            movie.rating = req_json.get("rating")

        db.session.add(movie)
        db.session.commit()
        return movies_schema.dump(movie), 200


def put(self, uid):
    movie = Movie.query.get(uid)
    req_json = request.json
    movie.title = req_json.get("title")
    movie.description = req_json.get("description")
    movie.trailer = req_json.get("trailer")
    movie.year = req_json.get("year")
    movie.rating = req_json.get("rating")

    db.session.add(movie)
    db.session.commit()
    return movies_schema.dump(movie), 200



# {'location':f'/movies/{new_movie.id}'}




if __name__ == '__main__':
    app.run(debug=True)

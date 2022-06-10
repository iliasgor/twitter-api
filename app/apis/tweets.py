# app/apis/tweets.py
# pylint: disable=missing-docstring

import marshal
from flask_restx import Namespace, Resource, fields, abort
from app.models import Tweet
from app import db

api = Namespace('tweets')  # Base route

json_tweet = api.model('Tweet',{
    'id': fields.Integer, 
    'text': fields.String,
    'created_at': fields.DateTime
})
json_tweet = api.model('Tweet', {
    'id': fields.Integer(required=True),
    'text': fields.String(required=True, min_length=1),
    'author': fields.String(required=True, min_length=1),
    'created_at': fields.DateTime(required=True),
})

@api.route('/<int:id>')  # route extension (ie: /tweets/<int:id>)
@api.response(404, 'Tweet not found')
@api.param('id', 'The tweet unique identifier')
class TweetResource(Resource):
    @api.marshal_with(json_tweet)
    def get(self, id):
        tweet = db.session.query(Tweet).get(id)
        if tweet is None:
            api.abort(404, "Tweet {} doesn't exist".format(id))
        else:
            return tweet
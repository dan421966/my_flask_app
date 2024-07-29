from flask import request
from flask_restx import Resource, fields, Namespace
from models import db, User

api = Namespace('users', description='User related operations')

user_model = api.model('User', {
    'id': fields.Integer(readonly=True, description='The user unique identifier'),
    'username': fields.String(required=True, description='The user username'),
    'email': fields.String(required=True, description='The user email address')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        data = request.json
        user = User(username=data['username'], email=data['email'])
        db.session.add(user)
        db.session.commit()
        return user, 201

    def get(self):
        users = User.query.all()
        return [{'id': u.id, 'username': u.username, 'email': u.email} for u in users]

@api.route('/<int:user_id>/skills')
class UserSkillList(Resource):
    def post(self, user_id):
        data = request.get_json()
        skill = UserSkill(
            user_id=user_id,
            skill_id=data['skill_id'],
            level=data['level']
        )
        db.session.add(skill)
        db.session.commit()
        return {'message': 'Skill added successfully'}, 201

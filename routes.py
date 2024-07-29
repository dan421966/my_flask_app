from flask import jsonify, request
from sqlalchemy import text
from models import db, User, JobTitle, SkillCategory, Skill, UserSkill, SkillCategorySkill
from flask_restx import Resource, fields
from app import app, api

# Define the User model for Swagger
user_model = api.model('User', {
    'id': fields.Integer(readonly=True, description='The user unique identifier'),
    'username': fields.String(required=True, description='The user username'),
    'email': fields.String(required=True, description='The user email address')
})

@api.route('/')
class HelloWorld(Resource):
    def get(self):
        return {"message": "Hello, World!"}

@api.route('/test_db_connection')
class TestDBConnection(Resource):
    def get(self):
        with db.engine.connect() as connection:
            result = connection.execute(text('SELECT 1'))
        return {"message": "Database connection successful", "result": [row[0] for row in result]}

@api.route('/users')
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
        return jsonify([{'id': u.id, 'username': u.username, 'email': u.email} for u in users])

@api.route('/users/<int:user_id>/skills')
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

@api.route('/job_titles')
class JobTitleList(Resource):
    def get(self):
        job_titles = JobTitle.query.all()
        return jsonify([{'id': jt.id, 'name': jt.name} for jt in job_titles])

@api.route('/skill_categories/<int:job_title_id>')
class SkillCategoryList(Resource):
    def get(self, job_title_id):
        skill_categories = SkillCategory.query.filter_by(job_title_id=job_title_id).all()
        return jsonify([{'id': sc.id, 'name': sc.name} for sc in skill_categories])

@api.route('/skills/<int:skill_category_id>')
class SkillList(Resource):
    def get(self, skill_category_id):
        skills = db.session.query(Skill).join(SkillCategorySkill).filter(SkillCategorySkill.skill_category_id == skill_category_id).all()
        return jsonify([{'id': s.id, 'name': s.name} for s in skills])

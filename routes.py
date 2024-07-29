from flask import jsonify, request
from sqlalchemy import text
from models import db, User, JobTitle, SkillCategory, Skill, UserSkill, SkillCategorySkill
from app import app

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/test_db_connection', methods=['GET'])
def test_db_connection():
    with db.engine.connect() as connection:
        result = connection.execute(text('SELECT 1'))
    return jsonify({"message": "Database connection successful", "result": [row[0] for row in result]}), 200

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/users/<int:user_id>/skills', methods=['POST'])
def add_skill(user_id):
    data = request.get_json()
    skill = UserSkill(
        user_id=user_id,
        skill_id=data['skill_id'],
        level=data['level']
    )
    db.session.add(skill)
    db.session.commit()
    return jsonify({'message': 'Skill added successfully'}), 201

@app.route('/job_titles', methods=['GET'])
def get_job_titles():
    job_titles = JobTitle.query.all()
    return jsonify([{'id': jt.id, 'name': jt.name} for jt in job_titles])

@app.route('/skill_categories/<int:job_title_id>', methods=['GET'])
def get_skill_categories(job_title_id):
    skill_categories = SkillCategory.query.filter_by(job_title_id=job_title_id).all()
    return jsonify([{'id': sc.id, 'name': sc.name} for sc in skill_categories])

@app.route('/skills/<int:skill_category_id>', methods=['GET'])
def get_skills(skill_category_id):
    skills = db.session.query(Skill).join(SkillCategorySkill).filter(SkillCategorySkill.skill_category_id == skill_category_id).all()
    return jsonify([{'id': s.id, 'name': s.name} for s in skills])

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username, 'email': u.email} for u in users])

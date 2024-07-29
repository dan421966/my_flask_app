from flask import Flask, request, jsonify
from config import Config
from models import db, User, JobTitle, SkillCategory, Skill, UserSkill, SkillCategorySkill

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

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

if __name__ == '__main__':
    app.run(debug=True)

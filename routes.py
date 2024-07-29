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

@app.route('/users', methods=['GET'])
def get_users():
    """
    Retrieve all users from the database and return them as a JSON response.

    Returns:
        A JSON response containing a list of dictionaries, where each dictionary represents a user.
        Each dictionary contains the user's id, username, and email.
    """
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username, 'email': u.email} for u in users])

@app.route('/users', methods=['POST'])
def add_user():
    """
    Add a new user to the database.

    This function receives a JSON payload containing the username and email of the user.
    It creates a new User object with the provided data and adds it to the database.
    Finally, it commits the changes to the database and returns a JSON response with a success message.

    Returns:
        A JSON response with a success message and a status code of 201 (Created).
    """
    data = request.get_json()
    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/users/<int:user_id>/skills', methods=['POST'])
def add_skill(user_id):
    """
    Add a skill to a user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        tuple: A tuple containing a JSON response and a status code.
            The JSON response contains a message indicating the success of the operation.
            The status code is set to 201 if the skill was added successfully.
    """
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
    """
    Retrieve all job titles from the database and return them as JSON.

    Returns:
        A JSON response containing a list of dictionaries, where each dictionary represents a job title.
        Each dictionary contains the 'id' and 'name' of the job title.
    """
    job_titles = JobTitle.query.all()
    return jsonify([{'id': jt.id, 'name': jt.name} for jt in job_titles])

@app.route('/skill_categories/<int:job_title_id>', methods=['GET'])
def get_skill_categories(job_title_id):
    """
    Retrieve skill categories based on job title ID.

    Args:
        job_title_id (int): The ID of the job title.

    Returns:
        Flask Response: A JSON response containing a list of skill categories with their IDs and names.
    """
    skill_categories = SkillCategory.query.filter_by(job_title_id=job_title_id).all()
    return jsonify([{'id': sc.id, 'name': sc.name} for sc in skill_categories])

@app.route('/skills/<int:skill_category_id>', methods=['GET'])
def get_skills(skill_category_id):
    """
    Retrieve skills based on the given skill category ID.

    Parameters:
    - skill_category_id (int): The ID of the skill category.

    Returns:
    - JSON response: A JSON response containing a list of skills with their IDs and names.
    """
    skills = db.session.query(Skill).join(SkillCategorySkill).filter(SkillCategorySkill.skill_category_id == skill_category_id).all()
    return jsonify([{'id': s.id, 'name': s.name} for s in skills])


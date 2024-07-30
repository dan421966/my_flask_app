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
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username, 'email': u.email} for u in users])

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

@app.route('/previous_job_role', methods=['POST'])
def previous_job_role():
    """
    This endpoint receives the user's previous job role ID and returns the related skill categories.
    """
    data = request.get_json()
    job_role_id = data['job_role_id']
    skill_categories = SkillCategory.query.filter_by(job_title_id=job_role_id).all()
    return jsonify([{'id': sc.id, 'name': sc.name} for sc in skill_categories]), 200

@app.route('/skills_for_previous_role', methods=['POST'])
def skills_for_previous_role():
    """
    This endpoint receives the user's previous job role skill details and adds them to the database.
    """
    data = request.get_json()
    user_id = data['user_id']
    skill_id = data['skill_id']
    level = data['level']
    user_skill = UserSkill(user_id=user_id, skill_id=skill_id, level=level)
    db.session.add(user_skill)
    db.session.commit()
    return jsonify({'message': 'Skill added for previous role successfully'}), 201

@app.route('/desired_job_role', methods=['POST'])
def desired_job_role():
    """
    This endpoint receives the user's desired job role ID and returns the related skill categories.
    """
    data = request.get_json()
    job_role_id = data['job_role_id']
    skill_categories = SkillCategory.query.filter_by(job_title_id=job_role_id).all()
    return jsonify([{'id': sc.id, 'name': sc.name} for sc in skill_categories]), 200

@app.route('/skills_for_desired_role', methods=['POST'])
def skills_for_desired_role():
    """
    This endpoint receives the user's desired job role skill details and adds them to the database.
    """
    data = request.get_json()
    user_id = data['user_id']
    skill_id = data['skill_id']
    level = data['level']
    user_skill = UserSkill(user_id=user_id, skill_id=skill_id, level=level)
    db.session.add(user_skill)
    db.session.commit()
    return jsonify({'message': 'Skill added for desired role successfully'}), 201


'''
### 1. Test Database Connection
**Description**: Tests the database connection.
**cURL Command**:
```sh
curl -X GET http://127.0.0.1:5000/test_db_connection
```
**Expected Output**:
```json
{
    "message": "Database connection successful",
    "result": [1]
}
```

### 2. Get All Users
**Description**: Retrieves all users from the database.
**cURL Command**:
```sh
curl -X GET http://127.0.0.1:5000/users
```
**Expected Output**:
```json
[
    {"id": 1, "username": "user1", "email": "user1@example.com"},
    {"id": 2, "username": "user2", "email": "user2@example.com"}
]
```
**Output Parameters**:
- `id`: Integer
- `username`: String
- `email`: String

### 3. Add a New User
**Description**: Adds a new user to the database.
**cURL Command**:
```sh
curl -X POST http://127.0.0.1:5000/users \
-H "Content-Type: application/json" \
-d '{"username": "new_user", "email": "new_user@example.com"}'
```
**Expected Output**:
```json
{
    "message": "User created successfully"
}
```
**Input Parameters**:
- `username`: String
- `email`: String

### 4. Add a Skill to a User
**Description**: Adds a skill to a user.
**cURL Command**:
```sh
curl -X POST http://127.0.0.1:5000/users/1/skills \
-H "Content-Type: application/json" \
-d '{"skill_id": 2, "level": "Intermediate"}'
```
**Expected Output**:
```json
{
    "message": "Skill added successfully"
}
```
**Input Parameters**:
- `skill_id`: Integer
- `level`: String

### 5. Get All Job Titles
**Description**: Retrieves all job titles from the database.
**cURL Command**:
```sh
curl -X GET http://127.0.0.1:5000/job_titles
```
**Expected Output**:
```json
[
    {"id": 1, "name": "Software Engineer"},
    {"id": 2, "name": "Data Scientist"}
]
```
**Output Parameters**:
- `id`: Integer
- `name`: String

### 6. Get Skill Categories by Job Title ID
**Description**: Retrieves skill categories based on the job title ID.
**cURL Command**:
```sh
curl -X GET http://127.0.0.1:5000/skill_categories/1
```
**Expected Output**:
```json
[
    {"id": 1, "name": "Programming Languages"},
    {"id": 2, "name": "Web Development"}
]
```
**Output Parameters**:
- `id`: Integer
- `name`: String

### 7. Get Skills by Skill Category ID
**Description**: Retrieves skills based on the skill category ID.
**cURL Command**:
```sh
curl -X GET http://127.0.0.1:5000/skills/1
```
**Expected Output**:
```json
[
    {"id": 1, "name": "Python"},
    {"id": 2, "name": "JavaScript"}
]
```
**Output Parameters**:
- `id`: Integer
- `name`: String

### 8. Previous Job Role
**Description**: Receives the user's previous job role ID and returns related skill categories.
**cURL Command**:
```sh
curl -X POST http://127.0.0.1:5000/previous_job_role \
-H "Content-Type: application/json" \
-d '{"job_role_id": 1}'
```
**Expected Output**:
```json
[
    {"id": 1, "name": "Programming Languages"},
    {"id": 2, "name": "Web Development"}
]
```
**Input Parameters**:
- `job_role_id`: Integer

**Output Parameters**:
- `id`: Integer
- `name`: String

### 9. Skills for Previous Role
**Description**: Receives the user's previous job role skill details and adds them to the database.
**cURL Command**:
```sh
curl -X POST http://127.0.0.1:5000/skills_for_previous_role \
-H "Content-Type: application/json" \
-d '{"user_id": 1, "skill_id": 2, "level": "Intermediate"}'
```
**Expected Output**:
```json
{
    "message": "Skill added for previous role successfully"
}
```
**Input Parameters**:
- `user_id`: Integer
- `skill_id`: Integer
- `level`: String

### 10. Desired Job Role
**Description**: Receives the user's desired job role ID and returns related skill categories.
**cURL Command**:
```sh
curl -X POST http://127.0.0.1:5000/desired_job_role \
-H "Content-Type: application/json" \
-d '{"job_role_id": 1}'
```
**Expected Output**:
```json
[
    {"id": 1, "name": "Programming Languages"},
    {"id": 2, "name": "Web Development"}
]
```
**Input Parameters**:
- `job_role_id`: Integer

**Output Parameters**:
- `id`: Integer
- `name`: String

### 11. Skills for Desired Role
**Description**: Receives the user's desired job role skill details and adds them to the database.
**cURL Command**:
```sh
curl -X POST http://127.0.0.1:5000/skills_for_desired_role \
-H "Content-Type: application/json" \
-d '{"user_id": 1, "skill_id": 2, "level": "Intermediate"}'
```
**Expected Output**:
```json
{
    "message": "Skill added for desired role successfully"
}
```
**Input Parameters**:
- `user_id`: Integer
- `skill_id`: Integer
- `level`: String
'''
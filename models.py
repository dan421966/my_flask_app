from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    skills = db.relationship('UserSkill', backref='user', lazy=True, cascade="all, delete-orphan")

class JobTitle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    skill_categories = db.relationship('SkillCategory', backref='job_title', lazy=True, cascade="all, delete-orphan")

class SkillCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    job_title_id = db.Column(db.Integer, db.ForeignKey('job_title.id'), nullable=False)
    skills = db.relationship('SkillCategorySkill', backref='skill_category', lazy=True, cascade="all, delete-orphan")

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    skill_categories = db.relationship('SkillCategorySkill', backref='skill', lazy=True, cascade="all, delete-orphan")
    users = db.relationship('UserSkill', backref='skill', lazy=True, cascade="all, delete-orphan")

class SkillCategorySkill(db.Model):
    skill_category_id = db.Column(db.Integer, db.ForeignKey('skill_category.id'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), primary_key=True)

class UserSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    level = db.Column(db.String(64), nullable=False)
    db.UniqueConstraint('user_id', 'skill_id', name='unique_user_skill')

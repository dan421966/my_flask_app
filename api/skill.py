from flask_restx import Resource, Namespace
from models import db, Skill, SkillCategory, SkillCategorySkill

api = Namespace('skills', description='Skill related operations')

@api.route('/categories/<int:job_title_id>')
class SkillCategoryList(Resource):
    def get(self, job_title_id):
        skill_categories = SkillCategory.query.filter_by(job_title_id=job_title_id).all()
        return [{'id': sc.id, 'name': sc.name} for sc in skill_categories]

@api.route('/<int:skill_category_id>')
class SkillList(Resource):
    def get(self, skill_category_id):
        skills = db.session.query(Skill).join(SkillCategorySkill).filter(SkillCategorySkill.skill_category_id == skill_category_id).all()
        return [{'id': s.id, 'name': s.name} for s in skills]

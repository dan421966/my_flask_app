from flask_restx import Resource, Namespace
from models import JobTitle

api = Namespace('job_titles', description='Job Title related operations')

@api.route('/')
class JobTitleList(Resource):
    def get(self):
        job_titles = JobTitle.query.all()
        return [{'id': jt.id, 'name': jt.name} for jt in job_titles]

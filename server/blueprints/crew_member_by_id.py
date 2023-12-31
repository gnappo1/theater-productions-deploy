from blueprints import abort, make_response, g, request, Resource, Blueprint, ValidationError, login_required
from models import db
from models.crew_member import CrewMember
from schemas.crew_member_schema import CrewMemberSchema
from sqlalchemy import func

crew_member_schema = CrewMemberSchema()
crew_member_by_id_bp = Blueprint('crew_member_by_id', __name__, url_prefix='/crew-members/<int:id>')

class CrewMemberByID(Resource):
    def get(self, id):
        cm = db.session.get(CrewMember, id)
        serialized_data = crew_member_schema.dump(cm)
        return make_response(serialized_data, 200)
    
    def patch(self, id):
        try:
            crew = db.session.get(CrewMember, id)
            data = request.json
            crew_member_schema.validate(data)
            updated_crew = crew_member_schema.load(data, instance=crew, partial=True)
            db.session.commit()
            
            serialized_crew = crew_member_schema.dump(updated_crew)
            return make_response(serialized_crew, 200)
        #! ma error that will be raised in case the schema validations are not met 
        except (ValidationError, ValueError)  as e:
            abort(400, str(e))

    def delete(self, id):
        try:
            cm = db.session.get(CrewMember, id)
            db.session.delete(cm)
            db.session.commit()
            return make_response("", 204)
        except ValueError as e:
            abort(400, str(e))
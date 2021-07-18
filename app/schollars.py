import pandas as pd
from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

from app.utilities.twilio_util import sendTwilioSMS, subscribeTwilioClient

from . import twilio_util

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(
    app,
    version="1.0",
    title="Schollars",
    description="Scholarships API",
)

ns = api.namespace("schollars", description="")

# search_fields = api.model(
#     "search_fields",
#     {
#         "benefactor": fields.String(readonly=True, description="scholarship provider"),
#         "institution": fields.String(readonly=True, description="specific institution"),
#         "faculty": fields.String(readonly=True, description="faculty or area"),
#         "educationLevel": fields.String(readonly=True, description="level of education"),
#         "isRural": fields.Boolean(readonly=True, description="rural only"),
#         "isFemale": fields.Boolean(readonly=True, description="women only"),
#         "isLGBT": fields.Boolean(readonly=True, description="LGBT only"),
#         "isIndigenous": fields.Boolean(readonly=True, description="indigenous only"),
#         "hardship": fields.Boolean(readonly=True, description="hardship only"),
#         "minATAR": fields.Integer(readonly=True, description="minimum ATAR required"),
#     },
# )
scholarship_model = api.model(
    "output_fields",
    {
        "benefactor": fields.String(readonly=True, description="scholarship provider"),
        "institution": fields.String(readonly=True, description="specific institution"),
        "faculty": fields.String(readonly=True, description="faculty or area"),
        "educationLevel": fields.String(readonly=True, description="level of education"),
        "isRural": fields.Boolean(readonly=True, description="rural only"),
        "isFemale": fields.Boolean(readonly=True, description="women only"),
        "isLGBT": fields.Boolean(readonly=True, description="LGBT only"),
        "isIndigenous": fields.Boolean(readonly=True, description="indigenous only"),
        "hardship": fields.Boolean(readonly=True, description="hardship only"),
        "minATAR": fields.Integer(readonly=True, description="minimum ATAR required"),
        "title": fields.String(readonly=True, description="title of scholarship"),
        "link": fields.String(readonly=True, description="URL to original scholarship"),
        "value": fields.Integer(readonly=True, description="scholarship value"),
        "valuePerAnnum": fields.Integer(readonly=True, description="scholarship value per year"),
        "notes": fields.String(readonly=True, description="additional notes"),
    },
)


class SubscriptionsDAO:
    def __init__(self):
        self.subscribed_users = []

    # returns True if any of the user's filter matches the criteria
    def __matchCriteria__(criteria, user_filter):
        for field, val in criteria.items():
            if user_filter[field] == val:
                return True
            return False

    # criteria is new incoming when a scholarship is created
    # returns list of matched users to the new filter
    def getMatchedSubscribers(self, criteria):
        matched_users = []
        for user in self.subscribed_users:
            if self.__matchCriteria__(criteria, user.criteria):
                matched_users.append(user)

        return matched_users

    # saves a user subscription
    def create(self, email, mobile, criteria):
        user_details = {"email": email, "mobile": mobile, "criteria": criteria}
        self.subscribed_users.append(user_details)


class ScholarshipsDAO:
    def formatScholarship(criteria):
        # TODO: format the scholarship criteria for user consumption
        return criteria

    def create(self, criteria):
        # creates new data row
        # for future implementation
        pass


DAO = SubscriptionsDAO()
scholarshipDAO = ScholarshipsDAO()
# DAO.create({"task": "Build an API"})
# DAO.create({"task": "?????"})
# DAO.create({"task": "profit!"})


# @ns.route("/search")
# class Scholarships(Resource):
#     """Search the Scholarships database and return matching rows """

#     @ns.doc("search_database")
#     @ns.marshal_list_with(search_filter)
#     def get(self):
#         # Get search criteria from payload and return found data
#         criteria = api.payload
#         return DAO.get(criteria)

#     @ns.doc("create_entry")
#     @ns.expect(todo)
#     @ns.marshal_with(todo, code=201)
#     def post(self):
#         """Create a new task"""
#         return DAO.create(api.payload), 201


@ns.route("/subscribe")
@ns.response(404, "Todo not found")
@ns.param("email", "mobile")
class Scholarships(Resource):
    @ns.doc("create_subscription")
    # @ns.marshal_with(todo)
    def post(self, email, mobile):
        criteria = api.payload
        return DAO.create(email, mobile, criteria)

    @ns.doc("create_scholarship")
    def create(self, criteria):
        # for demo version, does not actually store anywhere but does trigger the subscription alert
        matchedUsers = DAO.getMatchedSubscribers(criteria)
        # JSON?

        for user in matchedUsers:
            mobile = user.mobile
            scholarshipData = scholarshipDAO.formatScholarship(criteria)
            client = twilio_util.subscribeTwilioClient(mobile)
            twilio_util.sendTwilioSMS(client, scholarshipData, mobile)


if __name__ == "__main__":
    app.run(debug=True)

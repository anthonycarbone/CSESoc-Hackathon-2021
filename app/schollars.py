import pandas as pd
from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(
    app,
    version="1.0",
    title="Schollars",
    description="Scholarships API",
)

ns = api.namespace("schollars", description="")

search_fields = api.model(
    "search_fields",
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
    },
)
output_fields = api.model(
    "output_fields",
    {
        "title": fields.String(readonly=True, description="title of scholarship"),
        "link": fields.String(readonly=True, description="URL to original scholarship"),
        "value": fields.Integer(readonly=True, description="scholarship value"),
        "valuePerAnnum": fields.Integer(readonly=True, description="scholarship value per year"),
        "notes": fields.String(readonly=True, description="additional notes"),
    },
)


class ScholarshipsDAO:
    def __init__(self):
        df = pd.read_csv("database.csv")

    def get(self, criteria):
        for field in criteria:
            if todo["id"] == id:
                return todo

        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        todo["id"] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo

    def update(self, id, data):
        todo = self.get(id)
        todo.update(data)
        return todo

    def delete(self, id):
        todo = self.get(id)
        self.todos.remove(todo)


DAO = ScholarshipsDAO()
DAO.create({"task": "Build an API"})
DAO.create({"task": "?????"})
DAO.create({"task": "profit!"})


@ns.route("/search")
class Scholarships(Resource):
    """Search the Scholarships database and return matching rows """

    @ns.doc("search_database")
    @ns.marshal_list_with(search_filter)
    def get(self):
        # Get search criteria from payload and return found data
        criteria = api.payload
        return DAO.get(criteria)

    @ns.doc("create_entry")
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        """Create a new task"""
        return DAO.create(api.payload), 201


# @ns.route("/<int:id>")
# @ns.response(404, "Todo not found")
# @ns.param("id", "The task identifier")
# class Todo(Resource):
#     """Show a single todo item and lets you delete them"""

#     @ns.doc("get_todo")
#     @ns.marshal_with(todo)
#     def get(self, id):
#         """Fetch a given resource"""
#         return DAO.get(id)

#     @ns.doc("delete_todo")
#     @ns.response(204, "Todo deleted")
#     def delete(self, id):
#         """Delete a task given its identifier"""
#         DAO.delete(id)
#         return "", 204

#     @ns.expect(todo)
#     @ns.marshal_with(todo)
#     def put(self, id):
#         """Update a task given its identifier"""
#         return DAO.update(id, api.payload)


if __name__ == "__main__":
    app.run(debug=True)

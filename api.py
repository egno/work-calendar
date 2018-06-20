from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api
from werkzeug.contrib.fixers import ProxyFix
import datetime
import dateutil.parser
from gov_work_calendar import GovCalendar

app = Flask(__name__)
CORS(app)
api = Api(app)

calendar = GovCalendar()


class Today(Resource):
    def get(self):
        date = datetime.date.today()
        return(calendar.date(date))


class Day(Resource):
    def get(self, day):
        date = dateutil.parser.parse(day).date()
        return(calendar.date(date))


class Update(Resource):
    def get(self):
        return(calendar.update())


api.add_resource(Today, '/day/')
api.add_resource(Day, '/day/<string:day>/')
api.add_resource(Update, '/update/')


app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
    # app.run(host='0.0.0.0', port='8080')
    app.run()

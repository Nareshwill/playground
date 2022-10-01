from flask import Flask
import pymongo
from flask_sqlalchemy import SQLAlchemy
from healthcheck import HealthCheck

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://demouser1:password@localhost/test_manager'

db = SQLAlchemy(app=app)
mongo_client = pymongo.MongoClient("mongodb://demouser1:password@localhost:27017/?authSource=close_loop_validation")
health = HealthCheck()

app.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health.run())


def monitor_db_health_status():
    is_database_working = True
    output = "database is up & running"

    try:
        # Checking MongoDB
        mongo_client.admin.command("ping")
        # Checking MySQL
        db.session.execute("SELECT 1")
    except Exception as e:
        output = str(e)
        is_database_working = False
    return is_database_working, output


health.add_section("db_health_checker", monitor_db_health_status)

if __name__ == "__main__":
    app.run()

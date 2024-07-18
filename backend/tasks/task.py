from models.models import *
from app import scheduler
import logging
from datetime import datetime, timedelta
from extensions.extensions import db
from app import app


logging.basicConfig(level=logging.INFO)


def delete_users_more_than_expected_year():
    """
        This task runs every 24 hours and delete users that
        has been registered for 5 years.  
    """

    with  scheduler.app.app_context():

        STUDENT = 0

        five_years_ago = datetime.now() - timedelta(days=5*365)

        db.session.query(User).filter(User.date_registered <= five_years_ago, User.user_type==STUDENT).delete()

        db.session.commit()
        
        logging.info('This runs and deletes user who has expired date.')

scheduler.start()
scheduler.add_job(
    id='delete_users_more_than_expected_year',
    func=delete_users_more_than_expected_year,
    trigger='cron',
    minute='*')

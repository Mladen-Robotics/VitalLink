from flask import (Blueprint,render_template,
                request, redirect, url_for,
                flash)

from web_app_new.db_utilities import *
from flask_cors import cross_origin

from .auth import login_required # Check if user is logged!!


pdashboard_bl = Blueprint('patient_dashboard', __name__, template_folder='templates/patient_dashboard', url_prefix='/')

@pdashboard_bl.route('/patient/<int:id>/')
@cross_origin(origin='*', supports_credentials=True)
def main(id):
    print('yes')
    return render_template('main.html')
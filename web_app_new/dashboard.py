from flask import (Blueprint,render_template,
                request, redirect, url_for,
                flash)

from web_app.db_utilities import *

from .auth import login_required # Check if user is logged!!
from flask_cors import cross_origin

dashboard_bl = Blueprint('dashboard', __name__, template_folder='templates/dashboard', url_prefix='/')

@dashboard_bl.route('/', endpoint="main_dashboard")
@login_required
@cross_origin(origin='*', supports_credentials=True)
def index():
    return render_template('main.html')

@dashboard_bl.route('/about')
@cross_origin(origin='*', supports_credentials=True)
def about():
    return render_template('about.html')

@dashboard_bl.route('/patient/<int:id>')
@cross_origin(origin='*', supports_credentials=True)
def patient_info(id):
    return render_template('patient_dashboard.html')
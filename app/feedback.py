from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from .models.user import User
from flask import Blueprint
from .models.modelFeedback import Feedback
from flask_paginate import Pagination, get_page_parameter
from flask import current_app as app
from datetime import datetime

bp = Blueprint('feedback', __name__)

class UserIDForm(FlaskForm):
    userid = IntegerField('User ID', validators=[DataRequired()])
    submit = SubmitField('Submit')

class FeedbackForm(FlaskForm):
    userid = IntegerField('User ID', validators=[DataRequired()])
    productid = IntegerField('Product ID (0 If Null)')
    sellerid = IntegerField('Seller ID (0 If Null)')
    review = StringField('Review')
    revtime = DateField('Time of Review')
    submit2 = SubmitField('Submit')

class DeleteForm(FlaskForm):
    userid = IntegerField('User ID', validators=[DataRequired()])
    productid = IntegerField('Product ID (0 If Null)')
    sellerid = IntegerField('Seller ID (0 If Null)')
    submit3 = SubmitField('Submit')

@bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)

    form = UserIDForm()
    form2 = FeedbackForm()
    form3 = DeleteForm()
    feedback = []
    feedback2 = []
    pagination = []
    offset = (page-1)*10
    per_page = 10
    if form.submit.data and form.validate():
        return redirect(
            url_for("feedback.feedback") +
            "?userid=" + str(form.userid.data))
    form.userid.data = request.args.get("userid")
    feedback = Feedback.get_by_uid(form.userid.data)
    feedback2 = feedback[offset: offset + per_page]
    pagination = Pagination(page=page, total=len(feedback), search=search, record_name='feedback', show_single_page = True)

    form2.revtime.data = datetime.now()
    form2.revtime.data = form2.revtime.data.replace(microsecond=0)
    if form2.submit2.data and form2.validate():
        Feedback.update(1,
                        form2.userid.data,
                        form2.productid.data,
                        form2.sellerid.data,
                        form2.review.data,
                        form2.revtime.data)

    if form3.submit3.data and form3.validate():
        Feedback.delete(form3.userid.data,
                        form3.productid.data,
                        form3.sellerid.data)

    psum = Feedback.psummary()
    ssum = Feedback.ssummary()

    return render_template('feedback.html', title='Submit', form=form, form2=form2, form3=form3, feedback=feedback2, pagination=pagination, psum=psum, ssum=ssum)
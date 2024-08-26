from flask import render_template, redirect, url_for, flash, request, jsonify, Blueprint
from flask_login import login_required, current_user
from app import db
from app.models import Schedule, User
from app.forms import ScheduleForm

schedules = Blueprint('schedules', __name__)

@schedules.route('/view_schedule')
@login_required
def view_schedule():
    schedules = Schedule.query.all()
    return render_template('view_schedule.html', title='View Schedule', schedules=schedules)



@schedules.route('/create_schedule', methods=['GET', 'POST'])
@login_required
def create_schedule():
    form = ScheduleForm()
    if form.validate_on_submit():
        schedule = Schedule(
            title=form.title.data,
            start=form.start.data,
            end=form.end.data,
            venue=form.venue.data,
            examiner_id=form.examiner.data
        )
        db.session.add(schedule)
        db.session.commit()
        flash('Schedule created successfully', 'success')
        return redirect(url_for('schedules.create_schedule'))
    return render_template('create_schedule.html', title='Create Schedule', form=form)


@schedules.route('/schedule/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_schedule(id):
    schedule = Schedule.query.get_or_404(id)
    form = ScheduleForm(obj=schedule)
    if form.validate_on_submit():
        schedule.title = form.title.data
        schedule.start = form.start.data
        schedule.end = form.end.data
        schedule.venue = form.venue.data
        schedule.examiner_id = form.examiner.data
        db.session.commit()
        flash('Schedule updated successfully!', 'success')
        return redirect(url_for('schedules.view_schedules'))
    return render_template('edit_schedule.html', title='Edit Schedule', form=form)




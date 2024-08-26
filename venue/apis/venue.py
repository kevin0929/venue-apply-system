from flask import Blueprint, request, redirect, url_for, flash, render_template, jsonify, make_response, session

from manager.venue import *
from manager.user import *
from manager.application import *


__all__ = ['venue_api']

venue_api = Blueprint('venue_api', __name__)


@venue_api.route("/<vid>/index/", methods=["GET", "POST"])
def index(vid):
    venue_manager = VenueManager()
    venues = venue_manager.get_all_venue()
    current_venue = venue_manager.get_venue_by_id(vid)

    app_manager = ApplicationManager()
    apps = app_manager.get_all_application()

    data = {
        "venues": venues,
        "current_venue": current_venue,
        "apps": apps
    }

    return render_template("index.html", data=data)


@venue_api.route("/<vid>/apply/<datetime>", methods=["GET", "POST"])
def apply(vid, datetime):
    venue_manager = VenueManager()
    user_manager = UserManager()
    app_manager = ApplicationManager()

    # get current user and venue to relate application
    current_venue = venue_manager.get_venue_by_id(vid)

    userid = session.get("userid")
    current_user = user_manager.get_user_by_id(userid)

    # check this venue whether has been reserved by other user
    conflict_flag = app_manager.check_application_conflict(venue=current_venue, datetime=datetime)
    if conflict_flag:
        return make_response('This venue has already reserved by other user', 409)

    app_manager.add_application(current_user, current_venue, datetime, 1)

    return redirect(url_for('venue_api.index', vid=vid))


@venue_api.route("/<vid>/delete/<datetime>", methods=["GET", "POST"])
def delete(vid, datetime):
    venue_manager = VenueManager()
    user_manager = UserManager()
    app_manager = ApplicationManager()

    current_venue = venue_manager.get_venue_by_id(vid)

    userid = session.get("userid")
    current_user = user_manager.get_user_by_id(userid)

    # delete application
    app_manager.delete_application(user=current_user, venue=current_venue, datetime=datetime)

    return redirect(url_for('venue_api.index', vid=vid))


@venue_api.route("/<vid>/queue/<datetime>", methods=["GET", "POST"])
def queue(vid, datetime):
    venue_manager = VenueManager()
    user_manager = UserManager()
    app_manager = ApplicationManager()

    current_venue = venue_manager.get_venue_by_id(vid)

    userid = session.get("userid")
    current_user = user_manager.get_user_by_id(userid)

    # get maximum order
    max_order = app_manager.get_order_from_venue_and_datetime(venue=current_venue, datetime=datetime)
    print(max_order)
    new_order = max_order + 1

    # add new application to this venue stand in line
    app_manager.add_application(user=current_user, venue=current_venue, datetime=datetime, order=new_order)

    return redirect(url_for('venue_api.index', vid=vid))


@venue_api.route("/<vid>/get_applications", methods=["GET"])
def get_applications(vid):
    app_manager = ApplicationManager()

    apps = app_manager.get_all_application()
    app_data = [{"date": app.datetime, "user": app.user.username, "venue_id": app.venue.vid} for app in apps]

    return jsonify(app_data)

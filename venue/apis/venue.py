from flask import Blueprint, request, redirect, url_for, flash, render_template, jsonify, make_response

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

    data = {
        "venues": venues,
        "current_venue": current_venue
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

    return make_response('Successfully apply!')


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

    return make_response('Successfully delete!')


@venue_api.route("/<vid>/get_applications", methods=["GET"])
def get_applications(vid):
    app_manager = ApplicationManager()

    apps = app_manager.get_all_application()
    app_data = [{"date": app.datetime, "user": app.user.username} for app in apps]

    return jsonify(app_data)

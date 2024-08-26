from flask import Blueprint, request, redirect, url_for, flash, render_template, jsonify

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


@venue_api.route("/<vid>/reserve/<date>", methods=["GET", "POST"])
def reserve(vid, date):
    venue_manager = VenueManager()
    user_manager = UserManager()
    app_manager = ApplicationManager()

    # get current user and venue to relate application
    venue = venue_manager.get_venue_by_id(vid)

    userid = session.get("userid")
    current_user = user_manager.get_user_by_id(userid)

    app_manager.add_application(current_user, venue, date, 1)

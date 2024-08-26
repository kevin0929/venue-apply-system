from flask import Blueprint, request, redirect, url_for, flash, session, render_template, make_response

from manager.user import *
from manager.venue import *


__all__ = ['admin_api']

admin_api = Blueprint('admin_api', __name__)


@admin_api.route("/index", methods=["GET", "POST"])
def index():
    return render_template("admin/index.html")


'''
The route above is all about venue management
'''


@admin_api.route("/venue/index", methods=["GET", "POST"])
def venue():
    venue_manager = VenueManager()
    venues = venue_manager.get_all_venue()

    return render_template("admin/venue.html", venues=venues)


@admin_api.route("/venue/add_venue", methods=["GET", "POST"])
def add_venue():
    if request.method == "POST":
        create_name = request.form.get("venue_name")
    
    # add new venue
    venue_manager = VenueManager()
    venue_manager.add_venue(create_name)

    return redirect(url_for("admin_api.venue"))


@admin_api.route("/venue/<vid>/delete", methods=["GET", "POST"])
def delete_venue(vid):
    venue_manager = VenueManager()
    venue_manager.delete_venue(vid)

    return redirect(url_for("admin_api.venue"))


@admin_api.route("/venue/<vid>/edit_venue", methods=["GET", "POST"])
def edit_venue(vid):
    venue_manager = VenueManager()
    venue = venue_manager.get_venue_by_id(vid)

    if request.method == "POST":
        new_name = request.form.get("venue_name")

    # modify name
    venue_manager.edit_venue(venue=venue, new_name=new_name)

    return redirect(url_for("admin_api.venue"))


'''
The route above is all about venue management
'''


@admin_api.route("/user/index", methods=["GET", "POST"])
def user():
    user_manager = UserManager()
    users = user_manager.get_all_user()

    return render_template("admin/user.html", users=users)


@admin_api.route("/user/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        username = request.form.get("user_name")
        password = request.form.get("user_password")
        email = request.form.get("user_email")
        role = request.form.get("user_role")

    # add user
    userinfo = {
        "username": username,
        "password": password,
        "email": email,
        "role": role
    }
    user_manager = UserManager()
    user_manager.add_user(userinfo)

    return redirect(url_for("admin_api.user"))


@admin_api.route("/user/<userid>/edit_user", methods=["GET", "POST"])
def edit_user(userid):
    if request.method == "POST":
        username = request.form.get("user_name")
        email = request.form.get("user_email")
        role = request.form.get("user_role")

    # edit user
    userinfo = {
        "username": username,
        "email": email,
        "role": role
    }
    user_manager = UserManager()
    user = user_manager.get_user_by_id(userid)
    user_manager.edit_user(user, userinfo)

    return redirect(url_for("admin_api.user"))


@admin_api.route("/user/<userid>/delete_user", methods=["GET", "POST"])
def delete_user(userid):
    user_manager = UserManager()
    user_manager.delete_user(userid)

    return redirect(url_for("admin_api.user"))

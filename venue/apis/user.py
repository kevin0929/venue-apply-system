from flask import Blueprint, request, redirect, url_for, flash, session

from manager.user import *


__all__ = ['user_api']

user_api = Blueprint('user_api', __name__)


@user_api.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user_manager = UserManager()
        user = user_manager.get_user_by_username(username)
        match_password = user.password
        userid = user.userid
        role = user.role

        '''
            1. if match_password is str, it means that this is correct query.
            2. if tuple, it means there has something wrong, and we will get error msg.
        '''
        if isinstance(match_password, str):
            if password == match_password:
                # store user information into session
                session["userid"] = userid
                session["role"] = role
                session.permanent = True

                return redirect(url_for("venue_api.index", vid=1))
            else:
                flash("Incorrect password. Please try again.", "error")
                return redirect(url_for("login_page"))
        else:
            flash(match_password[1], "error")
            return redirect(url_for("login_page"))


@user_api.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("userid", None)

    return redirect(url_for("login_page")) 

from functools import wraps
from flask import abort, session, flash, redirect, url_for


def login_required(role: str):
    '''check user wheher has logged in by session'''

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            username = session.get("userid")
            user_role = session.get("role")
            
            if not username:
                flash("Not Logged In!", "error")
                return redirect(url_for("login_page"))
            else:
                if (role == "admin") and (user_role != role):
                    flash("Permission error!", "error")
                    return redirect(url_for("user_api.logout"))
                elif (role == "user") and (user_role not in ["admin", "user"]):
                    flash("Please Log In!", "error")
                    return redirect(url_for("user_api.logout"))

            return func(*args, **kwargs)

        return wrapper

    return decorator
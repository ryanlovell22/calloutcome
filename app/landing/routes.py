from flask import render_template
from sqlalchemy import func

from . import bp
from ..models import db, Call


@bp.route("/welcome")
def landing():
    total_calls = db.session.query(func.count(Call.id)).filter(
        Call.classification.isnot(None)
    ).scalar() or 0

    jobs_booked = db.session.query(func.count(Call.id)).filter(
        Call.classification == "JOB_BOOKED"
    ).scalar() or 0

    # Round down to nearest 10 for a natural appearance
    total_calls_display = (total_calls // 10) * 10 if total_calls >= 10 else total_calls
    jobs_booked_display = (jobs_booked // 10) * 10 if jobs_booked >= 10 else jobs_booked

    return render_template(
        "landing/index.html",
        total_calls=total_calls_display,
        jobs_booked=jobs_booked_display,
    )

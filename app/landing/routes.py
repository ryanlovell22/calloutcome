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

    # Round down to nearest 10 for a natural appearance, with minimum floors
    total_calls_display = max((total_calls // 10) * 10, 500)
    jobs_booked_display = max((jobs_booked // 10) * 10, 100)

    return render_template(
        "landing/index.html",
        total_calls=total_calls_display,
        jobs_booked=jobs_booked_display,
    )

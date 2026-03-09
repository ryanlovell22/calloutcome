from urllib.parse import urlencode

from flask import render_template, request
from sqlalchemy import func

from . import bp
from ..models import db, Call
from ..utm_utils import capture_utm, UTM_PARAMS


def _get_stats():
    """Get call stats for landing page display."""
    total_calls = db.session.query(func.count(Call.id)).filter(
        Call.classification.isnot(None)
    ).scalar() or 0

    jobs_booked = db.session.query(func.count(Call.id)).filter(
        Call.classification == "JOB_BOOKED"
    ).scalar() or 0

    total_calls_display = max((total_calls // 10) * 10, 500)
    jobs_booked_display = max((jobs_booked // 10) * 10, 100)
    return total_calls_display, jobs_booked_display


@bp.route("/welcome")
def landing():
    capture_utm()
    total_calls, jobs_booked = _get_stats()
    return render_template(
        "landing/index.html",
        total_calls=total_calls,
        jobs_booked=jobs_booked,
    )


@bp.route("/try")
def try_page():
    capture_utm()
    total_calls, jobs_booked = _get_stats()

    # Pass UTM query string so CTA links preserve params
    utm = {p: request.args[p] for p in UTM_PARAMS if p in request.args}
    utm_query = '?' + urlencode(utm) if utm else ''

    # Pass utm_content for dynamic hero headline matching
    utm_content = request.args.get('utm_content', '')

    return render_template(
        "landing/try.html",
        total_calls=total_calls,
        jobs_booked=jobs_booked,
        utm_query=utm_query,
        utm_content=utm_content,
    )

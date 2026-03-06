import logging
from datetime import datetime, timedelta, timezone

import requests as http_requests
from flask import render_template, request, redirect, url_for, session, abort, Response
from werkzeug.security import check_password_hash

from ..models import db, Call, SharedDashboard, Account
from . import bp

logger = logging.getLogger(__name__)


@bp.route("/proof/<share_token>")
def public_dashboard(share_token):
    """Public proof dashboard — no login required."""
    dashboard = SharedDashboard.query.filter_by(
        share_token=share_token, active=True
    ).first_or_404()

    # Password protection check
    if dashboard.password_hash:
        session_key = f"proof_auth_{share_token}"
        if not session.get(session_key):
            return render_template("shared/password.html", share_token=share_token)

    # Build call query scoped to the shared link's tracking lines
    query = Call.query.filter_by(account_id=dashboard.account_id)
    line_ids = [l.id for l in dashboard.tracking_lines]
    if line_ids:
        query = query.filter(Call.tracking_line_id.in_(line_ids))
    else:
        query = query.filter(False)

    # Date window: use the configured rolling window, or default to 30 days
    today = datetime.now(timezone.utc).date()
    window_days = dashboard.date_window_days or 30
    date_from = (today - timedelta(days=window_days)).strftime("%Y-%m-%d")
    date_to = today.strftime("%Y-%m-%d")

    try:
        dt_from = datetime.strptime(date_from, "%Y-%m-%d")
        query = query.filter(Call.call_date >= dt_from)
    except ValueError:
        pass
    try:
        dt_to = datetime.strptime(date_to, "%Y-%m-%d") + timedelta(days=1)
        query = query.filter(Call.call_date < dt_to)
    except ValueError:
        pass

    # Only count completed, answered calls for stats
    answered_query = query.filter(
        Call.call_outcome != "missed",
        Call.status == "completed",
    )
    booked = answered_query.filter(Call.classification == "JOB_BOOKED").count()
    not_booked = answered_query.filter(Call.classification == "NOT_BOOKED").count()
    total_answered = booked + not_booked
    rate = round(booked / total_answered * 100, 1) if total_answered > 0 else 0

    calls = answered_query.order_by(Call.call_date.desc()).all()

    # Build a human-readable window label
    if window_days <= 7:
        window_label = "Last 7 days"
    elif window_days <= 14:
        window_label = "Last 14 days"
    elif window_days <= 30:
        window_label = "Last 30 days"
    elif window_days <= 60:
        window_label = "Last 60 days"
    elif window_days <= 90:
        window_label = "Last 90 days"
    else:
        window_label = f"Last {window_days} days"

    return render_template(
        "shared/dashboard.html",
        dashboard=dashboard,
        calls=calls,
        stats={"total": total_answered, "booked": booked, "not_booked": not_booked, "rate": rate},
        window_label=window_label,
        share_token=share_token,
    )


@bp.route("/proof/<share_token>/auth", methods=["POST"])
def public_dashboard_auth(share_token):
    """Authenticate for a password-protected proof dashboard."""
    dashboard = SharedDashboard.query.filter_by(
        share_token=share_token, active=True
    ).first_or_404()

    password = request.form.get("password", "")
    if dashboard.password_hash and check_password_hash(dashboard.password_hash, password):
        session[f"proof_auth_{share_token}"] = True
        return redirect(url_for("shared.public_dashboard", share_token=share_token))

    return render_template(
        "shared/password.html",
        share_token=share_token,
        error="Incorrect password.",
    )


@bp.route("/proof/<share_token>/calls/<int:call_id>")
def public_call_detail(share_token, call_id):
    """Public call detail page."""
    dashboard = SharedDashboard.query.filter_by(
        share_token=share_token, active=True
    ).first_or_404()

    # Password check
    if dashboard.password_hash:
        if not session.get(f"proof_auth_{share_token}"):
            return redirect(url_for("shared.public_dashboard", share_token=share_token))

    call = Call.query.filter_by(
        id=call_id, account_id=dashboard.account_id
    ).first_or_404()

    # Verify call belongs to dashboard scope
    shared_line_ids = [l.id for l in dashboard.tracking_lines]
    if call.tracking_line_id not in shared_line_ids:
        abort(404)

    return render_template(
        "shared/call_detail.html",
        dashboard=dashboard,
        call=call,
        share_token=share_token,
    )


@bp.route("/proof/<share_token>/calls/<int:call_id>/recording")
def public_call_recording(share_token, call_id):
    """Proxy recording audio for shared proof links."""
    dashboard = SharedDashboard.query.filter_by(
        share_token=share_token, active=True
    ).first_or_404()

    # Password check
    if dashboard.password_hash:
        if not session.get(f"proof_auth_{share_token}"):
            abort(403)

    if not dashboard.show_recordings:
        abort(404)

    call = Call.query.filter_by(
        id=call_id, account_id=dashboard.account_id
    ).first_or_404()

    # Verify call belongs to dashboard scope
    shared_line_ids = [l.id for l in dashboard.tracking_lines]
    if call.tracking_line_id not in shared_line_ids:
        abort(404)

    if not call.recording_url:
        return "Recording not available", 404

    account = db.session.get(Account, dashboard.account_id)
    if not account:
        return "Recording not available", 404

    # Twilio recordings need auth; CallRail CDN URLs are pre-signed
    is_twilio = "twilio.com" in call.recording_url
    if is_twilio:
        resp = http_requests.get(
            f"{call.recording_url}.mp3",
            auth=(account.twilio_account_sid, account.twilio_auth_token_encrypted),
            stream=True,
            timeout=30,
        )
    else:
        resp = http_requests.get(
            call.recording_url,
            stream=True,
            timeout=30,
        )

    if resp.status_code != 200:
        return "Recording not available", 404

    content_type = resp.headers.get("Content-Type", "audio/mpeg")

    return Response(
        resp.iter_content(chunk_size=8192),
        content_type=content_type,
        headers={"Content-Disposition": "inline"},
    )

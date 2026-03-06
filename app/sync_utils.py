import threading

from flask import current_app

from .models import db
from .poll_service import run_full_sync


def spawn_backfill(account_id, days=7):
    """Run a full Twilio sync in a background thread."""
    from .models import Account
    app = current_app._get_current_object()

    def _run():
        with app.app_context():
            account = db.session.get(Account, account_id)
            if account:
                run_full_sync(account, days=days)

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()


def spawn_callrail_backfill(account_id, days=7):
    """Run a CallRail backfill in a background thread."""
    from .models import Account
    app = current_app._get_current_object()

    def _run():
        with app.app_context():
            account = db.session.get(Account, account_id)
            if account:
                from .poll_service import run_callrail_backfill
                run_callrail_backfill(account, days=days)

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()

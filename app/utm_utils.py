from flask import request, session

UTM_PARAMS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content']


def capture_utm():
    """Capture UTM params from query string into session (first touch wins)."""
    if any(request.args.get(p) for p in UTM_PARAMS):
        if 'utm_data' not in session:
            utm = {p: request.args.get(p, '') for p in UTM_PARAMS if request.args.get(p)}
            utm['landing_page'] = request.path
            session['utm_data'] = utm

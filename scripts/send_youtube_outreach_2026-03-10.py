#!/usr/bin/env python3
"""
YouTube Sponsorship Outreach — Send personalised emails via Resend API.

Usage:
    # Send first batch (batch 1)
    python scripts/send_youtube_outreach_2026-03-10.py --batch 1

    # Send follow-ups (batch 2) — use 5-7 days after batch 1
    python scripts/send_youtube_outreach_2026-03-10.py --batch 2

    # Dry run (preview emails without sending)
    python scripts/send_youtube_outreach_2026-03-10.py --batch 1 --dry-run

    # Send to a specific creator only
    python scripts/send_youtube_outreach_2026-03-10.py --batch 1 --only getbizzyllc
"""

import argparse
import json
import os
import sys
from datetime import datetime

import requests

RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
FROM_EMAIL = "Ryan <ryan@calloutcome.com>"
REPLY_TO = "ryan@lovelldigitalproperties.com"

# ── Creator data ────────────────────────────────────────────────────────────

CREATORS = {
    "getbizzyllc": {
        "name": "Israel",
        "channel": "Get Bizzy LLC",
        "handle": "@GetBizzyLLC",
        "subs": "6.79K",
        "email": "israel@izzymarketing.com",
        "video_title": "Building a Google-Ranking Wix Website for a Local Contractor (Live Tutorial)",
        "utm_campaign": "getbizzyllc",
        "template": "direct",
    },
    "ippeiseo": {
        "name": "Ippei",
        "channel": "Ippei - Local SEO Lead Generation",
        "handle": "@IppeiSEO",
        "subs": "9.75K",
        "email": "ippeikanehara7@gmail.com",
        "video_title": "Rank and Rent - On-Page SEO Secrets in 2026",
        "utm_campaign": "ippeiseo",
        "template": "direct",
    },
    "leadbase": {
        "name": "Ryan",
        "channel": "Leadbase",
        "handle": "@getleadbase",
        "subs": "11.7K",
        "email": "hello@getleadbase.com",
        "video_title": "How Jacob Sold $100K in Leads in 40 Days",
        "utm_campaign": "leadbase",
        "template": "direct",
    },
    "nateancelet": {
        "name": "Nate",
        "channel": "Nate Ancelet",
        "handle": "@Nateancelet",
        "subs": "3.55K",
        "email": "nate@anceletadvising.com",
        "video_title": "$17,000/Wk With Final Expense From The Calls We Gave Him",
        "utm_campaign": "nateancelet",
        "template": "soft",
    },
    # ── Tier 2 (send if Tier 1 doesn't get enough responses) ──
    "decodingads": {
        "name": "there",
        "channel": "Decoding Ads",
        "handle": "@decodingads",
        "subs": "14K",
        "email": "admin@decodingads.org",
        "video_title": "How Beginners Can Start Pay Per Call + Advanced SEO (Live Class Step-by-Step)",
        "utm_campaign": "decodingads",
        "template": "direct",
    },
    "adammcinnes": {
        "name": "Adam",
        "channel": "Adam McInnes",
        "handle": "@adammcinnes",
        "subs": "6.42K",
        "email": "support@joinghlmastery.com",
        "video_title": "HighLevel Just Dropped Video Reviews. Here's How to Set It Up FAST",
        "utm_campaign": "adammcinnes",
        "template": "soft",
    },
    "gatlinmcbride": {
        "name": "Gatlin",
        "channel": "Gatlin McBride",
        "handle": "@Gatlin.McBride",
        "subs": "5.35K",
        "email": "info@dirtymint.com",
        "video_title": "Winter Is the Real Test For Home Service Businesses",
        "utm_campaign": "gatlinmcbride",
        "template": "soft",
    },
}

# Which creators to include in each batch
BATCHES = {
    1: ["getbizzyllc", "ippeiseo", "leadbase", "nateancelet"],
    2: ["decodingads", "adammcinnes", "gatlinmcbride"],
}


# ── Email templates ─────────────────────────────────────────────────────────

def template_direct(c):
    """Direct pitch — for channels with 5K+ subs."""
    return {
        "subject": f"Sponsorship opportunity — $150 for a mention in a video",
        "html": f"""<p>Hey {c['name']},</p>

<p>I've been watching your content — really solid stuff, especially your video "{c['video_title']}".</p>

<p>I built a tool called <a href="https://calloutcome.com/try?utm_source=youtube&utm_medium=sponsorship&utm_campaign={c['utm_campaign']}">CallOutcome</a> that auto-classifies call recordings as job booked, not booked, or voicemail. It connects to CallRail or Twilio and uses AI to score every call — basically what lead gen operators do manually (listening to recordings) but automated.</p>

<p>Would you be open to a <strong>$150 sponsored mention</strong> in one of your upcoming videos? Not looking for a full dedicated video — just a 60-90 second segment showing what it does.</p>

<p>Happy to set you up with a <strong>free lifetime Pro account</strong> ($79/mo value) so you can try it with your own calls first. No strings attached either way.</p>

<p>Cheers,<br>
Ryan</p>

<p><a href="https://calloutcome.com/try?utm_source=youtube&utm_medium=sponsorship&utm_campaign={c['utm_campaign']}">calloutcome.com</a></p>""",
    }


def template_soft(c):
    """Softer approach — for smaller channels or less direct fit."""
    return {
        "subject": "Free tool for your lead gen workflow — want to try it?",
        "html": f"""<p>Hey {c['name']},</p>

<p>I run rank-and-rent sites across 20+ niches and got tired of listening to every call recording to figure out what booked. So I built a tool that does it with AI.</p>

<p>It's called <a href="https://calloutcome.com/try?utm_source=youtube&utm_medium=sponsorship&utm_campaign={c['utm_campaign']}">CallOutcome</a> — connects to CallRail or Twilio, transcribes every call, and classifies the outcome automatically. Also has partner proof dashboards so your clients can see results without you sending spreadsheets.</p>

<p>Wanted to offer you a <strong>free Pro account</strong> to try it. If you find it useful and want to mention it in a video at some point, I'd be happy to pay for a sponsored mention ($150-200). But no pressure — genuinely just think you'd find it useful based on your content, especially "{c['video_title']}".</p>

<p>Let me know if you're interested and I'll set up your account.</p>

<p>Cheers,<br>
Ryan</p>

<p><a href="https://calloutcome.com/try?utm_source=youtube&utm_medium=sponsorship&utm_campaign={c['utm_campaign']}">calloutcome.com</a></p>""",
    }


def template_followup(c):
    """Follow-up — send 5-7 days after initial email. Lower ask: $50 + free lifetime account."""
    return {
        "subject": f"Re: Quick follow-up — free tool + $50 for a mention",
        "html": f"""<p>Hey {c['name']}, just following up on my email from last week. No worries if it's not a fit — just wanted to make sure it didn't get buried.</p>

<p>Quick recap: I built <a href="https://calloutcome.com/try?utm_source=youtube&utm_medium=sponsorship&utm_campaign={c['utm_campaign']}">CallOutcome</a> — it auto-classifies call recordings as job booked, not booked, or voicemail. Built for lead gen operators and rank-and-rent people.</p>

<p>I'd love to give you a <strong>free lifetime Pro account</strong> (normally $79/mo) to try with your own calls. If you like it enough to mention it in a video — even just 30-60 seconds — I'll send <strong>$50 via PayPal</strong> as a thank you. Zero pressure either way.</p>

<p>Let me know if you're keen and I'll set up your account.</p>

<p>Cheers,<br>Ryan</p>""",
    }


TEMPLATES = {
    "direct": template_direct,
    "soft": template_soft,
    "followup": template_followup,
}


# ── Send email via Resend ──────────────────────────────────────────────────

def send_email(to, subject, html, dry_run=False):
    """Send an email via Resend API. Returns (success, response_data)."""
    if dry_run:
        print(f"  [DRY RUN] Would send to: {to}")
        print(f"  Subject: {subject}")
        print(f"  From: {FROM_EMAIL}")
        print(f"  Reply-To: {REPLY_TO}")
        print()
        return True, {"id": "dry-run"}

    if not RESEND_API_KEY:
        print("ERROR: RESEND_API_KEY not set. Run: export $(cat ~/.claude/credentials.env | grep -v '^#' | xargs)")
        sys.exit(1)

    resp = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "from": FROM_EMAIL,
            "to": [to],
            "reply_to": REPLY_TO,
            "subject": subject,
            "html": html,
        },
    )

    if resp.status_code == 200:
        data = resp.json()
        print(f"  ✓ Sent to {to} (Resend ID: {data.get('id', 'unknown')})")
        return True, data
    else:
        print(f"  ✗ Failed to send to {to}: {resp.status_code} {resp.text}")
        return False, resp.text


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Send YouTube sponsorship outreach emails")
    parser.add_argument("--batch", type=int, required=True, help="Batch number (1=first outreach, 2=tier 2)")
    parser.add_argument("--dry-run", action="store_true", help="Preview emails without sending")
    parser.add_argument("--only", type=str, help="Send to a specific creator only (by key)")
    parser.add_argument("--followup", action="store_true", help="Send follow-up template instead of initial")
    args = parser.parse_args()

    if args.batch not in BATCHES:
        print(f"ERROR: Unknown batch {args.batch}. Available: {list(BATCHES.keys())}")
        sys.exit(1)

    keys = BATCHES[args.batch]
    if args.only:
        if args.only not in CREATORS:
            print(f"ERROR: Unknown creator '{args.only}'. Available: {list(CREATORS.keys())}")
            sys.exit(1)
        keys = [args.only]

    print(f"\n{'=' * 60}")
    print(f"YouTube Sponsorship Outreach — Batch {args.batch}")
    print(f"{'=' * 60}")
    if args.dry_run:
        print("[DRY RUN MODE — no emails will be sent]\n")
    print()

    results = []
    for key in keys:
        c = CREATORS[key]
        template_name = "followup" if args.followup else c["template"]
        template_fn = TEMPLATES[template_name]
        email_data = template_fn(c)

        print(f"→ {c['channel']} ({c['handle']}, {c['subs']} subs)")
        success, resp = send_email(c["email"], email_data["subject"], email_data["html"], args.dry_run)

        results.append({
            "key": key,
            "name": c["name"],
            "channel": c["channel"],
            "email": c["email"],
            "template": template_name,
            "success": success,
            "resend_id": resp.get("id") if isinstance(resp, dict) else None,
            "timestamp": datetime.utcnow().isoformat(),
        })

    # Print summary
    sent = sum(1 for r in results if r["success"])
    failed = len(results) - sent
    print(f"\n{'=' * 60}")
    print(f"Done. Sent: {sent}, Failed: {failed}")
    print(f"{'=' * 60}\n")

    # Log results
    log_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "marketing",
        "youtube-outreach-send-log.json",
    )
    existing = []
    if os.path.exists(log_file):
        with open(log_file) as f:
            existing = json.load(f)
    existing.extend(results)
    with open(log_file, "w") as f:
        json.dump(existing, f, indent=2)
    print(f"Send log saved to: {log_file}")


if __name__ == "__main__":
    main()

---
title: "How I Stopped Manually Listening to 200+ Calls a Month Across My R&R Sites"
slug: case-study-rank-and-rent-call-scoring
description: "I run a hot tub repair site in Spokane and appliance repair sites in Australia. Here's how I automated call scoring and what the real numbers look like."
date: 2026-03-08
author: CallOutcome Team
---

I've got two rank-and-rent operations running right now — a hot tub repair site in Spokane, WA and a few appliance repair sites in Toowoomba, Australia. Between them I'm pushing 200+ calls a month to trade partners.

The whole business model falls apart if you can't answer one question: **did that call actually book a job?**

I spent way too long trying to answer that manually. Here's what I ended up doing instead.

## Spokane: Hot Tub Repair

I bought this site about 6 months ago. It'd been ranking for 2 years already — I basically acquired it as a cash-flowing asset. The site pushes calls to one partner, a local hot tub repair guy, across 4 tracking numbers covering Spokane, Spokane Valley, Coeur d'Alene, and Sandpoint.

He pays $350/week flat for exclusive leads. Good deal for both of us, but he wanted something I wasn't expecting — **regular reports on call stats**. How many came in, how many booked, which areas were producing, how many he was missing.

Fair enough. But at ~100 calls a month, producing those reports meant sitting down and listening to recordings. I tried it for a couple months. It sucked. We're talking 8-10 hours a month of just... listening to phone calls. I do this as a side gig. I don't have that kind of time.

I also tried the lazy shortcut — [treating call duration as a proxy for bookings](/blog/how-to-track-call-conversions-for-lead-gen). Anything over 2 minutes = probably booked. Turns out that's garbage. I had 4-minute calls where someone price-shopped and hung up, and 40-second calls where the customer said "Can you come Saturday?" and the tech said "Yep, 9am" — that's a booking in under a minute.

### What I did

I connected my tracking numbers to CallOutcome. It pulls the recordings, transcribes them, and the AI reads the transcript to figure out if a job was booked, not booked, or missed. Every call gets a full transcript so I can spot-check anything that looks off.

The big win honestly wasn't even the scoring itself — it was the [shared dashboard](/blog/how-to-prove-lead-quality-to-clients). My partner can just log in and see everything. Every call, every transcript, every classification. No more me cobbling together a spreadsheet on Sunday night. He checks it when he wants to and we haven't had a single billing argument since.

**The numbers:**

- Went from ~8-10 hrs/month reviewing calls to maybe 20 minutes (just spot-checking edge cases)
- My partner stopped questioning call volume — the data's right there
- Cost: about $3-4/month in AI processing for ~100 calls. Compared to 8-10 hours of my time. Yeah.

## Toowoomba: Appliance Repair

Different setup here. I've got 3 sites — oven repair, dishwasher repair, and general appliance repair — with 4 tracking lines and 2 trade partners splitting the work. These are newer sites, only been scoring calls for about a week.

The key difference is the billing model. Instead of a flat weekly rate, my partners pay **$50 per booked job and $12.50 per missed call**.

This changes everything. With Spokane, if I miscategorise a call, it doesn't affect what my partner pays — it just makes my reports slightly wrong. With Toowoomba, every wrong classification costs someone real money. If I call something "booked" when it wasn't, I'm overcharging $50. If I miss a real booking, I'm leaving $50 on the table. Multiply that by 100+ calls a week and you can see why guessing doesn't cut it.

### How it actually works

The AI isn't doing keyword matching or some basic "was the call longer than 2 minutes" check. It's [reading the transcript and understanding what happened](/blog/how-ai-call-scoring-works). Customer says "I need my oven fixed", tech says "I can come Thursday at 2pm", customer says "perfect" — that's a booked job. Customer asks about pricing and says "let me talk to my wife" — not booked. It gets the nuance.

After the first week: 100+ calls processed, and I only felt the need to manually check 3 of them. Those 3 were genuine edge cases — stuff like the customer saying "yeah sounds good, I'll call back to confirm the time." The AI flagged those as not booked (no firm appointment), which is the right call.

## Stuff I didn't expect

**Missed call data is weirdly powerful.** I started tracking missed calls mostly as an afterthought, but it turned into one of the most useful things. When I can show a partner they missed 8 calls last Tuesday, the conversation shifts from "your leads are bad" to "you need to answer your phone." That's a completely different dynamic.

**It works for both billing models.** Flat rate (Spokane) — scoring builds trust and keeps the partner happy. Per-lead (Toowoomba) — scoring directly protects my revenue. Either way, you need to know which calls booked.

**Manual review just doesn't scale.** If you've got one site doing 10 calls a week, sure, listen to everything. Once you're running multiple sites across multiple markets? Forget it. I'm at 200+ calls a month now. There's no version of this where I'm listening to all of those.

**It costs basically nothing.** Less than $10/month across both operations. I was burning more than that in time during a single review session.

## My setup if you want to copy it

1. **Call tracking:** Twilio for the tracking numbers. Most R&R operators use [CallRail](/blog/callrail-vs-calloutcome) — CallOutcome works with both.
2. **Scoring:** CallOutcome handles transcription + AI classification. Took about 5 minutes to connect my Twilio account, another 10 to pick which numbers to track.
3. **Billing:** I pull the stats and invoice partners based on booked/missed counts.
4. **Partner access:** Each partner gets their own login. They only see their own calls. Full transparency.

Whole thing took maybe 15 minutes to set up. If you're still manually listening to calls or guessing based on duration, you're wasting hours every month that you don't need to.

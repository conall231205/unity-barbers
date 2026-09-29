# Unity Barbers website: context for Claude Code

Demo website built as a sales pitch for Unity Barbers, 166 Alfreton Road, Radford, Nottingham NG7 3NS.
Instagram: @unitybarbersnotts. Their Instagram bio says open 9am to 11pm.

## Stack
Plain static site. No build step, no framework.
- index.html: all markup
- css/styles.css: all styles (design tokens on :root)
- js/main.js: SITE config object at the top (phone, WhatsApp, hours, prices, links), then behaviour
- images/: graded WebP images (Pexels stock, free licence, see README)
- capture/record.py: Playwright script that records the walkthrough videos

Preview: `python3 -m http.server 8000` then open http://localhost:8000

## Design system (keep consistent)
- Palette: night #0F1620, panel #172230, line #26334A, sodium amber #F2A541, chalk #F3EEE4, ink #191C21, mute #93A0B2
- Type: Big Shoulders Display (headings, uppercase, 800/900) + Figtree (body)
- Concept: "after hours" barbershop. Late opening is the headline selling point.
  Signature element is the glowing "Open till 11" sign in the hero, which shows live open/closed state.
- Every photo has the same grade: slightly desaturated, warm amber mids, cool navy shadows.
  Apply the same grade to any new photo so the set stays consistent.
- Avoid: all-caps eyebrow labels, numbered section markers, fade-in-on-scroll effects on every section.

## Confirmed by owner (2026-09-29)
- Phone: 07494 831141 (+447494831141). The 07535 and 07424 numbers in old listings are NOT used.
- Hours: 9am to 11pm, 7 days.
- Cut & beard: GBP 20. Shape up: GBP 10 (replaced the old "Beard trim & line-up" line).

## Still to confirm with the owner
- Remaining prices are demo values: skin fade 18, fade/taper 16, scissor cut 16, buzz 10,
  kids 12, hot towel 10, eyebrow 4, hair design from 5, cornrows from 20, student 14.
- Which award they won (Instagram bio says award-winning). No award claim is on the site yet.

## Rules
- Business data lives only in the SITE object in js/main.js. Don't hard-code it into the HTML.
- Keep it mobile-first. The sticky Call/WhatsApp/Directions bar on mobile must stay.
- Test at 390px, 768px, 1440px and 1920px before calling anything done.
- When the owner's real photos arrive, crop, grade and export them to images/ as WebP (max 1400px wide) and swap them in.
- Remove the "Photography: Pexels (demo imagery)" footer line once real photos replace stock.

## Re-recording the pitch videos
    pip install playwright && playwright install chromium
    python3 -m http.server 8000 &
    python3 capture/record.py desk && python3 capture/record.py mob
    ffmpeg -framerate 30 -i capture/frames_desk/f%05d.jpg -c:v libx264 -crf 20 -pix_fmt yuv420p -movflags +faststart unity-desktop.mp4
    ffmpeg -framerate 30 -i capture/frames_mob/f%05d.jpg -vf scale=1080:1920 -c:v libx264 -crf 20 -pix_fmt yuv420p -movflags +faststart unity-mobile.mp4
The script freezes the clock at 7pm on a Friday so the sign reads "Open now".

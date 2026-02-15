#!/usr/bin/env python3
"""
Generates an updated Ramadan schedule PNG with past days crossed out,
plus an HTML page for Samsung Family Hub fridge browser display.
"""

from PIL import Image, ImageDraw, ImageFont
from pdf2image import convert_from_path
from datetime import date, datetime
import os

# ── Config ──────────────────────────────────────────────────
PDF_PATH = "BVMCC_-_Ramadan_1447_2026_Athan_and_Iqama_schedule.pdf"
OUTPUT_DIR = "docs"
DPI = 200

# Row mapping: (date, y_start, y_end) at 200 DPI
DATE_ROWS = [
    (date(2026, 2, 17), 143, 185),
    (date(2026, 2, 18), 188, 253),
    (date(2026, 2, 19), 256, 281),
    (date(2026, 2, 20), 285, 373),
    (date(2026, 2, 21), 376, 405),
    (date(2026, 2, 22), 408, 464),
    (date(2026, 2, 23), 467, 496),
    (date(2026, 2, 24), 499, 524),
    (date(2026, 2, 25), 528, 557),
    (date(2026, 2, 26), 560, 584),
    (date(2026, 2, 27), 586, 663),
    (date(2026, 2, 28), 665, 689),
    (date(2026, 3, 1),  693, 746),
    (date(2026, 3, 2),  749, 772),
    (date(2026, 3, 3),  776, 801),
    (date(2026, 3, 4),  805, 827),
    (date(2026, 3, 5),  830, 853),
    (date(2026, 3, 6),  857, 946),
    (date(2026, 3, 7),  949, 975),
    (date(2026, 3, 8),  979, 1045),
    (date(2026, 3, 9),  1049, 1076),
    (date(2026, 3, 10), 1079, 1108),
    (date(2026, 3, 11), 1112, 1142),
    (date(2026, 3, 12), 1145, 1174),
    (date(2026, 3, 13), 1177, 1267),
    (date(2026, 3, 14), 1270, 1303),
    (date(2026, 3, 15), 1306, 1356),
    (date(2026, 3, 16), 1359, 1392),
    (date(2026, 3, 17), 1395, 1428),
    (date(2026, 3, 18), 1432, 1461),
    (date(2026, 3, 19), 1464, 1492),
    (date(2026, 3, 20), 1494, 1588),
    (date(2026, 3, 21), 1590, 1620),
]

TABLE_LEFT = 15
TABLE_RIGHT = 2185


def generate_schedule(as_of_date):
    """Generate crossed-out schedule image."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Converting PDF at {DPI} DPI...")
    base_img = convert_from_path(PDF_PATH, dpi=DPI)[0]

    result = base_img.copy().convert('RGBA')
    overlay = Image.new('RGBA', result.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    crossed = 0
    today_row = None

    for d, y_start, y_end in DATE_ROWS:
        if d < as_of_date:
            # Gray overlay + red strikethrough for past days
            draw.rectangle(
                [TABLE_LEFT, y_start, TABLE_RIGHT, y_end],
                fill=(80, 80, 80, 140)
            )
            y_mid = (y_start + y_end) // 2
            draw.line(
                [(TABLE_LEFT, y_mid), (TABLE_RIGHT, y_mid)],
                fill=(220, 30, 30, 230), width=4
            )
            crossed += 1
        elif d == as_of_date:
            # Highlight today's row with a bright border
            today_row = (y_start, y_end)
            draw.rectangle(
                [TABLE_LEFT, y_start, TABLE_RIGHT, y_end],
                outline=(0, 120, 255, 200), width=4
            )

    result = Image.alpha_composite(result, overlay).convert('RGB')

    output_path = os.path.join(OUTPUT_DIR, "schedule.png")
    result.save(output_path, quality=95)
    print(f"Saved: {output_path} ({crossed} days crossed out)")
    return output_path


def generate_html(as_of_date):
    """Generate a simple HTML page that displays the schedule image."""
    # Find today's key times
    today_info = ""
    for d, _, _ in DATE_ROWS:
        if d == as_of_date:
            today_info = f"Today: {as_of_date.strftime('%A, %B %d, %Y')}"
            break

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="3600"> <!-- Auto-refresh every hour -->
    <title>Ramadan 1447 Schedule</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: #1a1a2e;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            color: #fff;
        }}
        .header {{
            padding: 10px 20px;
            text-align: center;
            background: linear-gradient(135deg, #16213e, #0f3460);
            width: 100%;
        }}
        .header h1 {{
            font-size: 1.2em;
            color: #e2e2e2;
        }}
        .header .date {{
            font-size: 0.9em;
            color: #a0c4ff;
            margin-top: 2px;
        }}
        .header .updated {{
            font-size: 0.7em;
            color: #888;
            margin-top: 2px;
        }}
        .schedule-container {{
            flex: 1;
            width: 100%;
            overflow: auto;
            display: flex;
            justify-content: center;
            padding: 5px;
        }}
        .schedule-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 4px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>BVMCC Ramadan 1447 Schedule</h1>
        <div class="date">{today_info}</div>
        <div class="updated">Last updated: {datetime.now().strftime('%b %d, %Y at %I:%M %p')}</div>
    </div>
    <div class="schedule-container">
        <img src="schedule.png?v={as_of_date.isoformat()}" alt="Ramadan Schedule">
    </div>
</body>
</html>"""

    path = os.path.join(OUTPUT_DIR, "index.html")
    with open(path, 'w') as f:
        f.write(html)
    print(f"Saved: {path}")


if __name__ == "__main__":
    today = date.today()
    print(f"Date: {today}")
    generate_schedule(today)
    generate_html(today)
    print("Done!")

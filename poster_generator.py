from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime
from sheets_client import fetch_roster_data  # fetch sheet rows or mapping

# Constants
CANVAS_WIDTH = 1000
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SIZE = 24
LINE_HEIGHT = 30
MARGIN = 40
COLUMN_GAP = 40  # space between team columns

os.makedirs("poster_output", exist_ok=True)


def measure_text(draw, text, font):
    """Returns width, height of given text with this font."""
    x0, y0, x1, y1 = draw.textbbox((0, 0), text, font=font)
    return x1 - x0, y1 - y0


def get_scaled_font(draw, text, max_width, start_size):
    """Return a font scaled down so text width <= max_width."""
    size = start_size
    font = ImageFont.truetype(FONT_PATH, size)
    w, _ = measure_text(draw, text, font)
    while w > max_width and size > 1:
        size -= 1
        font = ImageFont.truetype(FONT_PATH, size)
        w, _ = measure_text(draw, text, font)
    return font


def generate_poster(team1, team2=None, mode='two_teams'):
    """
    Generates a roster poster image, always 1000px wide.
    team1, team2: lists of squad dicts
    mode: 'one_team' or 'two_teams'
    """
    # Load roster data mapping IDs to row dicts
    raw_data = fetch_roster_data()
    roster_map = {}
    # If fetch_roster_data returns dict of {id: row_dict}
    if isinstance(raw_data, dict):
        roster_map = {str(k): v for k, v in raw_data.items()}
    else:
        # assume list of dict rows with 'RCON ID' and 'Name'
        for row in raw_data:
            pid_val = row.get('RCON ID') or row.get('steam_id') or row.get('id')
            if pid_val is not None:
                roster_map[str(pid_val)] = row

    # Determine teams array
    mode = mode.lower()
    teams = [team1] if mode == 'one_team' else [team1, team2 or []]

    # Calculate canvas height
    rows_counts = [sum(1 + len(s.get('players', [])) for s in t) for t in teams]
    max_rows = rows_counts[0] if len(teams) == 1 else max(rows_counts)
    canvas_height = MARGIN * 2 + max_rows * LINE_HEIGHT

    # Column widths
    if len(teams) == 1:
        col_widths = [CANVAS_WIDTH - 2 * MARGIN]
    else:
        inner = CANVAS_WIDTH - 2 * MARGIN - COLUMN_GAP
        half = inner // 2
        col_widths = [half, inner - half]

    # Create image
    image = Image.new('RGB', (CANVAS_WIDTH, canvas_height), color=(20, 20, 20))
    draw = ImageDraw.Draw(image)

    # Draw header
    header = f"HLL Roster - Mode: {mode.replace('_', ' ').title()}"
    header_font = get_scaled_font(draw, header, CANVAS_WIDTH - 2 * MARGIN, FONT_SIZE)
    hw, hh = measure_text(draw, header, header_font)
    draw.text(((CANVAS_WIDTH - hw) // 2, MARGIN // 2), header, font=header_font, fill=(255, 255, 255))

    # Draw teams
    for idx, team in enumerate(teams):
        x0 = MARGIN + idx * (col_widths[0] + COLUMN_GAP)
        y = MARGIN
        # Team label
        label = f"Team {idx+1}"
        label_font = get_scaled_font(draw, label, col_widths[idx], FONT_SIZE)
        draw.text((x0, y), label, font=label_font, fill=(255, 215, 0))
        y += LINE_HEIGHT
        # Squads and players
        for squad in team:
            title = f"{squad.get('squad', 'Squad')}:"
            title_font = get_scaled_font(draw, title, col_widths[idx], FONT_SIZE)
            draw.text((x0, y), title, font=title_font, fill=(200, 200, 200))
            y += LINE_HEIGHT
            for pid in squad.get('players', []):
                # Lookup name from roster_map
                row = roster_map.get(str(pid), {})
                display_name = row.get('Name', str(pid))
                text = f"• {display_name}"
                player_font = get_scaled_font(draw, text, col_widths[idx] - 20, FONT_SIZE)
                draw.text((x0 + 20, y), text, font=player_font, fill=(180, 180, 180))
                y += LINE_HEIGHT

    # Save image
    ts = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    out_dir = 'poster_output'
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f'poster_{ts}.png')
    image.save(path)
    image.save(os.path.join(out_dir, 'poster_latest.png'))
    return path

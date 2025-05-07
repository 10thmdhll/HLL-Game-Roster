from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime
from sheets_client import fetch_roster_data

# Constants
CANVAS_WIDTH = 1000
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SIZE = 20
LINE_HEIGHT = 40
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


def build_name_map(raw_data):
    """Builds a simple mapping of ID strings to Name strings from fetch_roster_data output."""
    name_map = {}
    # If dict mapping id -> row dict
    if isinstance(raw_data, dict):
        for k, v in raw_data.items():
            # v should be a dict with 'Name'
            name_map[str(k)] = v.get('Name', '') if isinstance(v, dict) else ''
    # If list of lists: first row is header
    elif isinstance(raw_data, list) and raw_data and isinstance(raw_data[0], (list, tuple)):
        header = raw_data[0]
        try:
            id_idx = header.index('RCON ID')
            name_idx = header.index('Name')
        except ValueError:
            return name_map
        for row in raw_data[1:]:
            if len(row) > max(id_idx, name_idx):
                name_map[str(row[id_idx])] = row[name_idx]
    # If list of dicts
    elif isinstance(raw_data, list):
        for row in raw_data:
            pid = row.get('RCON ID') or row.get('steam_id') or row.get('id')
            if pid is not None:
                name_map[str(pid)] = row.get('Name', '')
    return name_map


def generate_poster(team1, team2=None, mode='two_teams'):
    """
    Generates a roster poster image, always 1000px wide.
    team1, team2: lists of squad dicts
    mode: 'one_team' or 'two_teams'
    """
    raw_data = fetch_roster_data()
    print(raw_data)
    name_map = build_name_map(raw_data)

    mode = mode.lower()
    teams = [team1] if mode == 'one_team' else [team1, team2 or []]

    # Compute height
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

    # Header
    header = f"HLL Roster - Mode: {mode.replace('_', ' ').title()}"
    header_font = get_scaled_font(draw, header, CANVAS_WIDTH - 2 * MARGIN, FONT_SIZE)
    hw, hh = measure_text(draw, header, header_font)
    draw.text(((CANVAS_WIDTH - hw) // 2, MARGIN // 2), header,
              font=header_font, fill=(255, 255, 255))

    # Draw teams
    for idx, team in enumerate(teams):
        x0 = MARGIN + idx * (col_widths[0] + COLUMN_GAP)
        y = MARGIN
        # Team label
        label = f"Team {idx+1}"
        label_font = get_scaled_font(draw, label, col_widths[idx], FONT_SIZE)
        draw.text((x0, y), label, font=label_font, fill=(255, 215, 0))
        y += LINE_HEIGHT
        # Squads & players
        for squad in team:
            title = f"{squad.get('squad', 'Squad')}:"
            title_font = get_scaled_font(draw, title, col_widths[idx], FONT_SIZE)
            draw.text((x0, y), title, font=title_font, fill=(200, 200, 200))
            y += LINE_HEIGHT
            for pid in squad.get('players', []):
                display = name_map.get(str(pid)) or str(pid)
                line = f"• {display}"
                font = get_scaled_font(draw, line, col_widths[idx] - 20, FONT_SIZE)
                draw.text((x0 + 20, y), line, font=font, fill=(180, 180, 180))
                y += LINE_HEIGHT

    # Save
    ts = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    out_dir = 'poster_output'
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f'poster_{ts}.png')
    image.save(path)
    image.save(os.path.join(out_dir, 'poster_latest.png'))
    return path
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

FONT_PATH    = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SIZE    = 24
LINE_HEIGHT  = 30
MARGIN       = 40
COLUMN_GAP   = 40  # space between the two team columns

os.makedirs("poster_output", exist_ok=True)

def measure_text(draw, text, font):
    """
    Returns (width, height) of text when drawn with this font.
    Uses textbbox under the hood so it works on all Pillow versions.
    """
    x0, y0, x1, y1 = draw.textbbox((0, 0), text, font=font)
    return x1 - x0, y1 - y0


def get_scaled_font(draw, text, max_width, start_size):
    """
    Returns an ImageFont instance at or below start_size such that
    the text fits within max_width.
    """
    size = start_size
    font = ImageFont.truetype(FONT_PATH, size)
    w, _ = measure_text(draw, text, font)
    while (w > max_width) and size > 1:
        size -= 1
        font = ImageFont.truetype(FONT_PATH, size)
        w, _ = measure_text(draw, text, font)
    return font


def calculate_image_dimensions(teams):
    """
    Returns (width, height, [col1_width, col2_width]) so that
    every squad title and player line fits at FONT_SIZE.
    """
    # --- compute total height ---
    lines = sum(1 + len(squad.get("players", []))
                for team in teams
                for squad in team)
    height = MARGIN + lines * LINE_HEIGHT + MARGIN

    # --- compute column widths ---
    temp_img = Image.new("RGB", (1, 1))
    draw     = ImageDraw.Draw(temp_img)

    col_widths = []
    for team in teams:
        max_w = 0
        for squad in team:
            # squad title
            title = f"{squad.get('squad','Unnamed Squad')}:"
            font_title = ImageFont.truetype(FONT_PATH, FONT_SIZE)
            w, _ = measure_text(draw, title, font_title)
            max_w = max(max_w, w)
            # each player
            for player in squad.get("players", []):
                bullet = f"• {player}"
                font_player = ImageFont.truetype(FONT_PATH, FONT_SIZE)
                w, _ = measure_text(draw, bullet, font_player)
                max_w = max(max_w, w + 20)  # account for indent
        col_widths.append(max_w)

    # total width = left margin + col1 + gap + col2 + right margin
    width = MARGIN + col_widths[0] + COLUMN_GAP + col_widths[1] + MARGIN
    return width, height, col_widths


def generate_poster(team1, team2, mode):
    teams = [team1, team2]
    width, height, col_widths = calculate_image_dimensions(teams)

    image = Image.new("RGB", (width, height), color=(20, 20, 20))
    draw  = ImageDraw.Draw(image)

    # --- draw centered header ---
    header = f"HLL Roster - Mode: {mode}"
    header_font = get_scaled_font(draw, header, width - 2 * MARGIN, FONT_SIZE)
    h_w, h_h = measure_text(draw, header, header_font)
    header_x = (width - h_w) // 2
    header_y = MARGIN // 2
    draw.text((header_x, header_y), header, font=header_font, fill=(255, 255, 255))

    # --- draw team columns ---
    y_cursor = MARGIN
    for idx, team in enumerate(teams):
        x_cursor = MARGIN + idx * (col_widths[0] + COLUMN_GAP)

        # team label
        label = f"TEAM {idx+1}"
        label_font = get_scaled_font(draw, label, col_widths[idx], FONT_SIZE)
        draw.text((x_cursor, y_cursor), label, font=label_font, fill=(255, 215, 0))
        y = y_cursor + LINE_HEIGHT

        # squads and players
        for squad in team:
            title = f"{squad.get('squad','Unnamed Squad')}:" 
            title_font = get_scaled_font(draw, title, col_widths[idx], FONT_SIZE)
            draw.text((x_cursor, y), title, font=title_font, fill=(200, 200, 200))
            y += LINE_HEIGHT
            for player in squad.get("players", []):
                bullet = f"• {player}"
                player_font = get_scaled_font(draw, bullet, col_widths[idx] - 20, FONT_SIZE)
                draw.text((x_cursor + 20, y), bullet, font=player_font, fill=(180, 180, 180))
                y += LINE_HEIGHT

    # --- save files ---
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    outpath   = f"poster_output/poster_{timestamp}.png"
    image.save(outpath)
    latest    = "poster_output/poster_latest.png"
    image.save(latest)
    return latest

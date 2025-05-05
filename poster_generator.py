from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

FONT_PATH    = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SIZE    = 24
LINE_HEIGHT  = 30
MARGIN       = 40
COLUMN_GAP   = 40  # space between team columns

os.makedirs("poster_output", exist_ok=True)

def measure_text(draw, text, font):
    """
    Returns (width, height) of text when drawn with this font.
    """
    x0, y0, x1, y1 = draw.textbbox((0, 0), text, font=font)
    return x1 - x0, y1 - y0


def get_scaled_font(draw, text, max_width, start_size):
    """
    Scales down the font size until text width <= max_width.
    """
    size = start_size
    font = ImageFont.truetype(FONT_PATH, size)
    w, _ = measure_text(draw, text, font)
    while w > max_width and size > 1:
        size -= 1
        font = ImageFont.truetype(FONT_PATH, size)
        w, _ = measure_text(draw, text, font)
    return font


def calculate_image_dimensions(teams):
    """
    Calculate canvas width, height, and column widths for given teams.
    Uses max rows among columns when rendering two columns.
    """
    # prepare to measure text
    temp_img = Image.new("RGB", (1, 1))
    draw     = ImageDraw.Draw(temp_img)

    # determine row counts per team
    rows_per_team = [sum(1 + len(s.get("players", [])) for s in team) for team in teams]
    # for two columns, height is based on max rows; for single, sum rows
    rows = max(rows_per_team) if len(teams) > 1 else rows_per_team[0]
    height = MARGIN * 2 + rows * LINE_HEIGHT

    # compute column widths
    col_widths = []
    for team in teams:
        max_w = 0
        for squad in team:
            title = f"{squad.get('squad','Unnamed Squad')}:"
            font_title = ImageFont.truetype(FONT_PATH, FONT_SIZE)
            w, _ = measure_text(draw, title, font_title)
            max_w = max(max_w, w)
            for player in squad.get("players", []):
                bullet = f"• {player}"
                font_pl = ImageFont.truetype(FONT_PATH, FONT_SIZE)
                w, _ = measure_text(draw, bullet, font_pl)
                max_w = max(max_w, w + 20)
        col_widths.append(max_w)

    # total width: margins + sum columns + gaps
    gaps = COLUMN_GAP * max(0, len(col_widths) - 1)
    width = MARGIN * 2 + sum(col_widths) + gaps
    return width, height, col_widths


def generate_poster(team1, team2, mode):
    """
    Generate roster poster. mode should be 'one_team' or 'two_teams'.
    """
    mode = mode.lower()
    if mode == "one_team":
        teams = [team1]
    else:
        teams = [team1, team2]

    width, height, col_widths = calculate_image_dimensions(teams)
    image = Image.new("RGB", (width, height), color=(20, 20, 20))
    draw  = ImageDraw.Draw(image)

    # header
    header = f"HLL Roster - Mode: {mode}"
    header_font = get_scaled_font(draw, header, width - 2 * MARGIN, FONT_SIZE)
    h_w, h_h    = measure_text(draw, header, header_font)
    draw.text(((width - h_w) // 2, MARGIN // 2), header,
              font=header_font, fill=(255, 255, 255))

    # draw columns
    y_start = MARGIN
    for idx, team in enumerate(teams):
        x_offset = MARGIN + sum(col_widths[:idx]) + COLUMN_GAP * idx

        label = f"TEAM {idx+1}"
        label_font = get_scaled_font(draw, label, col_widths[idx], FONT_SIZE)
        draw.text((x_offset, y_start), label,
                  font=label_font, fill=(255, 215, 0))
        y = y_start + LINE_HEIGHT

        # squads and players
        for squad in team:
            title = f"{squad.get('squad','Unnamed Squad')}:"
            title_font = get_scaled_font(draw, title, col_widths[idx], FONT_SIZE)
            draw.text((x_offset, y), title,
                      font=title_font, fill=(200, 200, 200))
            y += LINE_HEIGHT
            for player in squad.get("players", []):
                bullet = f"• {player}"
                pl_font = get_scaled_font(draw, bullet, col_widths[idx] - 20, FONT_SIZE)
                draw.text((x_offset + 20, y), bullet,
                          font=pl_font, fill=(180, 180, 180))
                y += LINE_HEIGHT

    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = f"poster_output/poster_{ts}.png"
    image.save(path)
    image.save("poster_output/poster_latest.png")
    return path

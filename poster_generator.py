from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

FONT_PATH    = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SIZE    = 24
LINE_HEIGHT  = 30
MARGIN       = 40
COLUMN_GAP   = 40  # space between team columns when multiple

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
    while w > max_width and size > 1:
        size -= 1
        font = ImageFont.truetype(FONT_PATH, size)
        w, _ = measure_text(draw, text, font)
    return font


def calculate_image_dimensions(teams):
    """
    Returns (width, height, col_widths) so that
    every text element fits within its column at FONT_SIZE.
    """
    # total rows = sum squad titles + players
    rows = sum(1 + len(squad.get("players", []))
               for team in teams
               for squad in team)
    height = MARGIN * 2 + rows * LINE_HEIGHT

    # measure each column width
    temp_img = Image.new("RGB", (1, 1))
    draw     = ImageDraw.Draw(temp_img)

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
                font_player = ImageFont.truetype(FONT_PATH, FONT_SIZE)
                w, _ = measure_text(draw, bullet, font_player)
                max_w = max(max_w, w + 20)  # indent
        col_widths.append(max_w)

    # compute total width: left margin + sum cols + gaps + right margin
    gaps = COLUMN_GAP * max(0, len(col_widths) - 1)
    width = MARGIN * 2 + sum(col_widths) + gaps
    return width, height, col_widths


def generate_poster(team1, team2, mode):
    # determine columns: one_team shows only first team, else two
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
        # compute x offset based on previous column widths + gaps
        x_offset = MARGIN + sum(col_widths[:idx]) + COLUMN_GAP * idx

        # team label
        label = f"TEAM {idx+1}"
        label_font = get_scaled_font(draw, label, col_widths[idx], FONT_SIZE)
        draw.text((x_offset, y_start), label,
                  font=label_font, fill=(255, 215, 0))
        y = y_start + LINE_HEIGHT

        # squads & players
        for squad in team:
            title = f"{squad.get('squad','Unnamed Squad')}:"
            title_font = get_scaled_font(draw, title, col_widths[idx], FONT_SIZE)
            draw.text((x_offset, y), title,
                      font=title_font, fill=(200, 200, 200))
            y += LINE_HEIGHT
            for player in squad.get("players", []):
                bullet = f"• {player}"
                player_font = get_scaled_font(draw, bullet, col_widths[idx] - 20, FONT_SIZE)
                draw.text((x_offset + 20, y), bullet,
                          font=player_font, fill=(180, 180, 180))
                y += LINE_HEIGHT

    # save outputs
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = f"poster_output/poster_{ts}.png"
    image.save(path)
    image.save("poster_output/poster_latest.png")
    return path

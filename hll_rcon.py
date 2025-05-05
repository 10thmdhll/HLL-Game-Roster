from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

# Fixed canvas width
CANVAS_WIDTH = 1000
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


def generate_poster(team1, team2, mode, name_map=None):
    """
    Generates a poster always 1000px wide. Mode: 'one_team' or 'two_teams'.
    name_map: optional dict mapping player IDs to display names.
    """
    mode = mode.lower()
    if mode == "one_team":
        teams = [team1]
    else:
        teams = [team1, team2]

    # compute rows per team for height
    rows_per_team = [sum(1 + len(s.get("players", [])) for s in team) for team in teams]
    rows = rows_per_team[0] if len(teams) == 1 else max(rows_per_team)
    canvas_height = MARGIN * 2 + rows * LINE_HEIGHT

    # compute column widths
    if len(teams) == 1:
        col_widths = [CANVAS_WIDTH - 2 * MARGIN]
    else:
        inner_width = CANVAS_WIDTH - 2 * MARGIN - COLUMN_GAP
        w1 = inner_width // 2
        w2 = inner_width - w1
        col_widths = [w1, w2]

    # create canvas
    image = Image.new("RGB", (CANVAS_WIDTH, canvas_height), color=(20, 20, 20))
    draw  = ImageDraw.Draw(image)

    # header
    header = f"HLL Roster - Mode: {mode}"
    header_font = get_scaled_font(draw, header, CANVAS_WIDTH - 2 * MARGIN, FONT_SIZE)
    h_w, h_h    = measure_text(draw, header, header_font)
    draw.text(((CANVAS_WIDTH - h_w) // 2, MARGIN // 2), header,
              font=header_font, fill=(255, 255, 255))

    # draw teams
    y_start = MARGIN
    for idx, team in enumerate(teams):
        x_offset = MARGIN + idx * (col_widths[0] + COLUMN_GAP)

        # team label
        label = f"TEAM {idx+1}"
        label_font = get_scaled_font(draw, label, col_widths[idx], FONT_SIZE)
        draw.text((x_offset, y_start), label,
                  font=label_font, fill=(255, 215, 0))
        y = y_start + LINE_HEIGHT

        # squads and players
        for squad in team:
            # squad title
            title = f"{squad.get('squad','Unnamed Squad')}:"
            title_font = get_scaled_font(draw, title, col_widths[idx], FONT_SIZE)
            draw.text((x_offset, y), title,
                      font=title_font, fill=(200, 200, 200))
            y += LINE_HEIGHT

            # player lines
            for player in squad.get("players", []):
                # map ID to name if provided
                disp = name_map.get(str(player), str(player)) if name_map else str(player)
                bullet = f"• {disp}"
                pl_font = get_scaled_font(draw, bullet, col_widths[idx] - 20, FONT_SIZE)
                draw.text((x_offset + 20, y), bullet,
                          font=pl_font, fill=(180, 180, 180))
                y += LINE_HEIGHT

    # save outputs
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    outpath = f"poster_output/poster_{ts}.png"
    image.save(outpath)
    image.save("poster_output/poster_latest.png")
    return outpath
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

FONT_PATH    = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SIZE    = 24
LINE_HEIGHT  = 30
MARGIN       = 40
COLUMN_GAP   = 40  # space between the two team columns

os.makedirs("poster_output", exist_ok=True)

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
    font     = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    col_widths = []
    for team in teams:
        max_w = 0
        for squad in team:
            # squad title
            text = f"{squad.get('squad','Unnamed Squad')}:"
            w, _ = draw.textsize(text, font=font)
            max_w = max(max_w, w)
            # each player
            for player in squad.get("players", []):
                text = f"• {player}"
                w, _ = draw.textsize(text, font=font)
                # account for the indent of 20 px
                max_w = max(max_w, w + 20)
        col_widths.append(max_w)

    # total width = left margin + col1 + gap + col2 + right margin
    width = MARGIN + col_widths[0] + COLUMN_GAP + col_widths[1] + MARGIN
    return width, height, col_widths

def generate_poster(team1, team2, mode):
    teams = [team1, team2]
    width, height, col_widths = calculate_image_dimensions(teams)

    image = Image.new("RGB", (width, height), color=(20, 20, 20))
    draw  = ImageDraw.Draw(image)
    font  = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    # --- draw centered header ---
    header = f"HLL Roster - Mode: {mode}"
    h_w, h_h = draw.textsize(header, font=font)
    header_x = (width - h_w) // 2
    header_y = MARGIN // 2
    draw.text((header_x, header_y), header, font=font, fill=(255, 255, 255))

    # --- draw team columns ---
    y_cursor = MARGIN
    for idx, team in enumerate(teams):
        x_cursor = MARGIN + idx * (col_widths[0] + COLUMN_GAP)

        # team label
        label = f"TEAM {idx+1}"
        draw.text((x_cursor, y_cursor), label, font=font, fill=(255, 215, 0))
        y = y_cursor + LINE_HEIGHT

        # squads and players
        for squad in team:
            title = f"{squad.get('squad','Unnamed Squad')}:"
            draw.text((x_cursor, y), title, font=font, fill=(200, 200, 200))
            y += LINE_HEIGHT
            for player in squad.get("players", []):
                bullet = f"• {player}"
                draw.text((x_cursor + 20, y), bullet, font=font, fill=(180, 180, 180))
                y += LINE_HEIGHT

    # --- save files ---
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    outpath   = f"poster_output/poster_{timestamp}.png"
    image.save(outpath)
    latest    = "poster_output/poster_latest.png"
    image.save(latest)
    return latest

# --- example usage ---
if __name__ == "__main__":
    example_team1 = [
        {"squad":"Alpha", "players":["Alice","Bob"]},
        {"squad":"Bravo", "players":["Carol","Dave","Eve"]}
    ]
    example_team2 = [
        {"squad":"Charlie","players":["Frank"]},
        {"squad":"Delta","players":["Grace","Heidi","Ivan","Judy"]}
    ]
    path = generate_poster(example_team1, example_team2, mode="one_team")
    print("Saved:", path)

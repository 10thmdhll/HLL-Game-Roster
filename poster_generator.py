from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SIZE = 24
LINE_HEIGHT = 30

os.makedirs("poster_output", exist_ok=True)

def calculate_image_height(teams):
    lines = 0
    for team in teams:
        for squad in team:
            lines += 1  # squad title
            lines += len(squad['players'])  # one line per player
    return 100 + lines * LINE_HEIGHT

def generate_poster(team1, team2, mode):
    width = 1000
    height = calculate_image_height([team1, team2])
    image = Image.new("RGB", (width, height), color=(20, 20, 20))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    draw.text((width // 2 - 150, 20), f"HLL Roster - Mode: {mode}", font=font, fill=(255, 255, 255))

    y_offset = 80
    for idx, team in enumerate([team1, team2]):
        x_offset = 50 if idx == 0 else width // 2 + 50
        team_label = "TEAM 1" if idx == 0 else "TEAM 2"
        draw.text((x_offset, y_offset), team_label, font=font, fill=(255, 215, 0))
        y = y_offset + 40

        for squad in team:
            draw.text((x_offset, y), f"{squad['squad']}:", font=font, fill=(200, 200, 200))
            y += LINE_HEIGHT
            for player in squad['players']:
                draw.text((x_offset + 20, y), f"• {player}", font=font, fill=(180, 180, 180))
                y += LINE_HEIGHT

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"poster_output/poster_{timestamp}.png"
    image.save(filename)

    latest_path = "poster_output/poster_latest.png"
    image.save(latest_path)

    return latest_path

from PIL import Image, ImageSequence
import os

INPUT_DIR = "7tv_emotes_OSRS/Animated"
OUTPUT_DIR = "7tv_emotes_OSRS/Animated_FIXED"

os.makedirs(OUTPUT_DIR, exist_ok=True)

for filename in os.listdir(INPUT_DIR):
    if not filename.lower().endswith(".gif"):
        continue

    path = os.path.join(INPUT_DIR, filename)
    out_path = os.path.join(OUTPUT_DIR, filename)

    with Image.open(path) as img:
        frames = []
        durations = []

        base = Image.new("RGBA", img.size, (0, 0, 0, 0))

        for frame in ImageSequence.Iterator(img):
            base = base.copy()
            base.paste(frame.convert("RGBA"), (0, 0), frame.convert("RGBA"))
            frames.append(base)
            durations.append(frame.info.get("duration", 33))

        frames[0].save(
            out_path,
            save_all=True,
            append_images=frames[1:],
            duration=durations,
            loop=0,
            disposal=2
        )

print("GIFs coalesced")

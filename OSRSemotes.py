import requests
import os

# --- Configuration ---
USER_ID = "01FD7GADQR0009D1JB6G15TDDN"
OUT = "7tv_emotes_OSRS"
STATIC = f"{OUT}/STATIC"
ANIM = f"{OUT}/ANIMATED"
UA = "Mozilla/5.0 (X11; Linux x86_64)"
HEADERS = {"User-Agent": UA}
TIMEOUT = 10

# --- Setup ---
os.makedirs(STATIC, exist_ok=True)
os.makedirs(ANIM, exist_ok=True)

def download_file(url, path, quiet=False):
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        with open(path, "wb") as f:
            f.write(r.content)
        return True
    except requests.RequestException as e:
        if not quiet:
            print(f"Download failed: {url} -> {e}")
        return False

# --- Fetch user ---
user_url = f"https://7tv.io/v3/users/{USER_ID}"
try:
    user_data = requests.get(user_url, headers=HEADERS, timeout=TIMEOUT).json()
except requests.RequestException as e:
    print(f"Failed to fetch user data: {e}")
    exit(1)

# --- Collect emote set IDs ---
set_ids = set()

if isinstance(user_data.get("emote_set"), dict):
    set_ids.add(user_data["emote_set"]["id"])

for es in user_data.get("emote_sets", []):
    if isinstance(es, dict) and "id" in es:
        set_ids.add(es["id"])

seen = set()

# --- Download emotes ---
for set_id in set_ids:
    set_url = f"https://7tv.io/v3/emote-sets/{set_id}"

    try:
        set_data = requests.get(set_url, headers=HEADERS, timeout=TIMEOUT).json()
    except requests.RequestException as e:
        print(f"Failed to fetch emote set {set_id}: {e}")
        continue

    for emote in set_data.get("emotes", []):
        emote_id = emote.get("id")
        name = emote.get("name")

        if not emote_id or not name or emote_id in seen:
            continue

        seen.add(emote_id)

        # --- Try animated first (GIF) ---
        gif_url = f"https://cdn.7tv.app/emote/{emote_id}/2x.gif"
        gif_path = f"{ANIM}/{name}.gif"

        if download_file(gif_url, gif_path, quiet=True):
            continue

        # --- Fallback to static PNG ---
        png_url = f"https://cdn.7tv.app/emote/{emote_id}/2x.png"
        png_path = f"{STATIC}/{name}.png"

        download_file(png_url, png_path)

print(f"✅ Done. Emotes saved to {OUT}/")

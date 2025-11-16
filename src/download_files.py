import requests
import time
from pathlib import Path
import sys

# List of files to download
DOWNLOAD_TASKS = [
    # --- Lore ---
    {'url': 'https://ageofsigmar.lexicanum.com/wiki/Stormcast_Eternals',
     'file_name': 'stormcast_eternals.html',
     'folder': 'data/raw/lore/'},

    {'url': 'https://ageofsigmar.lexicanum.com/wiki/Nighthaunt',
     'file_name': 'nighthaunt.html',
     'folder': 'data/raw/lore/'},

    {'url': 'https://ageofsigmar.lexicanum.com/wiki/Mortal_Realms',
     'file_name': 'mortal_realms.html',
     'folder': 'data/raw/lore/'},

    {'url': 'https://ageofsigmar.lexicanum.com/wiki/Age_of_Sigmar',
     'file_name': 'age_of_sigmar_epoch.html',
     'folder': 'data/raw/lore/'},

    # --- Rules / Getting Started ---
    {'url': 'https://www.warhammer-community.com/en-gb/articles/cGx42cA0/how-to-get-started-with-warhammer-age-of-sigmar/',
     'file_name': 'how_to_get_started_warcom.html',
     'folder': 'data/raw/rules/'},

    {'url': 'https://ageofsigmar.com/getting-started-with-age-of-sigmar/',
     'file_name': 'getting_started_official.html',
     'folder': 'data/raw/rules/'},

    {'url': 'https://www.goonhammer.com/getting-started-with-warhammer-age-of-sigmar-part-1/',
     'file_name': 'goonhammer_getting_started_part1.html',
     'folder': 'data/raw/rules/'},

    # NOTE: Part 2 link currently returns 404, so we skip it for now.
    # {'url': 'https://www.goonhammer.com/getting-started-with-warhammer-age-of-sigmar-part-2-the-factions/',
    #  'file_name': 'goonhammer_getting_started_part2_factions.html',
    #  'folder': 'data/raw/rules/'},

    # --- Guides / Army advice ---
    {'url': 'https://www.warhammer-community.com/en-gb/articles/wteZPXrg/every-faction-in-warhammer-age-of-sigmar-in-a-nutshell/',
     'file_name': 'every_faction_in_a_nutshell.html',
     'folder': 'data/raw/guides/'},

    {'url': 'https://ageofminiatures.com/fr/beginners-guide-to-age-of-sigmar-factions-and-races/',
     'file_name': 'beginners_guide_factions_ageofminiatures.html',
     'folder': 'data/raw/guides/'},

    {'url': 'https://www.goonhammer.com/start-competing-your-guide-to-getting-better-at-warhammer-age-of-sigmar/',
     'file_name': 'goonhammer_start_competing.html',
     'folder': 'data/raw/guides/'},

    # --- Core Rules PDF (direct link) ---
    {
        'url': 'https://assets.warhammer-community.com/ageofsigmar_corerules%26keydownloads_therules_eng_24.09-tbf4egjql3.pdf',
        'file_name': 'aos_core_rules_2024.pdf',
        'folder': 'data/raw/rules_update/'
    },

    # If you later find a direct Rules Updates PDF link, add it here.
    # {
    #     'url': 'https://assets.warhammer-community.com/ACTUAL_RULES_UPDATE_FILE.pdf',
    #     'file_name': 'aos_rules_updates_2025_10_29.pdf',
    #     'folder': 'data/raw/rules_update/'
    # },
]

# Pretend to be a browser
HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/91.0.4472.124 Safari/537.36'
    )
}


def download_file(url, folder, file_name):
    """
    Downloads content from a URL and saves it to the specified folder/file.
    """
    try:
        save_path = Path(folder) / file_name
        save_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"[{file_name}] Downloading: {url} ...")
        response = requests.get(url, headers=HEADERS, timeout=20)
        response.raise_for_status()

        # Binary for PDFs, text for HTML
        if file_name.endswith('.pdf'):
            with open(save_path, 'wb') as f:
                f.write(response.content)
        else:
            # Force UTF-8; if decoding issues appear, you can use response.apparent_encoding
            text = response.text
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(text)

        print(f"✅ Success: {save_path}")

    except requests.exceptions.HTTPError as e:
        print(f"❌ ERROR (HTTP): {e} for URL: {url}", file=sys.stderr)
    except requests.exceptions.ConnectionError as e:
        print(f"❌ ERROR (Connection): Could not connect to {url}. {e}", file=sys.stderr)
    except requests.exceptions.Timeout as e:
        print(f"❌ ERROR (Timeout): Request timed out for {url}. {e}", file=sys.stderr)
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR ({file_name}): {e}", file=sys.stderr)


def main():
    total_tasks = len(DOWNLOAD_TASKS)
    print(f"--- Starting {total_tasks} total download tasks ---")

    for i, task in enumerate(DOWNLOAD_TASKS):
        if not task.get('url') or not task.get('file_name'):
            continue

        print(f"\n--- Task {i+1}/{total_tasks} ---")
        download_file(task['url'], task['folder'], task['file_name'])

        # politeness delay
        time.sleep(1)

    print("\n--- All tasks completed. ---")


if __name__ == "__main__":
    main()

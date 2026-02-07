# ------------------------------------------------------------
# This script scans all year folders (e.g. 2022, 2023) located
# in the current root directory.
#
# For each detected year folder, it processes the direct
# subfolders representing months and renames them into a
# consistent format:
#
#   01_Januar
#   02_Februar
#   03_März
#   ...
#
# The script supports multiple existing naming schemes:
#   - "Januar"
#   - "01 Januar"
#   - "02Februar"
#   - "03 März"
#
# Missing months are ignored; no folders are created.
# Non-matching folders remain unchanged.
#
# The script must be executed from the root directory.
# ------------------------------------------------------------


import os
import re

MONTHS = {
    "januar": "01_Januar",
    "februar": "02_Februar",
    "märz": "03_März",
    "maerz": "03_März",
    "april": "04_April",
    "mai": "05_Mai",
    "juni": "06_Juni",
    "juli": "07_Juli",
    "august": "08_August",
    "september": "09_September",
    "oktober": "10_Oktober",
    "november": "11_November",
    "dezember": "12_Dezember",
}


def normalize(name: str) -> str:
    return (
        name.lower()
        .replace("_", "")
        .replace(" ", "")
    )


for year in os.listdir("."):
    if not os.path.isdir(year):
        continue

    # nur Jahresordner wie 2022, 2023, 1999 …
    if not re.fullmatch(r"\d{4}", year):
        continue

    print(f"\n📂 Jahr {year}")

    for entry in os.listdir(year):
        old_path = os.path.join(year, entry)

        if not os.path.isdir(old_path):
            continue

        clean = normalize(entry)
        clean = re.sub(r"^\d+", "", clean)

        for key, target in MONTHS.items():
            if clean == key:
                new_path = os.path.join(year, target)

                if entry != target:
                    print(f"  ↳ {entry} → {target}")
                    os.rename(old_path, new_path)
                break

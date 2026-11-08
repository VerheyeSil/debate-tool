"""Create the data folders for GroenLinks and VVD with their core values and key policies.

Run from anywhere with: python scripts/create_party_data.py
Existing context.json files are overwritten; the .txt files are left untouched.
"""

import json

from debate_tool.parties import party_dir


def create_party_structure(party_name, core_values, key_policies):
    """Create the folder, context.json and empty text files for a party."""
    folder = party_dir(party_name)
    folder.mkdir(parents=True, exist_ok=True)

    context = {"party_name": party_name, "core_values": core_values, "key_policies": key_policies}
    with open(folder / "context.json", "w", encoding="utf-8") as f:
        json.dump(context, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # Placeholders to fill in by hand.
    (folder / "verkiezingsprogramma.txt").touch()
    (folder / "standpunten.txt").touch()

    print(f"Structuur aangemaakt voor {party_name}")


def main():
    create_party_structure(
        "GroenLinks",
        ["duurzaamheid", "sociale rechtvaardigheid", "gelijkheid", "progressieve belastingen"],
        {
            "klimaat": "Klimaatneutraal in 2030, afbouwen fossiele brandstoffen",
            "wonen": "100.000 betaalbare woningen, huurbevriezing, limiteren verhuurders",
            "belastingen": "Progressieve belastingen, vermogensbelasting vanaf €1M",
            "zorg": "Sterke publieke gezondheidszorg, prioriteit voor geestelijke gezondheid",
        },
    )
    create_party_structure(
        "VVD",
        ["economische vrijheid", "eigen verantwoordelijkheid", "veiligheid", "pragmatisme"],
        {
            "economie": "Lagere belastingen, minder regelgeving, ondernemers ondersteunen",
            "wonen": "Woningaanbod vergroten via marktmechanismen",
            "belastingen": "Lagere inkomstenbelasting, minder herverdeling",
            "veiligheid": "Sterke rechtshandhaving, grenscontrole",
        },
    )
    print("\nVoltooid! Voeg nu handmatig meer details toe aan de verkiezingsprogramma.txt bestanden.")


if __name__ == "__main__":
    main()

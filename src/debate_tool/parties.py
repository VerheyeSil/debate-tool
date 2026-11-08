"""Loading party data from ``data/parties/<party>/``.

Each party folder contains:

- ``context.json``: party name, core values and key policies (required)
- ``verkiezingsprogramma.txt``: text from the election programme (optional)
- ``standpunten.txt``: extra positions as free text (optional)
"""

import json
from pathlib import Path

PARTIES_DIR = Path(__file__).parent / "data" / "parties"


def party_dir(party_name):
    """Return the data folder for a party, e.g. 'Groen Links' -> data/parties/groen_links."""
    return PARTIES_DIR / party_name.lower().replace(" ", "_")


def _read_text(path):
    """Read a text file, or return an empty string when it doesn't exist."""
    return path.read_text(encoding="utf-8").strip() if path.exists() else ""


def load_party_context(party_name):
    """Load all data for a party into one dict.

    Raises FileNotFoundError when the party has no ``context.json``, so a typo
    in a party name doesn't silently produce a debater without any positions.
    """
    folder = party_dir(party_name)
    context_file = folder / "context.json"
    if not context_file.exists():
        known = ", ".join(sorted(p.name for p in PARTIES_DIR.iterdir() if p.is_dir()))
        raise FileNotFoundError(f"No party data for '{party_name}' at {context_file}. Known parties: {known}")

    context = {"party_name": party_name, "core_values": [], "key_policies": {}}
    context.update(json.loads(context_file.read_text(encoding="utf-8")))
    context["verkiezingsprogramma"] = _read_text(folder / "verkiezingsprogramma.txt")
    context["standpunten"] = _read_text(folder / "standpunten.txt")
    return context

import os
import json

def create_party_structure(party_name, core_values, key_policies):
    """Creëer mappenstructuur en basis context voor een partij"""
    
    party_dir = f"data/parties/{party_name.lower().replace(' ', '_')}"
    os.makedirs(party_dir, exist_ok=True)
    
    context = {
        "party_name": party_name,
        "core_values": core_values,
        "key_policies": key_policies
    }
    
    with open(f"{party_dir}/context.json", 'w', encoding='utf-8') as f:
        json.dump(context, f, indent=2, ensure_ascii=False)
    
    # Creëer placeholder bestanden
    open(f"{party_dir}/verkiezingsprogramma.txt", 'a', encoding='utf-8').close()
    open(f"{party_dir}/standpunten.txt", 'a', encoding='utf-8').close()
    
    print(f"Structuur aangemaakt voor {party_name}")

# Creëer GroenLinks
create_party_structure(
    "GroenLinks",
    ["duurzaamheid", "sociale rechtvaardigheid", "gelijkheid", "progressieve belastingen"],
    {
        "klimaat": "Klimaatneutraal in 2030, afbouwen fossiele brandstoffen",
        "wonen": "100.000 betaalbare woningen, huurbevriezing, limiteren verhuurders",
        "belastingen": "Progressieve belastingen, vermogensbelasting vanaf €1M",
        "zorg": "Sterke publieke gezondheidszorg, prioriteit voor geestelijke gezondheid"
    }
)

# Creëer VVD
create_party_structure(
    "VVD",
    ["economische vrijheid", "eigen verantwoordelijkheid", "veiligheid", "pragmatisme"],
    {
        "economie": "Lagere belastingen, minder regelgeving, ondernemers ondersteunen",
        "wonen": "Woningaanbod vergroten via marktmechanismen",
        "belastingen": "Lagere inkomstenbelasting, minder herverdeling",
        "veiligheid": "Sterke rechtshandhaving, grenscontrole"
    }
)

print("\nVoltooid! Voeg nu handmatig meer details toe aan de verkiezingsprogramma.txt bestanden.")
import os
from datetime import datetime

PROJEKTMALLAR = {
    "python": {
        "data": [
            "raw/.gitkeep",
            "processed/.gitkeep",
            "output/.gitkeep",
        ],
        "dokumentation": ["README.md"],
        "src": ["__init__.py"],
        "tests": [],
        "notebooks": [],
        "config": [],
        ".github": ["workflows/ci.yml"]
    },
    "webb": {
        "data": [],
        "public": ["index.html", "style.css", "script.js"],
        "assets": [],
        "src": [],
        ".github": ["workflows/ci.yml"]
    }
}

GITIGNORE_REGLER = {
    "python": [
        "# Ignorera allt i data/",
        "data/**",
        "!data/**/.gitkeep",
    ],
    "webb": [
        "# Ignorera node_modules och byggfiler",
        "node_modules/",
        "dist/",
        "data/**",
        "!data/**/.gitkeep",
    ],
}

EDITORCONFIG_INNEHALL = """root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
indent_style = space
indent_size = 4
"""

LICENSE_MIT = """MIT License

Copyright (c) {}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction..."""

def skapa_mappstruktur(basväg: str, struktur: dict):
    for mapp, filer in struktur.items():
        mappsökväg = os.path.join(basväg, mapp)
        os.makedirs(mappsökväg, exist_ok=True)
        print(f"📁 Skapade mapp: {mappsökväg}")

        for fil in filer:
            filsökväg = os.path.join(mappsökväg, fil)
            os.makedirs(os.path.dirname(filsökväg), exist_ok=True)
            with open(filsökväg, "w", encoding="utf-8") as f:
                f.write("")
            print(f"📄 Skapade fil: {filsökväg}")

        if not filer:
            gitkeep = os.path.join(mappsökväg, ".gitkeep")
            with open(gitkeep, "w") as f:
                f.write("")
            print(f"📄 Skapade .gitkeep i: {mappsökväg}")

def uppdatera_gitignore(basväg: str, malltyp: str):
    gitignore_sökväg = os.path.join(basväg, ".gitignore")
    regler = GITIGNORE_REGLER.get(malltyp, [])

    befintliga = []
    if os.path.exists(gitignore_sökväg):
        with open(gitignore_sökväg, "r", encoding="utf-8") as f:
            befintliga = f.read().splitlines()

    nya = [rad for rad in regler if rad not in befintliga]
    if nya:
        with open(gitignore_sökväg, "a", encoding="utf-8") as f:
            f.write("\n" + "\n".join(nya) + "\n")
        print("🛡️ Uppdaterade .gitignore")
    else:
        print("✅ .gitignore redan uppdaterad")

def skapa_readme(basväg: str, malltyp: str, projekt_namn: str):
    innehåll = ""
    if malltyp == "python":
        innehåll = f"""# 🐍 Python-projekt: {projekt_namn}

Detta projekt är strukturerat enligt Sävsjö kommuns riktlinjer.

## Struktur
- `src/` – programkod
- `tests/` – testmoduler
- `data/` – ej versionerad data
"""
    elif malltyp == "webb":
        innehåll = f"""# 🌐 Webbprojekt: {projekt_namn}

Detta är ett webbprojekt initierat med en standardstruktur.

## Struktur
- `public/` – HTML, CSS, JS
- `assets/` – bilder och resurser
- `data/` – JSON eller testdata
"""
    with open(os.path.join(basväg, "README.md"), "w", encoding="utf-8") as f:
        f.write(innehåll)
    print("📝 Skapade README.md")

def skapa_editorconfig(basväg: str):
    with open(os.path.join(basväg, ".editorconfig"), "w", encoding="utf-8") as f:
        f.write(EDITORCONFIG_INNEHALL)
    print("🛠️ Skapade .editorconfig")

def skapa_license(basväg: str):
    år = datetime.now().year
    innehåll = LICENSE_MIT.format(år)
    with open(os.path.join(basväg, "LICENSE"), "w", encoding="utf-8") as f:
        f.write(innehåll)
    print("📜 Skapade LICENSE")

if __name__ == "__main__":
    try:
        malltyp = input("📘 Välj projekttyp ('python' eller 'webb'): ").strip().lower()
        if malltyp not in PROJEKTMALLAR:
            raise ValueError("Ogiltig malltyp – välj 'python' eller 'webb'")

        projekt_namn = input("📦 Ange namn på det nya projektet: ").strip()
        if not projekt_namn:
            raise ValueError("Projektnamn får inte vara tomt")

        skapa_mappstruktur(projekt_namn, PROJEKTMALLAR[malltyp])
        uppdatera_gitignore(projekt_namn, malltyp)
        skapa_readme(projekt_namn, malltyp, projekt_namn)
        skapa_editorconfig(projekt_namn)
        skapa_license(projekt_namn)

        print(f"\n✅ Projekt '{projekt_namn}' skapades enligt mall: {malltyp}")

    except Exception as e:
        print(f"❌ Fel: {e}")

    input("\nTryck [Enter] för att avsluta...")

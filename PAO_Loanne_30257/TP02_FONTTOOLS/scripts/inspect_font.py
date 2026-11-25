import argparse
from pathlib import Path
from fontTools.ttLib import TTFont


def get_name(font, name_ids):
    if "name" not in font:
        return "Non disponible"
    for name_id in name_ids:
        for record in font["name"].names:
            if record.nameID == name_id:
                try:
                    value = record.toUnicode().strip()
                    if value:
                        return value
                except Exception:
                    pass
    return "Non disponible"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("font_file", help="Chemin vers un fichier .ttf ou .otf")
    args = parser.parse_args()

    font_path = Path(args.font_file)

    if not font_path.is_file():
        raise SystemExit(f"Fichier introuvable : {font_path}")

    try:
        font = TTFont(str(font_path))
    except Exception as error:
        raise SystemExit(f"Impossible de lire cette police : {error}")

    family = get_name(font, (16, 1))
    style = get_name(font, (17, 2))
    glyph_count = len(font.getGlyphOrder())
    cmap = font.getBestCmap() or {}
    unicode_count = len(cmap)
    tables = sorted(font.keys())

    print("INSPECTION DE LA POLICE")
    print(f"Fichier : {font_path}")
    print(f"Famille : {family}")
    print(f"Style : {style}")
    print(f"Nombre de glyphes : {glyph_count}")
    print(f"Nombre de caractères Unicode : {unicode_count}")
    print("Tables du fichier :")
    for table in tables:
        print(f"- {table}")


if __name__ == "__main__":
    main()

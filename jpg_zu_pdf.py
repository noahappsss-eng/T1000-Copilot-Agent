import argparse
from pathlib import Path

from PIL import Image


ENDUNGEN = {".jpg", ".jpeg"}


def konvertiere_bilder(hauptordner: Path) -> tuple[int, list[str]]:
    anzahl = 0
    fehler = []

    for datei in hauptordner.rglob("*"):
        if not datei.is_file() or datei.suffix.lower() not in ENDUNGEN:
            continue

        try:
            pdf_pfad = datei.with_suffix(".pdf")

            # Falls schon eine PDF mit gleichem Namen existiert, überspringen.
            if pdf_pfad.exists():
                print(f"Übersprungen, PDF existiert bereits: {pdf_pfad}")
                continue

            with Image.open(datei) as bild:
                bild.convert("RGB").save(pdf_pfad, "PDF", resolution=100.0)

            # Nur löschen, wenn die PDF erfolgreich erstellt wurde.
            if pdf_pfad.exists() and pdf_pfad.stat().st_size > 0:
                datei.unlink()
                print(f"Ersetzt: {datei} -> {pdf_pfad}")
                anzahl += 1
            else:
                fehler.append(str(datei))

        except Exception as error:
            fehler.append(f"{datei} | Fehler: {error}")

    return anzahl, fehler


def main() -> None:
    parser = argparse.ArgumentParser(
        description="JPG- und JPEG-Dateien rekursiv in PDF-Dateien umwandeln."
    )
    parser.add_argument(
        "hauptordner",
        type=Path,
        help="Pfad zu dem Ordner, der rekursiv durchsucht werden soll",
    )
    args = parser.parse_args()

    if not args.hauptordner.is_dir():
        parser.error(f"Ordner nicht gefunden: {args.hauptordner}")

    anzahl, fehler = konvertiere_bilder(args.hauptordner)

    print()
    print(f"Fertig. Ersetzte Dateien: {anzahl}")

    if fehler:
        print("\nFehler bei folgenden Dateien:")
        for eintrag in fehler:
            print(eintrag)


if __name__ == "__main__":
    main()

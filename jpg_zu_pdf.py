from pathlib import Path
from PIL import Image

# Hauptordner Pfad
hauptordner = Path(r"\\hau-drive\hau-drive\_transfers\_public\Obertscheider D\NOAH\Variantenanträge")

# Unterstützte Dateiendungen
endungen = [".jpg", ".jpeg"]

anzahl = 0
fehler = []

for datei in hauptordner.rglob("*"):
    if datei.is_file() and datei.suffix.lower() in endungen:
        try:
            pdf_pfad = datei.with_suffix(".pdf")

            # Falls schon eine PDF mit gleichem Namen existiert, überspringen
            if pdf_pfad.exists():
                print(f"Übersprungen, PDF existiert bereits: {pdf_pfad}")
                continue

            with Image.open(datei) as img:
                img = img.convert("RGB")
                img.save(pdf_pfad, "PDF", resolution=100.0)

            # Nur löschen, wenn PDF erfolgreich erstellt wurde
            if pdf_pfad.exists() and pdf_pfad.stat().st_size > 0:
                datei.unlink()
                print(f"Ersetzt: {datei} -> {pdf_pfad}")
                anzahl += 1
            else:
                fehler.append(str(datei))

        except Exception as e:
            fehler.append(f"{datei} | Fehler: {e}")

print()
print(f"Fertig. Ersetzte Dateien: {anzahl}")

if fehler:
    print("\nFehler bei folgenden Dateien:")
    for f in fehler:
        print(f)
import argparse
import csv
import re
import sys
from pathlib import Path


def detect_encoding(path: Path) -> str:
    raw = path.read_bytes()[:131072]
    try:
        raw.decode("utf-8-sig")
        return "utf-8-sig"
    except UnicodeDecodeError:
        return "cp1252"


def detect_dialect(path: Path, encoding: str):
    with path.open("r", encoding=encoding, newline="") as f:
        sample = f.read(65536)
    try:
        return csv.Sniffer().sniff(sample, delimiters=";,\t|")
    except csv.Error:
        delimiter = "," if sample.count(",") > sample.count(";") else ";"
        class FallbackDialect(csv.excel):
            pass
        FallbackDialect.delimiter = delimiter
        return FallbackDialect


def is_zero(value: str) -> bool:
    value = value.strip().replace(" ", "").replace(",", ".")
    try:
        return float(value) == 0.0
    except ValueError:
        return False


def safe_filename(text: str, max_length: int = 150) -> str:
    text = text.strip()
    text = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", text)
    text = re.sub(r"\s+", " ", text).strip(" .")
    if not text:
        text = "Unbenannter Artikel"
    # Problematische Windows-Geraetenamen vermeiden.
    reserved = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}
    if text.upper() in reserved:
        text = "_" + text
    return text[:max_length].rstrip(" .")


def unique_output_path(output_dir: Path, article: str) -> Path:
    base = safe_filename(f"{article} Stückliste")
    candidate = output_dir / f"{base}.csv"
    counter = 2
    while candidate.exists():
        candidate = output_dir / f"{base} ({counter}).csv"
        counter += 1
    return candidate


def split_csv(input_path: Path, output_dir: Path, baustufe_col: int = 0, article_col: int = 8) -> tuple[int, int]:
    if not input_path.is_file():
        raise FileNotFoundError(f"Eingabedatei nicht gefunden: {input_path}")
    if input_path.resolve() == output_dir.resolve():
        raise ValueError("Der Ausgabeordner darf nicht die Eingabedatei sein.")

    output_dir.mkdir(parents=True, exist_ok=True)
    encoding = detect_encoding(input_path)
    dialect = detect_dialect(input_path, encoding)

    current_file = None
    current_writer = None
    created = 0
    ignored_before_first_zero = 0

    try:
        with input_path.open("r", encoding=encoding, newline="") as source:
            reader = csv.reader(source, dialect)
            try:
                header = next(reader)
            except StopIteration:
                raise ValueError("Die CSV-Datei ist leer.")

            required_index = max(baustufe_col, article_col)
            if len(header) <= required_index:
                raise ValueError(
                    f"Die CSV hat nur {len(header)} Spalten; benötigt wird mindestens Spalte {required_index + 1}."
                )

            for line_number, row in enumerate(reader, start=2):
                if not row or all(not cell.strip() for cell in row):
                    continue
                if len(row) <= required_index:
                    print(f"Warnung: Zeile {line_number} hat zu wenige Spalten und wurde übersprungen.", file=sys.stderr)
                    continue

                if is_zero(row[baustufe_col]):
                    if current_file is not None:
                        current_file.close()
                    article = row[article_col].strip()
                    output_path = unique_output_path(output_dir, article)
                    current_file = output_path.open("w", encoding="utf-8-sig", newline="")
                    current_writer = csv.writer(
                        current_file,
                        delimiter=dialect.delimiter,
                        quotechar='"',
                        quoting=csv.QUOTE_MINIMAL,
                        doublequote=True,
                        lineterminator="\r\n",
                    )
                    current_writer.writerow(header)
                    created += 1

                if current_writer is not None:
                    current_writer.writerow(row)
                else:
                    ignored_before_first_zero += 1
    finally:
        if current_file is not None:
            current_file.close()

    return created, ignored_before_first_zero


def main() -> None:
    parser = argparse.ArgumentParser(description="CSV-Stücklisten an Baustufe 0 aufteilen.")
    parser.add_argument("csv_datei", type=Path, help="Pfad zur grossen CSV-Datei")
    parser.add_argument("-o", "--ausgabe", type=Path, default=Path("aufgeteilte_stuecklisten_MRF"), help="Ausgabeordner")
    parser.add_argument("--baustufe-spalte", type=int, default=1, help="Baustufe-Spalte als Excel-Nummer, Standard: 1 (= A)")
    parser.add_argument("--artikel-spalte", type=int, default=9, help="Artikelbezeichnung-Spalte als Excel-Nummer, Standard: 9 (= I)")
    args = parser.parse_args()

    if args.baustufe_spalte < 1 or args.artikel_spalte < 1:
        parser.error("Spaltennummern müssen mindestens 1 sein.")

    created, ignored = split_csv(
        args.csv_datei,
        args.ausgabe,
        baustufe_col=args.baustufe_spalte - 1,
        article_col=args.artikel_spalte - 1,
    )
    print(f"Fertig: {created} CSV-Datei(en) in '{args.ausgabe}' erstellt.")
    if ignored:
        print(f"Hinweis: {ignored} Datenzeile(n) vor der ersten Baustufe 0 wurden nicht ausgegeben.")


if __name__ == "__main__":
    main()
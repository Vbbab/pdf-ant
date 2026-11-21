import argparse
from pathlib import Path

from pdf_ant.export_file import export_annots
from pdf_ant.import_file import import_annots

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export and import PDF annotations as blob-free JSON."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    export_parser = subparsers.add_parser(
        "export", help="Extract annotations from a PDF to JSON."
    )
    export_parser.add_argument("annotated_pdf", type=Path, help="Input annotated PDF")
    export_parser.add_argument("json_out", type=Path, help="Output JSON annotation file")

    import_parser = subparsers.add_parser(
        "import", help="Apply annotations from JSON onto a clean (annotation-free) copy of the original PDF."
    )
    import_parser.add_argument("clean_pdf", type=Path, help="Clean copy of source PDF")
    import_parser.add_argument("json_in", type=Path, help="Input JSON annotation file")
    import_parser.add_argument("output_pdf", type=Path, help="Output annotated PDF")

    return parser.parse_args()

def main() -> None:
    args = parse_args()
    if args.command == "export":
        export_annots(args.annotated_pdf, args.json_out)
    elif args.command == "import":
        import_annots(args.clean_pdf, args.json_in, args.output_pdf)

if __name__ == '__main__':
    main()

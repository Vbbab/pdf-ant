# pdf-ant

Small (janky!!!) Python tool built on qpdf (pikepdf) to allow version controlling PDF annotations.

## Usage

```
pdf-ant [-h] {export,import} ...

Export and import PDF annotations as blob-free JSON.

positional arguments:
  {export,import}
    export         Extract annotations from a PDF to JSON.
    import         Apply annotations from JSON onto a clean (annotation-free) copy of the original PDF.

options:
  -h, --help       show this help message and exit
```
```
pdf-ant export [-h] annotated_pdf json_out

positional arguments:
  annotated_pdf  Input annotated PDF
  json_out       Output JSON annotation file

options:
  -h, --help     show this help message and exit
```
```
pdf-ant import [-h] clean_pdf json_in output_pdf

positional arguments:
  clean_pdf   Clean copy of source PDF
  json_in     Input JSON annotation file
  output_pdf  Output annotated PDF

options:
  -h, --help  show this help message and exit
```

## Development
This project is built with [uv](https://docs.astral.sh/uv/), but also incluides a helper wrapper script `./uvw` that functions like `gradlew`.
Run it, and it will create a venv at `.venv` where you can develop this project, with `uv` included.

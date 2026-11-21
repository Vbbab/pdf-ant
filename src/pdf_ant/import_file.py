from pathlib import Path
import pikepdf

def import_annots(clean_pdf: Path, json_in: Path, output_pdf: Path) -> None:
    with pikepdf.Pdf.new() as tmp_pdf:
        tmp_pdf.update_from_qpdf_json(json_in)

        with pikepdf.open(clean_pdf) as pdf:
            for idx, tmp_page in enumerate(tmp_pdf.pages):
                target_page = pdf.pages[idx]
                tmp_annots = tmp_page.get("/Annots")
                if tmp_annots:
                    rebuilt = pikepdf.Array()
                    for annot in tmp_annots:
                        copied = pdf.copy_foreign(annot)
                        copied[pikepdf.Name("/P")] = target_page.obj
                        rebuilt.append(pdf.make_indirect(copied))
                    target_page[pikepdf.Name("/Annots")] = rebuilt
                elif "/Annots" in target_page:
                    del target_page[pikepdf.Name("/Annots")]

            output_pdf.parent.mkdir(parents=True, exist_ok=True)
            pdf.save(output_pdf)

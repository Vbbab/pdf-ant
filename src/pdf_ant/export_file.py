import io
import json
from pathlib import Path
import pikepdf
from typing import Any

from pdf_ant.constants import (
    SKIP_ANNOT_KEYS,
    KEEP_PAGE_KEYS,
    # QPDF_JSON_VERSION
)


def export_annots(annotated_pdf: Path, json_out: Path) -> None:
    with pikepdf.open(annotated_pdf) as pdf:
        for page in pdf.pages:
            annots = page.get("/Annots")
            if not annots:
                continue
            for annot in annots:
                for key in list(annot.keys()):
                    if str(key) in SKIP_ANNOT_KEYS:
                        del annot[key]

        buf = io.BytesIO()
        pdf.write_qpdf_json(buf)

    full_qpdf = json.loads(buf.getvalue().decode("utf-8"))
    header, all_objects = full_qpdf["qpdf"]

    # 1. Start with empty (null) copies of all objects so no reference ever dangles
    annot_objects: dict[str, dict[str, Any]] = {
        key: {"value": None} for key in all_objects if key != "trailer"
    }
    annot_objects["trailer"] = all_objects["trailer"]

    def copy_with_refs(obj_key: str) -> None:
        if obj_key not in all_objects or annot_objects.get(obj_key) == all_objects[obj_key]:
            return
        annot_objects[obj_key] = all_objects[obj_key]

        def walk_refs(val: Any) -> None:
            if isinstance(val, dict):
                for v in val.values():
                    walk_refs(v)
            elif isinstance(val, list):
                for v in val:
                    walk_refs(v)
            elif isinstance(val, str) and val.endswith(" R"):
                copy_with_refs(f"obj:{val}")

        walk_refs(all_objects[obj_key].get("value"))

    # 2. Repopulate Catalog, Page tree, stripped Pages, and Annotations (+ nested refs)
    root_key = f"obj:{all_objects['trailer']['value']['/Root']}"
    annot_objects[root_key] = all_objects[root_key]
    pages_root_key = f"obj:{all_objects[root_key]['value']['/Pages']}"

    def walk_page_tree(node_key: str) -> None:
        val = all_objects[node_key]["value"]
        if "/Kids" in val:
            annot_objects[node_key] = all_objects[node_key]
            for kid_ref in val["/Kids"]:
                walk_page_tree(f"obj:{kid_ref}")
        else:
            slim_page = {k: v for k, v in val.items() if k in KEEP_PAGE_KEYS}
            slim_page.setdefault("/Type", "/Page")
            annot_objects[node_key] = {"value": slim_page}
            for annot_ref in val.get("/Annots", []):
                copy_with_refs(f"obj:{annot_ref}")

    walk_page_tree(pages_root_key)
    full_qpdf["qpdf"] = [header, annot_objects]

    json_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(
        json.dumps(full_qpdf, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw


class VerificationError(RuntimeError): pass


def _run(*args: str) -> str:
    result = subprocess.run(args, check=False, capture_output=True, text=True)
    if result.returncode:
        raise VerificationError(f"Command failed: {' '.join(args)}: {result.stderr.strip()}")
    return result.stdout


def verify_pdfs(pdf_dir: Path, qa_dir: Path, detailed_name: str, brief_name: str, latest_tag: str, brief_title: str) -> dict:
    qa_dir.mkdir(parents=True, exist_ok=True); checks = {}
    expected = {detailed_name: ["Executive assessment", "Detailed version and Feature timeline", "Feature evolution by technical dimension", "Sources and methodology", latest_tag], brief_name: [brief_title, "Release evolution timeline", "Key version milestones", "Deployment takeaways", latest_tag]}
    for filename, terms in expected.items():
        pdf = pdf_dir / filename
        if not pdf.exists() or pdf.stat().st_size < 4000: raise VerificationError(f"Missing or suspicious PDF: {pdf}")
        info = _run("pdfinfo", str(pdf)); text = _run("pdftotext", "-layout", str(pdf), "-")
        missing = [term for term in terms if term not in text]
        prefix = qa_dir / pdf.stem
        for stale in qa_dir.glob(f"{pdf.stem}-*.png"):
            stale.unlink()
        _run("pdftoppm", "-png", "-r", "140", str(pdf), str(prefix))
        images = sorted(qa_dir.glob(f"{pdf.stem}-*.png"))
        if not images: raise VerificationError(f"No rendered pages for {pdf}")
        rendered = [Image.open(image).convert("RGB") for image in images]
        contact = Image.new("RGB", (max(image.width for image in rendered), sum(image.height for image in rendered)), "white")
        y = 0
        for image in rendered: contact.paste(image, (0, y)); y += image.height
        contact.save(qa_dir / f"{pdf.stem}-contact-sheet.png")
        checks[filename] = {"pdfinfo": info, "page_count": len(images), "size": pdf.stat().st_size, "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(), "missing_terms": missing, "rendered_pages": [image.name for image in images]}
        if missing: raise VerificationError(f"Required text missing from {filename}: {missing}")
    if checks.get(brief_name, {}).get("page_count") != 2: raise VerificationError("Evolution brief must be exactly two pages")
    result = {"passed": True, "reports": checks}; (qa_dir / "verification.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result

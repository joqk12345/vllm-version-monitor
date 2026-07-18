from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Iterable

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .config import Config
from .models import FeatureEvidence, ReleaseRecord, Stage


def _styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("Title", parent=base["Title"], fontSize=21, leading=25, textColor=colors.HexColor("#11233F")),
        "h1": ParagraphStyle("H1", parent=base["Heading1"], fontSize=15, leading=18, textColor=colors.HexColor("#0B5E8E"), spaceBefore=12),
        "body": ParagraphStyle("Body", parent=base["BodyText"], fontSize=8.7, leading=12),
        "small": ParagraphStyle("Small", parent=base["BodyText"], fontSize=7.2, leading=9),
    }


def _header_footer(label):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(colors.HexColor("#52616B"))
        canvas.drawString(1.6 * cm, 1.0 * cm, f"{label} Release Intelligence · Official-source analysis")
        canvas.drawRightString(A4[0] - 1.6 * cm, 1.0 * cm, f"Page {doc.page}")
        canvas.restoreState()
    return draw

def _unused_header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#52616B"))
    canvas.drawString(1.6 * cm, 1.0 * cm, "vLLM Release Intelligence · Official-source analysis")
    canvas.drawRightString(A4[0] - 1.6 * cm, 1.0 * cm, f"Page {doc.page}")
    canvas.restoreState()


def _table(rows, widths):
    table = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#123A5A")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 7.2),
        ("LEADING", (0, 0), (-1, -1), 9), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#C9D5DF")), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F8FA")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def render_detail(output: Path, config: Config, records: list[ReleaseRecord], features: list[FeatureEvidence], stages: list[Stage], cutoff: str) -> None:
    styles = _styles(); output.parent.mkdir(parents=True, exist_ok=True)
    stable = [record for record in records if record.release_kind == "stable"]
    latest = stable[-1] if stable else records[-1]
    by_tag = defaultdict(list)
    for feature in features: by_tag[feature.tag].append(feature)
    story = [Paragraph(config.project["titles"]["detailed"], styles["title"]), Spacer(1, 8), Paragraph(f"Cutoff: {cutoff} UTC · Latest official stable: <link href='{latest.release_url}'>{latest.tag}</link> ({latest.published_at[:10]}) · Source mode: {latest.source_mode}", styles["body"])]
    for heading, text in [
        ("Executive assessment", "vLLM is analyzed from official releases and current official documentation. Version transitions are grouped by explicit editorial boundaries; feature claims retain release-level source links."),
        ("Project positioning and current architecture", str(config.project.get("architecture_summary", "Current architecture must be verified against configured official documentation.")) + " Current architecture sources: " + ", ".join(f"<link href='{url}'>{name}</link>" for name, url in config.project["docs"].items())),
        ("Evolution at a glance", "\n".join(f"<b>{stage.name}</b>: {stage.summary}" for stage in stages)),
    ]:
        story += [Spacer(1, 8), Paragraph(heading, styles["h1"]), Paragraph(text, styles["body"])]
    story += [PageBreak(), Paragraph("Detailed version and Feature timeline", styles["h1"])]
    rows = [["Release", "UTC date", "Kind", "Feature evidence / source"]]
    for record in records:
        evidence = by_tag[record.tag][:2]
        note = "<br/>".join(feature.snippet for feature in evidence) or "No taxonomy match; retained in normalized index."
        rows.append([Paragraph(f"<link href='{record.release_url}'>{record.tag}</link>", styles["small"]), record.published_at[:10], record.release_kind, Paragraph(note, styles["small"])])
    story.append(_table(rows, [3.2 * cm, 2.0 * cm, 1.4 * cm, 10.0 * cm]))
    story += [Paragraph("Feature evolution by technical dimension", styles["h1"])]
    categories = defaultdict(list)
    for feature in features: categories[feature.category].append(feature.tag)
    story.append(_table([["Dimension", "Release evidence"]] + [[category, ", ".join(list(dict.fromkeys(tags))[-8:])] for category, tags in sorted(categories.items())], [5 * cm, 11.6 * cm]))
    story += [Paragraph("Engineering strengths and risks", styles["h1"]), Paragraph("Strengths and risks must be validated against the deployment workload. In particular, removal/deprecation statements refer to the named implementation path, not necessarily to the underlying concept. The v0.25 legacy PagedAttention implementation removal does not mean block-oriented KV management ceased to exist.", styles["body"]), Paragraph("Best-fit scenarios and operational cautions", styles["h1"]), Paragraph("Validate models, kernels, parallel topology, cache configuration, and API compatibility against the target hardware before upgrading. Pin images and dependencies for production rollouts.", styles["body"]), Paragraph("Sources and methodology", styles["h1"]), Paragraph(f"Official releases: <link href='https://github.com/{config.repo_slug}/releases'>GitHub Releases</link>. Drafts are excluded; RCs are retained in normalized data but excluded from primary stages. Post/patch releases are retained. Data cutoff: {cutoff}.", styles["body"])]
    temp = NamedTemporaryFile(suffix=".pdf", dir=output.parent, delete=False); temp.close()
    doc = SimpleDocTemplate(temp.name, pagesize=A4, leftMargin=1.6*cm, rightMargin=1.6*cm, topMargin=1.5*cm, bottomMargin=1.5*cm, title=config.project["titles"]["detailed"], author="release-report")
    footer = _header_footer(config.project["display_name"])
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    Path(temp.name).replace(output)

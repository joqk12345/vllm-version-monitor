from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .config import Config
from .models import FeatureEvidence, ReleaseRecord, Stage


def render_brief(output: Path, config: Config, records: list[ReleaseRecord], features: list[FeatureEvidence], stages: list[Stage], cutoff: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True); styles = getSampleStyleSheet()
    title = ParagraphStyle("brief-title", parent=styles["Title"], fontSize=24, leading=28, textColor=colors.HexColor("#123A5A")); body = ParagraphStyle("brief-body", parent=styles["BodyText"], fontSize=9, leading=12)
    stable = [record for record in records if record.release_kind == "stable"]; latest = stable[-1] if stable else records[-1]
    name = config.project["display_name"]
    story = [Paragraph(config.project["titles"]["brief"], title), Paragraph(f"Official-release evolution through {cutoff} · latest stable: <link href='{latest.release_url}'>{latest.tag}</link>", body), Spacer(1, 8), Paragraph("One-line conclusion", styles["Heading2"]), Paragraph(f"{name} evolved through release-documented engine, scheduling, model-support, and distributed-serving changes. This brief only summarizes official-source evidence.", body), Spacer(1, 8), Paragraph("Release evolution timeline", styles["Heading2"])]
    rows = [["Stage", "Representative releases", "Architectural transition"]] + [[stage.name, f"{stage.releases[0]} – {stage.releases[-1]}", stage.summary] for stage in stages]
    table = Table(rows, colWidths=[5*cm, 5*cm, 16*cm], repeatRows=1); table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#123A5A")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.25,colors.grey),("VALIGN",(0,0),(-1,-1),"TOP"),("FONTSIZE",(0,0),(-1,-1),8),("LEADING",(0,0),(-1,-1),10),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#F3F7FA")])]))
    story += [table, Spacer(1, 8), Paragraph("Engine path · scale path · model path", styles["Heading2"]), Paragraph("Engine: release-documented execution, compilation, and kernel changes. Scale: release-documented parallelism and disaggregation changes. Models: release-documented dense, MoE, multimodal, speech, and hybrid-model support. Consult configured official documentation for current architecture details.", body), PageBreak(), Paragraph("Key version milestones", styles["Heading2"])]
    milestones = [record for record in records if record.release_kind == "stable"]
    picks = [milestones[round(i*(len(milestones)-1)/min(9,len(milestones)-1))] for i in range(min(10,len(milestones)))] if len(milestones)>1 else milestones
    story.append(Table([["Date", "Release", "Official source"]] + [[record.published_at[:10], record.tag, record.release_url] for record in picks], colWidths=[4*cm,5*cm,17*cm], repeatRows=1, style=TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#123A5A")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.25,colors.grey),("FONTSIZE",(0,0),(-1,-1),8),("VALIGN",(0,0),(-1,-1),"TOP")])) )
    story += [Spacer(1, 10), Paragraph("Deployment takeaways", styles["Heading2"]), Paragraph(f"Why {name}: release-documented serving and scaling evolution. What to manage: version cadence, model/hardware compatibility, cache and parallel settings, and migration notes for defaults/deprecations.", body), Spacer(1, 8), Paragraph(f"Sources: <link href='https://github.com/{config.repo_slug}/releases'>official GitHub Releases</link> and configured official documentation. Cutoff {cutoff}; source mode {latest.source_mode}.", body)]
    temp = NamedTemporaryFile(suffix=".pdf", dir=output.parent, delete=False); temp.close()
    doc = SimpleDocTemplate(temp.name, pagesize=landscape(A4), leftMargin=1.5*cm, rightMargin=1.5*cm, topMargin=1.2*cm, bottomMargin=1.2*cm, title=config.project["titles"]["brief"], author="release-report")
    doc.build(story); Path(temp.name).replace(output)

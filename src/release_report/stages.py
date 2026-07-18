from __future__ import annotations

from packaging.version import Version

from .config import Config
from .models import ReleaseRecord, Stage
from .normalize import version_from_tag


def build_stages(records: list[ReleaseRecord], config: Config) -> list[Stage]:
    stages: list[Stage] = []
    for override in config.data.get("stage_overrides", []):
        start, end = Version(str(override["start"])), Version(str(override["end"]))
        tags = tuple(record.tag for record in records if record.release_kind != "rc" and (value := version_from_tag(record.tag)) and start <= value <= end)
        if tags:
            stages.append(Stage(str(override["name"]), str(override["summary"]), tags))
    return stages

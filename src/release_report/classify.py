from __future__ import annotations

import re

from .config import Config
from .models import FeatureEvidence, ReleaseRecord


def classify(records: list[ReleaseRecord], config: Config) -> list[FeatureEvidence]:
    taxonomy = config.data["feature_taxonomy"]
    result: list[FeatureEvidence] = []
    for record in records:
        for raw_line in record.body_text.splitlines():
            line = re.sub(r"^\s*(?:[-*+] |\d+[.)] )", "", raw_line).strip()
            if len(line) < 12:
                continue
            lower = line.lower()
            for category, keywords in taxonomy.items():
                if any(re.search(rf"(?<![a-z0-9]){re.escape(str(keyword).lower())}(?![a-z0-9])", lower) for keyword in keywords):
                    result.append(FeatureEvidence(record.tag, category, line[:260], record.release_url))
    return result

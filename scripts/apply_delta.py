#!/usr/bin/env python3
"""
Apply a features-delta.json to the current features.json to produce a merged result.

Usage:
    python apply_delta.py <features.json> <features-delta.json> [--in-place]

Without --in-place, writes the merged result to stdout.
With --in-place, overwrites the input features.json with the merged result
(and creates a .bak backup).
"""

import sys
import json
import shutil
from datetime import datetime
from pathlib import Path


def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def find_feature(features: list, feature_id: str) -> dict | None:
    for f in features:
        if f["id"] == feature_id:
            return f
    return None


def apply_delta(features: list, delta: dict) -> list:
    """Apply delta changes and return the merged feature list."""
    merged = [dict(f) for f in features]  # deep copy at top level
    changes = delta.get("changes", {})

    # 1. Remove features
    for removed in changes.get("removed", []):
        merged = [f for f in merged if f["id"] != removed["id"]]

    # 2. Add new features
    for added in changes.get("added", []):
        # Ensure version field
        if "version" not in added:
            added["version"] = 1
        merged.append(dict(added))

    # 3. Modify existing features
    for modified in changes.get("modified", []):
        target = find_feature(merged, modified["id"])
        if target is None:
            print(f"Warning: modified feature '{modified['id']}' not found in features.json", file=sys.stderr)
            continue

        mod_changes = modified.get("changes", {})
        for key, value in mod_changes.items():
            if key == "version":
                target["version"] = value
            elif key in ("states", "interactions", "acceptanceCriteria"):
                # These are additive — merge and deduplicate
                if key not in target:
                    target[key] = []
                for item in value:
                    if item not in target[key]:
                        target[key].append(item)
            else:
                target[key] = value

    return merged


def validate_unaffected(merged: list, delta: dict) -> list[str]:
    """Check that unaffected features still exist. Returns list of warnings."""
    warnings = []
    unaffected = delta.get("unaffected", [])
    merged_ids = {f["id"] for f in merged}
    for fid in unaffected:
        if fid not in merged_ids:
            warnings.append(f"Unaffected feature '{fid}' not found in merged result — was it removed?")
    return warnings


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    in_place = "--in-place" in sys.argv

    if len(args) < 2:
        print("Usage: python apply_delta.py <features.json> <features-delta.json> [--in-place]")
        sys.exit(1)

    features_path = args[0]
    delta_path = args[1]

    features_data = load_json(features_path)
    delta = load_json(delta_path)

    features = features_data if isinstance(features_data, list) else features_data.get("features", [])
    merged = apply_delta(features, delta)

    # Validate
    warnings = validate_unaffected(merged, delta)
    for w in warnings:
        print(f"Warning: {w}", file=sys.stderr)

    result = {"features": merged, "lastMerged": datetime.now().isoformat()}

    if in_place:
        backup = features_path + ".bak"
        shutil.copy2(features_path, backup)
        with open(features_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Merged {len(features)} → {len(merged)} features (backup: {backup})")
        for w in warnings:
            print(f"Warning: {w}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

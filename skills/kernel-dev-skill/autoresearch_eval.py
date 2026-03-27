#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import json

skill_path = Path('/home/ares/yyskills/output/linux-kernel-modernization-skill/SKILL.md')
text = skill_path.read_text(encoding='utf-8')

checks = [
    ("simplicity_principle", "简单优于一切" in text),
    ("shortest_path_section", "执行顺序（最短路径）" in text),
    ("structured_output_template", all(k in text for k in [
        "## 1) Build blockers",
        "## 2) Minimal patch set",
        "## 3) Runtime smoke checks",
        "## 4) Regression risks",
        "## 5) Next smallest step",
    ])),
    ("enough_actionable_commands", text.count("```bash") >= 5),
    ("explicit_length_control", "输出长度控制" in text),
    ("compatibility_layer_strategy", "兼容层" in text),
    (
        "efficiency_mode",
        ("高效模式（30分钟）" in text) and ("最多执行 3 条命令" in text),
    ),
]

score = sum(1 for _, ok in checks if ok)
out = {
    "score": score,
    "max_score": len(checks),
    "pass_rate": round(score * 100.0 / len(checks), 1),
    "checks": [{"name": name, "passed": ok} for name, ok in checks],
}
print(json.dumps(out, ensure_ascii=False, indent=2))

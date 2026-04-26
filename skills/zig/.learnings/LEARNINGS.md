# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice

---

## [AUTO-EXP 2026-04-16T18:02:15.384Z] 经验候选: 首次慢调用
**工具/动作**: WebFetch / call
**上下文**: url=https://ziglang.org/download/0.16.0/release-notes.html
**触发条件**: 首次成功调用耗时 32431ms，超过阈值 4000ms。
**试验与结果**: 当前仅有基线样本（慢）。
**有效做法（候选）**: 缩小查询范围，优先复用已验证输入结构。
**复用片段（草案）**:
```text
Tool=WebFetch; Action=call; Context=url=https://ziglang.org/download/0.16.0/release-notes.html; Strategy=先窄后宽
```
**适用边界**: 同类任务键=WebFetch::call::url=https://ziglang.org/download/0.16.0/release-notes.html
**下次检查项**: 关注后续样本是否出现 >=40% 提速。

## [AUTO-EXP 2026-04-16T18:04:58.314Z] 经验候选: 首次慢调用
**工具/动作**: Read / call
**触发条件**: 首次成功调用耗时 2844ms，超过阈值 2000ms。
**试验与结果**: 当前仅有基线样本（慢）。
**有效做法（候选）**: 缩小查询范围，优先复用已验证输入结构。
**复用片段（草案）**:
```text
Tool=Read; Action=call; Context=default; Strategy=先窄后宽
```
**适用边界**: 同类任务键=Read::call::default
**下次检查项**: 关注后续样本是否出现 >=40% 提速。

## [AUTO-EXP 2026-04-16T18:05:53.084Z] 已内化经验: 同类调用显著提速
**工具/动作**: Read / call
**触发条件**: 同类任务出现稳定提速（基线 2844ms -> 当前 1504ms，提升 47%）。
**试验与结果**: 早期宽泛探索慢；后续复用结构化输入后明显变快。
**有效做法（已验证）**: 先用窄查询/限定条件命中关键目标，再逐步扩展。
**复用片段（建议）**:
```text
1) 固定动作: call
2) 固定上下文骨架: context=default
3) 先窄后宽: 先限定关键词/目标页面，再扩展范围
```
**适用边界**: 同类任务键=Read::call::default
**下次检查项**: 若连续3次回退到慢阈值以上，重开探索并更新模板。

## [AUTO-EXP 2026-04-16T23:33:08.912Z] 经验候选: 首次慢调用
**工具/动作**: WebFetch / call
**上下文**: url=https://ziglang.org/download/0.16.0/release-notes.html#toc-Language-Changes
**触发条件**: 首次成功调用耗时 105039ms，超过阈值 4000ms。
**试验与结果**: 当前仅有基线样本（慢）。
**有效做法（候选）**: 缩小查询范围，优先复用已验证输入结构。
**复用片段（草案）**:
```text
Tool=WebFetch; Action=call; Context=url=https://ziglang.org/download/0.16.0/release-notes.html#toc-Language-Changes; Strategy=先窄后宽
```
**适用边界**: 同类任务键=WebFetch::call::url=https://ziglang.org/download/0.16.0/release-notes.html#toc-Language-Changes
**下次检查项**: 关注后续样本是否出现 >=40% 提速。

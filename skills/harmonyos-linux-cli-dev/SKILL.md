---
name: harmonyos-linux-cli-dev
description: 在 Linux 下使用 HarmonyOS Command Line Tools + SDK CLI 进行应用开发、构建、打包、安装、调试与日志排查。内置命令全集、文档刷新流程，以及可重复执行的一键环境安装/校验脚本。
---

# HarmonyOS Linux CLI Dev Skill

## Scope

用于以下场景：
- 纯命令行开发 HarmonyOS 应用（不依赖 IDE 图形界面）
- 设备连接、安装、启动、调试、日志抓取
- HAP/HSP/App/HQF/APPQF 打包与拆包
- Linux CI 环境的自动化构建与部署

## Canonical References

- 入口页：`https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-commandline-get`
- 已抓取子页 Markdown（技能内置）：`skills/harmonyos-linux-cli-dev/references/harmonyos-commandline-docs/*.md`
- 子页索引：`skills/harmonyos-linux-cli-dev/references/harmonyos-commandline-docs/README.md`
- 命令全集：`skills/harmonyos-linux-cli-dev/COMMANDS.md`

## Re-runnable Environment Scripts

- 环境安装脚本：`skills/harmonyos-linux-cli-dev/scripts/setup_harmonyos_env.sh`
- 环境校验脚本：`skills/harmonyos-linux-cli-dev/scripts/verify_harmonyos_env.sh`

示例：
```bash
bash skills/harmonyos-linux-cli-dev/scripts/setup_harmonyos_env.sh
bash skills/harmonyos-linux-cli-dev/scripts/verify_harmonyos_env.sh
```

说明：
- 默认目标目录是 `/home/ares/yyshm`。
- `setup_harmonyos_env.sh` 会写入 `source /home/ares/yyshm/env.sh` 到 `~/.zshrc`（幂等）。
- 会配置 `npm/ohpm` 镜像仓库与 `ohpm` trace 目录。

## Refresh Workflow (Must Run First)

1. 抓取入口页及命令行子页：
```bash
python3 skills/harmonyos-linux-cli-dev/scripts/fetch_harmonyos_commandline_pages.py --out-dir skills/harmonyos-linux-cli-dev/references/harmonyos-commandline-docs
```
2. 重新生成自动提取索引（可选）：
```bash
python3 skills/harmonyos-linux-cli-dev/scripts/extract_harmonyos_cli_commands.py --docs-dir skills/harmonyos-linux-cli-dev/references/harmonyos-commandline-docs --out skills/harmonyos-linux-cli-dev/references/harmonyos-commandline-docs/COMMANDS.md
```
3. 人工以 `skills/harmonyos-linux-cli-dev/COMMANDS.md` 为准进行命令归档（去噪后版本）。

## Linux Baseline Setup

```bash
# 1) 配置 Command Line Tools 到 PATH
export PATH=${COMMAND_LINE_TOOLS}/command-line-tools/bin:$PATH

# 2) 检查工具可见性
hdc version
bm help
aa help
hilog -h
param -h
```

## Standard App Dev Pipeline (CLI)

1. 构建：
```bash
./hvigorw clean
./hvigorw assembleHap   # 或 assembleApp
```
2. 安装：
```bash
hdc list targets
hdc install <path/to/app.hap>
# 或设备端 bm
hdc shell bm install -p /data/local/tmp/app.hap
```
3. 启动 Ability：
```bash
hdc shell aa start -b <bundleName> -a <abilityName>
```
4. 日志排查：
```bash
hilog -x
# 或
hdc shell hilog -w start
hdc file recv /data/log/hilog <local_path>
```
5. 卸载：
```bash
hdc uninstall <bundleName>
# 或
hdc shell bm uninstall -n <bundleName>
```

## Command Coverage Requirement

执行任务时，默认可调用并优先覆盖以下工具命令：
- `hdc`, `aa`, `bm`, `hilog`, `param`, `atm`, `anm`, `cem`, `edm`, `devicedebug`, `mediatool`
- `app_packing_tool.jar`, `app_unpacking_tool.jar`
- `hvigorw`, `ohpm`, `codelinter`, `hstack`

详细参数与示例命令必须从以下文件引用：
- `skills/harmonyos-linux-cli-dev/COMMANDS.md`
- `skills/harmonyos-linux-cli-dev/references/harmonyos-commandline-docs/*.md`

## Response Rules For This Skill

- 先给可直接执行的 Linux 命令，不先讲原理。
- 涉及设备操作时，先给 `hdc list targets` 检查步骤。
- 命令不确定时，先输出 `tool --help` 再给保守执行方案。
- 涉及打包签名时，明确区分 debug/release。
- 输出中必须标注命令适用工具（例如 `bm` 或 `aa`），避免混淆。

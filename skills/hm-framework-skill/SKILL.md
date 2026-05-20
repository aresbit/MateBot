---
name: hm-framework-skill
description: >-
  OpenHarmony (鸿蒙) 服务层/框架层代码仓库架构与命名规范领域知识。
  适用于识别、导航、分析和创建符合 OpenHarmony 分层架构标准的代码仓库。
  当用户需要以下任一场景时使用此 Skill：
  (1) 分析 OpenHarmony 服务层或框架层代码仓库的目录结构与命名约定，
  (2) 判断一个仓库是否符合 OpenHarmony foundation 分层架构规范（subsystem/component 路径模式），
  (3) 理解 bundle.json 组件描述符与 GN 构建系统的路径映射关系，
  (4) 在 OpenHarmony 项目内新增组件、服务或接口时遵循正确的命名格式,
  (5) 理解 frameworks/ vs services/ vs interfaces/ vs common/ 的分层职责边界。
---

# OpenHarmony 服务层框架架构技能

## 概述

本技能提供 OpenHarmony (鸿蒙) 服务层代码仓库的分层架构、目录命名规范和 GN 构建系统约定知识。适用于 foundation 层所有子系统（multimedia, ai, filemanagement, communication 等），代码仓库遵循统一的 `foundation/<subsystem>/<component>` 路径模式，并在构建系统中通过 `//foundation/<subsystem>/<component>` 路径引用。

## 核心架构：五层目录模型

每个标准 OpenHarmony 服务层仓库由以下顶级目录组成：

| 目录 | 职责 | 是否必须 |
|------|------|----------|
| `frameworks/` | 客户端框架实现（SDK、NAPI 封装、内部套件） | 是 |
| `services/` | 服务端 System Ability (SA) 守护进程 | 视组件类型 |
| `interfaces/` | 纯头文件接口定义（公开 SDK + 内部 API） | 是 |
| `common/` | 跨模块共享工具代码 | 视需要 |
| `etc/` | 配置文件与参数 | 视需要 |
| `tools/` | CLI 工具与开发者实用程序 | 视需要 |
| `test/` | 测试套件（单元、模糊测试、系统、XTS） | 是 |

必选文件：
- `BUILD.gn` — GN 构建入口点
- `bundle.json` — 组件包描述符，声明 `subsystem`、`name`、`deps`、`build` 目标

## 命名规范

### 组件级命名：`<subsystem_prefix>_<feature>_<type>`

目录使用子系统前缀命名空间，后跟功能标识符和可选的类型后缀：

- `media_` 前缀 → 多媒体子系统组件（如 `media_scanner`、`media_thumbnail`、`media_backup_extension`）
- `neural_network_` 前缀 → AI 子系统组件（如 `neural_network_core`、`neural_network_runtime`）
- 无前缀 → 通用或单组件仓库（如 `common/` 内的 `media_ipc_common`、`utils`）

### 每个组件内部：`include/` + `src/` 模式

每个服务/框架组件内部遵循标准 C/C++ 分离：

```
services/media_scanner/
├── include/      # 公共头文件
└── src/          # 实现源文件
```

## 目录职责边界

### `frameworks/` — 客户端框架

实现供应用使用的客户端 SDK 和内部平台库：
- `js/` — NAPI JS 绑定（位于 `frameworks/js/`）
- `native/` — 原生 C/C++ 接口
- `innerkitsimpl/` — 内部套件实现（如 `media_library_manager`、`media_library_helper`）
- `client/` — 客户端 IPC 代理
- `ani/` — ArkTS 原生接口（.ets + .cpp）
- `services/` — 框架内部服务（非独立 SA）

### `services/` — 系统能力 (SA) 服务

独立的 System Ability 守护进程，作为后台服务运行。每个服务是一个具有自己事件循环的独立 SA：
- `media_scanner/` — 文件扫描 SA
- `media_thumbnail/` — 缩略图生成 SA
- `media_cloud_sync_service/` — 云同步 SA
- `media_backup_extension/` — 备份扩展 SA

### `interfaces/` — API 定义

仅头文件，无实现：
- `interfaces/kits/` — 公共 SDK（`kits/c/`—C API，`kits/cj/`—CJ FFI，`kits/js/`—JS/NAPI 接口）
- `interfaces/inner_api/` 或 `interfaces/innerkits/` — 系统内部（非公共）API

## bundle.json 路径映射

`bundle.json` 中的 `segment.destPath` 定义了系统源树中的组件位置：

```json
{
  "segment": { "destPath": "foundation/multimedia/media_library" },
  "component": { "name": "media_library", "subsystem": "multimedia" }
}
```

构建目标随后引用为 `//foundation/multimedia/media_library/<dir>:<target>`。

## 跨仓库一致性验证

使用仓库的 `bundle.json` 的快速验证检查表：

1. 是否存在 `BUILD.gn` + `bundle.json` 作为根必选文件？
2. `frameworks/` 是否包含客户端实现（非纯服务）？
3. `interfaces/` 是否仅包含头文件（无 .cpp 实现）？
4. `interfaces/kits/` 是否包含公共 API，在 `inner_api/` 或 `innerkits/` 中有内部 API？
5. 服务（如存在）是否遵循 `services/<prefix>_<feature>/` 命名？
6. 组件命名是否使用子系统前缀（如 `media_`、`neural_network_`）？

**纯框架仓库**（无独立 SA，如 `ai_neural_network_runtime`）在需要时省略 `services/` — 这仍然是符合规范的。

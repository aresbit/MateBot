# OpenHarmony 分层架构参考

## 系统架构上下文

OpenHarmony 遵循四层系统架构：

```
应用层 (Applications)
    ↓
框架层 (Framework Layer)     ← frameworks/ 代码在此实现
    ↓
系统服务层 (System Services)  ← services/ 代码在此实现
    ↓
内核层 (Kernel Layer)
```

代码仓库分为两类：
1. **框架仓库**：实现客户端 SDK 和框架组件（`frameworks/` + `interfaces/`，有或没有 `services/`）
2. **服务仓库**：实现 System Ability 守护进程（`services/` 为主，通常也包含 `frameworks/`）

## 跨子系统完整示例

### 示例 1：多媒体 — multimedia_media_library

```
foundation/multimedia/media_library/
├── BUILD.gn
├── bundle.json                    # subsystem: "multimedia", name: "media_library"
├── common/
│   ├── media_cloud_sync_data/     # 云同步数据共享工具
│   ├── media_ipc_common/          # IPC 共享工具
│   └── utils/                     # 通用工具
├── etc/param/                     # 系统参数
├── frameworks/
│   ├── ani/                       # ArkTS 原生接口
│   ├── client/                    # 客户端代理
│   ├── innerimpl/                 # 内部实现
│   ├── innerkitsimpl/             # 内部套件 (media_library_*)
│   │   ├── media_library_handler/
│   │   ├── media_library_helper/
│   │   ├── media_library_manager/
│   │   ├── media_library_cloud_sync/
│   │   └── analysis_data_kits/
│   ├── js/                        # NAPI 绑定 (src/ + napi_common/)
│   ├── native/                    # 原生 C/C++ 管理
│   ├── services/                  # 框架内部服务
│   │   ├── media_albums_refresh/
│   │   ├── media_async_worker/
│   │   ├── media_cloud_sync/
│   │   └── media_dfx/
│   └── utils/
├── interfaces/
│   ├── inner_api/                 # 内部 API 头文件
│   │   ├── analysis_data_kits/
│   │   ├── media_library_camera_helper/
│   │   ├── media_library_helper/
│   │   ├── media_permission_helper/
│   │   └── native/cloud_sync/
│   └── kits/                      # 公共 SDK 头文件
│       ├── c/                     # C API
│       ├── cj/                    # CJ (C+ArkTS) FFI
│       └── js/                    # JS NAPI 声明
├── services/                      # 独立 SA 守护进程
│   ├── media_albums_manager/
│   ├── media_analysis_data_manager/
│   ├── media_analysis_extension/
│   ├── media_assets_manager/
│   ├── media_backup_extension/
│   ├── media_cloud_enhancement/
│   ├── media_cloud_sync_service/
│   ├── media_custom_restore/
│   ├── media_facard/
│   ├── media_file_monitor/
│   ├── media_file_scan/
│   ├── media_fuse/
│   ├── media_kv_db/
│   ├── media_mtp/
│   ├── media_mtp_service/
│   ├── media_notification/
│   ├── media_old_notification/
│   ├── media_permission/
│   ├── media_rdbstore/
│   ├── media_refresh/
│   ├── media_scanner/
│   └── media_thumbnail/
├── tools/
│   ├── medialibrary_scanner/
│   └── medialibrary_tool/
└── MemoryLibraryExt/               # ArkTS 扩展
```

### 示例 2：AI — ai_neural_network_runtime

```
foundation/ai/neural_network_runtime/
├── BUILD.gn
├── bundle.json                    # subsystem: "ai", name: "neural_network_runtime"
├── common/                        # 共享工具
├── config/                        # 配置文件
├── example/                       # 开发者示例
│   ├── deep_learning_framework/   # 应用/框架示例
│   │   └── tflite/
│   └── drivers/                   # 设备驱动示例
├── figures/
├── frameworks/
│   └── native/                    # 原生框架实现
│       ├── neural_network_core/   # NNRt 核心库
│       └── neural_network_runtime/# NNRt 运行时实现
│           └── ops/               # 算子操作实现
├── interfaces/
│   ├── innerkits/                 # 内部 API
│   │   └── c/
│   └── kits/                      # 公共 SDK
│       └── c/
│           └── neural_network_runtime/
├── test/
│   ├── fuzztest/                  # 模糊测试
│   ├── system_test/               # 系统测试
│   ├── unittest/                  # 单元测试
│   │   ├── common/                # 通用测试（v1_0/、v2_0/）
│   │   ├── components/            # 组件测试（nn_tensor、nn_executor 等）
│   │   ├── inner_kits/
│   │   └── ops/
│   └── xtstest/                   # 跨工具链测试
```

### 对比分析

| 维度 | multimedia_media_library | ai_neural_network_runtime |
|------|--------------------------|---------------------------|
| **子系统** | `multimedia` | `ai` |
| **组件** | `media_library` | `neural_network_runtime` |
| **GN 基础路径** | `//foundation/multimedia/media_library` | `//foundation/ai/neural_network_runtime` |
| **`services/`** | ✅ 20 余个独立 SA 服务 | ❌ 无可独立 SA（纯框架组件） |
| **`frameworks/` 结构** | 深度嵌套（js/、native/、client/、ani/、innerkitsimpl/、services/） | 扁平（仅 `native/` 含 2 个子组件） |
| **`interfaces/kits/` 语言** | C / CJ / JS | 仅 C |
| **测试结构** | `frameworks/.../test/` | 专用的 `test/unittest/`、`test/fuzztest/`、`test/xtstest/` |
| **`example/`** | ❌ | ✅ 含开发者示例 |
| **组件命名前缀** | `media_` | `neural_network_` |

### 核心观点

两个仓库均遵循**完全相同的架构模式**：
1. `bundle.json` 中由 `segment.destPath` + `component.subsystem` 驱动的相同 `foundation/<subsystem>/<component>` 路径模式
2. 接口（公共 + 内部）与实现（框架 + 服务）严格分离
3. 标准 C/C++ `include/` + `src/` 组件内部布局
4. GN 构建系统通过 `//foundation/<subsystem>/<component>/<dir>:<target>` 引用目标
5. 以子系统为作用域的命名（`media_`、`neural_network_`）

差异源于架构角色：
- `media_library` 是一个**重服务**子系统，包含 20+ 个提供 System Capability 的独立 SA
- `neural_network_runtime` 是一个**框架组件**，向上对接 AI 推理框架，向下对接芯片驱动 — 无需独立 SA 守护进程

## bundle.json 模式参考

```json
{
  "name": "@ohos/<component_name>",
  "version": "4.0",
  "license": "Apache License 2.0",
  "publishAs": "code-segment",
  "segment": {
    "destPath": "foundation/<subsystem>/<component_name>"
  },
  "component": {
    "name": "<component_name>",
    "subsystem": "<subsystem>",
    "syscap": ["SystemCapability.<Subsystem>.<Feature>"],
    "features": ["<component>_feature_<name>"],
    "deps": {
      "components": ["ipc", "hilog", "napi", ...]
    },
    "build": {
      "group_type": {
        "fwk_group": ["//foundation/.../interfaces/kits/...", ...],
        "service_group": ["//foundation/.../services/...", ...]
      },
      "inner_kits": [
        {
          "name": "//foundation/<subsystem>/<component>/dir:target",
          "header": {
            "header_base": "//foundation/<subsystem>/<component>/interfaces/...",
            "header_files": ["file1.h", "file2.h"]
          }
        }
      ],
      "test": ["//foundation/.../test/..."]
    }
  }
}
```

## 验证检查表

分析任何 OpenHarmony 仓库时，使用以下检查表：

1. [ ] 根目录 `BUILD.gn` + `bundle.json` 是否存在？
2. [ ] `bundle.json` 中 `segment.destPath` 是否匹配实际仓库路径？
3. [ ] `frameworks/` 是否包含客户端/框架实现？
4. [ ] `interfaces/kits/` 是否存在（公共 SDK）？
5. [ ] `interfaces/inner_api/` 或 `interfaces/innerkits/` 是否存在（内部 API）？
6. [ ] 服务（如存在）是否在 `services/` 下，并使用 `include/` + `src/` 模式？
7. [ ] 所有组件名称是否使用子系统前缀（如 `media_`、`neural_network_`）？
8. [ ] 测试目录是否结构与实现组件对应？
9. [ ] `bundle.json` deps 中引用的组件名称是否仅使用下划线（非连字符）？

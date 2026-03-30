# 拆包工具

- slug: `unpacking-tool`
- updatedDate: `2026-03-30 08:12:45`
- source: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/unpacking-tool
- navigationAddress: `/hmos/hmos-dp1`

# 拆包工具

拆包工具是HarmonyOS提供的一种调测工具，支持通过命令行方式将HAP、HSP、App等文件解压成文件夹，并且提供Java接口对HAP、HSP、App等文件进行解析。

拆包所用的app_unpacking_tool.jar，可以在本地下载的HarmonyOS的SDK库中找到。

#### 约束与限制

拆包工具需要运行在Java8及其以上环境。

#### 拆包指令说明

#### [h2]HAP包模式拆包指令

开发者可以使用拆包工具的jar包对应用进行拆包，通过传入拆包选项、文件路径，将HAP包解压出来。

示例

```bash
java -jar app_unpacking_tool.jar --mode hap --hap-path <path> --out-path <path> [--force true]
```

参数含义及规范

#### [h2]App包模式拆包指令

开发者可以使用拆包工具的jar包对应用进行拆包，通过传入拆包选项、文件路径，将App包解压出来。

示例

```bash
java -jar app_unpacking_tool.jar --mode app --app-path <path> --out-path <path> [--force true]
```

参数含义及规范

#### [h2]从HAP包中获取rpcid文件

开发者可以使用拆包工具的jar包对应用进行拆包，通过传入拆包选项、文件路径，获取应用的rpcid。

示例

```bash
java -jar app_unpacking_tool.jar --mode hap --rpcid true --hap-path <path> --out-path <path> [--force true]
```

参数含义及规范

#### [h2]按照架构指数拆分HAP包

开发者可以使用拆包工具将hap包按照libs包含的架构类型拆包再打包，得到若干仅包含单架构类型库的hap包。

示例

```bash
java -jar app_unpacking_tool.jar --mode hap --hap-path <path> --out-path <path> [--force true] [--libs true] [--cpu-abis option]
```

参数含义及规范

#### [h2]HSP包模式拆包指令

开发者可以使用拆包工具的jar包对应用进行拆包，通过传入拆包选项、文件路径，将HSP包解压出来。

示例

```bash
java -jar app_unpacking_tool.jar --mode hsp --hsp-path <path> --out-path <path> [--force true]
```

参数含义及规范

#### [h2]按照架构指数拆分HSP包

开发者可以使用拆包工具将hsp包按照libs包含的架构类型拆包再打包，得到若干仅包含单架构类型库的hsp包。

示例

```bash
java -jar app_unpacking_tool.jar --mode hsp --hsp-path <path> --out-path <path> [--force true] [--libs true] [--cpu-abis option]
```

参数含义及规范

#### [h2]APPQF模式拆包指令

开发者可以使用拆包工具的jar包对应用进行拆包，通过传入拆包选项、文件路径，将APPQF包解压出来。

示例

```bash
java -jar app_unpacking_tool.jar --mode appqf --appqf-path <path> --out-path <path> [--force true]
```

参数含义及规范

#### 包解析接口

包解析接口仅用于应用市场对打好的HAP、HSP、App等包进行解析，获取其中配置文件等信息。

#### [h2]接口目录

接口功能：根据参数解析app包的pack.info信息。

输入参数：appPath app包路径，parseMode 解析模式枚举（ALL/HAP_LIST/HAP_INFO），hapName hap包名（parseMode为HAP_INFO时需要配置）。

返回值：UncompressResult。

接口功能：根据参数解析app包的pack.info信息。

输入参数：input app文件流，parseMode 解析模式枚举（ALL/HAP_LIST/HAP_INFO），hapName hap包名（parseMode为HAP_INFO时需要配置）。

返回值：UncompressResult。

接口功能：根据参数解析app包的json配置文件。

输入参数：hapPath HAP包路径。

返回值：UncompressResult。

接口功能：根据参数解析app包的json配置文件。

输入参数：input HAP包文件流。

返回值：UncompressResult。

#### 拆包工具信息字段

#### [h2]UncompressResult（Bundle信息）结构体信息

#### [h2]PackInfo结构体信息

#### [h2]ProfileInfo结构体信息

#### [h2]AppInfo结构体信息

标识bundle的类型，取值：

- app：应用。

- atomicService：元服务。

- shared：应用间共享库。

#### [h2]HapInfo结构体信息

标识应用的框架模型。

- FA：FA模型。

- STAGE：Stage模型。

#### [h2]AbilityInfo结构体信息

#### [h2]Distro结构体信息

#### [h2]MetaData结构体信息

#### [h2]MetaDataInfo结构体信息

#### [h2]CustomizeData结构体信息

#### [h2]ReqPermission结构体信息

#### [h2]UsedScene结构体信息

#### [h2]Shortcut结构体信息

#### [h2]IntentInfo结构体信息

#### [h2]DistroFilter结构体信息

#### [h2]ApiVersion结构体信息

#### [h2]ScreenShape结构体信息

#### [h2]ScreenDensity结构体信息

#### [h2]ScreenWindow结构体信息

#### [h2]CountryCode结构体信息

#### [h2]ExtensionAbilityInfo结构体信息

#### [h2]SkillInfo结构体信息

#### [h2]UriInfo结构体信息

#### [h2]AbilityFormInfo结构体信息

卡片的提供方所在的Ability或者extension名称。

1. FA模型：如果卡片配置在service类型的ability中，providerAbility配置为mainAbility。

2. FA模型：如果卡片配置在Page类型的Ability中，providerAbility配置为当前Ability。

3. FA模型：如果没有配置mainAbility，providerAbility配置为当前HAP包中的优先使用system.home，否则第一个page的Ability。

4. stage模型中（follow上述规则），providerAbility配置为mainElement。

#### [h2]CommonEvent结构体信息

#### [h2]DependencyItem结构体信息

#### [h2]ModuleAtomicService结构体信息

#### [h2]PreloadItem结构体信息

#### [h2]DeviceConfig结构体信息

#### [h2]DefPermission结构体信息

#### [h2]DefinePermission结构体信息

#### [h2]DefPermissionsGroups结构体信息

#### [h2]FormInfo结构体信息

#### [h2]ModuleMetadataInfo结构体信息

#### [h2]ModuleWindowInfo结构体信息

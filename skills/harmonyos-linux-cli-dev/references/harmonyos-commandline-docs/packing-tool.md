# 打包工具

- slug: `packing-tool`
- updatedDate: `2026-03-30 08:12:39`
- source: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/packing-tool
- navigationAddress: `/hmos/hmos-dp1`

# 打包工具

打包工具用于在程序编译完成后，对编译出的文件等进行打包，以供安装发布。开发者可以使用DevEco Studio进行打包，也可使用打包工具的JAR包进行打包，JAR包通常存放在SDK路径下的toolchains目录中。

打包工具支持生成：Ability类型的模块包（HAP）、动态共享包（HSP）、应用程序包（App）、快速修复模块包（HQF）、快速修复包（APPQF）。

打包指令中的文件来源于
DevEco Studio编译构建产物
，文件路径查看操作如下。

- 在DevEco Studio工程根目录下的/hvigor/hvigor-config.json5文件中，修改"logging"下的"level"字段为"debug"。
在DevEco Studio工程根目录下的/hvigor/hvigor-config.json5文件中，修改"logging"下的"level"字段为"debug"。

- 在DevEco Studio菜单栏，依次选择"构建 -> 清理项目"。
在DevEco Studio菜单栏，依次选择"构建 -> 清理项目"。

- 在DevEco Studio菜单栏，依次选择"构建 -> 构建APP(s)"。
在DevEco Studio菜单栏，依次选择"构建 -> 构建APP(s)"。

- 在DevEco Studio底部"构建"窗口，搜索"app_packing_tool.jar"，确认打包参数中文件的路径。
在DevEco Studio底部"构建"窗口，搜索"app_packing_tool.jar"，确认打包参数中文件的路径。

打包工具会对module.json文件属性进行合法性校验。module.json文件是编译构建产物，其属性值在编译构建时自动生成，与配置文件中配置项对应关系如下。

表1
module.json与配置文件属性的对照表

targetSdkVersion/compileSdkVersion

说明：targetSdkVersion存在时，targetAPIVersion由targetSdkVersion决定；

否则，targetAPIVersion由compileSdkVersion决定。

#### 约束与限制

- 打包工具需要运行在Java8及其以上环境。
- 打包指令中参数和参数值需成对出现。例如，HAP打包指令中--resources-path <path>，其中--resources-path为指令参数，path为参数值，两者需要同时出现。
#### HAP打包指令

开发者可以使用打包工具的JAR包对模块进行打包，通过传入打包选项、文件路径，生成所需的HAP包。

HAP打包时合法性校验

- 从API version 21开始，在打包entry类型的HAP时，如果module.json文件中querySchemes配置了超过50个URL scheme，则要求minAPIVersion大于等于21。
打包HAP时的压缩规则：

- 应用配置compressNativeLibs为true时，会按照--compress-level设置的压缩等级对--lib-path指定目录下的文件进行压缩。
- 出于运行时性能等考量，--lib-path指定目录外的文件不会进行压缩。
示例：

- Stage模型
示例：
java -jar app_packing_tool.jar --mode hap --json-path <path> [--resources-path <path>] [--ets-path <path>] [--index-path <path>] [--pack-info-path <path>] [--lib-path <path>] --out-path <path> [--force true] [--compress-level 5] [--pkg-context-path <path>] [--hnp-path <path>]
Stage模型
示例：

```bash
java -jar app_packing_tool.jar --mode hap --json-path <path> [--resources-path <path>] [--ets-path <path>] [--index-path <path>] [--pack-info-path <path>] [--lib-path <path>] --out-path <path> [--force true] [--compress-level 5] [--pkg-context-path <path>] [--hnp-path <path>]
```

- FA模型
示例：
java -jar app_packing_tool.jar --mode hap --json-path <path> [--maple-so-path <path>] [--profile-path <path>] [--maple-so-dir <path>] [--dex-path <path>] [--lib-path <path>] [--resources-path <path>] [--index-path <path>] --out-path <path> [--force true] [--compress-level 5]
FA模型
示例：

```bash
java -jar app_packing_tool.jar --mode hap --json-path <path> [--maple-so-path <path>] [--profile-path <path>] [--maple-so-dir <path>] [--dex-path <path>] [--lib-path <path>] [--resources-path <path>] [--index-path <path>] --out-path <path> [--force true] [--compress-level 5]
```

表2
HAP打包指令参数说明

dex文件路径，文件名必须以.dex为后缀。如果是多个dex需要用“，”分隔。

dex文件路径也可以为目录。

指定增量打包时的源HAP包路径，该路径必须指向一个已存在的、有效的.hap文件。当--lib-path-retain配置为true时，打包工具会直接拷贝源HAP包中的libs目录，不再打包--lib-path指定的libs目录，该特性称为增量打包。当--lib-path-retain配置为false时，正常打包--lib-path指定的libs目录，该参数无效。当libs目录中so文件压缩耗时比较久时，使用增量打包可以提升打包速度。

从API version 22开始支持该参数。

是否对libs目录做增量打包。为true时表示对libs目录做增量打包，直接拷贝--exist-src-path指向的源HAP中的libs目录，不再打包--lib-path指定的libs目录；为false时表示不做增量打包，打包--lib-path指向的目录。默认值为false。此参数必须与--exist-src-path配套使用，单独设置不生效。

从API version 22开始支持该参数。

#### HSP打包指令

HSP包实现了多个HAP对文件的共享，开发者可以使用打包工具的jar包对应用进行打包，通过传入打包选项、文件路径，生成所需的HSP包。

打包HSP时的压缩规则：

- 应用配置compressNativeLibs为true时，会按照--compress-level设置的压缩等级对--lib-path指定目录下的文件进行压缩。
- 出于运行时性能等考量，--lib-path指定目录外的文件不会进行压缩。
示例：

```bash
java -jar app_packing_tool.jar --mode hsp --json-path <path> [--resources-path <path>] [--ets-path <path>] [--index-path <path>] [--pack-info-path <path>] [--lib-path <path>] --out-path <path> [--force true] [--compress-level 5] [--pkg-context-path <path>]
```

表3
HSP打包指令参数说明

1. dex文件路径，文件名必须以.dex为后缀。如果是多个dex需要用“，”分隔。

2. dex文件路径也可以为目录。

指定增量打包时的源HSP包路径，该路径必须指向一个已存在的、有效的.hsp文件。当--lib-path-retain配置为true时，打包工具会直接拷贝源HSP包中的libs目录，不再打包--lib-path指定的libs目录，该特性称为增量打包。当--lib-path-retain配置为false时，正常打包--lib-path指定的libs目录，该参数无效。当libs目录中so文件压缩耗时比较久时，使用增量打包可以提升打包速度。

从API version 22开始支持该参数。

是否对libs目录做增量打包。为true时表示对libs目录做增量打包，直接拷贝--exist-src-path指向的源HSP中的libs目录，不再打包--lib-path指定的libs目录；为false时表示不做增量打包，打包--lib-path指向的目录。默认值为false。此参数必须与--exist-src-path配套使用，单独设置不生效。

从API version 22开始支持该参数。

#### App打包指令

开发者可以使用打包工具的jar包对应用进行打包，通过传入打包选项、文件路径，生成所需的App包。App包用于上架应用市场。

表4
App打包合法性校验规则

从API version 20开始，要求所有HAP的debug字段值均保持一致，如果HAP的debug字段值为false，HSP的debug字段值也必须为false。如果HAP的debug字段值为true，对HSP的debug字段值无要求。

对于API version 19及之前版本，要求所有HAP或HSP的debug字段值均保持一致。

从API version 20开始，要求所有HAP的minAPIVersion字段值均保持一致，且均不低于所有HSP对应字段的最大值。

对于API version 19及之前版本，要求所有HAP或HSP的minAPIVersion字段值均保持一致。

从API version 16开始，要求所有HAP的minCompatibleVersionCode字段值均保持一致，且均不低于所有HSP对应字段的最大值。

对于API version 15及之前版本，要求所有HAP或HSP的minCompatibleVersionCode字段值均保持一致。

从API version 16开始，要求所有HAP的targetAPIVersion字段值均保持一致，且均不低于所有HSP对应字段的最大值。

对于API version 15及之前版本，要求所有HAP或HSP的targetAPIVersion字段值均保持一致。

- module.json文件为DevEco Studio编译构建产物，其中的字段与配置文件的对应关系，请参考
表1 module.json与配置文件属性的对照表
。
打包App时的压缩规则：
打包App时，对release模式的HAP、HSP包会进行压缩，对debug模式的HAP、HSP包不会压缩。

若HAP或HSP中已压缩的so文件，在打包APP时再次压缩，将不会有明显体积缩减。

示例：

```bash
java -jar app_packing_tool.jar --mode app [--hap-path <path>] [--hsp-path <path>] --out-path <path> [--signature-path <path>] [--certificate-path <path>] --pack-info-path <path> [--pack-res-path <path>] [--force true] [--encrypt-path <path>] [--pac-json-path <path>] [--atomic-service-entry-size-limit <size>] [--atomic-service-non-entry-size-limit <size>] [--replace-pack-info false]
```

表5
App打包指令参数说明

HAP包文件路径，文件名必须以.hap为后缀。如果是多个HAP包需要用“,”分隔。

HAP包文件路径也可以是目录。

HSP包文件路径，文件名必须以.hsp为后缀。如果是多个HSP包需要用“,”分隔。

HSP包文件路径也可以是目录。

pac.json
文件路径，文件名必须为pac.json。

从API version 20开始支持该参数。

打包APP时，是否使用由--pack-info-path参数指定的pack.info文件替换HAP、HSP包中的pack.info文件。如果为true表示替换，false表示不替换，默认值为true。

从API version 22开始支持该参数。

#### 多工程打包指令

多工程打包适用于多个团队开发同一个应用，但不方便共享代码的情况。开发者通过传入已经打好的HAP、HSP和App包，将多个包打成一个最终的App包，并上架应用市场。

表6
多工程打包合法性校验规则

从API version 20开始，要求所有HAP的debug字段值均保持一致，如果HAP的debug字段值为false，HSP的debug字段值也必须为false。如果HAP的debug字段值为true，对HSP的debug字段值无要求。

对于API version 19及之前版本，要求所有HAP或HSP的debug字段值均保持一致。

从API version 20开始，要求所有HAP的minAPIVersion字段值均保持一致，且均不低于所有HSP对应字段的最大值。

对于API version 19及之前版本，要求所有HAP或HSP的minAPIVersion字段值均保持一致。

从API version 16开始，要求所有HAP的minCompatibleVersionCode字段值均保持一致，且均不低于所有HSP对应字段的最大值。

对于API version 15及之前版本，要求所有HAP或HSP的minCompatibleVersionCode字段值均保持一致。

从API version 16开始，要求所有HAP的targetAPIVersion字段值均保持一致，且均不低于所有HSP对应字段的最大值。

对于API version 15及之前版本，要求所有HAP或HSP的targetAPIVersion字段值均保持一致。

- module.json文件为DevEco Studio编译构建产物，其中的字段与配置文件的对应关系，请参考
表1 module.json与配置文件属性的对照表
。
示例：

```bash
java -jar app_packing_tool.jar --mode multiApp [--hap-list <path>] [--hsp-list <path>] [--app-list <path>] --out-path <option> [--force true] [--encrypt-path <path>] [--pac-json-path <path>] [--atomic-service-entry-size-limit <size>] [--atomic-service-non-entry-size-limit <size>]
```

表7
多工程打包指令参数说明

HAP包文件路径，文件名必须以.hap为后缀。如果是多个HAP包需要“,”分隔。

HAP文件路径也可以是目录。

HSP包文件路径，文件名必须以.hsp为后缀。如果是多个HSP包需要“,”分隔。

HSP文件路径也可以是目录。

App文件路径，文件名必须以.app为后缀。如果是多个App包需要用“,”分隔。

App文件路径也可以是目录。

--hap-list，--hsp-list，--app-list不可以都不传。

pac.json
文件路径，文件名必须为pac.json。

最终app产物中pac.json文件只来源于该参数，不配置的话，最终app产物不包含该文件。

--app-list参数指定的app包中的pac.json不会打包进最终app。

从API version 20开始支持该参数。

#### HQF打包指令

HQF包适用于
增量调试
场景。开发者可以使用打包工具的jar包对应用进行打包，通过传入打包选项、文件路径，生成所需的HQF包。

- HQF包不支持上架应用市场，仅用于增量调试。
示例:

```bash
java -jar app_packing_tool.jar --mode hqf --json-path <path> [--lib-path <path>] [--ets-path <path>] [--resources-path <path>] --out-path <path> [--force true]
```

表8
HQF打包指令参数说明

#### APPQF打包指令

APPQF包由一个或多个HQF文件组成。这些HQF包在应用市场会从APPQF包中拆分出来，再被分发到具体的设备上。开发者可以使用打包工具的jar包对应用进行打包，通过传入打包选项、文件路径，生成所需的APPQF包。

APPQF打包合法性校验

- 在打包生成APPQF包时，确保每个HQF的
patch.json文件
中的versionName、versionCode、patchVersionName、patchVersionCode保持一致。
- 所有HQF不得重复。HQF重复是指同时满足以下两个条件：
两个HQF的patch.json文件中module下的name字段相同。
两个HQF的patch.json文件中module下的deviceTypes属性相交（至少存在一个相同的设备类型）。
- 两个HQF的patch.json文件中module下的name字段相同。
- 两个HQF的patch.json文件中module下的deviceTypes属性相交（至少存在一个相同的设备类型）。
示例:

```bash
java -jar app_packing_tool.jar --mode appqf --hqf-list <path> --out-path <path> [--force true]
```

表9
APPQF打包指令参数说明

#### 版本归一指令（versionNormalize）

同一个App中，所有HAP、HSP包的versionName和versionCode需要保持一致。当只有一个HAP或HSP需要修改升级时，可以调用此命令，将多个HAP、HSP的版本统一。本命令会修改所传入的HAP、HSP的版本号和版本名称，并在指定目录生成修改后的同名HAP、HSP，以及一个version_record.json文件，用于记录所有HAP、HSP原有的版本号、版本名称。

示例：

```bash
java -jar app_packing_tool.jar --mode versionNormalize --input-list 1.hap,2.hsp --version-code 1000001 --version-name 1.0.1 --out-path out
```

表10
versionNormalize指令参数说明

1. HAP或HSP包文件路径，文件名必须以.HAP或.HSP为后缀。如果是多个HAP或HSP包需要“,”分隔。

2. 传入目录时，会读取目录下所有的HAP和HSP文件。

#### 包名归一指令（packageNormalize）

此命令可以修改传入的HSP的包名和版本号，并在指定目录生成修改后的同名HSP。

示例：

```bash
java -jar app_packing_tool.jar --mode packageNormalize --hsp-list 1.hsp,2.hsp --bundle-name com.example.myapplication --version-code 1000001 --out-path out
```

表11
参数含义及规范

1. HSP包文件路径，文件名必须以.hsp为后缀。如果是多个HSP包需要“,”分隔。

2. HSP包目录。仅处理目录内以.hsp为后缀的文件。

#### 通用归一指令（generalNormalize）

此命令可以修改传入的HAP或HSP的deviceType/bundleName/versionName/versionCode/minCompatibleVersionCode/minAPIVersion/targetAPIVersion/

apiReleaseType/bundleTypes/installationFree/deliveryWithInstall参数，并在指定目录生成修改后的同名HAP或HSP，以及一个general_record.json文件，用于记录所有HAP、HSP原有的参数名称和moduleName。上述设置的参数应符合正确打包规范，否则会在指定目录生成HAP或HSP失败，指定目录不会有文件生成。

- 从API version 20开始支持通用归一化指令。
示例：

```bash
java -jar app_packing_tool.jar --mode generalNormalize --input-list 1.hsp,2.hsp --bundle-name com.example.myapplication --version-code 1000001 --version-name 1.0.1 --min-compatible-version-code 14 --min-api-version 14 --target-api-version 14 --api-release-type Release1 --bundle-type app --installation-free false --delivery-with-install true --device-types default,tablet --out-path out
```

表12
参数含义及规范

1. HAP或HSP包文件路径，文件名必须以.hap或.hsp为后缀。多个HAP或HSP包文件路径之间使用“,”分隔。

2. 传入目录时，会读取目录下所有的HAP和HSP文件。

#### res模式打包指令

此命令用于打包元服务快照资源。

示例：

```bash
java -jar app_packing_tool.jar --mode res --entrycard-path <path> --pack-info-path <path> --out-path <path> [--force true]
```

表13
参数含义及规范

#### fastApp模式打包指令

开发者可以使用打包工具的jar包对应用进行打包，通过传入打包选项、HAP、HSP包文件目录路径，生成所需的App包。App包用于上架应用市场。

表14
fastApp打包合法性校验规则

从API version 20开始，要求所有HAP的debug字段值均保持一致，如果HAP的debug字段值为false，HSP的debug字段值也必须为false。如果HAP的debug字段值为true，对HSP的debug字段值无要求。

对于API version 19及之前版本，要求所有HAP或HSP的debug字段值均保持一致。

从API version 20开始，要求所有HAP的minAPIVersion字段值均保持一致，且均不低于所有HSP对应字段的最大值。

对于API version 19及之前版本，要求所有HAP或HSP的minAPIVersion字段值均保持一致。

从API version 16开始，要求所有HAP的minCompatibleVersionCode字段值均保持一致，且均不低于所有HSP对应字段的最大值。

对于API version 15及之前版本，要求所有HAP或HSP的minCompatibleVersionCode字段值均保持一致。

从API version 16开始，要求所有HAP的targetAPIVersion字段值均保持一致，且均不低于所有HSP对应字段的最大值。

对于API version 15及之前版本，要求所有HAP或HSP的targetAPIVersion字段值均保持一致。

- module.json文件为DevEco Studio编译构建产物，其中的字段与配置文件的对应关系，请参考
表1 module.json与配置文件属性的对照表
。
打包App时的压缩规则：
打包App时，对release模式的HAP、HSP包会进行压缩，对debug模式的HAP、HSP包不会压缩。

若HAP或HSP中已压缩的so文件，在打包APP时再次压缩，将不会有明显体积缩减。

示例：

```bash
java -jar app_packing_tool.jar --mode fastApp [--hap-path <path>] [--hsp-path <path>] --out-path <path> [--signature-path <path>] [--certificate-path <path>] --pack-info-path <path> [--pack-res-path <path>] [--force true] [--encrypt-path <path>] [--pac-json-path <path>] [--atomic-service-entry-size-limit <size>] [--atomic-service-non-entry-size-limit <size>]
```

表15
参数含义及规范

1. HSP包文件路径，文件名必须以.hsp为后缀。如果是多个HSP包需要用英文“,”分隔。

2. HSP包文件目录路径，目录内要包含一个完整的HSP包的所有文件。允许传入多个路径，多个路径需要用英文“,”分隔。

pac.json
文件路径，文件名必须为pac.json。

从API version 20开始支持该参数。

#### 打包工具错误码

#### [h2]10010001 执行打包工具失败

错误信息

Execute packing tool failed.

错误描述

执行打包工具失败。

可能原因

- 打包文件合法性校验失败。
- 需要打包的文件正在被其他程序使用，例如压缩软件或文件管理器。
处理步骤

- 根据报错信息检查
app.json5
和
module.json5
中的配置项是否准确。当有多条报错信息时，优先根据第一条报错信息进行排查。
- 检查是否有程序（如压缩软件、文件管理器）占用打包文件，关闭相关进程后重试。
#### [h2]10010002 打包参数解析失败

错误信息

Command parser failed.

错误描述

打包参数解析失败。

可能原因

- 参数值格式不正确（如路径为空、文件类型不匹配、非法字符）。
- 必填参数缺失或传入空值。
处理步骤

查看报错日志中第一条错误码，确认具体错误信息。

#### [h2]10010003 --force参数值校验失败

错误信息

Command verify failed.

错误描述

--force参数值校验失败。

可能原因

- --force参数值不是布尔类型。
- 参数值不在取值范围内，仅支持取值为true或false。
- 参数值大小写或格式错误，如True、FALSE、1、yes等。
处理步骤

检查参数值，确保明确指定为true或false。

#### [h2]10011001 打包HAP时参数校验失败

错误信息

Parse and check args invalid in hap mode.

错误描述

打包HAP时参数校验失败。

可能原因

参数值格式不正确，如路径为空、文件类型不匹配、非法字符。

处理步骤

查看报错日志中第一条错误码，确认具体错误信息。

#### [h2]10011002 打包HSP时参数校验失败

错误信息

Parse and check args invalid in hsp mode.

错误描述

打包HSP时参数校验失败。

可能原因

参数值格式不正确（如路径为空、文件类型不匹配、非法字符）。

处理步骤

查看报错日志中第一条错误码，确认具体错误信息。

#### [h2]10011003 打包App时参数校验失败

错误信息

Parse and check args invalid in app mode.

错误描述

打包App时参数校验失败。

可能原因

参数值格式不正确（如路径为空、文件类型不匹配、非法字符）。

处理步骤

查看报错日志中第一条错误码，确认具体错误信息。

#### [h2]10011004 多工程打包时参数校验失败

错误信息

Parse and check args invalid in multiApp mode.

错误描述

多工程打包时参数校验失败。

可能原因

参数值格式不正确（如路径为空、文件类型不匹配、非法字符）。

处理步骤

查看报错日志中第一条错误码，确认具体错误信息。

#### [h2]10011005 res模式打包时参数校验失败

错误信息

Parse and check args invalid in res mode.

错误描述

res模式打包时参数校验失败。

可能原因

参数值格式不正确（如路径为空、文件类型不匹配、非法字符）。

处理步骤

查看报错日志中第一条错误码，确认具体错误信息。

#### [h2]10011006 打包HQF时参数校验失败

错误信息

Parse and check args invalid in hqf mode.

错误描述

打包HQF时参数校验失败。

可能原因

参数值格式不正确（如路径为空、文件类型不匹配、非法字符）。

处理步骤

查看报错日志中第一条错误码，确认具体错误信息。

#### [h2]10011007 打包APPQF时参数校验失败

错误信息

Parse and check args invalid in appqf mode.

错误描述

打包APPQF时参数校验失败。

可能原因

参数值格式不正确（如路径为空、文件类型不匹配、非法字符）。

处理步骤

查看报错日志中第一条错误码，确认具体错误信息。

#### [h2]10011008 包名归一化时参数校验失败

错误信息

Parse and check args invalid in packageNormalize mode.

错误描述

包名归一化时参数校验失败。

可能原因

参数值格式不正确（如路径为空、文件类型不匹配、非法字符）。

处理步骤

查看报错日志中第一条错误码，确认具体错误信息。

#### [h2]10011009 版本归一化时参数校验失败

错误信息

Parse and check args invalid in versionNormalize mode.

错误描述

版本归一化时参数校验失败。

可能原因

参数值格式不正确（如路径为空、文件类型不匹配、非法字符）。

处理步骤

查看报错日志中第一条错误码，确认具体错误信息。

#### [h2]10011011 --mode参数值校验失败

错误信息

Command verify mode is invalid.

错误描述

--mode参数值校验失败。

可能原因

- --mode参数值不是有效的打包模式。
- 参数值拼写错误或大小写不符合规范。
- 使用了当前工具版本尚未支持的打包模式。
处理步骤

- 检查--mode参数取值，确保使用打包资料中列举的合法打包模式。
- 核对参数拼写及大小写是否与文档保持一致。
- 确认所使用的打包工具版本是否支持该打包模式。
#### [h2]10011012 校验bundleType是否为shared时失败

错误信息

Check bundleType is shared failed.

错误描述

校验bundleType是否为shared时失败。

可能原因

解析--json-path指定的module.json文件失败。

处理步骤

- 检查--json-path指定的module.json文件，确保文件格式符合JSON格式规则。
- 查看报错日志中第一条错误码，确认具体错误信息。
#### [h2]10011016 检查HSP是否包含入口UIAbility失败

错误信息

Check hsp has entry ability failed.

错误描述

检查HSP是否包含入口UIAbility失败。

可能原因

解析--json-path指定的module.json文件失败。

处理步骤

- 检查--json-path指定的module.json文件，确保文件格式符合JSON格式规则。
- 查看报错日志中第一条错误码，确认具体错误信息。
#### [h2]10011017 检查HSP是否包含入口ExtensionAbility失败

错误信息

Check hsp has entry extensionAbility failed.

错误描述

检查HSP是否包含入口ExtensionAbility失败。

可能原因

解析--json-path指定的module.json文件失败。

处理步骤

- 检查--json-path指定的module.json文件，确保文件格式符合JSON格式规则。
- 查看报错日志中第一条错误码，确认具体错误信息。
#### [h2]10011018 检查--out-path参数失败

错误信息

Invalid output path.

错误描述

检查--out-path参数失败。

可能原因

- --force参数值为false，且--out-path指定的文件已存在。
- 当前为HAP打包模式，但--out-path指定的文件后缀不是.hap。
- 当前为HSP打包模式，但--out-path指定的文件后缀不是.hsp。
- 当前为app打包模式，但--out-path指定的文件后缀不是.app。
- 当前为res打包模式，但--out-path指定的文件后缀不是.res。
处理步骤

- 当--out-path指定的目标文件已存在时，请将--force参数设置为true以允许覆盖。
- 根据当前打包模式，确认--out-path指定的输出文件后缀正确。
#### [h2]10011020 版本归一化打包模式参数校验失败

错误信息

Handle hap and hsp input failed.

错误描述

版本归一化打包模式校验--input-list参数失败。

可能原因

--input-list参数指向的文件既不是HAP也不是HSP。

处理步骤

确认--input-list参数中列出的文件均为有效的.hap或.hsp包。

#### [h2]10011021 通用归一化打包模式参数校验失败

错误信息

Parse and check args invalid in generalNormalize mode.

错误描述

通用归一化打包模式参数校验失败。

可能原因

- 打包归一化后的pack.info文件失败。
- 通用归一化打包模式下的参数配置不正确。
处理步骤

查看报错日志中第一条错误码，确认具体错误信息。

#### [h2]10011022 检查元服务大小限制参数失败

错误信息

Parse atomicService size limit failed.

错误描述

检查元服务大小限制参数失败。

可能原因

- --atomic-service-entry-size-limit参数值不在[0, 4194304]范围内（单位KB）。
- --atomic-service-non-entry-size-limit参数值不在[0, 4194304]范围内（单位KB）。
处理步骤

- 确认--atomic-service-entry-size-limit参数值为[0, 4194304]范围内的整数（单位KB）。
- 确认--atomic-service-non-entry-size-limit参数值为[0, 4194304]范围内的整数（单位KB）。
#### [h2]10012001 执行压缩操作失败

错误信息

Execute compress process failed.

错误描述

执行打包操作时，例如打包HAP或App，执行压缩操作失败，导致打包中断。

可能原因

- 打包文件合法性校验失败。
- 需要打包的文件正在被其他程序使用，例如压缩软件或文件管理器。
处理步骤

- 根据报错信息检查
app.json5
和
module.json5
中的配置项是否准确。当有多条报错信息时，优先根据第一条报错信息进行排查。
- 检查是否有程序（如压缩软件、文件管理器）占用打包文件，关闭相关进程后重试。
#### [h2]10012002 HAP包压缩失败

错误信息

Compress Stage Hap failed.

错误描述

打包HAP时，执行压缩Stage模型的HAP包操作失败。

可能原因

- Stage模型HAP包打包文件合法性校验失败。
- 需要打包的文件正在被其他程序使用，例如压缩软件或文件管理器。
处理步骤

- 根据报错信息检查
app.json5
和
module.json5
中的配置项是否准确。当有多条报错信息时，优先根据第一条报错信息进行排查。
- 检查是否有程序（如压缩软件、文件管理器）占用打包文件，关闭相关进程后重试。
#### [h2]10012003 校验HAP信息失败

错误信息

Verify stage hap info failed.

错误描述

打包Stage模型HAP包时，配置信息校验失败。

可能原因

module.json5中atomicService或continueBundleName存在配置错误，或app.json5中asanEnabled或hwasanEnabled存在配置错误。

处理步骤

参考
asanEnabled配置错误码
、
hwasanEnabled配置错误码
、
atomicService配置错误码
、
continueBundleName配置错误码
，更改配置项。

#### [h2]10012004 检查参数asanEnabled失败

错误信息

Check asanEnabled failed.

错误描述

打包HAP或HSP时，app.json5中asanEnabled配置错误。

可能原因

asanEnabled和tsanEnabled被同时设置为true。

处理步骤

检查
app.json5
，修改asanEnabled和tsanEnabled，确保二者不会同时为true。

#### [h2]10012005 检查参数hwasanEnabled失败

错误信息

Check hwasanEnabled failed.

错误描述

打包HAP或HSP时，app.json5中hwasanEnabled配置错误。

可能原因

- hwasanEnabled和asanEnabled被同时配置为true。
- hwasanEnabled和tsanEnabled被同时配置为true。
- hwasanEnabled和GWPAsanEnabled被同时配置为true。
处理步骤

检查
app.json5
，确保asanEnabled、tsanEnabled、GWPAsanEnabled三项的中任一项与hwasanEnabled，不会同时配置为true。

#### [h2]10012006 检查atomicService失败

错误信息

Check atomicService failed.

错误描述

打包HAP或HSP时，atomicService配置检查失败。

可能原因

- module.json5中entry模块未配置ability，导致atomicService配置检查失败。
- 当app.json5中bundleType配置为atomicService时，但module.json5中installationFree为false。
处理步骤

- 检查
module.json5
，确保module.json5文件中正确配置了abilities标签，并且至少包含一个ability，详细请参见
abilities标签
。
- 检查module.json5和
app.json5
，当bundleType为atomicService时，确保installationFree配置为true，反之，需要配置为false。
#### [h2]10012007 检查continueBundleName无效

错误信息

Check continueBundleName invalid.

错误描述

打包HAP或HSP时，continueBundleName配置检查失败。

可能原因

module.json5中的continueBundleName与app.json5中bundleName相同。

处理步骤

修改continueBundleName，确保其与
app.json5
中的bundleName不同。

#### [h2]10012008 检查overlay失败

错误信息

Check whether is an overlay hsp failed.

错误描述

检查是否是overlay特性HSP包失败。

可能原因

- 在module.json5中同时配置了targetModuleName与requestPermissions。
在module.json5中同时配置了targetModuleName与requestPermissions。

- module.json5中的targetModuleName和module.json5中的name相同。
module.json5中的targetModuleName和module.json5中的name相同。

- 在module.json5中配置了targetPriority时，未配置targetModuleName。
在module.json5中配置了targetPriority时，未配置targetModuleName。

- 在app.json5中配置了targetBundleName时，module.json5中未配置targetModuleName。
在app.json5中配置了targetBundleName时，module.json5中未配置targetModuleName。

- 在app.json5中的targetBundleName与bundleName配置相同。
在app.json5中的targetBundleName与bundleName配置相同。

处理步骤

- 检查
module.json5
，确保targetModuleName和requestPermissions不会同时出现。
- 检查module.json5，确保targetModuleName和name不同。
- 检查module.json5，确保配置targetPriority时，同时配置了targetModuleName。
- 检查
app.json5
和module.json5，确保配置targetBundleName时，同时配置了targetModuleName。
- 检查app.json5，确保targetBundleName与bundleName不同。
#### [h2]10012009 执行压缩操作时异常

错误信息

Process compress exception.

错误描述

执行压缩HAP或HSP/App操作时存在异常。

可能原因

- 打包文件合法性校验失败。
- 需要打包的文件正在被其他程序使用，例如压缩软件或文件管理器。
处理步骤

- 根据报错信息检查
app.json5
和
module.json5
中的配置项是否准确。当有多条报错信息时，优先根据第一条报错信息进行排查。
- 检查是否有程序（如压缩软件、文件管理器）占用打包文件，关闭相关进程后重试。
#### [h2]10012010 校验模块generateBuildHash属性失败

错误信息

Verify has generate build hash failed.

错误描述

校验模块generateBuildHash属性失败。

可能原因

解析--json-path指定的module.json文件失败。

处理步骤

检查--json-path指定的module.json文件，确保文件格式符合JSON格式规则。

#### [h2]10012011 设置generateBuildHash属性失败

错误信息

Set generate build hash failed.

错误描述

设置generateBuildHash属性失败。

可能原因

- 解析--json-path指定的module.json文件失败。
- 在对module.json进行格式化或写入时发生I/O异常。
处理步骤

- 检查--json-path指定的module.json文件，确保文件格式符合JSON格式规则。
- 根据日志中“Error Message:”信息，定位具体的I/O或格式化异常原因。
#### [h2]10012012 检查应用的ubsanEnabled属性失败

错误信息

Check ubsanEnabled failed.

错误描述

检查应用的ubsanEnabled属性失败。

可能原因

- 在app.json5中同时将ubsanEnabled和asanEnabled设置为true。
- 在app.json5中同时将ubsanEnabled和tsanEnabled设置为true。
- 在app.json5中同时将ubsanEnabled和hwasanEnabled设置为true。
处理步骤

修改app.json5配置，确保ubsanEnabled不与asanEnabled、tsanEnabled或hwasanEnabled中的任一属性同时为true。

#### [h2]10012013 解析module.json文件失败

错误信息

Read Stage hap verify info exist exception.

错误描述

解析module.json文件失败。

可能原因

解析module.json时发生I/O异常。

处理步骤

根据日志中“Error Message:”信息，定位具体的I/O或格式化异常原因。

#### [h2]10012014 打包--lib-path指定目录失败

错误信息

Parallel compress exception.

错误描述

打包--lib-path指定目录失败。

可能原因

- 待压缩文件在压缩过程中被删除。
- 读取文件时发生I/O错误（坏盘、网络文件系统异常）。
- 文件路径过长、包含不支持的字符。
- 磁盘空间不足。
处理步骤

- 确认待压缩文件存在。
- 更换待压缩文件存储位置，重试打包。
- 检查并修改文件路径和文件名，重试打包。
- 清理磁盘，确认充足磁盘空间。
#### [h2]10012015 构建App包失败

错误信息

Compress app file failed.

错误描述

构建App包失败。

可能原因

- App打包文件合法性校验失败。
- 需要打包的文件正在被其他程序使用，例如压缩软件或文件管理器。
处理步骤

- 根据报错信息检查
app.json5
和
module.json5
中的配置项是否准确。当有多条报错信息时，优先根据第一条报错信息进行排查。
- 检查是否有程序（如压缩软件、文件管理器）占用打包文件，关闭相关进程后重试。
#### [h2]10012016 打包指定的HAP或HSP文件无效

错误信息

Check input hap or hsp file is invalid.

错误描述

打包指定的HAP或HSP文件无效。

可能原因

- 打包参数中指定的HAP或HSP文件名为空。
- 打包参数中HAP文件名后缀不是.hap或者HSP文件名后缀不是.hsp。
处理步骤

- 确认打包参数中HAP或HSP文件名不为空。
- 确认打包参数中HAP文件名后缀是.hap或者HSP文件名后缀是.hsp。
#### [h2]10012017 检查SharedAPP无效

错误信息

Check shared App mode invalid.

错误描述

构建
bundleType
为shared的App包时，检查HSP包无效。

可能原因

- 存在两个以上的
HSP包
。例如下图使用DevEco Studio构建App时，工程中包含了两个HSP包library和library1，此时打包APP包失败。
存在两个以上的
HSP包
。例如下图使用DevEco Studio构建App时，工程中包含了两个HSP包library和library1，此时打包APP包失败。

- HSP包在module.json5中配置了dependencies。
HSP包在module.json5中配置了dependencies。

处理步骤

- 检查打包文件，确保bundleType为shared的App包中，HSP包不超过一个。
- 检查打包文件，删除HSP包中
module.json5
配置的dependencies。
#### [h2]10012018 检查应用的Bundle类型无效

错误信息

Check bundleType is invalid.

错误描述

检查应用的Bundle类型无效。

可能原因

参与打包的HAP和HSP的bundleType不相同。

处理步骤

检查所有参与打包的HAP和HSP的app.json5配置文件，确认bundleType配置完全一致。

#### [h2]10012019 检查元服务包大小失败

错误信息

Check app atomicservice compress size failed.

错误描述

检查元服务包大小失败。

可能原因

- 解析元服务包时抛I/O异常。
- 元服务应用内没有HAP（module.json5文件中type字段值为entry或feature）和HSP（module.json5文件中type字段值为shared）包。
处理步骤

- 根据日志中“Error Message:”信息，定位具体的I/O或格式化异常原因。
- 检查元服务应用，确认包含HAP（module.json5文件中type字段值为entry或feature）和HSP（module.json5文件中type字段值为shared）包。
#### [h2]10012020 解析FA应用config.json文件失败

错误信息

Read FA hap verify info exist exception.

错误描述

解析FA应用config.json文件失败。

可能原因

解析FA应用的HAP或HSP包的config.json文件抛I/O异常。

处理步骤

根据日志中“Error Message:”信息，定位具体的I/O或格式化异常原因。

#### [h2]10012021 打包App时抛I/O异常

错误信息

IO exception when compress app.

错误描述

打包App时抛I/O异常。

可能原因

打包App时，应用的
pack.info
文件覆盖HAP或HSP包内pack.info文件时抛I/O异常。

处理步骤

根据日志中“Error Message:”信息，定位具体的I/O或格式化异常原因。

#### [h2]10012022 校验Stage HSP失败

错误信息

Verify stage hsp info failed.

错误描述

打包HSP时，校验Stage模型HSP包失败。

可能原因

- module.json5中的atomicService、continueBundleName存在配置错误，或app.json5中的asanEnabled、hwasanEnabled存在配置错误。
- overlay配置出错。
处理步骤

- 参考
asanEnabled配置错误码
、
hwasanEnabled配置错误码
、
atomicService配置错误码
、
continueBundleName配置错误码
，更改配置项。
- 参考
检查overlay失败
，更改配置项。
#### [h2]10012023 json文件格式化失败

错误信息

Json special process exist exception.

错误描述

json文件格式化失败。

可能原因

json文件格式化时抛异常。

处理步骤

根据日志中“Error Message:”信息，定位具体的I/O或格式化异常原因。

#### [h2]10012024 校验元服务大小失败

错误信息

Check atomicService size failed.

错误描述

打包App时，元服务包的大小超出了限制。

可能原因

元服务包及依赖的共享库或资源文件大小超出了限制。具体限制请参考
表5 App打包指令参数说明
中--atomic-service-entry-size-limit和--atomic-service-non-entry-size-limit参数描述。

处理步骤

优化并减少包的大小，例如删除不必要的资源、精简代码或减少依赖。

#### [h2]10012025 多工程打包失败

错误信息

Compress in app mode for multi project failed.

错误描述

多工程打包失败。

可能原因

- multiApp打包文件合法性校验失败。
- 需要打包的文件正在被其他程序使用，例如压缩软件或文件管理器。
处理步骤

- 根据报错信息检查
app.json5
和
module.json5
中的配置项是否准确。当有多条报错信息时，优先根据第一条报错信息进行排查。
- 检查是否有程序（如压缩软件、文件管理器）占用打包文件，关闭相关进程后重试。
#### [h2]10012028 打包--app-list参数失败

错误信息

Dispose app failed.

错误描述

处理app失败。

可能原因

多工程打包时，--app-list指定的app不包含pack.info文件。

处理步骤

确认--app-list指定的app包含pack.info文件。

#### [h2]10012029 APP/HAP/HSP不包含pack.info文件

错误信息

pack.info does not find in hap or app.

错误描述

多工程打包模式下，参与打包的APP/HAP/HSP不包含pack.info文件。

可能原因

多工程打包模式下，参与打包的APP/HAP/HSP包中缺失pack.info文件。

处理步骤

确认多工程打包模式下，所有参与打包的APP/HAP/HSP包均包含有效的pack.info文件。

#### [h2]10012034 解析moduleName失败

错误信息

Get module name from line string failed.

错误描述

res打包模式下，解析moduleName失败。

可能原因

res打包模式下，--pack-info-path指定的
pack.info
文件缺失moduleName标签或moduleName标签值为空。

处理步骤

确认--pack-info-path指定的pack.info文件包含moduleName标签且moduleName标签值不为空。

#### [h2]10012035 APPQF模式打包失败

错误信息

Compress in appqf mode failed.

错误描述

APPQF模式打包失败。

可能原因

APPQF打包模式下，校验--hqf-list参数失败。

处理步骤

查看报错日志中第一条错误码，确认具体错误信息。

#### [h2]10012037 HQF一致性校验失败

错误信息

Check hqf has same app fields failed.

错误描述

在APPQF打包模式下，打包工具对--hqf-list参数指定的多个HQF包进行一致性校验时失败。

可能原因

- APPQF打包模式下，--hqf-list指定的HQF集合中，存在两个及以上HQF的bundleName不相同。
- APPQF打包模式下，--hqf-list指定的HQF集合中，存在两个及以上HQF的versionCode不相同。
- APPQF打包模式下，--hqf-list指定的HQF集合中，存在两个及以上HQF的versionName不相同。
- APPQF打包模式下，--hqf-list指定的HQF集合中，存在两个及以上HQF的patchVersionCode不相同。
- APPQF打包模式下，--hqf-list指定的HQF集合中，存在两个及以上HQF的patchVersionName不相同。
处理步骤

- 确认--hqf-list指定的所有HQF的bundleName相同。
- 确认--hqf-list指定的所有HQF的versionCode相同。
- 确认--hqf-list指定的所有HQF的versionName相同。
- 确认--hqf-list指定的所有HQF的patchVersionCode相同。
- 确认--hqf-list指定的所有HQF的patchVersionName相同。
#### [h2]10012038 检查HQF的moduleName失败

错误信息

Check hqf module is invalid.

错误描述

在APPQF打包模式下，--hqf-list参数指定的多个HQF包的moduleName校验失败。

可能原因

APPQF打包模式下，--hqf-list指定的HQF集合中，存在两个HQF的moduleName相同且deviceTypes属性集合相交。

处理步骤

确认--hqf-list指定的所有HQF的moduleName不相同或deviceTypes属性集合不相交。

#### [h2]10012039 版本归一化模式打包失败

错误信息

Version normalize failed.

错误描述

版本归一化模式打包失败。

可能原因

- 版本归一化打包模式下，参与打包的HAP或HSP包同时存在module.json和config.json文件，导致冲突。
- 版本归一化打包模式下，参与打包的HAP或HSP包既不包含module.json也不包含config.json文件，缺失必要配置文件。
- 对pack.info、module.json或config.json文件解析失败，文件格式不合法或内容缺失。
处理步骤

- 确认参与打包的HAP或HSP包中仅包含module.json或者config.json中的一个。
- 查看报错日志中第一条错误码，确认具体错误信息。
#### [h2]10012040 校验模块的版本信息失败

错误信息

Verify module version failed.

错误描述

版本归一化打包模式下，校验模块的版本信息失败。

可能原因

版本归一化打包模式下，--version-code参数值小于--input-list参数中某个HAP或HSP包的versionCode值。

处理步骤

确认--version-code参数值大于等于--input-list参数中HAP或HSP包的versionCode值。

#### [h2]10012041 计算SHA-256值失败

错误信息

SHA-256 hash calculation failed.

错误描述

打包HAP或HSP时，计算SHA-256值失败。

可能原因

计算HAP或HSP包的SHA-256时抛I/O异常。

处理步骤

根据日志中“Error Message:”信息，定位具体的异常原因。

#### [h2]10012042 HAP或HSP包重复

错误信息

Select haps find duplicated hap.

错误描述

参与打包的HAP或HSP包中存在两个HAP包或两个HSP包文件名相同。

可能原因

多工程打包模式下，--app-list、--hap-list和--hsp-list参数值中存在两个HAP包或HSP包文件名相同。

处理步骤

确认--app-list、--hap-list和--hsp-list参数值中的HAP或HSP包文件名不相同。

#### [h2]10012046 解析config.json文件失败

错误信息

Parse and modify config.json failed.

错误描述

版本归一化模式或通用归一化模式下，解析config.json文件失败。

可能原因

- config.json文件不包含app标签。
- config.json文件中app标签下不包含version标签。
- config.json文件中app/version标签下不包含code标签。
- config.json文件中app/version标签下不包含name标签。
- config.json文件中module标签下不包含name标签。
处理步骤

- 检查config.json文件，确保包含app标签。
- 检查config.json文件，确保app标签下包含version标签。
- 检查config.json文件，确保app/version标签下包含code标签。
- 检查config.json文件，确保app/version标签下包含name标签。
- 检查config.json文件，确保module标签下包含name标签。
#### [h2]10012047 解析module.json文件失败

错误信息

Parse and modify module.json failed.

错误描述

版本归一化模式或通用归一化模式下，解析module.json文件失败。

可能原因

- module.json文件不包含app标签。
- module.json文件中app标签下不包含versionCode标签。
- module.json文件中app标签下不包含versionName标签。
- module.json文件中app标签下不包含bundleName标签。
- module.json文件中module标签下不包含name标签。
处理步骤

- 检查module.json文件，确保包含app标签。
- 检查module.json文件，确保app标签下包含versionCode标签。
- 检查module.json文件，确保app标签下包含versionName标签。
- 检查module.json文件，确保app标签下包含bundleName标签。
- 检查module.json文件，确保module标签下包含name标签。
#### [h2]10012050 检查插件宿主失败

错误信息

Check is plugin host failed.

错误描述

打包HSP时，检查插件宿主失败。

可能原因

--json-path指定的module.json文件中不包含module标签。

处理步骤

检查--json-path指定的module.json文件，确保包含module标签。

#### [h2]10012052 检查--pkg-context-path参数失败

错误信息

Check pkg context failed.

错误描述

打包HAP或HSP时，检查--pkg-context-path参数失败。

可能原因

- --pkg-context-path参数值为空。
- --pkg-context-path指定的不是pkgContextInfo.json文件。
处理步骤

- 确认--pkg-context-path参数值不为空。
- 确认--pkg-context-path指定的是pkgContextInfo.json文件。
#### [h2]10012053 检查插件属性失败

错误信息

Check app plugin failed.

错误描述

打包HSP时，检查插件属性失败。

可能原因

- --json-path指定的module.json文件不存在。
- --json-path指定的module.json文件不包含module标签。
- 检查--pkg-context-path参数失败。
- --json-path指定的module.json文件包含非embeddedUI类型的extensionAbilities。
- --json-path指定的module.json文件中bundleType是appPlugin时，module.json文件不包含
ohos.permission.kernel.SUPPORT_PLUGIN
权限。
处理步骤

- 确认--json-path指定的module.json文件存在。
- 确认--json-path指定的module.json文件包含module标签。
- 查看报错日志中第一条错误码，确认具体错误信息。
- 确认--json-path指定的module.json文件不包含非embeddedUI类型的extensionAbilities。
- 确认--json-path指定的module.json文件中bundleType是appPlugin时，module.json文件包含ohos.permission.kernel.SUPPORT_PLUGIN权限。
#### [h2]10012054 校验HAR去重属性失败

错误信息

Check deduplicateHar field failed.

错误描述

打包HSP/HAP时，校验
deduplicateHar
属性失败。

可能原因

HSP/HAP模块module.json文件中minAPIVersion小于21，且deduplicateHar的值为true。

处理步骤

打包HSP/HAP时，如果deduplicateHar的属性值为true时，则要求minAPIVersion大于等于21。

#### [h2]10013001 解析module.json或config.json文件异常

错误信息

Parse json object exception.

错误描述

解析module.json或config.json文件异常。

可能原因

json文本语法错误，例如括号未闭合、引号使用不当、非法转义字符等。

处理步骤

确认json文本语法正确。

#### [h2]10013002 解析module.json或config.json文件失败

错误信息

Parse json profile failed.

错误描述

解析json配置失败。

可能原因

- module.json或config.json文件不包含app标签。
- module.json或config.json文件不包含module标签。
- 解析module.json或config.json文件时抛异常。
处理步骤

- 检查module.json或config.json文件，确保包含app标签。
- 检查module.json或config.json文件，确保包含module标签。
- 检查module.json或config.json文件，确保文件格式符合json格式规则。
#### [h2]10013003 检查atomicService属性无效

错误信息

Check module atomicService invalid.

错误描述

检查atomicService属性无效。

可能原因

HAP或HSP的bundleType不是atomicService，但module.json中配置了atomicService标签。

处理步骤

HAP或HSP的bundleType不是atomicService，更改module.json中配置的atomicService标签。

#### [h2]10013004 解析module.json文件失败

错误信息

Failed to parse module.json for the Stage module.

错误描述

解析module.json文件失败。

可能原因

- module.json文件内不包含versionCode标签。
- module.json文件内不包含versionName标签。
- module.json文件内module标签内不包含name标签。
处理步骤

- 检查module.json文件，确保包含versionCode标签。
- 检查module.json文件，确保包含versionName标签。
- 检查module.json文件，确保module标签内包含name标签。
#### [h2]10013005 检查模块bundleType失败

错误信息

Failed to parse module.json and bundleType.

错误描述

检查模块bundleType失败。

可能原因

不符合配置要求，例如：

- 模块的
app.json5
配置文件中bundleType为app，但
module.json5
中的installationFree属性值为true。
- 模块的app.json5配置文件中bundleType为atomicService，但module.json5中的installationFree属性值为false。
- 模块的app.json5配置文件中bundleType为shared，但module.json5中的type属性值不是shared。
处理步骤

- 确保app.json5配置文件中bundleType为app时，module.json5中的installationFree属性值为false。
- 确保app.json5配置文件中bundleType为atomicService时，module.json5中的installationFree属性值为true。
- 确保app.json5配置文件中bundleType为shared时，module.json5中的type属性值也是shared。
- 当有多条报错信息时，优先根据第一条报错信息进行排查。
#### [h2]10013006 检查entry模块中的ability失败

错误信息

check entry module at least one ability failed.

错误描述

Entry类型包中没有ability。

可能原因

Entry类型包中不存在ability，该错误可能是由于module.json5未配置abilities或者abilities配置为空引起。

处理步骤

检查
module.json5
，确保Entry类型包abilities正确配置了ability。

#### [h2]10013007 检查installationFree错误

错误信息

Check module atomicService installationFree invalid.

错误描述

打包HAP或HSP时，检查atomicService和installationFree配置出错。

可能原因

- app.json5中的bundleType配置了无效值。
- 当bundleType为shared时，module.json5中installationFree未设置为false。
- 当installationFree为true时，bundleType未设置为atomicService。
处理步骤

- 检查
app.json5
，确保bundleType设置为app，atomicService，shared之一。
- 如果bundleType为shared，确保
module.json5
中的installationFree设置为false。
- 如果installationFree为true，确保bundleType设置为atomicService。
#### [h2]10013008 获取bundleName属性失败

错误信息

Get the bundleName from json file failed.

错误描述

获取bundleName属性失败。

可能原因

module.json文件内app标签内不包含bundleName属性。

处理步骤

检查module.json文件，确保app标签内包含bundleName属性。

#### [h2]10013009 解析proxyData属性失败

错误信息

Failed to parse module.json and proxyData object.

错误描述

解析proxyData属性失败。

可能原因

module.json文件中module标签下的proxyData标签中某个元素不包含uri标签。

处理步骤

检查module.json文件，确保module标签下的proxyData标签各元素包含uri标签。

#### [h2]10013010 检查bundleType一致性失败

错误信息

Failed to check the consistency of bundleType.

错误描述

检查bundleType一致性失败。

可能原因

- 各HAP模块的module.json文件中bundleType配置不一致。
- 各HSP模块的module.json文件中bundleType配置不一致。
处理步骤

- 检查各HAP模块的module.json文件，确保bundleType配置一致。
- 检查各HSP模块的module.json文件，确保bundleType配置一致。
#### [h2]10013011 解析patch.json中模块名失败

错误信息

Failed to parse patch module name from patch.json.

错误描述

解析patch.json中模块名失败。

可能原因

patch.json文件内module标签内不包含name属性。

处理步骤

检查patch.json文件，确保module标签内包含name属性。

#### [h2]10013012 获取FA模型模块的config.json文件失败

错误信息

Failed to parse FA hap verify info from config.json.

错误描述

获取FA模型模块的config.json文件失败。

可能原因

打包FA模型app时，有HAP/HSP不包含config.json文件。

处理步骤

打包FA模型app时，确保所有HAP/HSP包含config.json文件。

#### [h2]10013013 解析FA模型模块的config.json文件失败

错误信息

Failed to parse config.json for the FA module.

错误描述

解析FA模型模块的config.json文件失败。

可能原因

- config.json文件的app标签内不包含version标签。
- config.json文件的app标签内version标签不包含code标签。
- config.json文件的app标签内version标签不包含name标签。
- config.json文件的app标签内不包含apiVersion标签。
- config.json文件的module标签内不包含distro标签。
- config.json文件的module标签内distro标签不包含moduleName标签。
- config.json文件的module标签内不包含package标签。
处理步骤

- 检查config.json文件，确保app标签内包含version标签。
- 检查config.json文件，确保app标签内version标签包含code标签。
- 检查config.json文件，确保app标签内version标签包含name标签。
- 检查config.json文件，确保app标签内包含apiVersion标签。
- 检查config.json文件，确保module标签内包含distro标签。
- 检查config.json文件，确保module标签内distro标签包含moduleName标签。
- 检查config.json文件，确保module标签内包含package标签。
#### [h2]10013014 合并pack.info文件失败

错误信息

Merge two pack.info into one pack.info file failed.

错误描述

合并pack.info文件失败。

可能原因

- 校验pack.info文件失败。
- 合并pack.info文件抛异常。
处理步骤

- 查看报错日志中第一条错误码，确认具体错误信息。
- 根据日志中“Error Message:”确认异常信息。
#### [h2]10013015 校验pack.info文件失败

错误信息

Verify pack.info file failed.

错误描述

校验pack.info文件失败。

可能原因

- 参与合并的两个pack.info文件其中一个不包含summary标签。
- 参与合并的两个pack.info文件其中一个不包含app标签。
- 校验pack.info文件中app标签失败。
处理步骤

- 检查参与合并的两个pack.info文件，确认均包含summary标签。
- 检查参与合并的两个pack.info文件，确认均包含app标签。
- 查看报错日志中第一条错误码，确认具体错误信息。
#### [h2]10013016 合并pack.info文件时校验失败

错误信息

Verify app in pack.info failed.

错误描述

合并pack.info文件时校验失败。

可能原因

- 参与合并的两个pack.info文件的bundleName不一致。
- 参与合并的两个pack.info文件的bundleType不一致。
- 参与合并的两个pack.info文件其中一个app标签内不包含version标签。
- 参与合并的两个pack.info文件app标签内code标签值不一致。
处理步骤

- 检查参与合并的两个pack.info文件，确保bundleName一致。
- 检查参与合并的两个pack.info文件，确保bundleType一致。
- 检查参与合并的两个pack.info文件，确保app标签内包含version标签。
- 检查参与合并的两个pack.info文件，确保app标签内code标签值一致。
#### [h2]10013017 校验pack.info文件的bundleType失败

错误信息

Verify bundleType in pack.info file failed.

错误描述

校验pack.info文件的bundleType失败。

可能原因

参与合并的两个pack.info文件的bundleType不一致。

处理步骤

检查参与合并的两个pack.info文件，确保bundleType一致。

#### [h2]10013018 解析pack.info文件forms标签失败

错误信息

Parse forms name in pack.info file failed.

错误描述

解析pack.info文件forms标签对应的模块名失败。

可能原因

- pack.info文件不包含summary标签。
- pack.info文件中summary标签内不包含modules标签。
- pack.info文件中summary标签内modules标签中某个元素不包含distro标签。
- pack.info文件中summary/modules/distro标签不包含moduleName标签。
处理步骤

- 检查pack.info文件，确保包含summary标签。
- 检查pack.info文件，确保summary标签内包含modules标签。
- 检查pack.info文件，确保summary标签内modules标签中各元素均包含distro标签。
- 检查pack.info文件，确保summary/modules/distro标签包含moduleName标签。
#### [h2]10013019 合并pack.info文件失败

错误信息

Failed to merge pack.info objects.

错误描述

multiApp打包模式下，合并HAP或HSP包的pack.info文件失败。

可能原因

- 参与合并的两个pack.info文件其中一个不包含summary标签。
- 参与合并的两个pack.info文件其中一个summary标签内不包含modules标签。
- 参与合并的两个pack.info文件其中一个不包含packages标签。
处理步骤

- 检查参与合并的两个pack.info文件，确保均包含summary标签。
- 检查参与合并的两个pack.info文件，确保summary标签内包含modules标签。
- 检查参与合并的两个pack.info文件，确保均包含packages标签。
#### [h2]10013020 合并pack.info文件失败

错误信息

Failed to merge two pack.info files into one pack.info file by packagePair.

错误描述

multiApp打包模式下，合并app包的pack.info文件失败。

可能原因

- 校验pack.info文件失败。
- 合并pack.info文件抛异常。
处理步骤

- 查看报错日志中第一条错误码，确认具体错误信息。
- 根据日志中“Error Message:”确认异常信息。
#### [h2]10013022 解析pack.info文件的forms属性失败

错误信息

Failed to parse pack.info forms.

错误描述

解析pack.info文件的forms属性失败。

可能原因

- pack.info文件中forms标签内某元素不包含defaultDimension标签。
- pack.info文件中forms标签内某元素defaultDimension标签值包含多个*。
- pack.info文件中forms标签内存在一个或多个元素不包含supportDimensions标签。
处理步骤

- 检查pack.info文件，确保forms标签内各元素均包含defaultDimension标签。
- 检查pack.info文件，确保forms标签内各元素defaultDimension标签值均只包含1个*。
- 检查pack.info文件，确保forms标签各元素均包含supportDimensions标签。
#### [h2]10014001 未找到可用文件

错误信息

File available not found exception.

错误描述

使用打包工具打包时，需要打包的文件不可使用。

可能原因

- 指定的文件路径错误或文件不存在。
- 文件正在被其他程序使用，例如压缩软件或文件管理器。
- 当前用户没有访问该文件的权限。
处理步骤

- 确认提供的文件路径正确，并检查该文件是否存在。
- 检查是否有程序（如压缩软件、文件管理器）占用文件，关闭相关进程后重试。
- 检查并调整文件的访问权限，例如当前用户可以读取、修改、删除文件。
#### [h2]10014002 关闭.zip归档输出流异常

错误信息

Close zip output stream exception.

错误描述

关闭.zip归档输出流异常。

可能原因

- 磁盘I/O失败。
- 磁盘空间不足。
处理步骤

根据日志中“Error Message:”信息确认具体错误信息，下面列举可能原因对应的处理措施。

- 确保磁盘正常。
- 确保磁盘空间剩余配额充足。
#### [h2]10014003 关闭I/O输入流异常

错误信息

IO exception when closing stream.

错误描述

关闭I/O输入流异常。

可能原因

底层文件描述符异常失效。

处理步骤

- 根据日志中“Error Message:”确认异常信息。
- 检查系统日志，确保文件系统和磁盘正常。
#### [h2]10014004 获取文件内容失败

错误信息

Get file content failed.

错误描述

获取文件内容失败。

可能原因

文件I/O操作抛异常。

处理步骤

根据日志中“Error Message:”，确认异常信息。

#### [h2]10014005 文件不存在

错误信息

Parse file not exist.

错误描述

文件不存在。

可能原因

文件不存在。

处理步骤

根据日志中“Error Message:”信息，确保文件路径正确且文件存在。

#### [h2]10014006 获取文件大小失败

错误信息

Get file size failed.

错误描述

获取文件大小失败。

可能原因

- 文件不存在。
- 路径指向的不是文件。
处理步骤

根据日志中“Error Message:”信息确认文件路径，确保文件存在且是文件类型。

#### [h2]10014007 文件I/O异常

错误信息

File IO exception.

错误描述

文件I/O异常。

可能原因

- 文件不存在。
- 操作文件权限不足。
- 磁盘空间不足。
处理步骤

根据日志中“Error Message:”信息确认文件路径。

- 确保文件存在。
- 确保当前用户拥有操作文件权限。
- 确保磁盘空间剩余配额充足。
#### [h2]10014008 压缩文件异常

错误信息

Compress file exception.

错误描述

压缩文件异常。

可能原因

打包压缩文件时抛异常。

处理步骤

根据日志中“Error Message:”，确认异常信息。

检查系统日志，确保文件系统和磁盘正常。

#### [h2]10014009 删除文件失败

错误信息

File delete failed.

错误描述

删除文件失败。

可能原因

文件被其它进程占用。

处理步骤

根据日志中“Error Message:”信息确认文件路径。

确保文件当前不被其它进程占用，手动删除文件。

#### [h2]10015001 文件I/O异常

错误信息

IO exception.

错误描述

文件I/O异常。

可能原因

- 文件不存在。
- 操作文件权限不足。
- 磁盘空间不足。
- 系统内部错误。
处理步骤

根据日志中“Error Message:”信息确认文件路径。

- 确保文件存在。
- 确保当前用户拥有操作文件权限。
- 确保磁盘空间剩余配额充足。
- 查看相关错误信息确认具体异常原因。
#### [h2]10015002 空指针异常

错误信息

Null pointer exception.

错误描述

空指针异常。

可能原因

程序类对象未初始化。

处理步骤

根据日志中“Error Message:”，确认异常信息。

#### [h2]10016001 校验应用属性失败

错误信息

App fields is invalid.

错误描述

打包App时，校验应用属性失败。

可能原因

- 有两个HAP的minCompatibleVersionCode属性值不相同。
- 有两个HAP的targetAPIVersion属性值不相同。
- 有两个HAP的minAPIVersion属性值不相同。
- 有两个HAP的debug属性值不相同。
- HAP的minCompatibleVersionCode/targetAPIVersion/minAPIVersion属性值小于某HSP。
- HAP的debug属性值为false时，存在HSP的debug属性值为true。
处理步骤

根据日志中“Error Message:”信息，确认错误信息及存在问题的HAP或HSP名。

- 确保参与打包的HAP的minCompatibleVersionCode属性值相同。
- 确保参与打包的HAP的targetAPIVersion属性值相同。
- 确保参与打包的HAP的minAPIVersion属性值相同。
- 确保参与打包的HAP的debug属性值相同。
- 确保HAP的minCompatibleVersionCode/targetAPIVersion/minAPIVersion属性值大于等于所有HSP的对应属性值。
- 确保HAP的debug属性值为false时，所有HSP的debug属性值为false。
#### [h2]10016002 HAP或HSP属性不同

错误信息

Some app variable is different.

错误描述

打包App时，HAP或HSP属性不同。

可能原因

- 当前参与打包的HAP或HSP中，存在模块的bundleName与其他模块不一致。
- 当前参与打包的HAP或HSP中，存在模块的bundleType与其他模块不一致。
- 当前参与打包的HAP或HSP中，存在模块的versionCode与其他模块不一致。
- 当前参与打包的HAP或HSP中，存在模块的apiReleaseType（
app.json5
配置文件中的属性）与其他模块不一致。
- 当前参与打包的HAP或HSP中，存在模块的targetBundleName（app.json5配置文件中的属性）与其他模块不一致。
- 当前参与打包的HAP或HSP中，存在模块的targetPriority（app.json5配置文件中的属性）与其他模块不一致。
- 当前参与打包的HAP中，存在模块的multiAppMode（app.json5配置文件中的属性）与其他模块不一致。
处理步骤

- 确保当前参与打包的HAP或HSP的bundleName一致。
- 确保当前参与打包的HAP或HSP的bundleType一致。
- 确保当前参与打包的HAP或HSP的versionCode一致。
- 确保当前参与打包的HAP或HSP的apiReleaseType一致。
- 确保当前参与打包的HAP或HSP的targetBundleName一致。
- 确保当前参与打包的HAP或HSP的targetPriority一致。
- 确保当前参与打包的HAP的multiAppMode一致。
#### [h2]10016003 分发策略相交校验失败

错误信息

Check two distroFilter policy disjoint invalid.

错误描述

HAP唯一性校验
需要判断分发策略是否相交，由于分发策略配置错误，导致无法判断分发策略是否相交。

可能原因

分发策略policy、value标签为空或为无效值。

处理步骤

检查分发策略相关配置，确保policy的值为include或exclude，value取值参见
distributionFilter标签
。

#### [h2]10016004 校验模块名失败

错误信息

Check module name is invalid.

错误描述

打包app时校验模块名失败。

可能原因

- HAP或HSP的module.json文件module标签不包含name标签。
- 在参与打包的HAP或HSP中，存在两个或以上module.json文件，其中module/name标签值相同，并且module/deviceType属性值有交集，同时module/metadata/resource/distributionFilter属性值也有交集。
处理步骤

- 检查HAP或HSP的module.json文件，确保module标签包含name标签。
- 检查参与打包的HAP或HSP的module.json文件，确保module/name标签值不相同或者module/deviceType属性值集合不相交或者module/metadata/resource/distributionFilter属性值集合不相交。
#### [h2]10016005 校验应用包名失败

错误信息

Check packageName invalid.

错误描述

校验应用包名失败。

可能原因

在参与打包的HAP或HSP中，存在两个或以上module.json文件，其中module/package标签值相同，并且module/deviceType属性值有交集，同时module/metadata/resource/distributionFilter属性值也有交集。

处理步骤

根据日志中“Error Message:”信息，确认存在问题的HAP或HSP。

检查参与打包的HAP或HSP的module.json文件，确保module/package标签值不相同或者module/deviceType属性值集合不相交或者module/metadata/resource/distributionFilter属性值集合不相交。

#### [h2]10016006 检查HAP包无效

错误信息

Verify hap info is invalid.

错误描述

构建App包时，校验用于打包的HAP或HSP失败。

可能原因

多个HAP或HSP包配置之间存在冲突。

处理步骤

根据报错信息检查
app.json5
和
module.json5
中的配置项是否准确。当有多条报错信息时，优先根据第一条报错信息进行排查。

#### [h2]10016007 检查entry模块无效

错误信息

Check entry module invalid.

错误描述

构建App包时，当工程中存在多个Entry类型HAP包时，检查配置信息失败。

可能原因

不符合HAP唯一性校验规则。

处理步骤

参考
HAP唯一性校验
，调整工程中的Entry类型HAP配置。

#### [h2]10016008 检查dependency属性无效

错误信息

Check dependency is invalid.

错误描述

检查dependency属性无效。

可能原因

参与打包的HAP或HSP的module.json文件中module/installationFree属性值不一致。

处理步骤

检查参与打包的HAP或HSP的module.json文件，确保module/installationFree属性值一致。

#### [h2]10016009 检查依赖错误

错误信息

Check dependency list is invalid.

错误描述

构建App包时，模块依赖关系检查失败。

可能原因

- 模块间存在循环依赖，例如：模块library1的module.json5中dependencies配置了library2，同时模块library2中的dependencies配置了library1，则这两个模块之间构成循环依赖。
- module.json5配置中依赖的模块对应的module.json5中的type为entry或feature。
处理步骤

- 检查
module.json5
中的dependencies，删除循环依赖，确保App中不存在循环依赖。
- 检查module.json5中的dependencies的配置，删除对entry或feature类型模块的依赖。
#### [h2]10016010 检查元服务无效

错误信息

Check atomicservice is invalid.

错误描述

构建App包时，检查元服务无效。

可能原因

module.json5中preloads配置的moduleName错误。

处理步骤

检查
module.json5
中的
preloads属性
下的moduleName，不能配置为自身模块module.json5中的name，且moduleName对应的模块必须存在。

#### [h2]10016011 检查元服务预加载无效

错误信息

Atomicservice preloads is invalid.

错误描述

构建bundleType为atomicService类型的App包时，检查元服务包预加载的模块无效。

可能原因

- 元服务包module.json5中的preloads配置了重复的moduleName。
- 元服务包preloads配置的moduleName，和其他元服务包中module.json5中的name不匹配。
- 元服务包preloads配置的moduleName，和自身module.json5中的name相同。
处理步骤

检查
module.json5
中元服务
preloads属性
，确保没有配置重复的模块，配置所有的模块都存在且不能配置自身的模块名。

#### [h2]10016012 目标模块不存在

错误信息

TargetModuleName is not exist.

错误描述

构建App时，模块中配置了目标模块，但未找到该模块。

可能原因

module.json5中配置了targetModuleName，但和其他模块对应module.json5中的name均不同。

处理步骤

检查targetModuleName配置项，确保其正确配置（详细请参见
module.json5配置文件标签
及targetModuleName属性），必要时创建目标模块。

#### [h2]10016013 校验compileSdkType属性不一致

错误信息

CompileSdkType is different.

错误描述

校验compileSdkType属性不一致。

可能原因

参与打包的HAP或HSP的module.json文件中app/compileSdkType标签值不一致。

处理步骤

检查参与打包的HAP或HSP的module.json文件，确保app/compileSdkType标签值一致。

#### [h2]10016014 代理数据不唯一

错误信息

Proxy data uri is not unique.

错误描述

数据代理uri不唯一，存在重复项。

可能原因

module.json5中的proxyData配置的uri存在重复。

处理步骤

检查
module.json5
，删除proxyData中重复的uri，确保每个uri都是唯一的（详细请参见
proxyData标签
）。

#### [h2]10016015 ContinueType配置无效

错误信息

Check continueType is invalid.

错误描述

构建App时，检查continueType配置错误。

可能原因

- module.json5不同的ability存在重复的continueType配置项。
- 不同的module.json5中同时存在重复的deviceType配置项和continueType配置项。
处理步骤

检查
module.json5
，删除continueType或deviceType重复的配置项。

#### [h2]10016016 文件大小检查错误

错误信息

Check file size failed.

错误描述

构建元服务类型App时，单个包大小超过限制。

可能原因

单个包大小超过限制。具体限制请参考
表5 App打包指令参数说明
中--atomic-service-entry-size-limit和--atomic-service-non-entry-size-limit参数描述。

处理步骤

优化并减少对应单个包文件的大小，例如删除不必要的资源、精简代码或压缩文件。

#### [h2]10016017 HapVerifyInfos集合为空

错误信息

The provided list of HapVerifyInfos is empty.

错误描述

HapVerifyInfos集合为空。

可能原因

打包APP时，--hap-path和--hsp-path参数值均为空。

处理步骤

打包APP时，确保--hap-path和--hsp-path参数值不能均为空。

#### [h2]10016018 元服务模块大小检查错误

错误信息

Check the atomicService module size failed.

错误描述

构建元服务类型App时，单个包和其依赖的共享库大小超过限制。

可能原因

单个包和其依赖的共享库总大小超过限制。具体限制请参考
表5 App打包指令参数说明
中--atomic-service-entry-size-limit和--atomic-service-non-entry-size-limit参数描述。

处理步骤

优化并减少相应包的大小，例如删除不必要的资源、精简代码或减少依赖项。

#### [h2]10016019 检查分发策略无效

错误信息

Check the entry module distributionFilter is invalid.

错误描述

检查Entry类型模块分发策略错误。

可能原因

Entry类型模块分发策略配置存在错误。

处理步骤

检查Entry模块分发策略是否正确配置，例如policy的值应为exclude或include，详细请参考
distributionFilter标签
。

#### [h2]10017001 包名归一化模式校验HSP包的bundleName和versionCode属性失败

错误信息

Normalize HSP bundleName and versionCode failed.

错误描述

包名归一化模式校验HSP包的bundleName和versionCode属性失败。

可能原因

- HSP包的moduel.json文件不包含app标签。
- HSP包的pack.info文件不包含summary标签。
- HSP包的pack.info文件不包含summary/app标签。
- HSP包的pack.info文件不包含summary/version标签。
处理步骤

- 检查HSP包的moduel.json文件，确保包含app标签。
- 检查HSP包的pack.info文件，确保包含summary标签。
- 检查HSP包的pack.info文件，确保包含summary/app标签。
- 检查HSP包的pack.info文件，确保包含summary/version标签。
#### [h2]10017002 更新module.json文件失败

错误信息

Update module.json failed.

错误描述

更新module.json文件失败。

可能原因

module.json文件不包含app标签。

处理步骤

确保module.json文件包含app标签。

#### [h2]10017003 更新pack.info文件失败

错误信息

Update pack.info failed.

错误描述

更新pack.info文件失败。

可能原因

- pack.info文件不包含summary标签。
- pack.info文件不包含summary/app标签。
- pack.info文件不包含summary/version标签。
处理步骤

- 检查pack.info文件，确保包含summary标签。
- 检查pack.info文件，确保包含summary/app标签。
- 检查pack.info文件，确保包含summary/version标签。
#### [h2]10018001 fastApp模式打包校验失败

错误信息

Parse and check args invalid in fast app mode.

错误描述

fastApp模式打包校验失败。

可能原因

打包参数校验失败。

处理步骤

查看报错日志中第一条错误码，确认具体错误信息。

#### [h2]10018002 检查bundleType一致性失败

错误信息

Check bundleType consistency failed.

错误描述

fastApp模式打包检查bundleType一致性失败。

可能原因

- 参与打包的HAP包的bundleType属性值不一致。
- 参与打包的HSP包的bundleType属性值不一致。
处理步骤

- 检查参与打包的HAP包，确保bundleType属性值一致。
- 检查参与打包的HSP包，确保bundleType属性值一致。
#### [h2]10018003 检查pack.info文件无效

错误信息

Pack.info is invalid.

错误描述

fastApp模式打包检查pack.info文件无效。

可能原因

- --pack-info-path参数指向的pack.info文件的packages标签中有两个元素的name标签值相同。
- --pack-info-path参数指向的pack.info文件不包含packages标签或packages标签内容为空。
- --hap-path参数指向的HAP包的pack.info文件的packages标签中元素个数大于1。
- --pack-info-path参数指向的pack.info文件的packages标签不包含--hap-path参数指向的HAP包。
- --hap-path参数指向的HAP包中存在两个或以上HAP包的pack.info文件的packages/name标签值相同。
- --hsp-path参数指向的HSP包的pack.info文件的packages标签中元素个数大于1。
- --pack-info-path参数指向的pack.info文件的packages标签不包含--hsp-path参数指向的HSP包。
- --hsp-path参数指向的HSP包中存在两个或以上HSP包的pack.info文件的packages/name标签值相同。
处理步骤

根据日志中“Error Message:”信息，确认存在问题文件的路径。

- 检查--pack-info-path参数指向的pack.info文件。确保packages标签中各元素的name标签值均不相同。
- 检查--pack-info-path参数指向的pack.info文件，确保包含packages标签并且packages标签内容不为空。
- 检查--hap-path参数指向的HAP包的pack.info文件，确保packages标签中仅存在1个元素内容。
- 检查--pack-info-path参数指向的pack.info文件，确保packages标签包含--hap-path参数指向的HAP包。
- 检查--hap-path参数指向的HAP包中每个pack.info文件，确保packages/name的标签值唯一。
- 检查--hsp-path参数指向的HSP包的pack.info文件，确保packages标签中仅存在1个元素内容。
- 检查--pack-info-path参数指向的pack.info文件，确保packages标签包含--hsp-path参数指向的HSP包。
- 检查--hsp-path参数指向的HSP包中每个pack.info文件，确保packages/name的标签值唯一。
#### [h2]10018004 向压缩包中添加文件或目录条目失败

错误信息

Add archive entry failed.

错误描述

向压缩包中添加文件或目录条目失败。

可能原因

待打包文件夹为空。

处理步骤

仅作告警提示，无需处理。

根据“Error Message:”信息获取待打包空文件目录，确认该空文件符合打包预期。

#### [h2]10018005 打包libs目录异常

错误信息

Packing with multiple threads exception.

错误描述

打包libs目录异常。

可能原因

打包libs目录异常。

处理步骤

根据日志中“Error Message:”，确认异常信息。

#### [h2]10018006 fastApp模式重打包HSP异常

错误信息

Repack hsp exception.

错误描述

fastApp模式重打包HSP异常。

可能原因

重打包HSP异常。

处理步骤

根据日志中“Error Message:”，确认异常信息。

#### [h2]10019001 增量打包HAP异常

错误信息

Incremental pack hap exception.

错误描述

增量打包HAP异常。

可能原因

增量打包HAP时抛I/O异常。

处理步骤

根据日志中“Error Message:”，确认异常信息。

#### [h2]10019002 增量打包HSP异常

错误信息

Incremental pack hsp exception.

错误描述

增量打包HSP异常。

可能原因

增量打包HSP时抛I/O异常。

处理步骤

根据日志中“Error Message:”，确认异常信息。

#### [h2]10011021 通用归一化命令失败

错误信息

Parse and check args invalid in generalNormalize mode.

错误描述

通用归一化命令失败。

可能原因

- 传入的参数类型错误。
- 传入参数范围错误。
- 传入HAP或HSP包不完整，缺少json文件（json文件配置请参考Stage模型
module.json5
/FA模型
config.json
）。
处理步骤

检查并传入正确的命令参数和有效的包文件。

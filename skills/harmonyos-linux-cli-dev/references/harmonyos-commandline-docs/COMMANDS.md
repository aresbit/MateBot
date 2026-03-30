# HarmonyOS Linux CLI 命令清单

来源：`ide-commandline-get` 入口页递归抓取子页面后自动提取。

## hdc

- `hdc shell "aa start -A ohos.want.action.viewData -U 'https://www.example.com'"`
- `hdc shell "aa process -b com.example.myapplication -a EntryAbility -p perf-cmd"`
- `hdc shell bm dump -a`
- `hdc shell bm dump -n 包名`
- `hdc file recv /data/log/hilog/`
- `hdc shell param get const.ohos.apiversion`
- `hdc install不能安装release签名的企业应用。`
- `hdc shell bm install -p /data/hap名.hap`
- `hdc shell`
- `hdc file recv /data/log/faultlog/faultlogger/`
- `hdc（HarmonyOS Device Connector）是提供给开发人员的命令行调试工具，用于与设备进行交互调试、数据传输、日志查看以及应用安装等操作。该工具支持在Windows/Linux/MacOS系统上运行，为开发者提供高效，便捷的设备调试能力。`
- `hdc -t connect-key shell echo "Hello world"`
- `hdc list targets`
- `hdc wait`
- `hdc tmode usb`
- `hdc tmode port`
- `hdc tmode port close`
- `hdc tconn`
- `hdc install`
- `hdc uninstall`
- `hdc file send`
- `hdc file recv`
- `hdc fport`
- `hdc rport`
- `hdc start`
- `hdc kill`
- `hdc hilog`
- `hdc jpid`
- `hdc track-jpid`
- `hdc target boot`
- `hdc keygen`
- `hdc version`
- `hdc checkserver`
- `hdc bugreport`
- `hdc shell echo "Hello world"`
- `hdc -h [verbose]`
- `hdc help`
- `hdc list targets [-v]`
- `hdc -t [connect-key] [command]`
- `hdc wait # 等待设备正常连接。`
- `hdc -t [connect-key] wait # 等待指定的设备正常连接，connect-key需要替换为指定的设备标识符。`
- `hdc wait命令执行后，识别到正常连接的设备后结束。`
- `hdc tconn IP:port`
- `hdc -s [IP:]port [command]`
- `hdc tmode port [port-number]`
- `hdc tconn IP:port [-remove]`
- `hdc shell [-b bundlename] [command]`
- `hdc install [-cwd path|-r|-s|-w waitingTime|-u userId|-p|-h] src`
- `hdc uninstall [-n|-k|-s|-h] bundlename`
- `hdc file send [-a|-sync|-z|-m|-cwd path|-b bundlename] SOURCE DEST`
- `hdc file recv [-a|-sync|-z|-m|-cwd path|-b bundlename] DEST SOURCE`
- `hdc fport ls`
- `hdc fport localnode remotenode`
- `hdc rport remotenode localnode`
- `hdc fport rm taskstr`
- `hdc start [-r]`
- `hdc start -r # 服务进程启动状态下，触发服务进程重新启动。`
- `hdc kill [-r]`
- `hdc -p [command]`
- `hdc -m`
- `hdc hilog [-h]`
- `hdc track-jpid [-a|-p]`
- `hdc target boot [-bootloader|-recovery]`
- `hdc target boot [MODE]`
- `hdc target boot -bootloader  # 重启后进入fastboot模式。`
- `hdc target boot -recovery    # 重启后进入recovery模式。`
- `hdc target boot shutdown     # 关机。`
- `hdc keygen FILE`
- `hdc -v`
- `hdc（SDK）客户端进程版本信息。`
- `hdc（SDK）服务进程版本信息。`
- `hdc bugreport [FILE]`
- `hdc -l [level] [command]`
- `hdc -l 5 start`
- `hdc.log`
- `hdc-%Y%m%d-%H%M%S.log`
- `hdc-%Y%m%d-%H%M%S.log.tgz`
- `hdc shell hilog -w start                              # 开启hilog日志落盘(已开启hilog日志工具再次执行会报错)。`
- `hdc shell hilog -w stop                               # 关闭hilog日志落盘(已关闭hilog日志工具再次执行会报错)。`
- `hdc shell ls /data/log/hilog                          # 查看已落盘hilog日志。`
- `hdc file recv /data/log/hilog {local_path}            # 获取hilog已落盘日志（包含内核日志，local_path为本地路径，不同系统有所区别，这里未列举实际示例）。`
- `hdc tmode usb命令已废弃，参见`
- `hdc tmode命令有误。`
- `hdc tmode命令缺少参数或参数有误。`
- `hdc shell "bm dump -a | grep com.example.myapplication"`
- `hdc shell "bm dump -n com.example.myapplication | grep appProvisionType"`
- `hdc shell "mount |grep com.example.myapplication"`
- `hdc shell aa start -b com.example.myapplication -a EntryAbility`
- `hdc shell xxx，设备端命令不支持。`
- `hdc file send/recv 命令带-b选项时，SDK中的hdc或设备系统版本不支持该选项。`
- `hdc file recv /data/log/hilog/ .\%Dir%\`
- `hdc file recv /data/log/hilog/ ./$Dir/`
- `hdc shell hilog -d /system/bin/hilogTest`
- `hdc shell ls -l DEST`
- `hdc file recv DEST SOURCE`
- `hdc file send SOURCE DEST`
- `hdc shell rm DEST`

## aa

- `aa help`
- `aa start [-d <deviceId>] [-a <abilityName> -b <bundleName>] [-m <moduleName>] [-c] [-E] [-D] [-R] [-S] [-W] [--pi <key> <unsigned integer-value>] [--pb <key> <bool-value: true/false/t/f大小写不敏感] [--ps <key> <value>] [--psn <key>] [--wl <windowLeft>] [--wt <windowTop>] [--wh <windowHeight>] [--ww <windowWidth>] [-p <perf-cmd>]`
- `aa start [-d <deviceId>] [-U <URI>] [-t <type>] [-A <action>] [-e <entity>] [-c] [-D] [-E] [-R] [--pi <key> <unsigned integer-value>] [--pb <key> <bool-value: true/false/t/f大小写不敏感] [--ps <key> <value>] [--psn <key>] [--wl <windowLeft>] [--wt <windowTop>] [--wh <windowHeight>] [--ww <windowWidth>] [-p <perf-cmd>]`
- `aa start -U myscheme://www.test.com:8080/path`
- `aa start -U myscheme://www.test.com:8080/path --pi paramNumber 1 --pb paramBoolean true --ps paramString teststring  --psn paramNullString`
- `aa start -A ohos.want.action.viewData -U https://www.example.com`
- `aa stop-service [-d <deviceId>] -a <abilityName> -b <bundleName> [-m <moduleName>]`
- `aa stop-service -a EntryAbility -b com.example.myapplication -m entry`
- `aa dump -a`
- `aa dump命令从API version 7开始支持，从API version 9废弃，替换命令为`
- `aa dump -l`
- `aa dump -i 105`
- `aa force-stop <bundle-name> [-p pid] [-r kill-reason]`
- `aa force-stop com.example.myapplication`
- `aa test -b <bundleName> [-m <module-name>] [-p <package-name>] [-s class <test-class>] [-s level <test-level>] [-s size <test-size>] [-s testType <test-testType>] [-s timeout <test-timeout>] [-s <any-key> <any-value>] [-w <wait-time>] -s unittest <testRunner>`
- `aa test -b com.example.myapplication -s unittest ActsAbilityTest`
- `aa test -b com.example.myapplication -m entry_test -s unittest ActsAbilityTest`
- `aa test -b com.example.myapplication -m entry_test -s timeout 10000 -s unittest ActsAbilityTest`
- `aa attach -b <bundleName>`
- `aa attach -b com.example.myapplication`
- `aa detach -b <bundleName>`
- `aa detach -b com.example.myapplication`
- `aa appdebug -b <bundleName> [-p]`
- `aa appdebug -h`
- `aa appdebug -b com.example.myapplication [-p]`
- `aa appdebug -c`
- `aa appdebug -g`
- `aa process -b <bundleName> -a <abilityName> [-m <moduleName>] [-D <debug-cmd>] [-S]`
- `aa process -b <bundleName> -a <abilityName> [-m <moduleName>] [-p <perf-cmd>] [-S]`
- `aa process -b com.example.myapplication -a EntryAbility -D debug_cmd [-S]`
- `aa process -b com.example.myapplication -a EntryAbility -p perf-cmd [-S]`
- `aa send-memory-level -p <processId> -l <memoryLevel>`
- `aa send-memory-level -p 6066 -l 0`
- `aa start命令的参数wl、wt、wh、ww或aa test命令不支持release签名的应用程序。`
- `aa start命令不支持启动UIExtensionAbility。`
- `aa start命令的参数中携带的AppCloneIndex是一个无效值，则返回该错误码。`
- `aa stop命令停止ServiceAbility时，-a的参数abilityName对应的Ability不是Service类型。`
- `aa force-stop命令指定的bundleName是常驻进程。`
- `aa attach/detach命令指定的包名不存在。`
- `aa`

## bm

- `bm help`
- `bm install [-h] [-p filePath] [-r] [-w waitingTime] [-s hspDirPath] [-u userId]`
- `bm install -p /data/local/tmp/ohos.app.hap`
- `bm install -p /data/local/tmp/ohos.app.hap -u 100`
- `bm install -p /data/local/tmp/ohos.app.hap -r`
- `bm install -s xxx.hsp`
- `bm install -p aaa.hap -s xxx.hsp yyy.hsp`
- `bm install -p /data/local/tmp/hapPath/`
- `bm install -p /data/local/tmp/ohos.app.hap -w 180`
- `bm uninstall [-h] [-n bundleName] [-m moduleName] [-k] [-s] [-v versionCode] [-u userId]`
- `bm uninstall -n com.ohos.app`
- `bm uninstall -n com.ohos.app -u 100`
- `bm uninstall -n com.ohos.app -m entry`
- `bm uninstall -n com.ohos.example -s`
- `bm uninstall -n com.ohos.example -s -v 100001`
- `bm uninstall -n com.ohos.app -k`
- `bm dump [-h] [-a] [-g] [-n bundleName] [-s shortcutInfo] [-d deviceId] [-l label] [-u userId]`
- `bm dump -a`
- `bm dump -g`
- `bm dump -n com.ohos.app`
- `bm dump -n com.ohos.app -u 100`
- `bm dump -s -n com.ohos.app`
- `bm dump -n com.ohos.app -d xxxxx`
- `bm dump -n com.ohos.app -l`
- `bm dump -a -l`
- `bm clean [-h] [-c] [-n bundleName] [-d] [-i appIndex] [-u userId]`
- `bm clean -c -n com.ohos.app`
- `bm clean -c -n com.ohos.app -u 100`
- `bm clean -d -n com.ohos.app`
- `bm get [-h] [-u]`
- `bm get -u`
- `bm quickfix [-h] [-a -f filePath [-t targetPath] [-d] [-o]] [-q -b bundleName] [-r -b bundleName]`
- `bm quickfix -q -b com.ohos.app`
- `bm quickfix -a -f /data/app/`
- `bm quickfix -r -b com.ohos.app`
- `bm dump-shared [-h] [-a] [-n bundleName]`
- `bm dump-shared -a`
- `bm dump-shared -n com.ohos.lib`
- `bm dump-dependencies [-h] [-n bundleName] [-m moduleName]`
- `bm dump-dependencies -n com.ohos.app -m entry`
- `bm compile [-h] [-m mode] [-r bundleName] [-a]`
- `bm compile -m partial com.example.myapplication`
- `bm copy-ap [-h] [-a] [-n bundleName]`
- `bm copy-ap -n com.example.myapplication`
- `bm dump-overlay [-h] [-b bundleName] [-m moduleName] [-t targetModuleName] [-u userId]`
- `bm dump-overlay -b com.ohos.app`
- `bm dump-overlay -b com.ohos.app -u 100`
- `bm dump-overlay -b com.ohos.app -m libraryModuleName`
- `bm dump-overlay -b com.ohos.app -t entryModuleName`
- `bm dump-target-overlay [-h] [-b bundleName] [-m moduleName] [-u userId]`
- `bm dump-target-overlay -b com.ohos.app`
- `bm dump-target-overlay -b com.ohos.app -u 100`
- `bm dump-target-overlay -b com.ohos.app -m entry`
- `bm install-plugin [-h] [-n hostBundleName] [-p filePath]`
- `bm install-plugin -n com.ohos.app -p /data/plugin.hsp`
- `bm uninstall-plugin [-h] [-n hostBundleName] [-p pluginBundleName]`
- `bm uninstall-plugin -n com.ohos.app -p com.ohos.plugin`
- `bm install -p`
- `bm install`
- `bm install-plugin`
- `bm dump -n`
- `bm dump -n 命令`
- `bm`

## hilog

- `hilog.info(0x0000, 'testTag', '%{public}s', 'Ability onCreate');`
- `hilog -w start`
- `hilog [-h]`
- `hilog.isLoggable(0xFF00, "testTag", hilog.LogLevel.INFO);`
- `hilog.info(0xFF00, "testTag", "%{public}s World %{public}d", "hello", 3);`
- `hilog.info(0xFF00, "testTag", "peter is %{public}o", peter);`
- `hilog.setMinLogLevel(hilog.LogLevel.WARN);`
- `hilog.info(0x0000, 'testTag', 'this is an info level log');`
- `hilog.error(0x0000, 'testTag', 'this is an error level log');`
- `hilog.setLogLevel(hilog.LogLevel.INFO, hilog.PreferStrategy.PREFER_OPEN_LOG);`
- `hilog.info(0x0000, 'testTag', 'this is an another info level log');`
- `hilog.error(0x0000, 'testTag', 'this is an another error level log');`
- `hilog -h`
- `hilog -x`
- `hilog -L D/I/W/E/F`
- `hilog -t app`
- `hilog -D 01B06`
- `hilog -T tag`
- `hilog -a 8`
- `hilog -z 8`
- `hilog -P pid`
- `hilog -e start`
- `hilog -v time/color/epoch/monotonic/usec/nsec/year/zone/wrap`
- `hilog -w query`
- `hilog -b D/I/W/E/F`
- `hilog -b D/I/W/E/F --persist`
- `hilog -b D/I/W/E/F -D 0x[DOMAINID]`
- `hilog -b D/I/W/E/F -D d0[DOMAINID]`
- `hilog -b D/I/W/E/F -T [TAG]`
- `hilog -g`
- `hilog -G size`
- `hilog -r`
- `hilog -k on/off`
- `hilog -s`
- `hilog -S`
- `hilog -Q pidon/pidoff`
- `hilog -Q domainon/domainoff`
- `hilog -G 16M`
- `hilog -b X`
- `hilog -b I -D 0x3200（将03200 domain能够打印出来的日志级别设为INFO）`
- `hilog -b I -D 0x3201（将03201 domain能够打印出来的日志级别设为INFO）`
- `hilog -b I -D d003200（将03200 domain能够打印出来的日志级别设为INFO）`
- `hilog -b I -D d003201（将03201 domain能够打印出来的日志级别设为INFO）`

## param

- `param get persist.bms.supportIsolationMode`
- `param set persist.bms.supportIsolationMode [true|false]`
- `param get const.product.cpu.abilist`
- `param`
- `param -h`
- `param ls [-r] [name]`
- `param get [name]`
- `param set name value`
- `param wait name [value] [timeout]`
- `param save`

## atm

- `atm help`
- `atm dump [-h] [-t [-i <token-id>] [-b <bundle-name>] [-n <process-name>]] [-v [-i <token-id>] [-p <permission-name>]]`
- `atm dump -d`
- `atm dump -d -p *********`
- `atm dump -h`
- `atm dump -t`
- `atm dump -t -i *********`
- `atm dump -t -b ohos.telephony.resources`
- `atm dump -t -n *********`
- `atm`

## anm

- `anm help`
- `anm dump [<options>]`
- `anm dump -A`
- `anm setting [<options>]`
- `anm setting -k <deviceType>:<status>`
- `anm setting -b <deviceType>:<bundleName>:<uid>:<status>`
- `anm setting -o <deviceType>:<slotType>:<status>`
- `anm setting -c 100`
- `anm setting -k wearable:1`
- `anm setting -b litewearable:example:10100:0`
- `anm setting -o headset:0:1`
- `anm`

## cem

- `cem help`
- `cem publish [<options>]`
- `cem publish --event "testevent"`
- `cem publish -e "testevent" -o -c 100 -d "this is data"`
- `cem dump [<options>]`
- `cem dump -e "testevent"`
- `cem`

## edm

- `edm help`
- `edm enable-admin -h`
- `edm enable-admin -n <bundleName> -a <abilityName> [-t <adminType>]`
- `edm enable-admin -n com.example.mdmsample -a com.example.mdmsample.EnterpriseAdminAbility`
- `edm disable-admin -h`
- `edm disable-admin -n <bundleName>`
- `edm disable-admin -n com.example.mdmsample`
- `edm`

## devicedebug

- `devicedebug help`
- `devicedebug kill`
- `devicedebug kill -9 12111`
- `devicedebug`

## mediatool

- `mediatool`
- `mediatool send <path-to-local-media-file> [-ts] [-tas] [-rf] [-urf]`
- `mediatool list <resource-uri>`
- `mediatool recv <media-target> <dest-path>`
- `mediatool delete <resource-uri>`
- `mediatool query <display-name> [-p] [-u]`
- `mediatool ls -l <media-path>`

## packing

- `java -jar app_packing_tool.jar --mode hap --json-path <path> [--resources-path <path>] [--ets-path <path>] [--index-path <path>] [--pack-info-path <path>] [--lib-path <path>] --out-path <path> [--force true] [--compress-level 5] [--pkg-context-path <path>] [--hnp-path <path>]`
- `java -jar app_packing_tool.jar --mode hap --json-path <path> [--maple-so-path <path>] [--profile-path <path>] [--maple-so-dir <path>] [--dex-path <path>] [--lib-path <path>] [--resources-path <path>] [--index-path <path>] --out-path <path> [--force true] [--compress-level 5]`
- `java -jar app_packing_tool.jar --mode hsp --json-path <path> [--resources-path <path>] [--ets-path <path>] [--index-path <path>] [--pack-info-path <path>] [--lib-path <path>] --out-path <path> [--force true] [--compress-level 5] [--pkg-context-path <path>]`
- `java -jar app_packing_tool.jar --mode app [--hap-path <path>] [--hsp-path <path>] --out-path <path> [--signature-path <path>] [--certificate-path <path>] --pack-info-path <path> [--pack-res-path <path>] [--force true] [--encrypt-path <path>] [--pac-json-path <path>] [--atomic-service-entry-size-limit <size>] [--atomic-service-non-entry-size-limit <size>] [--replace-pack-info false]`
- `java -jar app_packing_tool.jar --mode multiApp [--hap-list <path>] [--hsp-list <path>] [--app-list <path>] --out-path <option> [--force true] [--encrypt-path <path>] [--pac-json-path <path>] [--atomic-service-entry-size-limit <size>] [--atomic-service-non-entry-size-limit <size>]`
- `java -jar app_packing_tool.jar --mode hqf --json-path <path> [--lib-path <path>] [--ets-path <path>] [--resources-path <path>] --out-path <path> [--force true]`
- `java -jar app_packing_tool.jar --mode appqf --hqf-list <path> --out-path <path> [--force true]`
- `java -jar app_packing_tool.jar --mode versionNormalize --input-list 1.hap,2.hsp --version-code 1000001 --version-name 1.0.1 --out-path out`
- `java -jar app_packing_tool.jar --mode packageNormalize --hsp-list 1.hsp,2.hsp --bundle-name com.example.myapplication --version-code 1000001 --out-path out`
- `java -jar app_packing_tool.jar --mode generalNormalize --input-list 1.hsp,2.hsp --bundle-name com.example.myapplication --version-code 1000001 --version-name 1.0.1 --min-compatible-version-code 14 --min-api-version 14 --target-api-version 14 --api-release-type Release1 --bundle-type app --installation-free false --delivery-with-install true --device-types default,tablet --out-path out`
- `java -jar app_packing_tool.jar --mode res --entrycard-path <path> --pack-info-path <path> --out-path <path> [--force true]`
- `java -jar app_packing_tool.jar --mode fastApp [--hap-path <path>] [--hsp-path <path>] --out-path <path> [--signature-path <path>] [--certificate-path <path>] --pack-info-path <path> [--pack-res-path <path>] [--force true] [--encrypt-path <path>] [--pac-json-path <path>] [--atomic-service-entry-size-limit <size>] [--atomic-service-non-entry-size-limit <size>]`

## unpacking

- `java -jar app_unpacking_tool.jar --mode hap --hap-path <path> --out-path <path> [--force true]`
- `java -jar app_unpacking_tool.jar --mode app --app-path <path> --out-path <path> [--force true]`
- `java -jar app_unpacking_tool.jar --mode hap --rpcid true --hap-path <path> --out-path <path> [--force true]`
- `java -jar app_unpacking_tool.jar --mode hap --hap-path <path> --out-path <path> [--force true] [--libs true] [--cpu-abis option]`
- `java -jar app_unpacking_tool.jar --mode hsp --hsp-path <path> --out-path <path> [--force true]`
- `java -jar app_unpacking_tool.jar --mode hsp --hsp-path <path> --out-path <path> [--force true] [--libs true] [--cpu-abis option]`
- `java -jar app_unpacking_tool.jar --mode appqf --appqf-path <path> --out-path <path> [--force true]`

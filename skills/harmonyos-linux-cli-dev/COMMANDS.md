# HarmonyOS Linux CLI 命令全集（开发应用）

来源：`https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-commandline-get` 入口页递归子页面（抓取时间：2026-03-30）。

## 0) 获取与环境
- `echo $SHELL`
- `vi ~/.bash_profile`
- `vi ~/.zshrc`
- `export PATH=${COMMAND_LINE_TOOLS}/command-line-tools/bin:$PATH`
- `source ~/.bash_profile`
- `source ~/.zshrc`
- `codelinter -v`

## 1) hdc（HarmonyOS Device Connector）

### 全局参数
- `hdc -t <connect-key> <command>`
- `hdc -l <0-6> <command>`
- `hdc -s [IP:]port <command>`
- `hdc -p <command>`
- `hdc -m`
- `hdc -e <listen-ip> -m`

### 核心命令
- `hdc list targets [-v]`
- `hdc wait`
- `hdc tmode usb`（文档标记已废弃）
- `hdc tmode port [port-number]`
- `hdc tmode port close`
- `hdc tconn IP:port [-remove]`
- `hdc shell [-b <bundleName>] [command]`
- `hdc install [-cwd path|-r|-s|-w waitingTime|-u userId|-p|-h] <src>`
- `hdc uninstall [-n|-k|-s|-h] <bundleName>`
- `hdc file send [-a|-sync|-z|-m|-cwd path|-b bundlename] <SOURCE> <DEST>`
- `hdc file recv [-a|-sync|-z|-m|-cwd path|-b bundlename] <DEST> <SOURCE>`
- `hdc fport ls`
- `hdc fport <localnode> <remotenode>`
- `hdc fport rm <taskstr>`
- `hdc rport <remotenode> <localnode>`
- `hdc start [-r]`
- `hdc kill [-r]`
- `hdc hilog [-h]`
- `hdc jpid`
- `hdc track-jpid [-a|-p]`
- `hdc target boot [-bootloader|-recovery|shutdown]`
- `hdc sideload <path>`
- `hdc smode [-r]`
- `hdc keygen <FILE>`
- `hdc version` / `hdc -v`
- `hdc checkserver`
- `hdc bugreport [FILE]`
- `hdc help` / `hdc -h [verbose]`

## 2) aa（Ability Manager）
- `aa help`
- `aa start [-d <deviceId>] [-a <abilityName> -b <bundleName>] [-m <moduleName>] [-c] [-E] [-D] [-R] [-S] [-W] [--pi <k> <uint>] [--pb <k> <bool>] [--ps <k> <v>] [--psn <k>] [--wl <x>] [--wt <y>] [--wh <h>] [--ww <w>] [-p <perf-cmd>]`
- `aa start [-d <deviceId>] [-U <URI>] [-t <type>] [-A <action>] [-e <entity>] [-c] [-D] [-E] [-R] [--pi <k> <uint>] [--pb <k> <bool>] [--ps <k> <v>] [--psn <k>] [--wl <x>] [--wt <y>] [--wh <h>] [--ww <w>] [-p <perf-cmd>]`
- `aa stop-service [-d <deviceId>] -a <abilityName> -b <bundleName> [-m <moduleName>]`
- `aa dump -l`
- `aa dump -i <missionId>`
- `aa force-stop <bundle-name> [-p pid] [-r kill-reason]`
- `aa test -b <bundleName> [-m <module>] [-p <pkg>] [-s class <testClass>] [-s level <n>] [-s size <n>] [-s testType <type>] [-s timeout <ms>] [-w <waitTime>] -s unittest <testRunner>`
- `aa attach -b <bundleName>`
- `aa detach -b <bundleName>`
- `aa appdebug -b <bundleName> [-p]`
- `aa appdebug -c`
- `aa appdebug -g`
- `aa process -b <bundleName> -a <abilityName> [-m <moduleName>] [-D <debug-cmd>] [-S]`
- `aa process -b <bundleName> -a <abilityName> [-m <moduleName>] [-p <perf-cmd>] [-S]`
- `aa send-memory-level -p <processId> -l <memoryLevel>`

## 3) bm（Bundle Manager）
- `bm help`
- `bm install [-h] [-p filePath] [-r] [-w waitingTime] [-s hspDirPath] [-u userId]`
- `bm uninstall [-h] [-n bundleName] [-m moduleName] [-k] [-s] [-v versionCode] [-u userId]`
- `bm dump [-h] [-a] [-g] [-n bundleName] [-s shortcutInfo] [-d deviceId] [-l label] [-u userId]`
- `bm clean [-h] [-c] [-n bundleName] [-d] [-i appIndex] [-u userId]`
- `bm get [-h] [-u]`
- `bm quickfix [-h] [-a -f filePath [-t targetPath] [-d] [-o]] [-q -b bundleName] [-r -b bundleName]`
- `bm dump-shared [-h] [-a] [-n bundleName]`
- `bm dump-dependencies [-h] [-n bundleName] [-m moduleName]`
- `bm compile [-h] [-m mode] [-r bundleName] [-a]`
- `bm copy-ap [-h] [-a] [-n bundleName]`
- `bm dump-overlay [-h] [-b bundleName] [-m moduleName] [-t targetModuleName] [-u userId]`
- `bm dump-target-overlay [-h] [-b bundleName] [-m moduleName] [-u userId]`
- `bm install-plugin [-h] [-n hostBundleName] [-p filePath]`
- `bm uninstall-plugin [-h] [-n hostBundleName] [-p pluginBundleName]`

## 4) hilog
- `hilog -h`
- `hilog -x`
- `hilog -L D/I/W/E/F`
- `hilog -t app`
- `hilog -D <domain>`
- `hilog -T <tag>`
- `hilog -a <count>`
- `hilog -z <size>`
- `hilog -P <pid>`
- `hilog -e start`
- `hilog -v time|color|epoch|monotonic|usec|nsec|year|zone|wrap`
- `hilog -w query`
- `hilog -b D/I/W/E/F [--persist]`
- `hilog -g`
- `hilog -G <size>`
- `hilog -r`
- `hilog -k on|off`
- `hilog -s`
- `hilog -S`
- `hilog -Q pidon|pidoff`
- `hilog -Q domainon|domainoff`

## 5) param
- `param -h`
- `param ls [-r] [name]`
- `param get [name]`
- `param set <name> <value>`
- `param wait <name> [value] [timeout]`
- `param save`

## 6) atm
- `atm help`
- `atm dump [-h] [-t [-i <token-id>] [-b <bundle-name>] [-n <process-name>]] [-v [-i <token-id>] [-p <permission-name>]]`

## 7) anm
- `anm help`
- `anm dump [<options>]`
- `anm setting [<options>]`
- `anm setting -k <deviceType>:<status>`
- `anm setting -b <deviceType>:<bundleName>:<uid>:<status>`
- `anm setting -o <deviceType>:<slotType>:<status>`
- `anm setting -c <capacity>`

## 8) cem
- `cem help`
- `cem publish [<options>]`
- `cem dump [<options>]`

## 9) edm
- `edm help`
- `edm enable-admin -n <bundleName> -a <abilityName> [-t <adminType>]`
- `edm disable-admin -n <bundleName>`

## 10) devicedebug
- `devicedebug help`
- `devicedebug kill`
- `devicedebug kill -9 <pid>`

## 11) mediatool
- `mediatool send <path-to-local-media-file> [-ts] [-tas] [-rf] [-urf]`
- `mediatool list <resource-uri>`
- `mediatool recv <media-target> <dest-path>`
- `mediatool delete <resource-uri>`
- `mediatool query <display-name> [-p] [-u]`
- `mediatool ls -l <media-path>`

## 12) app_packing_tool.jar
- `java -jar app_packing_tool.jar --mode hap ...`
- `java -jar app_packing_tool.jar --mode hsp ...`
- `java -jar app_packing_tool.jar --mode app ...`
- `java -jar app_packing_tool.jar --mode multiApp ...`
- `java -jar app_packing_tool.jar --mode hqf ...`
- `java -jar app_packing_tool.jar --mode appqf ...`
- `java -jar app_packing_tool.jar --mode versionNormalize ...`
- `java -jar app_packing_tool.jar --mode packageNormalize ...`
- `java -jar app_packing_tool.jar --mode generalNormalize ...`
- `java -jar app_packing_tool.jar --mode res ...`
- `java -jar app_packing_tool.jar --mode fastApp ...`

## 13) app_unpacking_tool.jar
- `java -jar app_unpacking_tool.jar --mode hap --hap-path <path> --out-path <path> [--force true]`
- `java -jar app_unpacking_tool.jar --mode app --app-path <path> --out-path <path> [--force true]`
- `java -jar app_unpacking_tool.jar --mode hap --rpcid true --hap-path <path> --out-path <path> [--force true]`
- `java -jar app_unpacking_tool.jar --mode hap --hap-path <path> --out-path <path> [--force true] [--libs true] [--cpu-abis option]`
- `java -jar app_unpacking_tool.jar --mode hsp --hsp-path <path> --out-path <path> [--force true]`
- `java -jar app_unpacking_tool.jar --mode hsp --hsp-path <path> --out-path <path> [--force true] [--libs true] [--cpu-abis option]`
- `java -jar app_unpacking_tool.jar --mode appqf --appqf-path <path> --out-path <path> [--force true]`

## 14) 命令行构建与依赖（入口页点名工具）
> 这部分在 `ide-commandline-get` 页面被点名，但该入口页未给出对应子页链接；实际参数以本机 `--help` 为准。

- `./hvigorw -v`
- `./hvigorw clean`
- `./hvigorw assembleHap`
- `./hvigorw assembleApp`
- `./hvigorw test`
- `ohpm -v`
- `ohpm install`
- `ohpm update`
- `ohpm list`
- `codelinter -v`
- `codelinter --help`
- `hstack --help`

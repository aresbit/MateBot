# atm工具

- slug: `atm-tool`
- updatedDate: `2026-03-30 08:12:30`
- source: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/atm-tool
- navigationAddress: `/hmos/hmos-dp1`

# atm工具

Access Token Manager (程序访问控制管理工具，简称atm工具)，是用于查询应用进程的权限、使用类型等信息的工具，为开发者提供了根据tokenid、包名、进程名等信息进行访问控制管理的能力。

#### 环境说明

在使用本工具前，开发者需要先获取
hdc工具
，执行hdc shell。

#### atm工具命令列表

#### 帮助命令

```bash
# 显示帮助信息
atm help
```

#### 查询命令

```bash
atm dump [-h] [-t [-i <token-id>] [-b <bundle-name>] [-n <process-name>]] [-v [-i <token-id>] [-p <permission-name>]]
```

下表所列命令中，-t为必选参数，-i、-b、-n、-p为可选参数。对atm dump -t命令，-i、-b、-n参数只能单独使用。

示例：

```bash
#查询系统中所有的权限定义
atm dump -d

#按权限名查询权限定义
atm dump -d -p *********
# 执行结果
# {
#     "permissionName": "ohos.permission.KERNEL_ATM_SELF_USE",
#     "grantMode": "SYSTEM_GRANT",
#     "availableLevel": "SYSTEM_CORE",
#     "availableType": "SYSTEM",
#     "distributedSceneEnable": true,
#     "isKernelEffect": true,
#     "hasValue": true,
# }

#显示atm dump的帮助信息
atm dump -h

#查询系统中所有应用进程的tokenid和包名
atm dump -t

#按tokenid查询权限信息
atm dump -t -i *********
# 执行结果
# {
#   "tokenID": 672078897,
#   "processName": "samgr",
#   "apl": 2,
#   "permStateList": [
#     {
#       "permissionName": "ohos.permission.DISTRIBUTED_DATASYNC",
#       "grantStatus": 0,
#       "grantFlag": 4,
#     }
#   ]
# }

#按包名查询权限信息
atm dump -t -b ohos.telephony.resources
# 执行结果
# {
#   "tokenID": 537280686,
#   "tokenAttr": 1,
#   "ver": 1,
#   "userId": 100,
#   "bundleName": "ohos.telephony.resources",
#   "instIndex": 0,
#   "dlpType": 0,
#   "isRemote": false,
#   "isPermDialogForbidden": false,
#   "permStateList": [
#     {
#       "permissionName": "ohos.permission.DISTRIBUTED_DATASYNC",
#       "grantStatus": 0,
#       "grantFlag": 4,
#     }
#   ]
# }

#按进程名查询权限信息
atm dump -t -n *********
```

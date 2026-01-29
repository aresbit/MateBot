# MateBot Tmux 配置

简化的 tmux 配置，专为 MateBot 长会话优化。

## 快速开始

```bash
# 一键安装
./tmux-setup.sh

# 启动 tmux
tmux new -s matebot
```

## 核心特性

- 🖱️ **鼠标支持** - 滚动、选择、调整窗格大小
- 📜 **大历史缓存** - 50000 行历史记录
- ⚡ **快速响应** - 10ms 按键响应时间
- 🎨 **MateBot 主题** - 深蓝/青色配色，顶部状态栏
- ⌨️ **Vi 模式** - 熟悉的 Vim 快捷键
- 🚀 **快捷键优化** - Alt+1-5 快速切换窗口

## 常用快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+b d` | 分离会话（后台运行） |
| `Ctrl+b c` | 创建新窗口 |
| `Alt+1~5` | 快速切换窗口（无需前缀） |
| `Ctrl+b %` | 垂直分割 |
| `Ctrl+b -` | 水平分割 |
| `Ctrl+b y` | 切换窗格同步模式 |
| `Ctrl+b m` | 切换鼠标模式 |

## 复制模式（Vi 风格）

1. `Ctrl+b [` 进入复制模式
2. `v` 开始选择
3. `y` 复制选中内容
4. `]` 粘贴

## 配置说明

所有配置都在 `.tmux.conf.local` 文件中，基于 [oh-my-tmux](https://github.com/gpakosz/.tmux) 框架。

主要优化：
- 鼠标支持：`set -g mouse on`
- 历史限制：`set -g history-limit 50000`
- 状态栏位置：`set -g status-position top`
- 响应速度：`set -s escape-time 10`

## 故障排除

```bash
# 检查鼠标是否启用
tmux show -g mouse

# 重新加载配置
tmux source-file ~/.tmux.conf

# 查看当前设置
tmux show -g
```
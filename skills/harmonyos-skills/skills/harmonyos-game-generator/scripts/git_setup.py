#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git 初始化和 GitHub 推送脚本
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_git_command(args, cwd=None, check=True):
    """执行 git 命令"""
    result = subprocess.run(
        ['git'] + args,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    if check and result.returncode != 0:
        print(f"❌ Git 命令失败: git {' '.join(args)}")
        print(result.stderr)
        return None
    return result


def is_git_repo(path):
    """检查是否是 Git 仓库"""
    result = run_git_command(['rev-parse', '--git-dir'], cwd=path, check=False)
    return result is not None and result.returncode == 0


def init_git_repo(project_path):
    """初始化 Git 仓库"""
    if is_git_repo(project_path):
        print("✓ Git 仓库已存在")
        return True

    print("🔧 初始化 Git 仓库...")
    result = run_git_command(['init'], cwd=project_path)
    if result is None:
        return False

    print("✓ Git 仓库初始化成功")
    return True


def create_gitignore(project_path):
    """创建 .gitignore 文件"""
    gitignore_path = os.path.join(project_path, '.gitignore')

    if os.path.exists(gitignore_path):
        print("✓ .gitignore 已存在")
        return

    content = '''# HarmonyOS
.idea/
.build/
.hvigor/
*.hap
*.so
*.a

# Build outputs
entry/build/
build/

# IDE
*.iml
.DS_Store
*.log

# Screenshots
screenshot_*.jpeg
screenshot_*.png
'''
    with open(gitignore_path, 'w') as f:
        f.write(content)

    print("✓ 创建 .gitignore")


def stage_files(project_path):
    """暂存文件"""
    print("📦 暂存文件...")

    # 添加所有文件
    result = run_git_command(['add', '.'], cwd=project_path)
    if result is None:
        return False

    # 显示状态
    result = run_git_command(['status', '--short'], cwd=project_path)
    if result:
        print(result.stdout)

    return True


def create_initial_commit(project_path, game_name):
    """创建初始提交"""
    print("📝 创建初始提交...")

    message = f"""feat: 初始化 {game_name} 鸿蒙元服务游戏

采用 MVVM 架构实现:
- Model层: 游戏实体和数据持久化
- ViewModel层: 游戏引擎和状态管理
- View层: Canvas渲染器和页面组件

Co-Authored-By: Claude (glm-5) <noreply@anthropic.com>
"""
    result = run_git_command(['commit', '-m', message], cwd=project_path)
    return result is not None


def get_github_username():
    """获取 GitHub 用户名"""
    result = subprocess.run(
        ['gh', 'api', 'user', '--jq', '.login'],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def create_github_repo(project_path, repo_name, description=''):
    """创建 GitHub 仓库"""
    print(f"🐙 创建 GitHub 仓库: {repo_name}")

    # 检查 gh 是否可用
    result = subprocess.run(['gh', '--version'], capture_output=True)
    if result.returncode != 0:
        print("❌ gh 命令不可用，请先安装 GitHub CLI")
        return False

    # 创建仓库
    cmd = ['gh', 'repo', 'create', repo_name, '--public', '--source=.', '--remote=origin']
    if description:
        cmd.extend(['--description', description])

    result = subprocess.run(
        cmd,
        cwd=project_path,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        if 'already exists' in result.stderr.lower():
            print("⚠️ 仓库已存在，尝试添加远程...")
            username = get_github_username()
            if username:
                run_git_command(['remote', 'add', 'origin', f'https://github.com/{username}/{repo_name}.git'], cwd=project_path, check=False)
        else:
            print(f"❌ 创建仓库失败: {result.stderr}")
            return False
    else:
        print("✓ GitHub 仓库创建成功")

    return True


def push_to_github(project_path):
    """推送到 GitHub"""
    print("🚀 推送到 GitHub...")

    result = run_git_command(['push', '-u', 'origin', 'main'], cwd=project_path, check=False)
    if result is None or result.returncode != 0:
        # 尝试 master 分支
        result = run_git_command(['push', '-u', 'origin', 'master'], cwd=project_path, check=False)

    if result is None or result.returncode != 0:
        print("❌ 推送失败")
        return False

    print("✓ 推送成功")
    return True


def main():
    parser = argparse.ArgumentParser(description='Git 初始化和 GitHub 推送')
    parser.add_argument('project_path', help='项目路径')
    parser.add_argument('--name', '-n', required=True, help='游戏名称 (用于仓库名)')
    parser.add_argument('--description', '-d', default='', help='仓库描述')
    parser.add_argument('--skip-repo', action='store_true', help='跳过创建 GitHub 仓库')
    args = parser.parse_args()

    print("\n📤 Git 初始化和 GitHub 推送工具\n")

    # 初始化 Git
    if not init_git_repo(args.project_path):
        return 1

    # 创建 .gitignore
    create_gitignore(args.project_path)

    # 暂存文件
    if not stage_files(args.project_path):
        return 1

    # 创建提交
    if not create_initial_commit(args.project_path, args.name):
        return 1

    # 创建 GitHub 仓库
    if not args.skip_repo:
        if not create_github_repo(args.project_path, args.name, args.description):
            return 1

        # 推送
        if not push_to_github(args.project_path):
            return 1

    print("\n✅ 完成!")
    return 0


if __name__ == '__main__':
    sys.exit(main())

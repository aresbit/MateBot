#!/usr/bin/env python3
"""Attention Manager for MateCode - Manus-style attention redirection

基于 Manus Context Engineering 的核心原则：
1. 【注意力重定向】通过 recitation 防止目标漂移
2. 【KV-Cache 优化】稳定提示前缀，动态内容后置
3. 【近期偏好利用】将关键目标放在上下文末尾
"""

import os
import re
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from external_memory import get_external_memory
from failure_memory import FailureMemory, get_failure_memory
from kv_cache import get_kv_cache


@dataclass
class PromptContext:
    """结构化提示词上下文"""
    static_prefix: str  # KV-Cache 友好的静态前缀
    working_memory: List[str]  # 工作记忆 (最近对话)
    retrieved_memories: List[str]  # 检索到的相关记忆
    user_input: str  # 当前用户输入
    task_state: str  # 当前任务状态 (todo.md)
    failures: List[str]  # 相关失败经验 (Manus: keep failures)
    timestamp: Optional[str] = None  # 可选时间戳


class AttentionManager:
    """注意力管理器 - 实现 Manus 的注意力操纵技巧

    核心策略:
    1. 静态系统提示前缀 (可缓存)
    2. 工作记忆 + 检索记忆 (中间层)
    3. 任务目标放在末尾 (利用 recency bias)
    """

    # 静态提示前缀 - 避免动态内容破坏 KV-Cache
    STATIC_SYSTEM_PREFIX = """【系统指令 - MateCode 编程助手】

你是一个专业的软件开发助手，擅长：
- 现代 C++ (C++17/20) 开发
- TypeScript/React 前端开发
- SQLite 数据库设计
- 系统架构设计

当前项目上下文:
- 项目类型: OpenHarmony MediaLibrary
- 技术栈: Modern C++, SQLite, TypeScript

回复规则:
1. 保持回答简洁、直接、技术准确
2. 代码块使用正确的语法高亮
3. 重要决策使用 -- memory 格式记录
4. 遇到错误时分析原因并使用 -- lesson 格式记录教训

教训记录格式 (-- lesson):
当遇到错误、失败或需要总结教训时，在回复末尾添加：

-- lesson
[一句话总结核心教训，包含：错误原因 + 正确做法]
--

示例:
-- lesson
数据库连接池未设置最大连接数导致耗尽，应该配置 max_connections 和超时机制。
--

"""

    # 分隔符
    SECTION_SEPARATOR = "\n" + "=" * 50 + "\n"
    SUB_SEPARATOR = "\n" + "-" * 30 + "\n"

    def __init__(self):
        self._external = get_external_memory()
        self._failure_memory = get_failure_memory()
        self._kv_cache = get_kv_cache()
        self._session_task_ids: Dict[str, str] = {}  # chat_id -> task_id

    def set_task_id(self, chat_id: str, task_id: str):
        """为会话设置当前任务 ID"""
        self._session_task_ids[str(chat_id)] = task_id

    def get_task_id(self, chat_id: str) -> str:
        """获取会话的当前任务 ID"""
        return self._session_task_ids.get(str(chat_id), "default")

    def build_optimized_prompt(
        self,
        user_input: str,
        chat_id: str,
        memories: Optional[List[Dict[str, Any]]] = None,
        working_memory: Optional[List[str]] = None,
        include_meta_prompt: bool = True,
        claude_md_content: Optional[str] = None,
    ) -> str:
        """构建 KV-Cache 优化的提示词

        结构 (从静态到动态):
        1. 静态系统前缀 (长期缓存)
        2. 项目元提示 (首次加载)
        3. 检索到的相关记忆
        4. 相关失败经验 (Manus: keep failures)
        5. 用户输入
        6. [分隔线]
        7. 当前任务目标 (todo.md) ← 放在末尾强化注意力

        Args:
            user_input: 用户当前输入
            chat_id: 会话 ID
            memories: 检索到的相关记忆
            working_memory: 工作记忆 (最近几轮对话)
            include_meta_prompt: 是否包含 .CLAUDE.md 的元提示
            claude_md_content: .CLAUDE.md 的内容

        Returns:
            优化后的完整提示词
        """
        parts = []

        # 1. 静态前缀 (KV-Cache 友好)
        parts.append(self.STATIC_SYSTEM_PREFIX.strip())

        # 2. 项目元提示 (仅新会话或首次)
        if include_meta_prompt and claude_md_content:
            meta_prompt = self._extract_meta_prompt(claude_md_content)
            if meta_prompt:
                parts.append(f"【项目特定指令】\n{meta_prompt}")

        # 3. 工作记忆 (最近对话上下文)
        if working_memory:
            wm_text = self._format_working_memory(working_memory)
            if wm_text:
                parts.append(wm_text)

        # 4. 检索到的长期记忆
        if memories:
            mem_text = self._format_retrieved_memories(memories)
            if mem_text:
                parts.append(mem_text)

        # 5. 相关失败经验 (Manus: 在操作前展示历史失败)
        failure_text = self._get_failure_lessons(chat_id, user_input)
        if failure_text:
            parts.append(failure_text)

        # 6. 用户当前输入 (主要指令)
        parts.append(f"【用户输入】\n{user_input}")

        # 7. 任务目标 - 放在末尾 (Manus: attention manipulation)
        task_state = self._get_task_state(chat_id)
        if task_state:
            parts.append(self._format_task_recitation(task_state))

        # 使用标准分隔符连接
        return self.SECTION_SEPARATOR.join(parts)

    def build_optimized_prompt_with_cache(
        self,
        user_input: str,
        chat_id: str,
        memories: Optional[List[Dict[str, Any]]] = None,
        working_memory: Optional[List[str]] = None,
        include_meta_prompt: bool = True,
        claude_md_content: Optional[str] = None,
        ttl_seconds: int = 3600,
    ) -> Tuple[str, Dict[str, Any]]:
        """构建 KV-Cache 优化的提示词（带缓存支持）

        结构 (从静态到动态):
        1. 静态系统前缀 (长期缓存)
        2. 项目元提示 (首次加载)
        3. 检索到的相关记忆
        4. 相关失败经验 (Manus: keep failures)
        5. 用户输入
        6. [分隔线]
        7. 当前任务目标 (todo.md) ← 放在末尾强化注意力

        缓存策略:
        - 基于静态前缀哈希和用户ID生成缓存键
        - 缓存完整提示词（假设动态内容变化不大）
        - TTL默认1小时

        Args:
            user_input: 用户当前输入
            chat_id: 会话 ID
            memories: 检索到的相关记忆
            working_memory: 工作记忆 (最近几轮对话)
            include_meta_prompt: 是否包含 .CLAUDE.md 的元提示
            claude_md_content: .CLAUDE.md 的内容
            ttl_seconds: 缓存生存时间（秒）

        Returns:
            Tuple[优化后的完整提示词, 缓存信息字典]
        """
        # 生成缓存键
        cache_key = self._kv_cache.generate_cache_key(
            self.STATIC_SYSTEM_PREFIX, str(chat_id)
        )

        # 尝试从缓存获取
        cached_prompt = self._kv_cache.get_cached_prompt(cache_key)
        cache_info = {"cache_hit": False, "cache_key": cache_key}

        if cached_prompt:
            # 缓存命中：直接返回缓存的提示词
            # 注意：这里假设动态内容（工作记忆、失败经验等）变化不大
            # 对于精确匹配的场景，这种简单缓存是有效的
            cache_info.update({
                "cache_hit": True,
                "source": "kv_cache",
            })
            return cached_prompt, cache_info

        # 缓存未命中：正常构建提示词
        prompt = self.build_optimized_prompt(
            user_input=user_input,
            chat_id=chat_id,
            memories=memories,
            working_memory=working_memory,
            include_meta_prompt=include_meta_prompt,
            claude_md_content=claude_md_content,
        )

        # 存储到缓存
        self._kv_cache.store_prompt(
            cache_key=cache_key,
            full_prompt=prompt,
            static_prefix=self.STATIC_SYSTEM_PREFIX,
            user_id=str(chat_id),
            ttl_seconds=ttl_seconds,
        )

        cache_info.update({
            "cache_hit": False,
            "source": "new_generation",
        })

        return prompt, cache_info

    def get_cache_stats(self) -> Dict[str, Any]:
        """获取KV-Cache统计信息

        Returns:
            缓存统计字典
        """
        return self._kv_cache.get_stats()

    def _extract_meta_prompt(self, claude_md_content: str) -> str:
        """从 .CLAUDE.md 提取元提示"""
        if not claude_md_content:
            return ""

        lines = claude_md_content.split("\n")
        in_initial_prompt = False
        prompt_lines = []

        for line in lines:
            if line.strip() == "## 初始提示词":
                in_initial_prompt = True
                continue
            if in_initial_prompt:
                if line.startswith("## "):
                    break
                prompt_lines.append(line)

        return "\n".join(prompt_lines).strip()

    def _format_working_memory(self, working_memory: List[str]) -> str:
        """格式化工作记忆"""
        if not working_memory:
            return ""

        lines = ["【近期对话上下文】"]
        for i, entry in enumerate(working_memory[-5:], 1):  # 只保留最近5轮
            lines.append(f"{i}. {entry}")

        return "\n".join(lines)

    def _format_retrieved_memories(self, memories: List[Dict[str, Any]]) -> str:
        """格式化学到的记忆"""
        if not memories:
            return ""

        lines = ["【相关历史记忆】"]
        for mem in memories[:5]:  # 最多5条
            content = mem.get("content", "")
            # 如果是外部引用，只显示摘要
            if "(see:" in content:
                content = content.split("(see:")[0].strip()
            lines.append(f"• {content[:150]}")

        return "\n".join(lines)

    def _get_task_state(self, chat_id: str) -> str:
        """获取当前任务状态 (todo.md)"""
        task_id = self.get_task_id(chat_id)
        try:
            return self._external.get_todo_md(str(chat_id), task_id)
        except Exception:
            return ""

    def _format_task_recitation(self, task_state: str) -> str:
        """格式化任务复述 (放在末尾强化注意力)"""
        # 提取关键部分，避免过长
        lines = task_state.split("\n")
        key_sections = []

        for line in lines:
            # 保留标题、目标、注意事项
            if any(line.strip().startswith(prefix) for prefix in
                   ["#", "## 主要目标", "## 待办", "## 注意", "- [ ]", "⚠️"]):
                key_sections.append(line)

        # 如果提取的内容太少，使用原始内容的前500字符
        if len("\n".join(key_sections)) < 100:
            task_summary = task_state[:500]
        else:
            task_summary = "\n".join(key_sections[:20])  # 最多20行

        return f"""【⚠️ 当前任务目标 - 请始终保持关注】
{task_summary}

【提醒】完成上述目标后，请更新任务状态。"""

    def update_task_from_response(self, chat_id: str, response: str) -> bool:
        """从 Agent 响应中提取并更新任务状态

        Manus 技巧: 让 Agent 持续重写目标到 todo.md
        检测响应中的任务更新标记
        """
        # 检测特定的任务更新标记
        task_update_pattern = r"--\s*task_update\s*\n(.*?)\n--"
        matches = re.findall(task_update_pattern, response, re.DOTALL)

        if matches:
            # 追加到 todo.md
            task_id = self.get_task_id(chat_id)
            combined_update = "\n\n".join(matches)
            return self._external.update_todo_md(
                str(chat_id), combined_update, task_id, append=True
            )

        return False

    def create_task(
        self,
        chat_id: str,
        goal: str,
        task_id: Optional[str] = None
    ) -> str:
        """创建新任务并设置 todo.md"""
        if task_id is None:
            task_id = f"task_{int(time.time())}"

        self.set_task_id(chat_id, task_id)

        template = f"""# 当前任务

## 主要目标
{goal}

## 已完成
- [ ]

## 待办事项
- [ ] 分析需求
- [ ] 设计方案
- [ ] 实现代码
- [ ] 测试验证

## 关键决策
[待记录]

## 注意事项
[待记录]

---
任务ID: {task_id}
创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""

        self._external.update_todo_md(str(chat_id), template, task_id)
        return task_id

    def get_prompt_stats(self, prompt: str) -> Dict[str, Any]:
        """分析提示词结构统计"""
        sections = prompt.split(self.SECTION_SEPARATOR.strip())

        static_len = len(self.STATIC_SYSTEM_PREFIX)
        total_len = len(prompt) if prompt else 1

        return {
            "total_chars": len(prompt),
            "total_lines": len(prompt.split("\n")),
            "section_count": len(sections),
            "sections": [s.split("\n")[0][:50] for s in sections if s.strip()],
            "has_task_recitation": "【⚠️ 当前任务目标" in prompt,
            "static_prefix_ratio": static_len / total_len,
            "static_prefix_ratio": len(self.STATIC_SYSTEM_PREFIX) / len(prompt) if prompt else 0,
        }

    def _get_failure_lessons(self, chat_id: str, user_input: str) -> str:
        """获取与当前操作相关的失败经验

        Manus 原则: 在操作前展示历史失败，防止重复犯错
        """
        try:
            failures = self._failure_memory.get_relevant_failures(
                str(chat_id), user_input, limit=3
            )
            if failures:
                return self._failure_memory.format_for_prompt(failures, max_chars=800)
        except Exception as e:
            print(f"Error getting failure lessons: {e}")
        return ""


class StablePromptBuilder:
    """稳定提示构建器 - 确保 KV-Cache 命中率

    关键原则:
    - 静态前缀占总提示的 70%+
    - 避免在前缀中使用时间戳、随机数
    - 动态内容只在一处插入
    """

    def __init__(self, attention_manager: Optional[AttentionManager] = None):
        self.am = attention_manager or AttentionManager()
        self._prefix_cache_key = "matecode_v1"

    def build_with_cache_optimization(
        self,
        user_input: str,
        chat_id: str,
        **kwargs
    ) -> Tuple[str, Dict[str, Any]]:
        """构建提示词并返回缓存分析（使用真正的KV-Cache）"""

        # 使用带缓存的构建方法
        prompt, cache_info = self.am.build_optimized_prompt_with_cache(
            user_input=user_input,
            chat_id=chat_id,
            **kwargs
        )

        # 获取提示词统计信息
        stats = self.am.get_prompt_stats(prompt)

        # 计算缓存效率（静态前缀比例）
        cache_efficiency = stats["static_prefix_ratio"]

        optimization_hints = []
        if cache_efficiency < 0.5:
            optimization_hints.append("静态前缀比例较低，建议减少动态前缀内容")
        if stats["total_chars"] > 8000:
            optimization_hints.append("提示词较长，建议使用外部记忆存储")

        # 合并缓存信息和统计信息
        return prompt, {
            "cache_efficiency": cache_efficiency,
            "optimization_hints": optimization_hints,
            "cache_hit": cache_info.get("cache_hit", False),
            "cache_key": cache_info.get("cache_key", ""),
            "cache_source": cache_info.get("source", "unknown"),
            **stats
        }


# 便捷的快捷函数
def get_attention_manager() -> AttentionManager:
    """获取 AttentionManager 单例"""
    return AttentionManager()


def build_prompt(
    user_input: str,
    chat_id: str,
    memories: Optional[List[Dict]] = None,
    **kwargs
) -> str:
    """快捷函数: 构建优化提示词"""
    am = get_attention_manager()
    return am.build_optimized_prompt(
        user_input=user_input,
        chat_id=chat_id,
        memories=memories,
        **kwargs
    )

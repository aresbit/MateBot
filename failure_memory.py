#!/usr/bin/env python3
"""Failure Memory System for MateCode - Learn from mistakes

Based on Manus Context Engineering Lesson 5: Keep Failures in Context
- Failed actions and error traces should remain in context, not be sanitized
- Reduces error recurrence by ~42%
- Creates implicit feedback loops for self-correction
- Allows the model to "see" its mistakes and update internal beliefs
"""

import hashlib
import json
import re
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple
from enum import Enum

from memory import get_memory


class ErrorType(Enum):
    """分类错误类型"""
    SYNTAX = "syntax"           # 语法错误
    LOGIC = "logic"             # 逻辑错误
    RUNTIME = "runtime"         # 运行时错误
    API_USAGE = "api_usage"     # API使用错误
    CONFIG = "config"           # 配置错误
    PERMISSION = "permission"   # 权限错误
    NETWORK = "network"         # 网络错误
    UNKNOWN = "unknown"         # 未知错误


@dataclass
class FailureRecord:
    """失败记录数据结构"""
    failure_id: str
    user_id: str
    action: str              # 尝试执行的操作
    error_message: str       # 错误信息
    error_type: str          # 错误类型
    context: str             # 上下文信息
    lesson: str              # 学到的教训
    timestamp: str
    recurrence_count: int = 0  # 重复发生次数
    resolved: bool = False
    metadata: Dict[str, Any] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FailureRecord':
        return cls(**data)


class FailureMemory:
    """失败记忆系统 - 保留错误经验防止重复犯错

    Manus 核心原则:
    1. 不要清理错误 - 保留失败痕迹
    2. 在相关操作前检索历史失败
    3. 创建自我纠正的反馈循环
    """

    # 错误类型检测模式
    ERROR_PATTERNS = {
        ErrorType.SYNTAX: [
            r'SyntaxError',
            r'syntax error',
            r'unexpected token',
            r'invalid syntax',
            r'expected.*but found',
        ],
        ErrorType.LOGIC: [
            r'LogicError',
            r'assertion failed',
            r'wrong result',
            r'incorrect output',
            r'unexpected behavior',
        ],
        ErrorType.RUNTIME: [
            r'RuntimeError',
            r'NullPointer',
            r'undefined.*reference',
            r'segmentation fault',
            r'memory leak',
        ],
        ErrorType.API_USAGE: [
            r'APIError',
            r'bad request',
            r'invalid parameter',
            r'method not allowed',
            r'not supported',
        ],
        ErrorType.CONFIG: [
            r'ConfigError',
            r'configuration',
            r'missing config',
            r'env variable',
            r'setting not found',
        ],
        ErrorType.PERMISSION: [
            r'PermissionError',
            r'access denied',
            r'unauthorized',
            r'forbidden',
            r'not allowed',
        ],
        ErrorType.NETWORK: [
            r'NetworkError',
            r'connection refused',
            r'timeout',
            r'ENOTFOUND',
            r'ECONNREFUSED',
        ],
    }

    def __init__(self):
        self._memory = get_memory()
        self.MESSAGE_TYPE = "failure_lesson"

    def _detect_error_type(self, error_message: str) -> ErrorType:
        """根据错误信息检测错误类型"""
        error_lower = error_message.lower()

        for error_type, patterns in self.ERROR_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, error_lower, re.IGNORECASE):
                    return error_type

        return ErrorType.UNKNOWN

    def _generate_id(self, user_id: str, action: str, error: str) -> str:
        """生成失败记录ID"""
        data = f"{user_id}:{action}:{error}:{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def record_failure(
        self,
        user_id: str,
        action: str,
        error_message: str,
        context: str = "",
        lesson: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> FailureRecord:
        """记录失败经验

        Args:
            user_id: 用户ID
            action: 尝试执行的操作
            error_message: 错误信息
            context: 上下文信息
            lesson: 学到的教训
            metadata: 额外元数据

        Returns:
            FailureRecord 对象
        """
        error_type = self._detect_error_type(error_message)

        # 检查是否已有类似错误
        similar = self._find_similar_failure(user_id, action, error_message)
        if similar:
            # 更新重复次数
            similar.recurrence_count += 1
            similar.timestamp = datetime.now().isoformat()
            self._update_failure(user_id, similar)
            return similar

        # 创建新记录
        record = FailureRecord(
            failure_id=self._generate_id(user_id, action, error_message),
            user_id=user_id,
            action=action,
            error_message=error_message,
            error_type=error_type.value,
            context=context,
            lesson=lesson or "待总结",
            timestamp=datetime.now().isoformat(),
            recurrence_count=1,
            resolved=False,
            metadata=metadata or {}
        )

        # 存储到记忆系统
        content = self._format_for_storage(record)
        self._memory.add(
            user_id=user_id,
            content=content,
            message_type=self.MESSAGE_TYPE,
            metadata={
                "failure_id": record.failure_id,
                "error_type": record.error_type,
                "action": action,
                "recurrence_count": record.recurrence_count,
                "resolved": record.resolved
            }
        )

        return record

    def _format_for_storage(self, record: FailureRecord) -> str:
        """格式化为存储格式"""
        return f"""失败记录:
action: {record.action}
error: {record.error_message}
type: {record.error_type}
context: {record.context[:200] if record.context else 'N/A'}
lesson: {record.lesson}
recurrence: {record.recurrence_count}x
"""

    def _find_similar_failure(
        self,
        user_id: str,
        action: str,
        error_message: str
    ) -> Optional[FailureRecord]:
        """查找类似的失败记录"""
        # 获取该用户的所有失败记录
        failures = self.get_user_failures(user_id, limit=50)

        action_normalized = action.lower().strip()
        error_normalized = error_message.lower().strip()[:100]

        for f in failures:
            # 检查 action 相似度
            if f.action.lower().strip() == action_normalized:
                # 检查 error 相似度
                if f.error_message.lower().strip()[:100] == error_normalized:
                    return f

        return None

    def _update_failure(self, user_id: str, record: FailureRecord) -> bool:
        """更新现有失败记录"""
        try:
            # 查找并删除旧记录
            memories = self._memory.get_by_type(user_id, self.MESSAGE_TYPE, limit=100)
            for mem in memories:
                metadata = mem.get("metadata", {})
                if metadata.get("failure_id") == record.failure_id:
                    self._memory.delete(user_id, mem["id"])
                    break

            # 添加更新后的记录
            content = self._format_for_storage(record)
            self._memory.add(
                user_id=user_id,
                content=content,
                message_type=self.MESSAGE_TYPE,
                metadata={
                    "failure_id": record.failure_id,
                    "error_type": record.error_type,
                    "action": record.action,
                    "recurrence_count": record.recurrence_count,
                    "resolved": record.resolved
                }
            )
            return True
        except Exception as e:
            print(f"Error updating failure record: {e}")
            return False

    def get_relevant_failures(
        self,
        user_id: str,
        current_action: str,
        limit: int = 3
    ) -> List[FailureRecord]:
        """获取与当前操作相关的失败经验

        在尝试操作前调用，检索相关的历史失败

        Args:
            user_id: 用户ID
            current_action: 当前要执行的操作
            limit: 返回记录数量上限

        Returns:
            相关的失败记录列表
        """
        # 获取该用户的所有未解决失败记录
        all_failures = self.get_user_failures(user_id, resolved_only=False, limit=50)

        # 按相关性排序
        scored_failures = []
        current_action_lower = current_action.lower()

        for f in all_failures:
            score = 0
            action_lower = f.action.lower()

            # 完全匹配
            if action_lower == current_action_lower:
                score += 100
            # 包含关系
            elif current_action_lower in action_lower or action_lower in current_action_lower:
                score += 50
            # 关键词匹配
            else:
                current_words = set(current_action_lower.split())
                failure_words = set(action_lower.split())
                common = current_words & failure_words
                score += len(common) * 10

            # 重复次数加权
            score += f.recurrence_count * 5

            scored_failures.append((score, f))

        # 按分数排序，返回最相关的
        scored_failures.sort(key=lambda x: x[0], reverse=True)
        return [f for _, f in scored_failures[:limit]]

    def get_user_failures(
        self,
        user_id: str,
        resolved_only: bool = False,
        limit: int = 20
    ) -> List[FailureRecord]:
        """获取用户的失败记录

        Args:
            user_id: 用户ID
            resolved_only: 仅返回已解决的
            limit: 返回数量上限
        """
        memories = self._memory.get_by_type(user_id, self.MESSAGE_TYPE, limit=limit * 2)

        records = []
        for mem in memories:
            metadata = mem.get("metadata", {})
            if resolved_only and not metadata.get("resolved"):
                continue

            # 解析 content 重建 FailureRecord
            record = self._parse_memory_to_record(mem)
            if record:
                records.append(record)

        return records[:limit]

    def _parse_memory_to_record(self, mem: Dict[str, Any]) -> Optional[FailureRecord]:
        """从记忆解析为 FailureRecord"""
        try:
            content = mem.get("content", "")
            metadata = mem.get("metadata", {})

            # 解析 content
            action_match = re.search(r'action:\s*(.+)', content)
            error_match = re.search(r'error:\s*(.+)', content)
            type_match = re.search(r'type:\s*(\w+)', content)
            context_match = re.search(r'context:\s*(.+)', content)
            lesson_match = re.search(r'lesson:\s*(.+)', content)
            recurrence_match = re.search(r'recurrence:\s*(\d+)x', content)

            return FailureRecord(
                failure_id=metadata.get("failure_id", "unknown"),
                user_id=mem.get("user_id", "unknown"),
                action=action_match.group(1) if action_match else "",
                error_message=error_match.group(1) if error_match else "",
                error_type=type_match.group(1) if type_match else "unknown",
                context=context_match.group(1) if context_match else "",
                lesson=lesson_match.group(1) if lesson_match else "",
                timestamp=mem.get("timestamp", ""),
                recurrence_count=int(recurrence_match.group(1)) if recurrence_match else 1,
                resolved=metadata.get("resolved", False),
                metadata=metadata
            )
        except Exception as e:
            print(f"Error parsing failure record: {e}")
            return None

    def mark_resolved(self, user_id: str, failure_id: str) -> bool:
        """标记失败记录为已解决"""
        failures = self.get_user_failures(user_id, resolved_only=False, limit=100)
        for f in failures:
            if f.failure_id == failure_id:
                f.resolved = True
                return self._update_failure(user_id, f)
        return False

    def format_for_prompt(
        self,
        failures: List[FailureRecord],
        max_chars: int = 1000
    ) -> str:
        """格式化失败经验用于提示词注入

        Manus 原则: 在操作前展示相关失败，防止重复犯错
        """
        if not failures:
            return ""

        lines = ["【⚠️ 相关失败经验 - 避免重复犯错】", ""]
        current_len = len(lines[0]) + 1

        for i, f in enumerate(failures, 1):
            # 格式化单条失败记录
            entry_lines = [
                f"{i}. 操作: {f.action}",
                f"   错误: {f.error_message[:100]}",
            ]

            if f.lesson and f.lesson != "待总结":
                entry_lines.append(f"   教训: {f.lesson}")

            if f.recurrence_count > 1:
                entry_lines.append(f"   (已重复 {f.recurrence_count} 次)")

            entry_text = "\n".join(entry_lines) + "\n"

            if current_len + len(entry_text) > max_chars:
                break

            lines.extend(entry_lines)
            lines.append("")
            current_len += len(entry_text) + 1

        return "\n".join(lines)

    def extract_lesson_from_response(self, response: str) -> Optional[str]:
        """从Agent响应中提取教训总结

        检测格式:
        -- lesson
        学到的教训总结
        --
        """
        pattern = r'--\s*lesson\s*\n(.*?)\n--'
        match = re.search(pattern, response, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None

    def get_stats(self, user_id: str) -> Dict[str, Any]:
        """获取失败统计信息"""
        all_failures = self.get_user_failures(user_id, resolved_only=False, limit=1000)

        resolved = sum(1 for f in all_failures if f.resolved)
        by_type = {}
        total_recurrences = 0

        for f in all_failures:
            by_type[f.error_type] = by_type.get(f.error_type, 0) + 1
            total_recurrences += f.recurrence_count

        return {
            "total_unique": len(all_failures),
            "resolved": resolved,
            "unresolved": len(all_failures) - resolved,
            "by_type": by_type,
            "total_occurrences": total_recurrences,
            "avg_recurrence": total_recurrences / len(all_failures) if all_failures else 0
        }


# 便捷函数
def get_failure_memory() -> FailureMemory:
    """获取 FailureMemory 单例"""
    return FailureMemory()


def record_failure(
    user_id: str,
    action: str,
    error_message: str,
    context: str = "",
    lesson: str = ""
) -> FailureRecord:
    """快捷函数: 记录失败"""
    fm = get_failure_memory()
    return fm.record_failure(user_id, action, error_message, context, lesson)


def get_relevant_failures(user_id: str, action: str, limit: int = 3) -> List[FailureRecord]:
    """快捷函数: 获取相关失败"""
    fm = get_failure_memory()
    return fm.get_relevant_failures(user_id, action, limit)

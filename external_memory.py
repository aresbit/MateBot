#!/usr/bin/env python3
"""External Memory System for MateCode - File system based external memory

Based on Manus Context Engineering principles:
- Use file system as unlimited external memory
- Store references instead of full content to reduce context window
- Maintain todo.md for task tracking and attention redirection
- Support reversible compression (store paths, not content)
"""

import hashlib
import json
import os
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict


@dataclass
class ExternalMemoryRef:
    """Reference to externally stored content"""
    ref_id: str
    content_type: str
    file_path: str
    summary: str
    created_at: str
    size_bytes: int
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ExternalMemoryRef':
        return cls(**data)

    def to_memory_format(self) -> str:
        """Format for insertion into memory (compact reference)"""
        return f"[{self.content_type}] {self.summary} (see: {self.file_path})"


class ExternalMemory:
    """File system based external memory storage

    Design principles from Manus:
    1. Restorable compression - store file paths/URLs instead of full content
    2. On-demand retrieval - agent reads files when needed
    3. Structured task tracking - maintain running todo.md files
    """

    BASE_DIR = Path.home() / ".matecode" / "external_memory"
    TODO_FILENAME = "todo.md"
    INDEX_FILENAME = "index.json"

    # Content size thresholds
    STORE_EXTERNALLY_THRESHOLD = 500  # chars
    COMPRESS_THRESHOLD = 200  # chars

    # Cleanup settings
    DEFAULT_RETENTION_DAYS = 30

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or self.BASE_DIR
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._init_index()

    def _init_index(self) -> None:
        """Initialize the index file if not exists"""
        index_path = self.base_dir / self.INDEX_FILENAME
        if not index_path.exists():
            self._save_index({"version": "1.0", "refs": {}})

    def _get_index(self) -> Dict[str, Any]:
        """Load the index"""
        index_path = self.base_dir / self.INDEX_FILENAME
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"version": "1.0", "refs": {}}

    def _save_index(self, index: Dict[str, Any]) -> None:
        """Save the index"""
        index_path = self.base_dir / self.INDEX_FILENAME
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

    def _generate_ref_id(self, user_id: str, content: str, content_type: str) -> str:
        """Generate unique reference ID"""
        data = f"{user_id}:{content_type}:{content[:100]}:{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def _get_user_dir(self, user_id: str) -> Path:
        """Get user-specific storage directory"""
        user_dir = self.base_dir / self._sanitize_path(user_id)
        user_dir.mkdir(exist_ok=True)
        return user_dir

    def _sanitize_path(self, name: str) -> str:
        """Sanitize string for use in file paths"""
        return re.sub(r'[^\w\-_.]', '_', name)[:50]

    def _generate_summary(self, content: str, max_length: int = 150) -> str:
        """Generate a summary of content"""
        lines = content.strip().split('\n')
        first_line = lines[0] if lines else ""

        # Try to extract key information
        if len(first_line) > max_length:
            return first_line[:max_length] + "..."

        # If first line is too short, add more context
        if len(first_line) < 50 and len(lines) > 1:
            second_part = ' '.join(lines[1:3])
            combined = f"{first_line} - {second_part}"
            return combined[:max_length] + "..." if len(combined) > max_length else combined

        return first_line

    def store_large_content(
        self,
        user_id: str,
        content: str,
        content_type: str = "general",
        metadata: Optional[Dict[str, Any]] = None
    ) -> ExternalMemoryRef:
        """Store large content externally and return a reference

        This implements Manus's "restorable compression" principle:
        - Store full content in file system
        - Return compact reference for storage in memory/SQLite
        - Allows on-demand retrieval when needed

        Args:
            user_id: User identifier
            content: Content to store
            content_type: Type of content (code, design, error, etc.)
            metadata: Additional metadata

        Returns:
            ExternalMemoryRef: Reference object for memory storage
        """
        if not content or not content.strip():
            raise ValueError("Content cannot be empty")

        content = content.strip()
        user_dir = self._get_user_dir(user_id)

        # Generate reference ID
        ref_id = self._generate_ref_id(user_id, content, content_type)

        # Create type-specific subdirectory
        type_dir = user_dir / self._sanitize_path(content_type)
        type_dir.mkdir(exist_ok=True)

        # File naming with timestamp for uniqueness
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_id = ref_id[:8]
        filename = f"{timestamp}_{safe_id}.md"
        file_path = type_dir / filename

        # Write content with metadata header
        header = f"""---
ref_id: {ref_id}
user_id: {user_id}
content_type: {content_type}
created_at: {datetime.now().isoformat()}
metadata: {json.dumps(metadata or {}, ensure_ascii=False)}
---

"""

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(header + content)

        # Create reference object
        ref = ExternalMemoryRef(
            ref_id=ref_id,
            content_type=content_type,
            file_path=str(file_path),
            summary=self._generate_summary(content),
            created_at=datetime.now().isoformat(),
            size_bytes=len(content.encode('utf-8')),
            metadata=metadata or {}
        )

        # Update index
        index = self._get_index()
        index["refs"][ref_id] = {
            "user_id": user_id,
            "file_path": str(file_path),
            "created_at": ref.created_at,
            "content_type": content_type
        }
        self._save_index(index)

        return ref

    def retrieve_content(self, ref_id: str) -> Optional[str]:
        """Retrieve full content by reference ID

        Args:
            ref_id: Reference ID

        Returns:
            Full content or None if not found
        """
        index = self._get_index()
        if ref_id not in index["refs"]:
            return None

        file_path = Path(index["refs"][ref_id]["file_path"])
        if not file_path.exists():
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse and remove YAML frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    return parts[2].strip()

            return content
        except Exception as e:
            print(f"Error retrieving content: {e}")
            return None

    def retrieve_by_path(self, file_path: str) -> Optional[str]:
        """Retrieve content by file path"""
        path = Path(file_path)
        if not path.exists():
            # Try relative to base_dir
            path = self.base_dir / file_path

        if not path.exists():
            return None

        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse and remove YAML frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    return parts[2].strip()

            return content
        except Exception as e:
            print(f"Error retrieving content: {e}")
            return None

    # =========================================================================
    # Todo.md Management - Attention Redirection Mechanism
    # =========================================================================

    def get_todo_md(self, user_id: str, task_id: str = "default") -> str:
        """Get or create todo.md for task tracking

        This implements Manus's attention manipulation through recitation:
        - Agent continuously rewrites objectives into todo.md
        - File is appended at end of context at every step
        - Keeps goals front-of-mind using LLM's recency bias

        Args:
            user_id: User identifier
            task_id: Task identifier (default for current active task)

        Returns:
            Content of todo.md or default template
        """
        user_dir = self._get_user_dir(user_id)
        todo_path = user_dir / f"{task_id}_{self.TODO_FILENAME}"

        if todo_path.exists():
            try:
                with open(todo_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"Error reading todo.md: {e}")

        # Return default template
        return self._default_todo_template()

    def update_todo_md(
        self,
        user_id: str,
        content: str,
        task_id: str = "default",
        append: bool = False
    ) -> bool:
        """Update todo.md - attention redirection mechanism

        Args:
            user_id: User identifier
            content: New content or content to append
            task_id: Task identifier
            append: If True, append to existing; if False, replace

        Returns:
            True if successful
        """
        user_dir = self._get_user_dir(user_id)
        todo_path = user_dir / f"{task_id}_{self.TODO_FILENAME}"

        try:
            if append and todo_path.exists():
                existing = todo_path.read_text(encoding='utf-8')
                # Add separator and timestamp
                separator = f"\n\n---\n*Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
                content = existing + separator + content

            todo_path.write_text(content, encoding='utf-8')
            return True
        except Exception as e:
            print(f"Error updating todo.md: {e}")
            return False

    def _default_todo_template(self) -> str:
        """Default todo.md template"""
        return """# 当前任务目标

## 主要目标
[在此描述当前会话的主要目标]

## 已完成
- [ ]

## 待办事项
- [ ]

## 关键决策
[记录重要的架构或设计决策]

## 注意事项
[记录需要特别注意的事项，如错误规避]

---
*Created: {timestamp}*
""".format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M'))

    def list_tasks(self, user_id: str) -> List[Dict[str, Any]]:
        """List all todo.md files for a user"""
        user_dir = self._get_user_dir(user_id)
        tasks = []

        try:
            for f in user_dir.glob(f"*_{self.TODO_FILENAME}"):
                task_id = f.name.replace(f"_{self.TODO_FILENAME}", "")
                stat = f.stat()
                tasks.append({
                    "task_id": task_id,
                    "file_path": str(f),
                    "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "size_bytes": stat.st_size
                })
        except Exception as e:
            print(f"Error listing tasks: {e}")

        return sorted(tasks, key=lambda x: x["modified_at"], reverse=True)

    # =========================================================================
    # Content Compression Helpers
    # =========================================================================

    def should_store_externally(self, content: str) -> bool:
        """Check if content should be stored externally"""
        return len(content) > self.STORE_EXTERNALLY_THRESHOLD

    def compress_for_memory(
        self,
        user_id: str,
        content: str,
        content_type: str = "general",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, Optional[ExternalMemoryRef]]:
        """Compress content for memory storage

        Implements Manus's restorable compression:
        - If content is large, store externally and return reference
        - If content is small, return as-is

        Returns:
            Tuple of (content_or_reference, ExternalMemoryRef if stored externally)
        """
        if not self.should_store_externally(content):
            return content, None

        ref = self.store_large_content(user_id, content, content_type, metadata)
        return ref.to_memory_format(), ref

    # =========================================================================
    # Cleanup and Maintenance
    # =========================================================================

    def cleanup_old_files(self, retention_days: int = DEFAULT_RETENTION_DAYS) -> Dict[str, int]:
        """Clean up files older than retention period

        Returns:
            Dict with cleanup statistics
        """
        cutoff = datetime.now() - timedelta(days=retention_days)
        stats = {"deleted_files": 0, "deleted_bytes": 0}

        index = self._get_index()
        refs_to_remove = []

        for ref_id, ref_data in index.get("refs", {}).items():
            try:
                created = datetime.fromisoformat(ref_data["created_at"])
                if created < cutoff:
                    file_path = Path(ref_data["file_path"])
                    if file_path.exists():
                        size = file_path.stat().st_size
                        file_path.unlink()
                        stats["deleted_bytes"] += size
                        stats["deleted_files"] += 1

                    # Clean up empty directories
                    parent = file_path.parent
                    if parent.exists() and not any(parent.iterdir()):
                        parent.rmdir()

                    refs_to_remove.append(ref_id)
            except Exception as e:
                print(f"Error cleaning up {ref_id}: {e}")

        # Update index
        for ref_id in refs_to_remove:
            del index["refs"][ref_id]
        self._save_index(index)

        return stats

    def get_storage_stats(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Get storage statistics"""
        stats = {
            "total_files": 0,
            "total_bytes": 0,
            "by_type": {},
            "by_user": {}
        }

        index = self._get_index()

        for ref_id, ref_data in index.get("refs", {}).items():
            file_path = Path(ref_data["file_path"])
            if not file_path.exists():
                continue

            try:
                size = file_path.stat().st_size
                content_type = ref_data.get("content_type", "unknown")
                uid = ref_data.get("user_id", "unknown")

                stats["total_files"] += 1
                stats["total_bytes"] += size

                stats["by_type"][content_type] = stats["by_type"].get(content_type, 0) + size
                stats["by_user"][uid] = stats["by_user"].get(uid, 0) + size
            except Exception:
                continue

        # If specific user requested, filter stats
        if user_id:
            user_bytes = stats["by_user"].get(user_id, 0)
            return {
                "user_id": user_id,
                "user_bytes": user_bytes,
                "user_files": sum(1 for r in index.get("refs", {}).values()
                                 if r.get("user_id") == user_id),
                "total_bytes": stats["total_bytes"]
            }

        return stats


# ============================================================================
# Singleton Instance
# ============================================================================

_external_memory_instance: Optional[ExternalMemory] = None


def get_external_memory(base_dir: Optional[Path] = None) -> ExternalMemory:
    """Get or create singleton ExternalMemory instance"""
    global _external_memory_instance
    if _external_memory_instance is None:
        _external_memory_instance = ExternalMemory(base_dir)
    return _external_memory_instance


# ============================================================================
# Integration with LocalMemory
# ============================================================================

class MemoryCompressor:
    """Helper class to integrate ExternalMemory with LocalMemory

    Usage:
        compressor = MemoryCompressor()

        # When adding memory
        compressed, ref = compressor.compress_if_needed(user_id, large_content, "code")
        local_memory.add(user_id, compressed, metadata={"has_external_ref": ref is not None})
    """

    def __init__(self, external_memory: Optional[ExternalMemory] = None):
        self.external = external_memory or get_external_memory()

    def compress_if_needed(
        self,
        user_id: str,
        content: str,
        content_type: str = "general",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, Optional[ExternalMemoryRef]]:
        """Compress content if it exceeds threshold"""
        return self.external.compress_for_memory(user_id, content, content_type, metadata)

    def expand_if_reference(self, content: str) -> str:
        """Expand content if it's an external reference

        Detects reference format: [type] summary (see: path)
        and retrieves full content
        """
        match = re.search(r'\(see: (.+?)\)', content)
        if match:
            file_path = match.group(1)
            full_content = self.external.retrieve_by_path(file_path)
            if full_content:
                return full_content
        return content


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    # Example usage
    ext_mem = ExternalMemory()
    user = "test_user"

    # Store large content
    large_code = """
def complex_function():
    '''This is a very long function with many lines'''
    # Line 1
    # Line 2
    # ... many more lines
    pass
""" * 20  # Make it large

    ref = ext_mem.store_large_content(user, large_code, "code", {"language": "python"})
    print(f"Stored externally: {ref.ref_id}")
    print(f"Memory format: {ref.to_memory_format()}")

    # Retrieve it back
    retrieved = ext_mem.retrieve_content(ref.ref_id)
    print(f"Retrieved length: {len(retrieved) if retrieved else 0}")

    # Todo.md management
    ext_mem.update_todo_md(user, "# Current Task\n\n## Goal\nImplement external memory")
    todo = ext_mem.get_todo_md(user)
    print(f"\nTodo.md content:\n{todo}")

    # Stats
    stats = ext_mem.get_storage_stats(user)
    print(f"\nStats: {stats}")

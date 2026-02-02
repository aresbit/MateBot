#!/usr/bin/env python3
"""Local Memory System for MateCode - SQLite-based long-term memory

Integrated with ExternalMemory for tiered storage:
- Small content (<500 chars): stored directly in SQLite
- Large content (>500 chars): stored in file system, reference in SQLite
"""

import hashlib
import json
import os
import re
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, Callable

# Import ExternalMemory for tiered storage
from external_memory import get_external_memory, ExternalMemoryRef


MEMORY_DIR = os.path.expanduser("~/.matecode")
MEMORY_DB = os.path.join(MEMORY_DIR, "memory.db")


class LocalMemory:
    """Local SQLite-based memory storage with FTS5 search.

    Tiered storage architecture:
    - Tier 1 (Working): Recent conversation context in memory
    - Tier 2 (Short-term): SQLite for quick access memories
    - Tier 3 (External): File system for large content via ExternalMemory
    """

    MAX_CONTENT_LENGTH = 10000
    DEFAULT_MESSAGE_TYPE = "conversation"

    # Threshold for external storage
    EXTERNAL_STORAGE_THRESHOLD = 500

    def __init__(self, db_path: str = MEMORY_DB):
        self.db_path = db_path
        # Only create directory for file-based databases
        if db_path != ":memory:":
            db_dir = os.path.dirname(db_path)
            if db_dir:  # Ensure db_dir is not empty
                os.makedirs(db_dir, exist_ok=True)
        self._external = get_external_memory()
        self._init_db()

    def _init_db(self) -> None:
        """Initialize SQLite database with FTS5."""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT,
                    message_type TEXT DEFAULT 'conversation'
                )
            """)
            conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS memory_search
                USING fts5(content, content_rowid=rowid)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_user_id ON memories(user_id)
            """)
            conn.commit()

    @contextmanager
    def _get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()


    def _generate_id(self, user_id: str, content: str) -> str:
        """Generate unique ID for memory entry."""
        data = f"{user_id}:{content}:{datetime.now().isoformat()}"
        return hashlib.md5(data.encode()).hexdigest()

    def _row_to_dict(self, row: Tuple, include_relevance: bool = False) -> Dict[str, Any]:
        """Convert database row to memory dictionary."""
        result = {
            "id": row[0],
            "content": row[1],
            "timestamp": row[2],
            "metadata": json.loads(row[3]) if row[3] else None,
        }
        if include_relevance and len(row) > 4:
            result["relevance"] = row[4]
        return result

    def add(self, user_id: str, content: str, metadata: Optional[Dict[str, Any]] = None,
            message_type: str = DEFAULT_MESSAGE_TYPE) -> bool:
        """Add a memory entry with tiered storage.

        - Content < 500 chars: stored directly in SQLite
        - Content >= 500 chars: stored in file system, reference in SQLite
        """
        if not content or not content.strip():
            return False

        content = content.strip()

        # Check if content should be stored externally (Manus: restorable compression)
        external_ref = None
        if len(content) >= self.EXTERNAL_STORAGE_THRESHOLD:
            compressed, ref = self._external.compress_for_memory(
                user_id, content, message_type, metadata
            )
            if ref:
                content = compressed
                external_ref = ref
                # Add external ref info to metadata
                if metadata is None:
                    metadata = {}
                metadata = {**metadata, "_external_ref": ref.ref_id, "_is_external": True}

        content = content[:self.MAX_CONTENT_LENGTH]
        memory_id = self._generate_id(user_id, content)
        metadata_json = json.dumps(metadata) if metadata else None

        try:
            with self._get_connection() as conn:
                conn.execute(
                    """INSERT OR REPLACE INTO memories
                       (id, user_id, content, timestamp, metadata, message_type)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (memory_id, user_id, content, datetime.now(), metadata_json, message_type)
                )
                conn.execute(
                    """INSERT OR REPLACE INTO memory_search(rowid, content)
                       VALUES ((SELECT rowid FROM memories WHERE id = ?), ?)""",
                    (memory_id, content)
                )
                conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding memory: {e}")
            return False

    def search(self, user_id: str, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search memories using FTS5."""
        if not query or not query.strip():
            return []

        sanitized_query = self._sanitize_query(query)
        if not sanitized_query:
            return []

        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    """SELECT m.id, m.content, m.timestamp, m.metadata, rank
                       FROM memories m
                       JOIN memory_search s ON m.rowid = s.rowid
                       WHERE m.user_id = ? AND memory_search MATCH ?
                       ORDER BY rank
                       LIMIT ?""",
                    (user_id, sanitized_query, limit)
                )
                return [self._row_to_dict(row, include_relevance=True) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error searching memories: {e}")
            return []

    def get_recent(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent memories without search."""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    """SELECT id, content, timestamp, metadata
                       FROM memories
                       WHERE user_id = ?
                       ORDER BY timestamp DESC
                       LIMIT ?""",
                    (user_id, limit)
                )
                return [self._row_to_dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error getting recent memories: {e}")
            return []

    def get_by_type(self, user_id: str, message_type: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get memories by message type."""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    """SELECT id, content, timestamp, metadata
                       FROM memories
                       WHERE user_id = ? AND message_type = ?
                       ORDER BY timestamp DESC
                       LIMIT ?""",
                    (user_id, message_type, limit)
                )
                return [self._row_to_dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error getting memories by type: {e}")
            return []

    def delete(self, user_id: str, memory_id: str) -> bool:
        """Delete a specific memory by ID."""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "SELECT rowid FROM memories WHERE id = ? AND user_id = ?",
                    (memory_id, user_id)
                )
                row = cursor.fetchone()
                if not row:
                    return False

                rowid = row[0]
                conn.execute("DELETE FROM memory_search WHERE rowid = ?", (rowid,))
                conn.execute("DELETE FROM memories WHERE id = ? AND user_id = ?", (memory_id, user_id))
                conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting memory: {e}")
            return False

    def delete_by_query(self, user_id: str, query: str) -> int:
        """Delete memories matching a query."""
        matches = self.search(user_id, query, limit=100)
        return sum(1 for mem in matches if self.delete(user_id, mem["id"]))

    def clear_all(self, user_id: str) -> bool:
        """Clear all memories for a user."""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute("SELECT rowid FROM memories WHERE user_id = ?", (user_id,))
                rowids = [row[0] for row in cursor.fetchall()]

                for rowid in rowids:
                    conn.execute("DELETE FROM memory_search WHERE rowid = ?", (rowid,))

                conn.execute("DELETE FROM memories WHERE user_id = ?", (user_id,))
                conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error clearing memories: {e}")
            return False

    def get_stats(self, user_id: str) -> Dict[str, Any]:
        """Get memory statistics for a user."""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "SELECT COUNT(*), MAX(timestamp), MIN(timestamp) FROM memories WHERE user_id = ?",
                    (user_id,)
                )
                count, newest, oldest = cursor.fetchone()

                type_cursor = conn.execute(
                    "SELECT message_type, COUNT(*) FROM memories WHERE user_id = ? GROUP BY message_type",
                    (user_id,)
                )
                by_type = dict(type_cursor.fetchall())

            return {
                "count": count or 0,
                "newest": newest,
                "oldest": oldest,
                "by_type": by_type
            }
        except sqlite3.Error as e:
            print(f"Error getting stats: {e}")
            return {"count": 0, "newest": None, "oldest": None, "by_type": {}}

    def _sanitize_query(self, query: str) -> str:
        """Sanitize query string for FTS5."""
        query = re.sub(r"[^\w\s\-_.]", " ", query)
        words = [w for w in query.split() if len(w) >= 2]
        return " AND ".join(f"{word}*" for word in words) if words else ""

    def _expand_external_refs(self, memories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Expand external references in memories when needed."""
        expanded = []
        for mem in memories:
            metadata = mem.get("metadata") or {}
            if metadata.get("_is_external") and metadata.get("_external_ref"):
                # Store reference info but keep compact for display
                mem["_external_ref_id"] = metadata["_external_ref"]
                mem["_has_full_content"] = True
            expanded.append(mem)
        return expanded

    def get_full_content(self, memory: Dict[str, Any]) -> Optional[str]:
        """Retrieve full content for a memory with external reference."""
        ref_id = memory.get("_external_ref_id")
        if ref_id:
            return self._external.retrieve_content(ref_id)
        return memory.get("content")

    def format_for_prompt(self, memories: List[Dict], max_chars: int = 2000, expand_external: bool = False) -> str:
        """Format memories for injection into Claude prompt.

        Args:
            memories: List of memory dicts
            max_chars: Maximum characters in output
            expand_external: If True, expand external references to full content
        """
        if not memories:
            return ""

        memories = self._expand_external_refs(memories)

        lines = ["【历史记忆】", ""]
        current_len = len("【历史记忆】\n\n")

        for mem in memories:
            content = mem["content"]

            # Optionally expand external references
            if expand_external and mem.get("_has_full_content"):
                full = self.get_full_content(mem)
                if full:
                    content = full

            content = content.replace("\n", " ")
            line = f"• {content}"

            if current_len + len(line) + 1 > max_chars:
                break

            lines.append(line)
            current_len += len(line) + 1

        return "\n".join(lines)

    # =========================================================================
    # Todo.md Integration - Attention Redirection
    # =========================================================================

    def get_todo_md(self, user_id: str, task_id: str = "default") -> str:
        """Get current task todo.md for attention redirection (Manus pattern)."""
        return self._external.get_todo_md(user_id, task_id)

    def update_todo_md(self, user_id: str, content: str, task_id: str = "default", append: bool = False) -> bool:
        """Update todo.md to keep goals front-of-mind."""
        return self._external.update_todo_md(user_id, content, task_id, append)

    def list_active_tasks(self, user_id: str) -> List[Dict[str, Any]]:
        """List all active task todos for a user."""
        return self._external.list_tasks(user_id)


_memory_instance: Optional[LocalMemory] = None


def get_memory() -> LocalMemory:
    """Get or create singleton memory instance."""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = LocalMemory()
    return _memory_instance


if __name__ == "__main__":
    mem = LocalMemory()

    mem.add("user_123", "Python is a great programming language")
    mem.add("user_123", "I prefer using SQLite for local storage")
    mem.add("user_123", "Machine learning is fascinating")

    print("Search 'python':")
    for r in mem.search("user_123", "python"):
        print(f"  - {r['content']}")

    print("\nSearch 'storage':")
    for r in mem.search("user_123", "storage"):
        print(f"  - {r['content']}")

    print(f"\nStats: {mem.get_stats('user_123')}")

#!/bin/bash
# 实时查看 MateBot 记忆系统

DB="${HOME}/.matecode/memory.db"

if [ ! -f "$DB" ]; then
    echo "❌ 数据库不存在: $DB"
    exit 1
fi

echo "=== 📚 MateBot 记忆系统 ==="
echo "数据库: $DB"
echo ""

sqlite3 "$DB" << 'SQL'
.headers on
.mode column
SELECT 
    substr(user_id, 1, 8) as user,
    message_type as type,
    substr(content, 1, 50) as content_preview,
    timestamp
FROM memories
ORDER BY timestamp DESC
LIMIT 10;
SQL

echo ""
echo "=== 统计 ==="
sqlite3 "$DB" "SELECT '总记录: ' || COUNT(*) || ' | 用户: ' || COUNT(DISTINCT user_id) FROM memories;"

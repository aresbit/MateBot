#!/usr/bin/env python3
"""
Convert code repository to formatted text for LLM analysis.
Similar to https://repo2txt.simplebasedomain.com/ but runs locally.
"""

import os
import sys
import argparse
import fnmatch
from pathlib import Path


DEFAULT_IGNORE_PATTERNS = [
    # Version control
    '.git',
    '.svn',
    '.hg',
    # Dependencies
    'node_modules',
    'vendor',
    '__pycache__',
    '.venv',
    'venv',
    'env',
    '.env',
    # Build outputs
    'dist',
    'build',
    'target',
    'out',
    '.output',
    # IDE
    '.idea',
    '.vscode',
    '.vs',
    # Logs
    '*.log',
    'logs',
    # Test coverage
    'coverage',
    '.coverage',
    'htmlcov',
    '.nyc_output',
    # OS files
    '.DS_Store',
    'Thumbs.db',
    # Package manager
    'package-lock.json',
    'yarn.lock',
    'pnpm-lock.yaml',
    'Pipfile.lock',
    'poetry.lock',
    'Cargo.lock',
    'Gemfile.lock',
    'composer.lock',
    # Binary/Generated files
    '*.pyc',
    '*.pyo',
    '*.so',
    '*.dll',
    '*.exe',
    '*.bin',
    '*.min.js',
    '*.min.css',
    '*.map',
    '*.svg',
    '*.png',
    '*.jpg',
    '*.jpeg',
    '*.gif',
    '*.ico',
    '*.woff',
    '*.woff2',
    '*.ttf',
    '*.eot',
    '*.pdf',
    '*.zip',
    '*.tar',
    '*.gz',
    '*.rar',
    '*.7z',
    '*.mp3',
    '*.mp4',
    '*.avi',
    '*.mov',
    '*.webm',
    # Large data files
    '*.csv',
    '*.json',
    'package.json',
    'tsconfig.json',
    'jest.config.js',
    'vite.config.ts',
    'webpack.config.js',
    'eslint.config.js',
    'tailwind.config.js',
    'postcss.config.js',
    '.babelrc',
    # Misc
    '.next',
    '.nuxt',
    '.svelte-kit',
    '.cache',
    'tmp',
    'temp',
]


def should_ignore(path, ignore_patterns):
    """Check if a path should be ignored based on patterns."""
    path_parts = Path(path).parts
    name = os.path.basename(path)

    for pattern in ignore_patterns:
        # Check if any part of the path matches
        for part in path_parts:
            if fnmatch.fnmatch(part, pattern):
                return True
        # Check if the name matches
        if fnmatch.fnmatch(name, pattern):
            return True
    return False


def get_file_extension(filename):
    """Get file extension for categorization."""
    return os.path.splitext(filename)[1].lower()


def categorize_file(filepath):
    """Categorize a file by its extension."""
    ext = get_file_extension(filepath)
    categories = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.jsx': 'React',
        '.tsx': 'React/TS',
        '.vue': 'Vue',
        '.svelte': 'Svelte',
        '.html': 'HTML',
        '.css': 'CSS',
        '.scss': 'SCSS',
        '.sass': 'Sass',
        '.less': 'Less',
        '.json': 'JSON',
        '.xml': 'XML',
        '.yaml': 'YAML',
        '.yml': 'YAML',
        '.md': 'Markdown',
        '.rs': 'Rust',
        '.go': 'Go',
        '.java': 'Java',
        '.kt': 'Kotlin',
        '.scala': 'Scala',
        '.c': 'C',
        '.cpp': 'C++',
        '.h': 'C/C++ Header',
        '.hpp': 'C++ Header',
        '.cs': 'C#',
        '.php': 'PHP',
        '.rb': 'Ruby',
        '.swift': 'Swift',
        '.m': 'Objective-C',
        '.mm': 'Objective-C++',
        '.r': 'R',
        '.jl': 'Julia',
        '.ex': 'Elixir',
        '.exs': 'Elixir Script',
        '.erl': 'Erlang',
        '.hs': 'Haskell',
        '.ml': 'OCaml',
        '.mli': 'OCaml Interface',
        '.fs': 'F#',
        '.fsx': 'F# Script',
        '.clj': 'Clojure',
        '.cljs': 'ClojureScript',
        '.lua': 'Lua',
        '.sh': 'Shell',
        '.bash': 'Bash',
        '.zsh': 'Zsh',
        '.fish': 'Fish',
        '.ps1': 'PowerShell',
        '.sql': 'SQL',
        '.dockerfile': 'Dockerfile',
        '.dockerignore': 'Docker Ignore',
        '.gitignore': 'Git Ignore',
        '.gitattributes': 'Git Attributes',
        '.env': 'Environment',
        '.toml': 'TOML',
        '.ini': 'INI',
        '.cfg': 'Config',
        '.conf': 'Config',
        '.cmake': 'CMake',
        '.make': 'Makefile',
        '.mk': 'Makefile',
        'Makefile': 'Makefile',
        '.gradle': 'Gradle',
        '.sbt': 'SBT',
        '.ivy': 'Ivy',
        '.pom': 'Maven POM',
        '.proto': 'Protocol Buffers',
        '.graphql': 'GraphQL',
        '.prisma': 'Prisma',
    }
    return categories.get(ext, 'Other')


def collect_files(repo_path, ignore_patterns, include_extensions=None, exclude_extensions=None):
    """Collect all files from the repository."""
    files = []

    for root, dirs, filenames in os.walk(repo_path):
        # Filter out ignored directories
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), ignore_patterns)]

        for filename in filenames:
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, repo_path)

            # Skip ignored files
            if should_ignore(rel_path, ignore_patterns):
                continue

            # Check extension filters
            ext = get_file_extension(filename)
            if include_extensions and ext not in include_extensions:
                continue
            if exclude_extensions and ext in exclude_extensions:
                continue

            files.append(rel_path)

    return sorted(files)


def generate_tree(files, repo_path):
    """Generate a tree-like representation of the file structure."""
    lines = []
    lines.append("=" * 80)
    lines.append("DIRECTORY STRUCTURE")
    lines.append("=" * 80)
    lines.append("")

    # Build tree structure
    tree = {}
    for f in files:
        parts = f.split(os.sep)
        current = tree
        for part in parts:
            if part not in current:
                current[part] = {}
            current = current[part]

    def print_tree(node, prefix="", is_last=True):
        items = list(node.items())
        for i, (name, children) in enumerate(items):
            is_last_item = (i == len(items) - 1)
            connector = "└── " if is_last_item else "├── "
            lines.append(f"{prefix}{connector}{name}")
            if children:
                new_prefix = prefix + ("    " if is_last_item else "│   ")
                print_tree(children, new_prefix, is_last_item)

    print_tree(tree)
    return "\n".join(lines)


def generate_file_contents(files, repo_path):
    """Generate formatted content for each file."""
    lines = []
    lines.append("")
    lines.append("=" * 80)
    lines.append("FILE CONTENTS")
    lines.append("=" * 80)
    lines.append("")

    for filepath in files:
        full_path = os.path.join(repo_path, filepath)
        category = categorize_file(filepath)

        lines.append("-" * 80)
        lines.append(f"File: {filepath}")
        lines.append(f"Type: {category}")
        lines.append("-" * 80)
        lines.append("")

        try:
            # Try to read as text
            with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

            # Skip binary or very large files
            if len(content) > 1000000:  # Skip files larger than 1MB
                lines.append(f"[File too large: {len(content)} bytes]")
            elif '\0' in content:
                lines.append("[Binary file - content skipped]")
            else:
                lines.append(content)
        except Exception as e:
            lines.append(f"[Error reading file: {e}]")

        lines.append("")
        lines.append("")

    return "\n".join(lines)


def generate_summary(files, repo_path):
    """Generate a summary of the repository."""
    lines = []
    lines.append("=" * 80)
    lines.append("REPOSITORY SUMMARY")
    lines.append("=" * 80)
    lines.append("")

    # Count files by type
    type_counts = {}
    total_lines = 0
    total_size = 0

    for filepath in files:
        category = categorize_file(filepath)
        type_counts[category] = type_counts.get(category, 0) + 1

        full_path = os.path.join(repo_path, filepath)
        try:
            size = os.path.getsize(full_path)
            total_size += size

            if size < 1000000:  # Only count lines for reasonably sized files
                with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
                    total_lines += len(f.readlines())
        except:
            pass

    lines.append(f"Total Files: {len(files)}")
    lines.append(f"Total Lines: {total_lines:,}")
    lines.append(f"Total Size: {total_size / 1024:.1f} KB")
    lines.append("")
    lines.append("Files by Type:")

    for file_type, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        lines.append(f"  {file_type}: {count}")

    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Convert code repository to formatted text for LLM analysis'
    )
    parser.add_argument('path', help='Path to the repository')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('-e', '--extensions',
                        help='Comma-separated list of extensions to include (e.g., .py,.js,.ts)')
    parser.add_argument('-x', '--exclude-extensions',
                        help='Comma-separated list of extensions to exclude')
    parser.add_argument('-i', '--ignore',
                        help='Additional patterns to ignore (comma-separated)')
    parser.add_argument('--no-tree', action='store_true',
                        help='Skip directory tree generation')
    parser.add_argument('--no-summary', action='store_true',
                        help='Skip summary generation')
    parser.add_argument('--max-file-size', type=int, default=1000000,
                        help='Maximum file size in bytes (default: 1000000)')

    args = parser.parse_args()

    repo_path = os.path.abspath(args.path)
    if not os.path.isdir(repo_path):
        print(f"Error: {repo_path} is not a valid directory", file=sys.stderr)
        sys.exit(1)

    # Build ignore patterns
    ignore_patterns = DEFAULT_IGNORE_PATTERNS.copy()
    if args.ignore:
        ignore_patterns.extend(args.ignore.split(','))

    # Parse extension filters
    include_extensions = None
    if args.extensions:
        include_extensions = [e.strip() for e in args.extensions.split(',')]

    exclude_extensions = None
    if args.exclude_extensions:
        exclude_extensions = [e.strip() for e in args.exclude_extensions.split(',')]

    # Collect files
    print(f"Scanning {repo_path}...", file=sys.stderr)
    files = collect_files(repo_path, ignore_patterns, include_extensions, exclude_extensions)
    print(f"Found {len(files)} files", file=sys.stderr)

    # Generate output
    output_lines = []

    if not args.no_summary:
        output_lines.append(generate_summary(files, repo_path))

    if not args.no_tree:
        output_lines.append(generate_tree(files, repo_path))

    output_lines.append(generate_file_contents(files, repo_path))

    # Write output
    result = "\n".join(output_lines)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Output written to {args.output}", file=sys.stderr)
    else:
        print(result)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Find duplicate annexed files in a git-annex repository.

This script identifies files that point to the same annexed content
by grouping files with identical annex keys.
"""

import subprocess
import sys
from collections import defaultdict
import argparse


def get_annexed_files():
    """Get all annexed files with their keys using git-annex find."""
    try:
        result = subprocess.run(
            ["git", "annex", "find", "--format=${key} ${file}\\n"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip().split("\n")
    except subprocess.CalledProcessError as e:
        print(f"Error running git-annex find: {e}", file=sys.stderr)
        sys.exit(1)


def parse_annexed_files(lines: list[str]):
    """Parse the output from git-annex find into key->files mapping."""
    key_to_files = defaultdict(list)

    for line in lines:
        if not line.strip():
            continue

        parts = line.split(" ", 1)
        if len(parts) == 2:
            key, filepath = parts
            key_to_files[key].append(filepath)

    return key_to_files


def find_duplicates(key_to_files):
    """Find keys that have multiple files pointing to them."""
    duplicates = {}

    for key, files in key_to_files.items():
        if len(files) > 1:
            duplicates[key] = files

    return duplicates


def format_size(size_str):
    """Extract and format file size from annex key."""
    # MD5E keys have format: MD5E-s<size>--<hash>.<ext>
    try:
        if "-s" in size_str:
            size_part = size_str.split("-s")[1].split("--")[0]
            size_bytes = int(size_part)

            # Convert to human readable
            for unit in ["B", "KB", "MB", "GB"]:
                if size_bytes < 1024:
                    return f"{size_bytes:.1f} {unit}"
                size_bytes /= 1024
            return f"{size_bytes:.1f} TB"
    except (ValueError, IndexError):
        pass

    return "unknown size"


def main():
    parser = argparse.ArgumentParser(description="Find duplicate annexed files")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed output"
    )
    parser.add_argument(
        "--summary", "-s", action="store_true", help="Show only summary statistics"
    )
    parser.add_argument(
        "--min-duplicates",
        "-m",
        type=int,
        default=2,
        help="Minimum number of duplicates to report (default: 2)",
    )

    args = parser.parse_args()

    print("Scanning annexed files for duplicates...")

    # Get all annexed files
    lines = get_annexed_files()
    key_to_files = parse_annexed_files(lines)

    # Find duplicates
    duplicates = find_duplicates(key_to_files)

    # Filter by minimum duplicates
    filtered_duplicates = {
        k: v for k, v in duplicates.items() if len(v) >= args.min_duplicates
    }

    if args.summary:
        total_files = sum(len(files) for files in key_to_files.values())
        duplicate_files = sum(len(files) for files in filtered_duplicates.values())
        duplicate_groups = len(filtered_duplicates)

        print(f"\nSummary:")
        print(f"Total annexed files: {total_files}")
        print(f"Files that are duplicates: {duplicate_files}")
        print(f"Duplicate groups: {duplicate_groups}")
        print(
            f"Space potentially wasted: {duplicate_files - duplicate_groups} file copies"
        )
        return

    if not filtered_duplicates:
        print("No duplicate annexed files found!")
        return

    print(f"\nFound {len(filtered_duplicates)} sets of duplicate files:")
    print("=" * 60)

    for i, (key, files) in enumerate(
        sorted(filtered_duplicates.items(), key=lambda x: len(x[1]), reverse=True), 1
    ):
        size = format_size(key)
        print(f"\n{i}. Duplicate set (Key: {key})")
        print(f"   Size: {size}")
        print(f"   {len(files)} copies:")

        for filepath in sorted(files):
            if args.verbose:
                print(f"     {filepath}")
            else:
                # Truncate long paths for readability
                if len(filepath) > 70:
                    print(f"     ...{filepath[-67:]}")
                else:
                    print(f"     {filepath}")


if __name__ == "__main__":
    main()

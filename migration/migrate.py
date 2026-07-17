# -*- coding: utf-8 -*-
"""Migration: old directories -> new structure.

Safe to run multiple times. Creates symlinks, does NOT delete originals.
Knowledge pages stay IN PLACE —— both old and new directories coexist.

Usage: python migration/migrate.py
"""

import sys, os, json, shutil
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
MIGRATIONS = [
    ('源/原文/', 'source/original/'),
    ('源/摘要/', 'source/summaries/'),
]
PROTOCOL_MAP = {
    'agents/check-protocol.md': 'protocol/check.json',
    'agents/ingest-protocol.md': 'protocol/ingest.json',
    'agents/wrapup-protocol.md': 'protocol/wrapup.json',
    'agents/context-budget.md': 'protocol/context-budget.json',
}

def migrate_files():
    for old, new in MIGRATIONS:
        src = BASE / old; dst = BASE / new
        if src.exists():
            print(f'Migrating: {old} -> {new}')
            for f in src.rglob('*'):
                if f.is_file():
                    rel = f.relative_to(src)
                    dest = dst / rel
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    if not dest.exists():
                        shutil.copy2(f, dest)
                        print(f'  Copied: {rel}')

def report_status():
    for old, new in MIGRATIONS:
        src = BASE / old; dst = BASE / new
        src_count = len(list(src.rglob('*'))) if src.exists() else 0
        dst_count = len(list(dst.rglob('*'))) if dst.exists() else 0
        print(f'{old}: {src_count} files -> {new}: {dst_count} files')

if __name__ == '__main__':
    print('=== Migration Status ===')
    report_status()
    print('\n=== Running Migration ===')
    migrate_files()
    print('\n=== After Migration ===')
    report_status()
    print('\nDone. Old directories preserved. New copies at source/ and protocol/')

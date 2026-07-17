# Agent Runtime — Your Personal AI Operating System

A general-purpose agent runtime that turns your markdown knowledge base into a self-maintaining, self-remembering system.

## What It Does

- **Auto-check** your knowledge base for stale pages and broken links
- **Auto-ingest** any URL or local file into structured knowledge
- **Remember** what happened in every session (Memory Store L0-L4)
- **Coordinate** multiple AI agents without conflicts (StateManager + EventBus)
- **Extend** with your own protocols (just write a JSON file)

## 5-Minute Start

`ash
cd D:/my-wiki
python agents/wiki-agent.py  # Run a check on your knowledge base
python migration/migrate.py  # Migrate old files to new structure
python executor/executor.py  # Execute a protocol directly
`

## Architecture

`
knowledge/  81 JSON sidecars — machine-readable metadata for every page
protocol/   JSON protocol definitions — what the system can do
executor/   Protocol Executor — runs protocol steps automatically
state/      State files — what is happening right now
memory/     Memory Store — what happened before (L0-L4)
planner/    Planner — picks tasks, matches protocols, executes
event-bus/  Event Bus — components communicate via typed events
graphs/     Dependency Graph — 81 nodes, 380 edges of knowledge relationships
`

## Make It Yours

1. Fork the repo
2. Add your own knowledge pages (Markdown with YAML frontmatter)
3. Run python agents/wiki-agent.py check to validate
4. Define your own protocols in protocol/*.json following protocol/TEMPLATE.json
5. Add custom handlers in executor/executor.py

No domain-specific code. Everything is pluggable.

## Status

v0.3.0-develop. Phase 0-3 complete. See CHANGELOG.md for details.

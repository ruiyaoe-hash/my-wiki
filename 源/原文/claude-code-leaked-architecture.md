---
type: source
title: "Claude Code 源码架构分析"
description: "Claude Code npm源码泄露分析，揭示BUDDY/Dream/KAIROS/ULTRAPLAN等内部架构"
timestamp: "2026-03-31T00:00:00Z"
created: 2026-07-08
tags: [claude-code, Anthropic, agent architecture, harness, source-leak]
status: archived
source: https://github.com/yasasbanukaofficial/claude-code
source_label: yasasbanukaofficial/claude-code GitHub仓库 (Claude Code源码泄露镜像)
---

# claude-code leaked source analysis
(Yasas Banuka mirror of the Claude Code npm sourcemap leak)

Key architectural insights from the leaked codebase:

## Entry point
- 785KB main.tsx with custom React terminal renderer (Ink)
- 40+ tools, complex multi-agent orchestration

## BUDDY - Terminal Tamagotchi
- Deterministic Gacha using Mulberry32 PRNG seeded from userId
- 18 Species from Common (Pebblecrab) to Legendary (Nebulynx)
- Stats: DEBUGGING, CHAOS, SNARK with soul descriptions written by Claude

## Undercover Mode
- For Anthropic employees using Claude Code on public repos
- Blocks internal model codenames (Capybara, Tengu)
- Hides that the user is an AI
- Confirms "Tengu" is likely the internal codename for Claude Code

## Dream System
- autoDream service runs as background subagent
- 1. Orient: Read MEMORY.md
- 2. Gather: Find new signals from daily logs
- 3. Consolidate: Update durable memory files
- 4. Prune: Keep context efficient

## KAIROS & ULTRAPLAN
- KAIROS: Always-on proactive assistant watching logs
- ULTRAPLAN: Offloads complex tasks to remote Opus 4.6 session for up to 30 min of deep planning

## Directory Structure
src/
  main.tsx — CLI Entrypoint (Commander.js + React/Ink)
  QueryEngine.ts — Core LLM logic
  Tool.ts — Base tool definitions
  tools/ — 40+ Agent tools (Bash, Files, LSP, Web)
  services/ — Backend (MCP, OAuth, Analytics, Dreams)
  coordinator/ — Multi-agent orchestration (Swarm)
  bridge/ — IDE Integration layer
  buddy/ — Tamagotchi system

Source: npm package sourcemap leak discovered by Chaofan Shou (@Fried_rice), March 31, 2026

# Conflict Resolution Merger Skill for Autonomous Agents

[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-blue.svg)](https://modelcontextprotocol.io)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-brightgreen.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero External Dependencies](https://img.shields.io/badge/dependencies-zero-success.svg)](requirements.txt)

Robust 3-way text and document reconciliation engine enabling multiple concurrent agents to modify shared workspaces, markdown documents, and source code files without overwriting each other's edits.

## Features
- **3-Way Line Reconciliation**: Reconciles Common Base against Agent A and Agent B changes.
- **Conflict Markers & Journaling**: Formats clean Git-style markers or returns structured conflict objects for automated LLM re-arbitration.
- **Zero Dependencies**: Pure Python standard library diff algorithms.

## MCP Server Integration
```bash
python mcp_server.py
```

### Available MCP Tools
- `merge_3way`: Merge two divergent agent modifications against an original base.
- `detect_conflicts`: Analyze whether two edits can be merged without collision.

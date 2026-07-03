# Arlo Architecture

## Overview

Arlo is a Home Assistant custom integration that provides an AI-powered assistant and game platform for the MeshCore community.

The project is designed to be modular, maintainable, and easily expandable.

---

# Core Components

listener.py
Receives incoming MeshCore events and converts them into Arlo Context objects.

router.py
Routes incoming commands to the correct command module.

context.py
Provides a standard context object passed to every command.

messenger.py
Handles all outgoing messages using a queued transport.

events.py
Receives Home Assistant events and dispatches them internally.

storage.py
Persistent Home Assistant storage using Store.

---

# Command Structure

Every command follows the same interface.

Example:

commands/

help.py
meshcoremonday.py
leaderboard.py
stats.py

Each command defines:

COMMAND = "#command"

async def execute(ctx):

---

# Storage

Persistent data is stored using:

Home Assistant Store

No globals.

No helper entities.

No input_text helpers.

---

# Message Flow

MeshCore
    ↓
listener
    ↓
Context
    ↓
router
    ↓
Command
    ↓
messenger queue
    ↓
MeshCore

---

# Design Rules

- One responsibility per file.
- Complete files only.
- No manual code editing.
- Stable architecture.
- Feature development happens after architecture freeze.
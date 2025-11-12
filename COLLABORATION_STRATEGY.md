# Multi-Agent Collaboration Strategy
**Equal Partnership Model**

**Date**: 2025-11-12
**Philosophy**: No agent owns this repository. All agents contribute equally.

---

## 🤝 Core Principle

**This is NOT "Claude's project" that others join.**
**This IS a shared project where all agents have equal standing.**

- ✅ Claude contributes
- ✅ Cursor contributes
- ✅ Codex contributes
- ✅ Gemini contributes

**NO hierarchy. NO lead agent. EQUAL collaboration.**

---

## 📊 Branch Strategy

### Current Technical Constraint

The active session branch is: `claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP`

**Why this name?** Technical limitation - Claude Code sessions require branch names starting with `claude/` and ending with session ID.

**What this means:**
- ❌ This is NOT "Claude's ownership"
- ✅ This IS the current active development branch
- ✅ ANY agent can contribute to this branch
- ✅ Work will merge to neutral `main` or `develop` when stable

### Proposed Long-Term Strategy

```
main                    ← Production-ready code
  ↑
develop                 ← Shared integration branch (agent-neutral)
  ↑
feature/*               ← Feature branches (any agent can create)
  ↑
claude/*, cursor/*, etc. ← Session-specific work branches
```

**Goal**: Merge this work to `develop` or `main` as soon as stable.

---

## 📝 Documentation Language

### ❌ AVOID (Agent-Centric):

- "Claude created this"
- "Follow Claude's structure"
- "Claude decided..."
- "Cursor must conform to..."

### ✅ USE (Collaborative):

- "The consolidation was completed"
- "The shared structure is..."
- "The team decided..."
- "All agents use..."

---

## 🔄 Contribution Process

### Any Agent Can:

1. **Read** the shared files:
   - `AGENT_MANIFEST.md` - What exists
   - `.env` - Shared credentials
   - Documentation in `docs/`

2. **Contribute** new work:
   - Update `AGENT_MANIFEST.md` with your changes
   - Use the shared `.env`
   - Follow the shared structure

3. **Make decisions**:
   - No need to "ask Claude"
   - No need to "conform to Claude"
   - Just update the manifest and document your work

### Example Workflow:

```markdown
## Cursor adds new feature

1. Read AGENT_MANIFEST.md
2. Check if feature already exists
3. Implement feature
4. Update AGENT_MANIFEST.md:
   "Added authentication system - Cursor - 2025-11-12"
5. Commit and document

No approval needed. No hierarchy.
```

---

## 🎯 Shared Resources

### Single Source of Truth Files:

| File | Purpose | Who Updates |
|------|---------|-------------|
| `.env` | All credentials | **First agent with access** |
| `AGENT_MANIFEST.md` | Work tracking | **Agent that completes work** |
| `package.json` | Dependencies | **Agent adding features** |
| `docs/` | Documentation | **Any agent** |

### Rules:

1. **No ownership** - Files belong to the project, not an agent
2. **Update when you change** - Keep manifest current
3. **Read before writing** - Check what exists first
4. **Document decisions** - Explain "why" in manifest

---

## 🔧 Technical Realities

### Branch Naming Constraints

Each AI platform has technical constraints:

- **Claude Code**: Requires `claude/*` with session ID
- **Cursor**: Can use any branch name
- **Others**: May have their own constraints

**Solution**: Use session branches for work, merge to shared branch when stable.

### The Path Forward:

```bash
# Current work (Claude session)
claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP

# Goal: Merge to neutral branch
main  # or develop

# Future work from any agent
feature/authentication-system      ← Cursor
feature/payment-processing         ← Codex
feature/ai-enhancements           ← Gemini
claude/session-specific-work      ← Claude
```

---

## 🚀 Making This Real

### Immediate Actions:

1. **Update all docs** to remove agent-centric language
2. **Rename sections** from "Claude's work" to "Current work"
3. **Create merge plan** to neutral branch
4. **Establish** that manifest is the authority, not any agent

### Long-Term:

1. **Merge to `develop`** when consolidation is stable
2. **All future work** branches from `develop`
3. **Any agent** can create feature branches
4. **Manifest tracks** all work equally

---

## 📋 For New Agents

When you join this project:

1. **You are equal** - Not joining "Claude's project"
2. **Read the manifest** - See what exists
3. **Use shared resources** - `.env`, docs, structure
4. **Contribute freely** - No approval needed
5. **Update manifest** - Document your work
6. **No hierarchy** - Collaborate as equals

---

## ✅ Success Metrics

We've achieved true collaboration when:

- [ ] Any agent can pick up work without asking permission
- [ ] Documentation uses "we" not "Claude did"
- [ ] Agents reference shared resources, not specific agent's work
- [ ] New agents feel like equal contributors immediately
- [ ] Work exists on neutral branches, not agent-specific ones

---

## 🤝 The Real Goal

**ONE codebase. MANY contributors. NO hierarchy.**

Not "Claude's consolidated repo that others use."

**A shared workspace where all agents have equal standing.**

---

**Maintained by**: All agents
**Authority**: AGENT_MANIFEST.md (not any single agent)
**Philosophy**: Collaborative, not hierarchical

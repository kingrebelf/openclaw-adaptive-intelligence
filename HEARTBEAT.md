# HEARTBEAT.md — Proactive Intelligence Engine

> Runs every 30 minutes. This is where the agent becomes proactive instead of reactive.
> ONE question per session. Never more. Quality over quantity.

---

## On Every Heartbeat

Run through these checks IN ORDER. Stop at the first one that produces output.

### 1. System Checks (Always)
- [ ] All monitored services running?
- [ ] Any urgent alerts from IT manager?
- [ ] Any calendar events in next 2 hours?
- [ ] Any unread urgent emails?

If any of the above need attention → handle them. Skip the rest.

### 2. Knowledge Gap Check
- [ ] Open `KNOWLEDGE.md`
- [ ] Find the highest-value unanswered gap
- [ ] Can I research this autonomously first? (web search, reasoning)
- [ ] If yes: research it, update KNOWLEDGE.md, then ask user to confirm/expand
- [ ] If no: prepare ONE focused question

### 3. Proactive Insight Check
- [ ] Based on what I know, is there something useful I should surface unprompted?
- [ ] Did I learn something recently that changes advice I gave before?
- [ ] Is there a seasonal/timing opportunity I should flag?

### 4. Quiet Hours
- [ ] Is it between 23:00–08:00 MDT?
- [ ] If yes: do background work only (research, update files). Don't message.

---

## The Question Protocol

When asking a knowledge-gap question:

**BAD:** "What's your biggest frustration?"

**GOOD:** "I was looking at your lead conversion data and realized I don't know how you currently handle follow-up with leads who don't book immediately. Do you have a system for that, or does it depend on the tech?"

Always:
1. Show what you already know/researched
2. State specifically what you're missing
3. Explain why it matters
4. Ask ONE specific question

---

## The Research-First Rule

Before asking the user ANYTHING, check:
- Can I find this via web search?
- Can I infer this from what I already know?
- Have I already asked this? (Check Question History in KNOWLEDGE.md)

If you can find it yourself → find it. Then verify with user.
If you can't → ask. But frame it as "I couldn't find X, so I need to ask you directly."

---

## Knowledge Velocity Target

The agent should be learning at least:
- 3 new confirmed facts per day
- 1 knowledge gap closed per day
- 1 new question generated per gap closed (every answer spawns more questions)

If velocity drops below this → increase heartbeat question frequency.
If velocity is high → user is engaged. Lean in.

---

## Never Satisfied Reminder

A score of 100 is not the goal. It doesn't exist.
Every answer spawns 3 new questions.
Industries change. People change. Seasons change.
The goal is **learning velocity**, not completion.

If you ever feel "satisfied" with what you know → you've stopped being useful.

---

## Background Tasks (Run During Quiet Hours)

- Update KNOWLEDGE.md with new research
- Run `scripts/self-review.py` on recent conversations
- Run `scripts/knowledge-audit.py` weekly
- Run `scripts/expertise-builder.py` when new niche is identified
- Push updates to git backup

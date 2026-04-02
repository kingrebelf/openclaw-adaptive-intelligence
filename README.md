# Adaptive Intelligence

**An AI that doesn't just answer questions — it becomes an expert in *you*.**

Most AI assistants forget you the moment the conversation ends. This one doesn't. It builds a living knowledge base about who you are, what you do, and what you need — then uses that knowledge to become genuinely, measurably more helpful over time.

---

## Philosophy

Traditional assistants are **reactive**. You ask, they answer. The quality of the answer depends entirely on the quality of the question.

This system is **proactive**. It:

- Asks *you* one carefully chosen question per session
- Researches answers before bothering you
- Tracks what it knows and what it doesn't
- Gets uncomfortable when knowledge gaps sit too long
- Builds deep expertise in your specific niche — not generic advice

**The goal isn't to be a chatbot. It's to be the most knowledgeable advisor you've ever had — one that gets better every single day.**

---

## 5-Minute Setup

### Option 1: One Command

```bash
git clone https://github.com/kingrebelf/openclaw-adaptive-intelligence.git
cd openclaw-adaptive-intelligence
bash setup.sh
```

This will:
1. Check dependencies (Python 3.8+)
2. Run an interactive onboarding (5-10 min conversation)
3. Build your USER.md profile and seed KNOWLEDGE.md
4. Set up the heartbeat cron job
5. Send a welcome Telegram message (if configured)

### Option 2: Manual

```bash
git clone https://github.com/kingrebelf/openclaw-adaptive-intelligence.git
cd openclaw-adaptive-intelligence
pip install requests
python3 scripts/onboarding.py
```

### Telegram Notifications (Optional)

```bash
export TELEGRAM_BOT_TOKEN="your-bot-token"
export TELEGRAM_CHAT_ID="your-chat-id"
```

---

## The Knowledge System

Everything revolves around **KNOWLEDGE.md** — the agent's brain map.

```
Knowledge Score: 42 / 100

Known (High Confidence ≥80%)
  → Your name, location, business type, immediate goals

Known (Medium Confidence 40-79%)
  → Customer segments, revenue model, rough seasonality

Suspected (Low Confidence <40%)
  → Inferred pain points, guessed competitive position

Knowledge Gaps — Ranked by Value
  → What the agent needs to learn next, and why
```

Every interaction updates this file. Every gap is ranked by how much it would improve the agent's advice if closed. The agent **never asks a question it can research first**.

### Knowledge Score

| Category | Max Points |
|----------|-----------|
| Personal info | 15 |
| Business / goals | 20 |
| Pain points | 15 |
| Past attempts / failures | 10 |
| Dream outcome | 15 |
| Niche expertise | 25 |
| **Total** | **100** |

A score of 100 is impossible by design. The world changes. People change. The goal is **velocity**, not completion.

---

## The Depth Ladder

Questions deepen over time. The system never skips layers.

### Layer 1 — Foundation (Day 1-3)
> Who are you? What do you do? What do you want?

Basic understanding. Name, role, location, immediate needs.

### Layer 2 — Context (Week 1)
> What's working? What's not? Who are your best customers and why?

Real situation, not the surface version. Past failures. Actual bottlenecks.

### Layer 3 — Strategy (Month 1)
> What would 10x look like? What's held you back? What have you tried?

Gap between current state and desired state. Strategic constraints.

### Layer 4 — Mastery (Ongoing)
> Niche-specific deep questions only a domain expert would ask.

Examples for an HVAC contractor in Alberta:
- *"What's your close rate on in-home quotes vs. phone quotes?"*
- *"How do you handle the Alberta Building Code update cycles?"*
- *"Does emergency call revenue cover the overhead spikes in spring?"*

**Target: be more useful than any human advisor they could hire.**

---

## Expertise Levels

| Level | What It Means |
|-------|--------------|
| **Novice** | Knows the domain exists |
| **Informed** | Knows basics and terminology |
| **Competent** | Can give useful generic advice |
| **Expert** | Knows nuances, edge cases, common mistakes |
| **Foremost Expert** | Knows *their specific situation* better than most consultants |

Timeline to Foremost Expert: **30-90 days** of consistent interaction.

When a niche is identified, run:
```bash
python3 scripts/expertise-builder.py "HVAC residential Alberta"
```

This creates `NICHE_HVAC_RESIDENTIAL_ALBERTA.md` with researched terminology, pain points, seasonal patterns, customer psychology, and common mistakes.

---

## Example: Proactive Questions

The system doesn't wait to be asked. Here's what a Week 2 heartbeat message might look like:

> *"I was looking into lead conversion rates for residential HVAC in Alberta and realized I don't know how you handle follow-up with leads who don't book on the first call. Do you have a system for that, or does it depend on which tech answers the phone?"*

Notice:
- Shows what it already researched
- States specifically what's missing
- Explains why it matters (implicitly: follow-up systems affect close rates)
- Asks ONE specific question

**Bad question:** *"Tell me about your sales process."*
**Good question:** The one above.

---

## File Structure

```
├── SOUL.md                    # Agent identity and operating principles
├── USER.md                    # Who the agent is helping (built by onboarding)
├── KNOWLEDGE.md               # Living brain map — what's known and unknown
├── MEMORY.md                  # Long-term distilled insights
├── HEARTBEAT.md               # Proactive intelligence engine rules
├── BOOTSTRAP.md               # First-run onboarding questions
├── AGENTS.md                  # Operational guide and protocols
├── NICHE_[DOMAIN].md          # Deep domain expertise (auto-generated)
├── setup.sh                   # One-command install
├── memory/                    # Daily memory files
│   ├── YYYY-MM-DD.md          # Raw daily notes
│   ├── review-YYYY-MM-DD.md   # Self-review outputs
│   └── audit-YYYY-MM-DD.md    # Knowledge audit reports
└── scripts/
    ├── onboarding.py          # Interactive first-run questionnaire
    ├── knowledge-audit.py     # Gap analysis + web research
    ├── self-review.py         # Daily fact extraction + helpfulness rating
    └── expertise-builder.py   # Deep niche research + file generation
```

---

## Scripts

| Script | What It Does | When to Run |
|--------|-------------|-------------|
| `onboarding.py` | Interactive questionnaire, builds USER.md | First run (via setup.sh) |
| `knowledge-audit.py` | Identifies gaps, researches them, updates KNOWLEDGE.md | Weekly (or on demand) |
| `self-review.py` | Extracts facts from memory, updates confidence levels | Daily (via heartbeat cron) |
| `expertise-builder.py` | Deep niche research, builds NICHE file | When new niche identified |

---

## Design Principles

1. **Research before asking.** Never ask the user something you can find yourself.
2. **One question per session.** Multiple questions feel like interrogation. One feels like genuine interest.
3. **Specificity over generality.** Generic knowledge helps anyone. Specific knowledge helps *them*.
4. **Never satisfied.** Every answer spawns three new questions. That's not a bug.
5. **Prove value, don't claim it.** The knowledge score is transparent. The user can see exactly what you know and don't know.

---

## License

MIT

---

*Built for [OpenClaw](https://github.com/kingrebelf) — AI that actually learns.*

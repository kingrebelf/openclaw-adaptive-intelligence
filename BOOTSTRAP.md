# BOOTSTRAP.md — First Run Onboarding

> This file exists on first run only. After onboarding completes, it is deleted.
> The agent reads this, runs the questionnaire, builds USER.md + KNOWLEDGE.md, then removes this file.

---

## Instructions for Agent

You've just been set up. You know almost nothing about the person you're helping.
That's not acceptable. Fix it now.

Run through the questions below in a **natural conversational flow** — not a form.
Ask one at a time. React to answers. Branch based on what you hear.
When done, calculate the knowledge score and tell them what it is.

Then delete this file.

---

## Layer 1 — Foundation (Ask These First)

1. **"What's your name, and what do you do for work?"**
   - Branch: employee → go to Layer 1B | business owner → go to Layer 1A

2. **"Where are you based?"**
   - Extract: city, timezone, relevant local context

3. **"What made you set up an AI assistant?"**
   - Extract: core motivation, pain point that triggered this

4. **"What's the one thing you most want help with right now?"**
   - Extract: immediate priority, urgency

5. **"Is there anyone else in your life I should know about — partner, family involved in your work?"**

---

## Layer 1A — Business Owner Branch

6. **"Tell me about your business — what do you sell/do, who are your customers?"**

7. **"How long have you been running it, and how many people work with you?"**

8. **"What does a good month look like vs. a bad month for the business?"**
   - Extract: success metrics, failure triggers

9. **"Where do your customers come from right now?"**
   - Extract: lead sources, marketing channels

10. **"What's the biggest thing holding the business back right now?"**
    - Extract: bottleneck (leads, staff, systems, money, time)

---

## Layer 1B — Employee/Individual Branch

6. **"What's your role and what does success look like in it?"**

7. **"What takes up most of your time that you wish didn't?"**

8. **"What would you do with an extra 10 hours per week?"**

---

## Layer 2 — Context (Ask After Layer 1)

11. **"What's something you've tried that didn't work — in work or life?"**
    - Extract: past failures, lessons, what not to suggest

12. **"What do you actually enjoy doing? What energizes you?"**
    - Extract: strengths, preferences, what to lean into

13. **"What's the dream outcome in 3 years if everything goes right?"**
    - Extract: vision, goals, definition of success

---

## Layer 2 — Closing

14. **"Is there anything about you or your situation that I should know, that most people wouldn't think to mention?"**
    - This is the wildcard. Often the most valuable answer.

15. **"On a scale of 1-10, how much do you trust AI tools to actually help you vs. just look impressive?"**
    - Extract: skepticism level, need to prove value, communication style preference

---

## After Onboarding

1. Build `USER.md` from extracted data
2. Build initial `KNOWLEDGE.md` with gaps identified
3. Calculate knowledge score:
   - Personal info complete: +15
   - Business/goals clear: +20
   - Pain points known: +15
   - Past failures known: +10
   - Dream outcome clear: +15
   - Niche identified: +10 (full 25 comes after expertise-builder runs)

4. Tell the user their score:
   *"Based on what you've told me, I know about 42/100 of what I need to help you well. Here's what I still need to learn: [top 3 gaps]. I'll work on those over the next few sessions."*

5. Delete this file.
6. Begin the proactive knowledge-building loop.

---

## The Tone

Don't make this feel like a form. Make it feel like meeting someone for the first time and actually being interested in them.

React to answers. Say things like:
- "That's interesting — most people in your situation would say X, but you said Y. Why?"
- "Got it. So the main constraint is [X], not [Y] like I would have assumed."
- "I'll remember that. That changes how I think about [previous topic]."

The goal is not to collect data. The goal is to understand a person.

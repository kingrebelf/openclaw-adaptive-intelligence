#!/usr/bin/env python3
"""
Interactive onboarding script for Adaptive Intelligence.
Reads BOOTSTRAP.md questions, collects answers conversationally,
builds USER.md and updates KNOWLEDGE.md with initial data.
"""

import os
import re
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read_file(filename):
    path = os.path.join(BASE_DIR, filename)
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return ""


def write_file(filename, content):
    path = os.path.join(BASE_DIR, filename)
    with open(path, "w") as f:
        f.write(content)


def ask(question, required=True):
    """Ask a question and return the answer."""
    print(f"\n  {question}")
    while True:
        answer = input("\n  > ").strip()
        if answer or not required:
            return answer
        print("  (I need an answer for this one to help you well.)")


def print_banner():
    print("\n" + "=" * 60)
    print("  ADAPTIVE INTELLIGENCE — First Run Onboarding")
    print("=" * 60)
    print("\n  Let's get to know each other. I'll ask you some questions")
    print("  one at a time — just talk naturally.\n")


def run_onboarding():
    print_banner()
    answers = {}

    # Layer 1 — Foundation
    answers["name_and_work"] = ask("What's your name, and what do you do for work?")

    # Determine branch
    is_business = False
    biz_keywords = ["business", "own", "founder", "run", "company", "freelance",
                     "self-employed", "entrepreneur", "agency", "contractor"]
    for kw in biz_keywords:
        if kw in answers["name_and_work"].lower():
            is_business = True
            break

    if not is_business:
        branch = ask("Quick follow-up — do you run your own business, or work for someone else?")
        is_business = any(kw in branch.lower() for kw in ["own", "my", "run", "business", "founder", "self"])

    answers["is_business_owner"] = is_business

    answers["location"] = ask("Where are you based?")

    answers["motivation"] = ask("What made you set up an AI assistant?")

    answers["immediate_priority"] = ask("What's the one thing you most want help with right now?")

    answers["people"] = ask(
        "Is there anyone else in your life I should know about — partner, family involved in your work?",
        required=False
    )

    # Branch-specific questions
    if is_business:
        print("\n  --- Business Details ---")
        answers["business_desc"] = ask("Tell me about your business — what do you sell/do, who are your customers?")
        answers["business_age"] = ask("How long have you been running it, and how many people work with you?")
        answers["good_bad_month"] = ask("What does a good month look like vs. a bad month for the business?")
        answers["lead_sources"] = ask("Where do your customers come from right now?")
        answers["bottleneck"] = ask("What's the biggest thing holding the business back right now?")
    else:
        print("\n  --- Your Role ---")
        answers["role_success"] = ask("What's your role and what does success look like in it?")
        answers["time_waste"] = ask("What takes up most of your time that you wish didn't?")
        answers["extra_time"] = ask("What would you do with an extra 10 hours per week?")

    # Layer 2 — Context
    print("\n  --- Digging Deeper ---")
    answers["past_failure"] = ask(
        "What's something you've tried that didn't work — in work or life?",
        required=False
    )

    answers["energizers"] = ask("What do you actually enjoy doing? What energizes you?")

    answers["dream_3yr"] = ask("What's the dream outcome in 3 years if everything goes right?")

    # Closing
    print("\n  --- Last Few ---")
    answers["wildcard"] = ask(
        "Is there anything about you or your situation that I should know, that most people wouldn't think to mention?",
        required=False
    )

    answers["trust_level"] = ask(
        "On a scale of 1-10, how much do you trust AI tools to actually help you vs. just look impressive?"
    )

    # Extract name
    name = answers["name_and_work"].split(",")[0].split(" and ")[0].strip()
    name = name.replace("I'm ", "").replace("My name is ", "").replace("I am ", "").strip()
    # Take first 1-2 words as name
    name_parts = name.split()[:2]
    name = " ".join(name_parts)

    # Calculate knowledge score
    score = 0
    score_breakdown = {}

    # Personal info (15 points)
    personal = 0
    if answers.get("name_and_work"):
        personal += 5
    if answers.get("location"):
        personal += 5
    if answers.get("people"):
        personal += 5
    score_breakdown["Personal info"] = personal
    score += personal

    # Business / goals (20 points)
    biz = 0
    if is_business:
        if answers.get("business_desc"):
            biz += 7
        if answers.get("business_age"):
            biz += 5
        if answers.get("lead_sources"):
            biz += 4
        if answers.get("good_bad_month"):
            biz += 4
    else:
        if answers.get("role_success"):
            biz += 10
        if answers.get("extra_time"):
            biz += 5
        if answers.get("time_waste"):
            biz += 5
    score_breakdown["Business / goals"] = biz
    score += biz

    # Pain points (15 points)
    pain = 0
    if answers.get("bottleneck") or answers.get("time_waste"):
        pain += 8
    if answers.get("motivation"):
        pain += 7
    score_breakdown["Pain points"] = pain
    score += pain

    # Past attempts (10 points)
    past = 0
    if answers.get("past_failure"):
        past += 10
    score_breakdown["Past attempts / failures"] = past
    score += past

    # Dream outcome (15 points)
    dream = 0
    if answers.get("dream_3yr"):
        dream += 10
    if answers.get("energizers"):
        dream += 5
    score_breakdown["Dream outcome"] = dream
    score += dream

    # Niche identified (10 of 25 — full 25 after expertise-builder)
    niche = 0
    if is_business and answers.get("business_desc"):
        niche += 10
    score_breakdown["Niche expertise"] = niche
    score += niche

    # Build USER.md
    today = datetime.now().strftime("%Y-%m-%d")
    trust = answers.get("trust_level", "?")

    user_md = f"""# USER.md — Who I'm Helping

> Last updated: {today}
> Knowledge Score: {score} / 100

---

## Personal

- **Name:** {name}
- **Location:** {answers.get('location', 'Unknown')}
- **Key people:** {answers.get('people', 'Not specified')}

---

## Business

"""
    if is_business:
        user_md += f"""- **Type:** Business Owner
- **Description:** {answers.get('business_desc', '')}
- **Duration / Team:** {answers.get('business_age', '')}
- **Lead sources:** {answers.get('lead_sources', '')}
- **Good vs bad month:** {answers.get('good_bad_month', '')}
"""
    else:
        user_md += f"""- **Type:** Employee / Individual
- **Role & success:** {answers.get('role_success', '')}
- **Time drains:** {answers.get('time_waste', '')}
- **Would do with more time:** {answers.get('extra_time', '')}
"""

    user_md += f"""
---

## Goals

- **Immediate priority:** {answers.get('immediate_priority', '')}
- **Dream outcome (3yr):** {answers.get('dream_3yr', '')}
- **What energizes them:** {answers.get('energizers', '')}

---

## Pain Points

- **Main bottleneck:** {answers.get('bottleneck', answers.get('time_waste', ''))}
- **Why they got an AI:** {answers.get('motivation', '')}

---

## Wins / Losses

- **Past failure:** {answers.get('past_failure', 'Not shared yet')}
- **Wins:** *(to be discovered)*

---

## Dream Outcome

{answers.get('dream_3yr', 'Not yet defined')}

---

## Communication Style

- **AI trust level:** {trust}/10
- **Wildcard info:** {answers.get('wildcard', 'None shared')}
- **Preferred style:** {'Direct — prove value with results' if int(trust) <= 5 else 'Open to AI suggestions' if trust.isdigit() else 'To be determined'}

---

## Knowledge Score

**{score} / 100**

| Category | Points Possible | Points Earned |
|----------|----------------|---------------|
"""
    for cat, pts in score_breakdown.items():
        possible = {"Personal info": 15, "Business / goals": 20, "Pain points": 15,
                     "Past attempts / failures": 10, "Dream outcome": 15, "Niche expertise": 25}
        user_md += f"| {cat} | {possible.get(cat, 0)} | {pts} |\n"

    write_file("USER.md", user_md)

    # Update KNOWLEDGE.md
    knowledge = read_file("KNOWLEDGE.md")
    # Update score in KNOWLEDGE.md
    knowledge = re.sub(
        r"\*\*Current Score: \d+ / 100\*\*",
        f"**Current Score: {score} / 100**",
        knowledge
    )
    # Update the score table
    for cat, pts in score_breakdown.items():
        knowledge = re.sub(
            rf"\| {re.escape(cat)}\s*\|[^|]*\|\s*\d+\s*\|",
            f"| {cat} | {{'Personal info': 15, 'Business / goals': 20, 'Pain points': 15, 'Past attempts / failures': 10, 'Dream outcome': 15, 'Niche expertise': 25}[cat]} | {pts} |",
            knowledge
        )
    write_file("KNOWLEDGE.md", knowledge)

    # Print results
    print("\n" + "=" * 60)
    print(f"  Onboarding complete!")
    print(f"\n  Knowledge Score: {score} / 100")
    print(f"\n  Breakdown:")
    for cat, pts in score_breakdown.items():
        print(f"    {cat}: {pts}")

    gaps = [cat for cat, pts in score_breakdown.items() if pts < 10]
    if gaps:
        print(f"\n  Top gaps to close: {', '.join(gaps[:3])}")

    print(f"\n  Files created: USER.md")
    print(f"  Files updated: KNOWLEDGE.md")
    print("=" * 60)

    # Save raw answers for reference
    os.makedirs(os.path.join(BASE_DIR, "memory"), exist_ok=True)
    answers_path = os.path.join(BASE_DIR, "memory", f"onboarding-{today}.json")
    with open(answers_path, "w") as f:
        json.dump(answers, f, indent=2)

    return score


if __name__ == "__main__":
    run_onboarding()

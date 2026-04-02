#!/usr/bin/env python3
"""
Self-Review Script for Adaptive Intelligence.
Reads today's memory file, extracts facts, updates KNOWLEDGE.md
confidence levels, and rates overall helpfulness.
"""

import os
import re
from datetime import datetime, timedelta

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


def get_today_memory():
    """Read today's memory file."""
    today = datetime.now().strftime("%Y-%m-%d")
    memory_dir = os.path.join(BASE_DIR, "memory")

    # Try today's file
    today_path = os.path.join(memory_dir, f"{today}.md")
    if os.path.exists(today_path):
        with open(today_path, "r") as f:
            return today, f.read()

    # Try yesterday if today doesn't exist yet
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday_path = os.path.join(memory_dir, f"{yesterday}.md")
    if os.path.exists(yesterday_path):
        with open(yesterday_path, "r") as f:
            return yesterday, f.read()

    # Try any recent .md file in memory/
    if os.path.exists(memory_dir):
        md_files = sorted(
            [f for f in os.listdir(memory_dir) if f.endswith(".md")],
            reverse=True
        )
        if md_files:
            path = os.path.join(memory_dir, md_files[0])
            with open(path, "r") as f:
                return md_files[0].replace(".md", ""), f.read()

    return today, ""


def extract_facts(memory_content):
    """Extract factual statements from memory content."""
    facts = []
    lines = memory_content.split("\n")
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("---"):
            continue
        # Lines that look like facts (contain substantive info)
        if len(line) > 20 and any(indicator in line.lower() for indicator in
            ["learned", "told me", "mentioned", "said", "discovered",
             "found out", "confirmed", "realized", "noticed", "is a",
             "works at", "lives in", "wants to", "needs", "prefers",
             "uses", "has been", "started", "plans to"]):
            # Clean up markdown formatting
            fact = re.sub(r"^[-*]\s+", "", line)
            fact = re.sub(r"\*\*(.+?)\*\*", r"\1", fact)
            facts.append(fact)
    return facts


def extract_questions_raised(memory_content):
    """Find questions that came up but weren't answered."""
    questions = []
    lines = memory_content.split("\n")
    for line in lines:
        line = line.strip()
        if "?" in line and len(line) > 15:
            q = re.sub(r"^[-*]\s+", "", line)
            questions.append(q)
    return questions


def update_knowledge_confidence(knowledge_md, facts):
    """Update confidence levels for knowledge entries that match new facts."""
    updated = 0
    today = datetime.now().strftime("%Y-%m-%d")

    for fact in facts:
        # Find entries whose topic appears in the fact
        pattern = r"([-*]\s+.+?:\s+.+?\s*\|\s*Confidence:\s*)(\d+)(%\s*\|\s*Last verified:\s*)([\d-]+)"
        matches = list(re.finditer(pattern, knowledge_md))
        for match in matches:
            topic_line = match.group(0)
            # Extract the topic
            topic_match = re.match(r"[-*]\s+(.+?):", topic_line)
            if topic_match:
                topic = topic_match.group(1).strip().lower()
                # If any significant word from the topic appears in the fact
                topic_words = [w for w in topic.split() if len(w) > 3]
                if any(w in fact.lower() for w in topic_words):
                    old_conf = int(match.group(2))
                    # Bump confidence (max +15 per verification, cap at 95)
                    new_conf = min(95, old_conf + 10)
                    if new_conf != old_conf:
                        old_str = f"{match.group(1)}{match.group(2)}{match.group(3)}{match.group(4)}"
                        new_str = f"{match.group(1)}{new_conf}{match.group(3)}{today}"
                        knowledge_md = knowledge_md.replace(old_str, new_str, 1)
                        updated += 1

    return knowledge_md, updated


def update_velocity(knowledge_md, facts_count, confidence_updates, new_questions):
    """Update the Knowledge Velocity section."""
    today = datetime.now().strftime("%Y-%m-%d")

    # Update facts learned
    knowledge_md = re.sub(
        r"Facts learned this week: \d+",
        f"Facts learned this week: {facts_count}",
        knowledge_md
    )
    knowledge_md = re.sub(
        r"Confidence improvements: \d+",
        f"Confidence improvements: {confidence_updates}",
        knowledge_md
    )
    knowledge_md = re.sub(
        r"New gaps discovered: \d+",
        f"New gaps discovered: {new_questions}",
        knowledge_md
    )

    return knowledge_md


def rate_helpfulness(memory_content, facts):
    """Rate the day's helpfulness based on memory content."""
    score = 0
    max_score = 10
    reasons = []

    # Did we learn new facts?
    if len(facts) >= 3:
        score += 3
        reasons.append(f"Learned {len(facts)} new facts")
    elif len(facts) >= 1:
        score += 1
        reasons.append(f"Learned {len(facts)} new fact(s)")
    else:
        reasons.append("No new facts learned")

    # Did we have substantive interactions?
    if len(memory_content) > 500:
        score += 2
        reasons.append("Substantive session content")
    elif len(memory_content) > 100:
        score += 1
        reasons.append("Light session content")

    # Were there action items or completions?
    action_words = ["completed", "done", "finished", "fixed", "resolved",
                     "created", "built", "set up", "configured"]
    actions = sum(1 for w in action_words if w in memory_content.lower())
    if actions >= 2:
        score += 3
        reasons.append(f"Multiple tasks completed ({actions} action indicators)")
    elif actions >= 1:
        score += 1
        reasons.append("Some tasks completed")

    # Were there proactive insights?
    proactive_words = ["suggested", "noticed", "flagged", "recommended",
                        "proactively", "anticipated", "opportunity"]
    proactive = sum(1 for w in proactive_words if w in memory_content.lower())
    if proactive >= 1:
        score += 2
        reasons.append("Proactive insights provided")

    return min(score, max_score), reasons


def run_review():
    print("=" * 60)
    print("  SELF-REVIEW — Adaptive Intelligence")
    print("=" * 60)

    date, memory_content = get_today_memory()
    knowledge_md = read_file("KNOWLEDGE.md")

    if not memory_content:
        print(f"\n  No memory file found for {date}.")
        print("  Nothing to review. Run some sessions first.")
        return

    print(f"\n  Reviewing memory for: {date}")
    print(f"  Memory size: {len(memory_content)} characters")

    # Extract facts
    facts = extract_facts(memory_content)
    print(f"\n  Facts extracted: {len(facts)}")
    for i, fact in enumerate(facts[:10], 1):
        print(f"    {i}. {fact[:80]}{'...' if len(fact) > 80 else ''}")

    # Extract unanswered questions
    questions = extract_questions_raised(memory_content)
    print(f"\n  Questions raised: {len(questions)}")
    for q in questions[:5]:
        print(f"    ? {q[:80]}")

    # Update KNOWLEDGE.md confidence levels
    print("\n  Updating confidence levels...")
    knowledge_md, confidence_updates = update_knowledge_confidence(knowledge_md, facts)
    print(f"  Updated {confidence_updates} confidence levels")

    # Update velocity
    knowledge_md = update_velocity(knowledge_md, len(facts), confidence_updates, len(questions))

    # Write updated KNOWLEDGE.md
    write_file("KNOWLEDGE.md", knowledge_md)
    print("  KNOWLEDGE.md updated")

    # Rate helpfulness
    helpfulness, reasons = rate_helpfulness(memory_content, facts)
    print(f"\n  Helpfulness rating: {helpfulness}/10")
    for r in reasons:
        print(f"    - {r}")

    # Save review
    today = datetime.now().strftime("%Y-%m-%d")
    review = f"""# Self-Review — {date}

## Facts Learned: {len(facts)}
{chr(10).join(f'- {f}' for f in facts) if facts else '- None'}

## Questions Raised: {len(questions)}
{chr(10).join(f'- {q}' for q in questions) if questions else '- None'}

## Confidence Updates: {confidence_updates}

## Helpfulness: {helpfulness}/10
{chr(10).join(f'- {r}' for r in reasons)}

---
*Generated by scripts/self-review.py at {datetime.now().strftime("%Y-%m-%d %H:%M")}*
"""
    os.makedirs(os.path.join(BASE_DIR, "memory"), exist_ok=True)
    write_file(f"memory/review-{today}.md", review)
    print(f"\n  Review saved to memory/review-{today}.md")

    print("\n" + "=" * 60)
    return helpfulness


if __name__ == "__main__":
    run_review()

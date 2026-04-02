#!/usr/bin/env python3
"""
Knowledge Audit Script for Adaptive Intelligence.
Reads KNOWLEDGE.md + MEMORY.md, identifies gaps, performs web research,
updates KNOWLEDGE.md, and outputs a gap analysis report.
"""

import os
import re
import json
from datetime import datetime

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

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


def parse_knowledge_entries(knowledge_md):
    """Extract knowledge entries with confidence levels."""
    entries = []
    # Match pattern: [topic]: [info] | Confidence: X% | Last verified: date
    pattern = r"[-*]\s+(.+?):\s+(.+?)\s*\|\s*Confidence:\s*(\d+)%\s*\|\s*Last verified:\s*(.+)"
    for match in re.finditer(pattern, knowledge_md):
        entries.append({
            "topic": match.group(1).strip(),
            "info": match.group(2).strip(),
            "confidence": int(match.group(3)),
            "last_verified": match.group(4).strip()
        })
    return entries


def parse_gaps(knowledge_md):
    """Extract knowledge gaps."""
    gaps = []
    pattern = r"[-*]\s+(.+?)\s*\|\s*Why it matters:\s*(.+?)\s*\|\s*Question to ask:\s*(.+?)\s*\|\s*Asked:\s*(YES|NO)"
    for match in re.finditer(pattern, knowledge_md):
        gaps.append({
            "gap": match.group(1).strip(),
            "why": match.group(2).strip(),
            "question": match.group(3).strip(),
            "asked": match.group(4).strip()
        })
    return gaps


def parse_score_table(knowledge_md):
    """Extract current knowledge score from table."""
    scores = {}
    pattern = r"\|\s*(.+?)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|"
    for match in re.finditer(pattern, knowledge_md):
        category = match.group(1).strip()
        if category in ("Category", "-------"):
            continue
        scores[category] = {
            "possible": int(match.group(2)),
            "earned": int(match.group(3))
        }
    return scores


def parse_memory_files():
    """Read all memory files for context."""
    memory_dir = os.path.join(BASE_DIR, "memory")
    memories = []
    if os.path.exists(memory_dir):
        for fname in sorted(os.listdir(memory_dir)):
            if fname.endswith(".md") or fname.endswith(".json"):
                fpath = os.path.join(memory_dir, fname)
                with open(fpath, "r") as f:
                    memories.append({"file": fname, "content": f.read()})
    return memories


def web_research(query):
    """Attempt web research via requests. Returns findings or None."""
    if not HAS_REQUESTS:
        return None
    try:
        # Use DuckDuckGo instant answer API as a free research source
        resp = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_html": 1},
            timeout=10
        )
        if resp.status_code == 200:
            data = resp.json()
            results = []
            if data.get("Abstract"):
                results.append(data["Abstract"])
            if data.get("RelatedTopics"):
                for topic in data["RelatedTopics"][:3]:
                    if isinstance(topic, dict) and topic.get("Text"):
                        results.append(topic["Text"])
            return "\n".join(results) if results else None
    except Exception:
        pass
    return None


def identify_new_gaps(knowledge_md, user_md, memories):
    """Identify gaps not already tracked."""
    existing_gaps = parse_gaps(knowledge_md)
    existing_topics = {g["gap"].lower() for g in existing_gaps}
    new_gaps = []

    # Check USER.md for incomplete sections
    incomplete_markers = [
        ("to be discovered", "User wins/successes", "Understanding wins helps replicate them"),
        ("not shared yet", "Past failures detail", "Knowing what failed prevents repeating suggestions"),
        ("not yet defined", "Dream outcome clarity", "Clear vision enables better strategic advice"),
        ("to be determined", "Communication preferences", "Right tone increases trust and engagement"),
    ]
    for marker, gap_name, why in incomplete_markers:
        if marker in user_md.lower() and gap_name.lower() not in existing_topics:
            new_gaps.append({
                "gap": gap_name,
                "why": why,
                "question": f"Can you tell me more about {gap_name.lower()}?",
                "asked": "NO"
            })

    # Check for stale knowledge (confidence decay)
    entries = parse_knowledge_entries(knowledge_md)
    today = datetime.now()
    for entry in entries:
        try:
            verified = datetime.strptime(entry["last_verified"].strip(), "%Y-%m-%d")
            days_old = (today - verified).days
            if days_old > 30 and entry["confidence"] > 50:
                gap_name = f"Verify: {entry['topic']}"
                if gap_name.lower() not in existing_topics:
                    new_gaps.append({
                        "gap": gap_name,
                        "why": f"Last verified {days_old} days ago, may be outdated",
                        "question": f"Is this still accurate: {entry['info'][:80]}?",
                        "asked": "NO"
                    })
        except (ValueError, AttributeError):
            pass

    return new_gaps


def calculate_score(knowledge_md):
    """Recalculate total knowledge score."""
    scores = parse_score_table(knowledge_md)
    total_earned = sum(s["earned"] for s in scores.values())
    total_possible = sum(s["possible"] for s in scores.values())
    return total_earned, total_possible


def generate_report(knowledge_md, user_md, new_gaps, research_results, scores):
    """Generate audit report."""
    today = datetime.now().strftime("%Y-%m-%d")
    total_earned, total_possible = sum(s["earned"] for s in scores.values()), sum(s["possible"] for s in scores.values())

    entries = parse_knowledge_entries(knowledge_md)
    high = [e for e in entries if e["confidence"] >= 80]
    medium = [e for e in entries if 40 <= e["confidence"] < 80]
    low = [e for e in entries if e["confidence"] < 40]

    existing_gaps = parse_gaps(knowledge_md)
    open_gaps = [g for g in existing_gaps if g["asked"] == "NO"]

    report = f"""# Knowledge Audit Report — {today}

## Score: {total_earned} / {total_possible}

### Knowledge Distribution
- High confidence (>=80%): {len(high)} entries
- Medium confidence (40-79%): {len(medium)} entries
- Low confidence (<40%): {len(low)} entries

### Category Breakdown
| Category | Earned | Possible | % |
|----------|--------|----------|---|
"""
    for cat, s in scores.items():
        pct = round(s["earned"] / s["possible"] * 100) if s["possible"] > 0 else 0
        report += f"| {cat} | {s['earned']} | {s['possible']} | {pct}% |\n"

    report += f"""
### Open Gaps: {len(open_gaps) + len(new_gaps)}
"""
    if new_gaps:
        report += "\n**Newly Identified:**\n"
        for g in new_gaps:
            report += f"- {g['gap']} — {g['why']}\n"

    if open_gaps:
        report += "\n**Previously Tracked (unanswered):**\n"
        for g in open_gaps:
            report += f"- {g['gap']} — {g['why']}\n"

    if research_results:
        report += "\n### Web Research Findings\n"
        for topic, result in research_results.items():
            report += f"\n**{topic}:**\n{result[:300]}\n"

    report += f"""
### Recommendations
1. Close the highest-value gap first
2. Verify any entries older than 30 days
3. Target: 3 new facts per day until score > 60
4. Run expertise-builder if niche is identified but NICHE file doesn't exist

---
*Generated by scripts/knowledge-audit.py*
"""
    return report


def run_audit():
    print("=" * 60)
    print("  KNOWLEDGE AUDIT — Adaptive Intelligence")
    print("=" * 60)

    knowledge_md = read_file("KNOWLEDGE.md")
    user_md = read_file("USER.md")
    memory_md = read_file("MEMORY.md")
    memories = parse_memory_files()

    print("\n  Reading KNOWLEDGE.md...")
    entries = parse_knowledge_entries(knowledge_md)
    print(f"  Found {len(entries)} knowledge entries")

    scores = parse_score_table(knowledge_md)
    total_earned = sum(s["earned"] for s in scores.values())
    total_possible = sum(s["possible"] for s in scores.values())
    print(f"  Current score: {total_earned}/{total_possible}")

    print("\n  Identifying gaps...")
    new_gaps = identify_new_gaps(knowledge_md, user_md, memories)
    print(f"  Found {len(new_gaps)} new gaps")

    # Web research on top gaps
    research_results = {}
    if HAS_REQUESTS and new_gaps:
        print("\n  Running web research on top gaps...")
        for gap in new_gaps[:3]:
            topic = gap["gap"]
            print(f"    Researching: {topic}")
            result = web_research(topic)
            if result:
                research_results[topic] = result
                print(f"    Found info for: {topic}")
            else:
                print(f"    No results for: {topic}")

    # Add new gaps to KNOWLEDGE.md
    if new_gaps:
        gap_section = "\n## Knowledge Gaps — Ranked by Value\n\n"
        gap_section += "*Format: [gap] | Why it matters: [reason] | Question to ask: [specific question] | Asked: NO*\n\n"

        existing_gaps = parse_gaps(knowledge_md)
        all_gaps = existing_gaps + new_gaps
        for g in all_gaps:
            gap_section += f"- {g['gap']} | Why it matters: {g['why']} | Question to ask: {g['question']} | Asked: {g['asked']}\n"

        # Replace the gaps section in KNOWLEDGE.md
        knowledge_md = re.sub(
            r"## Knowledge Gaps — Ranked by Value.*?(?=\n## |\Z)",
            gap_section.strip() + "\n\n",
            knowledge_md,
            flags=re.DOTALL
        )
        write_file("KNOWLEDGE.md", knowledge_md)
        print("\n  Updated KNOWLEDGE.md with new gaps")

    # Generate report
    report = generate_report(knowledge_md, user_md, new_gaps, research_results, scores)
    today = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(os.path.join(BASE_DIR, "memory"), exist_ok=True)
    report_path = f"memory/audit-{today}.md"
    write_file(report_path, report)
    print(f"\n  Report saved to {report_path}")

    print("\n" + report)
    print("=" * 60)
    return report


if __name__ == "__main__":
    run_audit()

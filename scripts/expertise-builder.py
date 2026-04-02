#!/usr/bin/env python3
"""
Expertise Builder for Adaptive Intelligence.
Takes a niche string, researches it via web, and builds a comprehensive
NICHE_[domain].md file with terminology, pain points, seasonal patterns,
customer psychology, and common mistakes.
"""

import os
import re
import sys
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


def sanitize_domain(niche):
    """Convert niche string to safe filename component."""
    # Take key words, lowercase, join with underscore
    words = re.sub(r"[^a-zA-Z0-9\s]", "", niche).lower().split()
    # Take up to 4 significant words
    significant = [w for w in words if len(w) > 2][:4]
    return "_".join(significant) if significant else "general"


def web_search(query):
    """Search via DuckDuckGo instant answer API."""
    if not HAS_REQUESTS:
        return None
    try:
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
                for topic in data["RelatedTopics"][:5]:
                    if isinstance(topic, dict) and topic.get("Text"):
                        results.append(topic["Text"])
            return results
    except Exception:
        pass
    return None


def research_niche(niche):
    """Perform multi-angle research on the niche."""
    research = {
        "overview": [],
        "terminology": [],
        "pain_points": [],
        "seasonal": [],
        "psychology": [],
        "mistakes": [],
    }

    queries = [
        (f"{niche} industry overview", "overview"),
        (f"{niche} terminology glossary", "terminology"),
        (f"{niche} biggest challenges problems", "pain_points"),
        (f"{niche} seasonal trends busy season", "seasonal"),
        (f"{niche} customer psychology buying behavior", "psychology"),
        (f"{niche} common mistakes to avoid", "mistakes"),
    ]

    for query, category in queries:
        print(f"    Searching: {query}")
        results = web_search(query)
        if results:
            research[category].extend(results)
            print(f"      Found {len(results)} results")
        else:
            print(f"      No results (will use template)")

    return research


def build_niche_file(niche, domain_key, research):
    """Build the NICHE_[domain].md file."""
    today = datetime.now().strftime("%Y-%m-%d")

    content = f"""# NICHE_{domain_key.upper()}.md — Domain Expertise File

> **Niche:** {niche}
> **Created:** {today}
> **Last Updated:** {today}
> **Expertise Level:** Informed (auto-researched, needs human verification)

---

## Overview

{chr(10).join(f'- {r}' for r in research['overview'][:5]) if research['overview'] else f'*{niche} — research pending. Fill in from conversations and manual research.*'}

---

## Terminology & Jargon

*Key terms that insiders use. Speaking the language builds trust.*

{chr(10).join(f'- **{r[:50].split(" - ")[0] if " - " in r else r[:30]}** — {r}' for r in research['terminology'][:10]) if research['terminology'] else f"""| Term | Meaning | When Used |
|------|---------|-----------|
| *(research pending)* | — | — |

*Priority: learn the terms the user actually uses in conversation and add them here.*"""}

---

## Pain Points & Challenges

*What keeps people in this niche up at night?*

{chr(10).join(f'- {r}' for r in research['pain_points'][:8]) if research['pain_points'] else """- *(To be discovered through conversation and research)*

Common categories to investigate:
1. Lead generation / customer acquisition
2. Operations / fulfillment bottlenecks
3. Staff / hiring / retention
4. Cash flow / seasonality
5. Competition / market pressure
6. Technology / systems gaps
7. Regulation / compliance
8. Scaling constraints"""}

---

## Seasonal Patterns

*When is the business busy, slow, and what drives the cycles?*

{chr(10).join(f'- {r}' for r in research['seasonal'][:5]) if research['seasonal'] else """| Period | Pattern | Implications |
|--------|---------|--------------|
| Q1 (Jan-Mar) | *(research needed)* | — |
| Q2 (Apr-Jun) | *(research needed)* | — |
| Q3 (Jul-Sep) | *(research needed)* | — |
| Q4 (Oct-Dec) | *(research needed)* | — |

*Key: understand when to push growth vs. when to prepare.*"""}

---

## Customer Psychology

*What motivates their customers? What are the buying triggers?*

{chr(10).join(f'- {r}' for r in research['psychology'][:8]) if research['psychology'] else """### Buying Triggers
- *(To be researched)*

### Decision Factors
- *(To be researched)*

### Common Objections
- *(To be researched)*

### Trust Builders
- *(To be researched)*"""}

---

## Common Mistakes

*What do people in this niche get wrong? What should we avoid suggesting?*

{chr(10).join(f'- {r}' for r in research['mistakes'][:8]) if research['mistakes'] else """1. *(To be researched)*

Categories to investigate:
- Pricing mistakes (too low, no anchor, hourly vs. flat)
- Marketing mistakes (wrong channel, wrong message, no follow-up)
- Operations mistakes (no systems, owner bottleneck, no delegation)
- Growth mistakes (scaling too fast, wrong hires, ignoring margins)"""}

---

## Competitive Landscape

*Who else operates in this space? What differentiates winners from losers?*

- *(To be built from conversations and research)*

---

## Key Metrics

*What numbers matter most in this niche?*

| Metric | Good | Great | Source |
|--------|------|-------|--------|
| *(to be discovered)* | — | — | — |

---

## Research Queue

*Things to investigate next for this niche:*

- [ ] Verify all auto-researched content with user
- [ ] Identify the user's specific sub-niche within this domain
- [ ] Map their competitive position
- [ ] Understand their pricing model
- [ ] Learn their customer journey from lead to sale
- [ ] Identify their highest-margin offerings

---

## Conversation Notes

*Niche-specific insights from actual conversations:*

*(Empty — will be populated as conversations happen)*

---

*This file is auto-generated by `scripts/expertise-builder.py` and should be continuously updated as knowledge deepens. Target: Foremost Expert level within 90 days.*
"""
    return content


def update_knowledge_domain(knowledge_md, niche, domain_key):
    """Add or update the domain entry in KNOWLEDGE.md."""
    today = datetime.now().strftime("%Y-%m-%d")
    new_row = f"| {niche} | Informed | Auto-researched via expertise-builder | Verify with user, deepen understanding |"

    # Check if domain already exists
    if niche.lower() in knowledge_md.lower():
        # Update existing
        pattern = rf"\|\s*{re.escape(niche)}\s*\|[^|]*\|[^|]*\|[^|]*\|"
        knowledge_md = re.sub(pattern, new_row, knowledge_md, flags=re.IGNORECASE)
    else:
        # Add new row (replace the "none yet" placeholder or append)
        if "*(none yet)*" in knowledge_md:
            knowledge_md = knowledge_md.replace(
                "| *(none yet)* | Novice | — | Run onboarding |",
                new_row
            )
        else:
            # Add before the Levels line
            knowledge_md = knowledge_md.replace(
                "**Levels:**",
                f"{new_row}\n\n**Levels:**"
            )

    # Update niche files section
    niche_ref = f"- `NICHE_{domain_key.upper()}.md` — {niche}"
    if f"NICHE_{domain_key.upper()}.md" not in knowledge_md:
        knowledge_md = knowledge_md.replace(
            "- Auto-generated by `scripts/expertise-builder.py`",
            f"- Auto-generated by `scripts/expertise-builder.py`\n{niche_ref}"
        )

    return knowledge_md


def run_builder(niche):
    print("=" * 60)
    print("  EXPERTISE BUILDER — Adaptive Intelligence")
    print("=" * 60)
    print(f"\n  Building expertise file for: {niche}")

    domain_key = sanitize_domain(niche)
    filename = f"NICHE_{domain_key.upper()}.md"
    print(f"  Output file: {filename}")

    # Research
    print("\n  Researching...")
    research = research_niche(niche)

    total_findings = sum(len(v) for v in research.values())
    print(f"\n  Total research findings: {total_findings}")

    # Build file
    print("\n  Building niche file...")
    content = build_niche_file(niche, domain_key, research)
    write_file(filename, content)
    print(f"  Created: {filename}")

    # Update KNOWLEDGE.md
    print("\n  Updating KNOWLEDGE.md...")
    knowledge_md = read_file("KNOWLEDGE.md")
    knowledge_md = update_knowledge_domain(knowledge_md, niche, domain_key)
    write_file("KNOWLEDGE.md", knowledge_md)
    print("  KNOWLEDGE.md updated with new domain entry")

    print(f"\n  Expertise file ready: {filename}")
    print(f"  Current level: Informed (auto-researched)")
    print(f"  Target: Foremost Expert (within 90 days)")
    print("\n  Next steps:")
    print("    1. Review the file with the user")
    print("    2. Fill in gaps from conversation")
    print("    3. Verify auto-researched content")
    print("=" * 60)

    return filename


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python expertise-builder.py \"<niche description>\"")
        print("Example: python expertise-builder.py \"HVAC residential Alberta\"")
        sys.exit(1)

    niche = " ".join(sys.argv[1:])
    run_builder(niche)

#!/usr/bin/env bash
# ============================================================
#  Adaptive Intelligence — One-Command Setup
#  Usage: curl -sL <raw-url>/setup.sh | bash
#  Or:    git clone <repo> && cd openclaw-adaptive-intelligence && bash setup.sh
# ============================================================

set -euo pipefail

REPO_URL="https://github.com/kingrebelf/openclaw-adaptive-intelligence.git"
DIR_NAME="openclaw-adaptive-intelligence"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo ""
echo -e "${CYAN}=======================================${NC}"
echo -e "${CYAN}  Adaptive Intelligence — Setup${NC}"
echo -e "${CYAN}=======================================${NC}"
echo ""

# Step 1: Clone if not already in the repo
if [ ! -f "$SCRIPT_DIR/SOUL.md" ]; then
    echo -e "${YELLOW}Cloning repository...${NC}"
    git clone "$REPO_URL" "$DIR_NAME"
    cd "$DIR_NAME"
    SCRIPT_DIR="$(pwd)"
else
    echo -e "${GREEN}Already in the repo directory.${NC}"
    cd "$SCRIPT_DIR"
fi

# Step 2: Check Python
echo ""
echo -e "${YELLOW}Checking Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON=python3
    echo -e "${GREEN}Found: $(python3 --version)${NC}"
elif command -v python &> /dev/null; then
    PYTHON=python
    echo -e "${GREEN}Found: $(python --version)${NC}"
else
    echo "Python is required but not installed."
    echo "Install Python 3.8+ and try again."
    exit 1
fi

# Step 3: Install dependencies
echo ""
echo -e "${YELLOW}Installing Python dependencies...${NC}"
$PYTHON -m pip install --quiet requests 2>/dev/null || {
    echo -e "${YELLOW}pip install failed — scripts will work without web research.${NC}"
}

# Step 4: Create memory directory
mkdir -p memory

# Step 5: Run onboarding
echo ""
echo -e "${CYAN}=======================================${NC}"
echo -e "${CYAN}  Starting Onboarding${NC}"
echo -e "${CYAN}=======================================${NC}"
$PYTHON scripts/onboarding.py

# Step 6: Set up heartbeat cron (every 30 minutes)
echo ""
echo -e "${YELLOW}Setting up heartbeat cron job...${NC}"
CRON_CMD="*/30 * * * * cd $SCRIPT_DIR && $PYTHON scripts/self-review.py >> memory/heartbeat.log 2>&1"
# Add to crontab without duplicating
(crontab -l 2>/dev/null | grep -v "self-review.py"; echo "$CRON_CMD") | crontab - 2>/dev/null && {
    echo -e "${GREEN}Heartbeat cron installed (every 30 minutes)${NC}"
} || {
    echo -e "${YELLOW}Could not install cron job. You can add it manually:${NC}"
    echo "  $CRON_CMD"
}

# Step 7: Send welcome Telegram message (if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are set)
echo ""
if [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
    echo -e "${YELLOW}Sending welcome Telegram message...${NC}"
    WELCOME_MSG="Adaptive Intelligence is online.

I've completed onboarding and I'm ready to start learning.

Current knowledge score: check USER.md
Next: I'll start building expertise in your niche.

— Your AI"
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d chat_id="${TELEGRAM_CHAT_ID}" \
        -d text="$WELCOME_MSG" \
        -d parse_mode="Markdown" > /dev/null 2>&1 && {
        echo -e "${GREEN}Welcome message sent!${NC}"
    } || {
        echo -e "${YELLOW}Telegram send failed. Check your TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.${NC}"
    }
else
    echo -e "${YELLOW}Telegram not configured.${NC}"
    echo "  Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables"
    echo "  to enable Telegram notifications."
fi

# Done
echo ""
echo -e "${CYAN}=======================================${NC}"
echo -e "${GREEN}  Setup Complete!${NC}"
echo -e "${CYAN}=======================================${NC}"
echo ""
echo "  Files created:"
echo "    - USER.md (your profile)"
echo "    - KNOWLEDGE.md (updated with your data)"
echo "    - memory/ (daily memory storage)"
echo ""
echo "  What happens next:"
echo "    - The heartbeat runs every 30 minutes"
echo "    - Each session, the AI reads your files and learns"
echo "    - Knowledge score improves over time"
echo "    - Run 'python3 scripts/knowledge-audit.py' for a gap report"
echo "    - Run 'python3 scripts/expertise-builder.py \"your niche\"' to build domain expertise"
echo ""
echo -e "${GREEN}  You're live. Let's get to work.${NC}"
echo ""

# AI Money Machines Content Crew

Production-ready **CrewAI** project that automates a full content pipeline for the niche: **AI Tools for Making Money** / Personal Finance + AI Side Hustles (faceless YouTube, Reels, TikTok).

## What It Does

Each run generates **7 short-form video pairs** (script + visuals prompt) in separate folders:

1. **Trend research** → 7 short-form video ideas (30–60s angle, with search).
2. **Scripts** → For each idea: one short-form script (500–800 words, dense for 30–60s at ~150 wpm): exhaustive step-by-step how-tos (5–10 steps per tool), expanded examples/case studies (names/dates/earnings), pro tips, common mistakes/pitfalls, variations for beginners/advanced, earnings breakdowns, tool comparisons, affiliate CTA, outro. Optimized for engagement and payouts.
3. **Visuals prompts** → For each script: one unified visuals prompt (500–1,000 words), scene-by-scene with timings, faceless cartoons/realism, copy-paste ready for Runway/Kling/ComfyUI/LTX-2.3 (4K, 30–60s).
4. **SEO** → Per video: basic title, description, tags, thumbnail prompt (appended to each `script.md` for easy posting).

Output is saved as `outputs/YYYY-MM-DD_video1/` … `outputs/YYYY-MM-DD_video7/`, each with `script.md` and `visuals_prompt.md`. No long-form scripts or audio prompts—short-form only.

## Setup

### 1. Environment

**Conda (recommended):**

```bash
conda create -n ai-money-crew python=3.11 -y
conda activate ai-money-crew
```

**Or use venv:**

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. API key

Copy the example env and add your OpenAI key:

```bash
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux
```

Edit `.env` and set:

```
OPENAI_API_KEY=sk-your-openai-key-here
```

Optional: use a different model (default is `gpt-4o-mini`):

```
OPENAI_MODEL_NAME=gpt-4o
```

## How to Run

From the project root:

```bash
python main.py
```

The crew runs sequentially with memory. Output is saved to **7 subfolders**:

```
outputs/YYYY-MM-DD_video1/
  script.md         # Short-form script (500–800 words) + SEO
  visuals_prompt.md # Unified visuals prompt (500–1,000 words) for Runway/Kling/etc.
outputs/YYYY-MM-DD_video2/
  ...
outputs/YYYY-MM-DD_video7/
  ...
```

The `outputs/` folder is created automatically on first run.

## Memory Management

Before generating new ideas, the crew **scans all existing script.md files** under `outputs/` (e.g. `outputs/2026-03-14_video1/script.md`). It extracts a short topic summary from each script and passes this list to the idea and script agents so they can produce **unique, non-overlapping content**. On the first run (no existing scripts), the memory step returns "no existing topics" and the agents generate freely. This keeps each run’s 7 videos distinct from previous runs and avoids duplicate topics.

## Sequential Folder Numbering

Before each run, the project **scans existing `outputs/` subfolders** (e.g. `2026-03-14_video1`, `video7`) to find the highest video number. The next batch of 7 folders starts from the following number (e.g. after video1–video7 exist, the next run creates video8–video14). Folder names include the date by default (e.g. `outputs/2026-03-15_video8/`). If there are no existing video folders, numbering starts at video1.

## Short-Form Batch Generation

Each run now generates **7 short-form video pairs** (script + visuals prompt) in separate folders per run. Each video is 30–60s and optimized for monetization: **TikTok 60s+ payouts**, **Instagram 30–60s bonuses**, **YouTube Shorts Fund** eligibility. Scripts are descriptive and engaging for high retention; visuals prompts are dynamic, viral-style faceless content (Runway/Kling/ComfyUI/LTX-2.3) with scene-by-scene timings that match the script.

## Enhanced Research

Agents now search the **web** and **X (Twitter)** for real tutorials, case studies, and how-tos (e.g. ChatGPT/Canva workflows, earnings proof, step-by-step guides). The idea agent and script agent use these searches to create **substantive, actionable content**: 7 ideas with researched angles, and 7 scripts that include real how-to steps, examples, and implementation tips for better engagement and monetization.

## Improved Scripts

Scripts are now **300–500 words** (still 30–60s when spoken at ~150 wpm) with **in-depth how-tos**, step-by-step instructions, real examples and case studies from web/X searches, tips, potential earnings, and beginner pitfalls. Longer, value-packed scripts boost watch time and retention for TikTok, Instagram, and YouTube Shorts payouts. Run `main.py` to see optional word-count output per script to verify length.

## Further Enhanced Scripts

Scripts are now **500–800 words** with **exhaustive how-tos** (5–10 steps per tool), multiple real examples and case studies (with names/dates/earnings from extended web/X searches), pro tips, common mistakes/pitfalls, variations for beginners vs advanced, potential earnings breakdowns, tool comparisons, and calls to experiment. Deeper, multi-query research per idea produces superior content quality; detailed scripts maximize engagement and watch time for better algo performance and payouts. `main.py` validates word count and prints a warning if any script is below 500 words.

## Customizing the Niche

The niche is hard-coded in `src/crew.py`:

```python
NICHE_KEYWORDS = "AI Tools for Making Money / Personal Finance + AI Side Hustles (faceless YouTube, Reels, TikTok content)"
```

Edit `NICHE_KEYWORDS` (and task descriptions in `src/tasks.py` if you want) to lock the crew to a different niche. The same 4 agents and 4 tasks will run; only the focus changes. Config in `src/crew.py`: `SCRIPT_CONFIG` (`num_videos=7`, `short_form_only=True`, `short_word_min`/`short_word_max`).

## Monetization Optimization

Short-form scripts are word-count optimized for 2026 short-form monetization:

- **TikTok:** 60s+ for payouts; scripts target 150–300 words (30–60s at ~150 wpm).
- **Instagram:** 30–60s for engagement bonuses.
- **YouTube Shorts:** Eligibility for Shorts Fund; same 30–60s format.
- **Visuals:** Each video gets a matching unified visuals prompt (500–1,000 words) for dynamic, viral faceless content in 4K.

## Example Output Structure

Each of the 7 folders contains:

- **script.md** — Short-form script only (150–300 words, hook/CTA/outro), then SEO (title, description, tags, thumbnail prompt). Copy-paste ready for ElevenLabs or other narration tools.
- **visuals_prompt.md** — One unified visuals prompt (500–1,000 words), scene-by-scene with timings. Copy-paste ready for Runway, Kling, ComfyUI, LTX-2.3.

## Project Layout

```
ai-money-machines-crew/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── main.py              # entry point
├── src/
│   ├── __init__.py
│   ├── agents.py        # 4 agents (trend, short-form script, visuals prompt engineer, SEO)
│   ├── tasks.py         # 4 tasks; 7 ideas, 7 short-form scripts, 7 visuals prompts, 7 SEO
│   ├── crew.py          # crew config + assembly
│   └── tools.py         # DuckDuckGo search
└── outputs/             # auto-created; outputs saved here
    └── .gitkeep
```

## Requirements

- Python 3.10+
- OpenAI API key (for CrewAI/LLM)
- DuckDuckGo search is used for trends (no API key)

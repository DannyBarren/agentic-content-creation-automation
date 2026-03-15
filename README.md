# AI Money Machines Content Crew

This repository contains an automated content generation system built with CrewAI and Python, designed for creators producing faceless videos in high-engagement niches like AI tools for making money and personal finance side hustles. It's tailored for platforms such as YouTube Shorts, Instagram Reels, and TikTok, where short-form content can drive significant revenue through ad RPMs, affiliates, and viewer retention.

The system generates 7 short-form video packs per run, including detailed scripts with actionable how-tos, visuals prompts for AI video tools, and optimized SEO. It's built to ensure uniqueness, scalability, and monetization potential, helping creators produce consistent output that scales to $5k–$20k/month as algorithms reward quality and volume.

## What This System Does (And Why It's Built This Way)

This CrewAI pipeline automates the creation of faceless AI content, from idea generation to ready-to-use assets. Run a single command (`python main.py`) to produce 7 complete short-form video packages. It's optimized for niches like AI-driven income strategies—think ChatGPT side hustles or Canva for passive revenue—where finance and tech topics yield strong RPMs ($9–$21 per 1,000 views) and affiliate opportunities (e.g., ClickBank or Amazon links).

Each run delivers:
- A scan of existing outputs to prevent topic repetition.
- Research into web and X trends for 7 unique video ideas.
- 7 detailed scripts (500–800 words each, packed with step-by-step instructions, examples, tips, pitfalls, and CTAs drawn from real-world sources).
- 7 visuals prompts (500–1,000 words, structured scene-by-scene for tools like Runway or Kling, supporting faceless cartoons or realistic styles).
- SEO elements for each video (title, description, tags, and thumbnail prompt).

Outputs are organized into dated, numbered folders (e.g., `outputs/2026-03-15_video8/`), with `script.md` (script + SEO) and `visuals_prompt.md`. Folder numbering continues sequentially across runs, simplifying library management.

The sequential design leverages CrewAI's strength in task chaining, where each step builds on the previous with built-in memory for consistency. This ensures reliable, high-quality results without unnecessary complexity. Scripts emphasize value for retention, with lengths optimized for monetization thresholds (60 seconds+ for TikTok rewards, 30–60 seconds for Instagram bonuses, and YouTube Shorts eligibility).

## Features That Make It Effective for Creators

- **Batch Efficiency**: Produces 7 videos per run, enabling daily or weekly execution to build a content backlog quickly and achieve platform monetization milestones in 3–6 months.
- **Content Uniqueness**: Automatically scans past scripts to summarize and avoid repeated topics, keeping your output fresh and algorithm-friendly.
- **Research Depth**: Agents use web and X searches (via DuckDuckGo) to incorporate real tutorials, case studies, and earnings examples, resulting in scripts with practical steps like "Log into ChatGPT, use prompt 'X' for Y—here's how it generated $500/month for one user."
- **Monetization Focus**: Scripts include hooks, affiliate CTAs, pro tips, and pitfalls to drive engagement; visuals prompts support dynamic 4K faceless content for better viewer retention.
- **Sequential Organization**: Scans the `outputs/` directory to resume numbering from the last video, avoiding overwrites and streamlining workflows.
- **Ready-to-Use Outputs**: Clean Markdown files for easy integration—paste scripts into ElevenLabs for narration or prompts into Kling for video generation.
- **Customization Options**: Adjust niche keywords, LLM models, or script parameters in `src/crew.py` to fit other topics like psychology facts or business documentaries.

This tool is ideal for content creators seeking to automate production while maintaining quality, allowing more time for posting, analytics, and scaling revenue streams.

## How It Works Under the Hood

### Architecture
- **Core Framework**: CrewAI handles multi-agent orchestration with a sequential process—tasks execute in order, each accessing prior outputs via `context=[...]`. Shared memory (`memory=True`) enables reuse of information, such as avoided topics.
- **LLM Integration**: Powered by OpenAI (default gpt-4o-mini; configurable to gpt-4o in `.env`). Temperature set to 0.8 for balanced creativity in detail generation.
- **Tools**: DuckDuckGo-based searches for web and X data (no additional API keys required). A custom `ScanOutputsTool` scans `outputs/` for script files and summarizes topics.
- **Technology Stack**: Python 3.11+, crewai, langchain-openai, duckduckgo-search, python-dotenv, and crewai-tools. Minimal dependencies for reliability.

### Execution Flow
1. **Initialization in `main.py`**:
   - Loads `.env` (requires OPENAI_API_KEY).
   - Ensures `outputs/` exists.
   - Scans subfolders using `get_start_video_number()`: Extracts numbers via regex (e.g., from `video8/`), determines the next starting point (defaults to 1 if empty).
   - Displays the batch range (e.g., "Generating video8 to video14").

2. **Crew Execution**:
   - `create_crew()` in `src/crew.py` assembles 5 agents and 5 tasks.
   - `Crew(...).kickoff()` processes sequentially: Memory scan → Idea generation → Script writing → Visuals prompts → SEO.

3. **Agents Overview**
   - **Memory Manager**: Uses a custom tool to scan `outputs/` for `script.md` files, summarizing topics (first 1–2 sentences, excluding headers/SEO). Also reports the maximum video number. Output includes topics to avoid for uniqueness.
   - **Trend Researcher**: Employs search tools, incorporating memory context to produce 7 distinct ideas (title, hook, angle, rationale based on current trends).
   - **Script Writer**: Conducts additional searches for in-depth how-tos, generating 7 blocks under headers like `## VIDEO 1`, each 500–800 words with practical details.
   - **Visuals Prompt Engineer**: Draws from scripts to create 7 scene-by-scene prompts, without additional tools.
   - **SEO Specialist**: Produces title, description, tags, and thumbnail prompt for each video.

4. **Post-Processing**:
   - Parses raw outputs with `split_video_blocks()`: Divides content based on `## VIDEO N` headers into 7 segments.
   - Creates folders like `outputs/{date}_video{start + i}/`, writing `script.md` (header + script + SEO) and `visuals_prompt.md` (header + prompt).
   - Validates script word counts, issuing console warnings if below 500 to maintain substance.

The memory scan integrates with numbering: The tool provides the max N for reference, while `main.py` performs its own scan for folder creation, ensuring accuracy.

## Setup Instructions

1. Clone the repository: `git clone [repository-url] && cd ai-money-machines-crew`
2. Create and activate the environment: `conda create -n ai-crew python=3.11 -y && conda activate ai-crew`
3. Install dependencies: `pip install -r requirements.txt`
4. Configure `.env`: Copy `.env.example` and add `OPENAI_API_KEY=sk-...` (obtain from OpenAI). Optionally set `OPENAI_MODEL_NAME=gpt-4o` for enhanced performance.
5. Execute: `python main.py`

The first run begins at video1, with outputs stored in `outputs/`. Files are formatted for direct use in downstream tools.

## Usage Guidelines for Creators

- Execute regularly: Generate content daily or weekly to accumulate a library, posting 3–5 videos per week to reach monetization thresholds in 1–3 months (e.g., 1,000 subscribers and 4,000 watch hours on YouTube).
- Customize as needed: Modify `NICHE_KEYWORDS` in `crew.py` for alternative niches, or adjust word counts for varied script lengths.
- Production Workflow: Transfer scripts to ElevenLabs for audio generation, visuals prompts to Kling for clips, and combine in CapCut. Incorporate affiliates in CTAs for additional revenue.
- Optimization Tip: Analyze performance and refine future runs by incorporating successful elements as examples in prompts.
- Estimated Costs: Approximately $0.025 per run using gpt-4o-mini; video generation adds $0.50–$2 per batch via tools like Kling.

## Configuration Options

- `src/crew.py`:
  - `NICHE_KEYWORDS`: Define search terms, such as "AI tools for making money".
  - `DEFAULT_LLM_MODEL`: Specify alternative models.
  - `SCRIPT_CONFIG`: Control parameters like num_videos=7 and min_script_words=500.
- `.env`: Manage API keys and model overrides.

## Benefits Over Manual Creation

For content creators focused on efficiency, this system eliminates repetitive tasks like research and drafting, allowing emphasis on distribution and audience growth. It's faceless-friendly, scalable, and positioned for revenue through optimized, research-backed output.

License: MIT—feel free to use and adapt, with credit appreciated for shared derivatives.

Contributions and feedback are welcome to refine this tool for broader creator use.

- Danny

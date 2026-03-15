"""Tasks for the AI Money Machines Content Crew."""

from crewai import Task

from .agents import (
    create_trend_researcher,
    create_script_writer,
    create_visuals_prompt_engineer,
    create_seo_specialist,
    create_memory_manager,
)


def create_tasks(agents: dict, niche_keywords: str, script_config: dict | None = None):
    """
    Create the five tasks with context chaining (memory first, then 7 short-form videos per run).
    agents: dict with keys memory_manager, trend_researcher, script_writer, visuals_prompt_engineer, seo_specialist
    script_config: optional dict with short_word_min, short_word_max, num_videos, short_form_only
    """
    config = script_config or {}
    short_min = config.get("short_word_min", config.get("min_script_words", 500))
    short_max = config.get("short_word_max", 800)
    num_videos = config.get("num_videos", 7)
    memory_manager = agents["memory_manager"]
    researcher = agents["trend_researcher"]
    writer = agents["script_writer"]
    visuals_engineer = agents["visuals_prompt_engineer"]
    seo = agents["seo_specialist"]

    task_memory = Task(
        description=(
            "Scan the outputs/ folder for ALL existing script.md files (e.g. outputs/2026-03-14_video1/script.md, "
            "outputs/video2/script.md, or any subfolder). Use the scan tool to find and read each file, then extract "
            "or summarize the main topic of each script in 1–2 sentences. The tool also returns the max video number "
            "from existing folders — include that in your output (e.g. 'Max video number: 7') so main can use it for "
            "sequential folder numbering. If no script.md files exist (e.g. first run), output 'No existing scripts. "
            "Generate freely.' and Max video number: 0. Otherwise output a clear list of existing topics/summaries "
            "so the next agents can generate UNIQUE ideas and scripts that do not repeat these topics verbatim."
        ),
        expected_output="List of existing topics (file path + 1–2 sentence topic summary per script), or 'No existing scripts' if empty; plus Max video number from folder scan (for sequential numbering). Used to avoid duplicate content.",
        agent=memory_manager,
    )

    task_trend_research = Task(
        description=(
            "Using the existing topics from the Memory Manager (above), research and generate 7 UNIQUE ideas that "
            f"do NOT repeat those topics verbatim. Search web and X (Twitter) for current trends in '{niche_keywords}' "
            "(e.g. ChatGPT/Canva tutorials, AI side hustles, earnings proof, beginner how-tos). "
            f"Output exactly {num_videos} substantive short-form video ideas (30–60s) that are distinct from the avoided list. "
            "For each idea provide: 1) Title/hook, 2) One-sentence angle from research, 3) Rationale. "
            "Number them (Idea 1, Idea 2, ...). If memory listed no existing scripts, generate freely."
        ),
        expected_output=f"A numbered markdown list of {num_videos} UNIQUE short-form video ideas, each with title, actionable angle, and rationale (non-overlapping with existing topics).",
        agent=researcher,
        context=[task_memory],
    )

    task_script = Task(
        description=(
            "Using the existing topics from the Memory Manager, ensure your scripts do not repeat those topics verbatim. "
            f"For EACH of the {num_videos} short-form video ideas from the Trend Researcher: "
            "Run several web/X searches for comprehensive how-tos, tutorials, case studies, success examples, "
            "mistakes, earnings, and variations (e.g. 'in-depth Canva graphics tutorial steps 2026', "
            "'ChatGPT content creation real case studies', 'Zapier pitfalls and tips', 'real earnings breakdown'). "
            "Then write ONE highly detailed short-form script per idea using what you found. "
            f"Output exactly {num_videos} script blocks. Use exact section headers: ## VIDEO 1, ## VIDEO 2, ... ## VIDEO " + str(num_videos) + ".\n\n"
            "Under each ## VIDEO N include ONLY the short-form script. Each script must be:\n"
            f"- {short_min}–{short_max} words (dense for 30–60s narration at 150 wpm), packed with info to maximize value/retention.\n"
            "- In-depth substance: multiple step-by-step how-tos (5–10 steps per tool), expanded examples/case studies with names/dates/earnings from searches, "
            "pro tips, common mistakes/pitfalls, variations for beginners vs advanced, potential earnings breakdowns, tool comparisons, and calls to experiment.\n"
            "- Structure: hook, main content (exhaustive steps, multiple examples, tips, pitfalls, comparisons), affiliate CTA, outro.\n"
            "- Maximum detail for algo engagement and payouts. No other content—just the script text per video."
        ),
        expected_output=(
            f"List of {num_videos} highly detailed scripts, each 500–800 words packed with researched substance. "
            f"Exactly {num_videos} blocks starting with ## VIDEO 1 through ## VIDEO {num_videos}; each block: one script with exhaustive how-tos, 5–10 steps per section, multiple examples, pro tips, pitfalls, earnings, CTAs."
        ),
        agent=writer,
        context=[task_memory, task_trend_research],
    )

    task_visuals_prompt = Task(
        description=(
            f"Using the {num_videos} short-form scripts from the Script Writer, create exactly {num_videos} unified "
            "visuals prompts—one for each script. Use exact section headers: ## VIDEO 1, ## VIDEO 2, ... ## VIDEO " + str(num_videos) + ".\n\n"
            "Under each ## VIDEO N write ONE unified visuals prompt (500–1,000 words) that:\n"
            "- Is scene-by-scene with timings matching the script (e.g. 0:00–0:08 hook, 0:08–0:25 main, 0:25–0:45 CTA/outro).\n"
            "- Specifies style: faceless cartoons or realism; 4K; dynamic, viral faceless content for Runway/Kling/ComfyUI/LTX-2.3.\n"
            "- Is copy-paste ready for 30–60s video generation. Reference script elements so visuals sync with narration.\n"
            "- No audio/voice content—visuals only. Optimized for high engagement and retention in short-form."
        ),
        expected_output=(
            f"Exactly {num_videos} visuals prompt blocks, each starting with ## VIDEO 1 through ## VIDEO {num_videos}. "
            "Each block: one unified visuals prompt (500–1,000 words), scene-by-scene with timings, matching its script."
        ),
        agent=visuals_engineer,
        context=[task_script],
    )

    task_seo = Task(
        description=(
            f"Using the {num_videos} short-form video ideas and their scripts, produce basic SEO for EACH video. "
            f"Output exactly {num_videos} SEO blocks. Use exact section headers: ## VIDEO 1, ## VIDEO 2, ... ## VIDEO " + str(num_videos) + ".\n\n"
            "Under each ## VIDEO N provide:\n"
            "1) TITLE: Click-worthy, under 60 chars, keyword-rich.\n"
            "2) DESCRIPTION: 1–2 short paragraphs with keywords (short-form video).\n"
            "3) TAGS: 10–15 relevant tags, comma-separated.\n"
            "4) THUMBNAIL PROMPT: One short paragraph for DALL·E/Midjourney (composition, text overlay, colors, 9:16 or 1:1 for shorts)."
        ),
        expected_output=(
            f"Exactly {num_videos} SEO blocks, each starting with ## VIDEO 1 through ## VIDEO {num_videos}. "
            "Each block: title, description, tags, thumbnail prompt (basic, for easy posting)."
        ),
        agent=seo,
        context=[task_script, task_visuals_prompt],
    )

    return [task_memory, task_trend_research, task_script, task_visuals_prompt, task_seo]

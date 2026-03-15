"""Agents for the AI Money Machines Content Crew."""

from crewai import Agent

from .tools import duckduckgo_search, web_search, x_keyword_search, scan_outputs_tool


def create_memory_manager(llm=None) -> Agent:
    """Memory Manager: scans existing scripts to extract topics and prevent duplicates."""
    return Agent(
        role="Memory Manager",
        goal="Scan the outputs folder for existing script.md files, extract or summarize each script's topic "
             "(1–2 sentences per script), and output a clear list of existing topics so the idea and script agents "
             "can generate unique, non-overlapping content.",
        backstory="You ensure content uniqueness by recalling past topics from generated files. You run the "
                  "scan tool, then format the results as a list of topics to avoid so new ideas and scripts "
                  "do not repeat verbatim.",
        tools=[scan_outputs_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


def create_trend_researcher(llm=None) -> Agent:
    """Trend Researcher: finds trends and generates 7 unique short-form video ideas using web/X search and memory."""
    return Agent(
        role="Trend Researcher",
        goal="Use the memory of existing topics (from the Memory Manager) to avoid repeats. Research viral trends "
             "and search web/X for real examples, tutorials, and case studies on AI money-making tools. "
             "Generate exactly 7 UNIQUE, non-repeating short-form video ideas with actionable angles.",
        backstory="You are an expert at spotting viral trends and finding real, substantive content. You receive "
                  "a list of existing topics to avoid and use web/X search to find new angles, then turn them "
                  "into 7 concrete, non-overlapping ideas (30–60s angle) with hooks and rationale.",
        tools=[duckduckgo_search, web_search, x_keyword_search],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


def create_script_writer(llm=None) -> Agent:
    """Script Writer: highly detailed, unique short-form scripts (500–800 words) using web/X research and memory."""
    return Agent(
        role="Short-Form Script Writer",
        goal="Use the memory of existing topics to avoid verbatim repeats. Conduct extensive web/X searches "
             "(multiple queries per idea) for in-depth tutorials, examples, success stories, and earnings data, "
             "then write highly detailed short-form scripts (500–800 words) that are unique and non-overlapping "
             "with existing scripts, with exhaustive step-by-step instructions, multiple examples, tips, pitfalls, "
             "comparisons, and CTAs for maximum substance and engagement.",
        backstory="You are a short-form content writer who grounds every script in deep research and avoids duplicates. "
                  "You receive a list of existing topics and use web/X search to gather new angles, then weave "
                  "exhaustive scripts (5–10 steps per tool, case studies, pro tips, pitfalls, comparisons, CTAs) "
                  "that do not repeat past content verbatim.",
        tools=[web_search, x_keyword_search],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


def create_visuals_prompt_engineer(llm=None) -> Agent:
    """AI Visuals Prompt Engineer: unified visuals prompts for short-form videos."""
    return Agent(
        role="AI Visuals Prompt Engineer",
        goal="Create one detailed unified visuals prompt per short-form script: 500–1,000 words, "
             "scene-by-scene with timings and styles for 30–60s faceless video. Copy-paste ready "
             "for Runway, Kling, ComfyUI, LTX-2.3 (4K, cartoons/realism). Match script timings for sync.",
        backstory="You are an expert at writing visual briefs for AI video tools. You produce "
                  "unified prompts that reference script elements and timings so visuals sync with "
                  "narration. Dynamic, viral-style faceless content for high engagement and retention.",
        tools=[],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


def create_seo_specialist(llm=None) -> Agent:
    """SEO Specialist: title, description, tags, thumbnail prompt."""
    return Agent(
        role="SEO Specialist",
        goal="Produce SEO-optimized YouTube metadata: title, description, tags, and "
             "a thumbnail prompt that drives clicks and matches the video content.",
        backstory="You are a YouTube SEO expert. You know how to write titles and "
                  "descriptions that rank and convert. You create thumbnail prompts "
                  "that are specific and visually compelling.",
        tools=[],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )



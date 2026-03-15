"""Crew assembly for the AI Money Machines Content Crew."""

from crewai import Crew, LLM, Process

from .agents import (
    create_trend_researcher,
    create_script_writer,
    create_visuals_prompt_engineer,
    create_seo_specialist,
    create_memory_manager,
)
from .tasks import create_tasks

# Config: niche and model (change here to customize)
NICHE_KEYWORDS = "AI Tools for Making Money / Personal Finance + AI Side Hustles (faceless YouTube, Reels, TikTok content)"
DEFAULT_LLM_MODEL = "gpt-4o-mini"  # Switch to "gpt-4o" for higher quality

# Batch size and short-form script config (short-form only, no long-form)
SCRIPT_CONFIG = {
    "num_videos": 7,             # Number of short-form video pairs (script + visuals prompt) per run
    "short_form_only": True,     # Only short-form scripts (30–60s); no long-form
    "min_script_words": 500,     # Minimum script length (strictly enforce 500+ words)
    "max_script_words": 800,     # Maximum script length for highly detailed content
    "short_word_min": 500,       # Short-form script min words (dense for retention)
    "short_word_max": 800,       # Short-form script max words (exhaustive substance)
}


def create_llm(model_name: str | None = None, temperature: float = 0.8):
    """Create LLM (OpenAI by default). Uses OPENAI_MODEL_NAME from env if set. temperature=0.8 for creativity in detail weaving."""
    import os
    name = model_name or os.getenv("OPENAI_MODEL_NAME", DEFAULT_LLM_MODEL)
    return LLM(model=name, temperature=temperature)


def create_crew(llm=None):
    """Build and return the Crew with sequential process and memory."""
    if llm is None:
        llm = create_llm()

    agents = {
        "memory_manager": create_memory_manager(llm=llm),
        "trend_researcher": create_trend_researcher(llm=llm),
        "script_writer": create_script_writer(llm=llm),
        "visuals_prompt_engineer": create_visuals_prompt_engineer(llm=llm),
        "seo_specialist": create_seo_specialist(llm=llm),
    }

    tasks = create_tasks(agents, NICHE_KEYWORDS, SCRIPT_CONFIG)

    # memory=True retains search results across tasks for richer script writing; verbose=True for search logging
    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        memory=True,
        verbose=True,
    )
    return crew

"""Tools for the AI Money Machines Content Crew."""

import re
from pathlib import Path

from crewai.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun

# Outputs dir for memory scan (project root / outputs)
OUTPUTS_DIR = Path(__file__).resolve().parent.parent / "outputs"


def get_max_video_number_from_outputs() -> int:
    """Scan outputs/ for subfolders matching *videoN*, return highest N (0 if none)."""
    if not OUTPUTS_DIR.exists():
        return 0
    numbers = []
    for name in OUTPUTS_DIR.iterdir():
        if not name.is_dir():
            continue
        match = re.search(r"video(\d+)$", name.name, re.IGNORECASE)
        if not match:
            match = re.search(r"video(\d+)", name.name, re.IGNORECASE)
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers, default=0)


class DuckDuckGoSearchTool(BaseTool):
    """CrewAI-compatible wrapper for DuckDuckGo web search."""

    name: str = "DuckDuckGo Search"
    description: str = (
        "Search the web for current information. Use this to find trending topics, "
        "news, and viral angles in AI tools for making money, side hustles, and personal finance."
    )

    def _run(self, query: str) -> str:
        """Execute the search and return results."""
        try:
            search = DuckDuckGoSearchRun()
            return search.run(query)
        except Exception as e:
            return f"Search error: {str(e)}"


class WebSearchTool(BaseTool):
    """Search the web for tutorials, case studies, how-tos, and real examples."""

    name: str = "Web Search"
    description: str = (
        "Search the web for step-by-step tutorials, case studies, real examples, and how-tos "
        "on AI tools for making money (e.g. ChatGPT/Canva workflows, earnings proof, beginner tips). "
        "Use queries like 'real examples [topic] step-by-step tutorials 2026' or 'how to make money with [tool] case study'."
    )

    def _run(self, query: str) -> str:
        """Execute web search and return results."""
        try:
            search = DuckDuckGoSearchRun()
            return search.run(query)
        except Exception as e:
            return f"Web search error: {str(e)}"


class XKeywordSearchTool(BaseTool):
    """Search X (Twitter) for real examples, tips, and discussions."""

    name: str = "X (Twitter) Search"
    description: str = (
        "Search X (Twitter) for real examples, tips, earnings proof, and discussions about "
        "AI tools for making money, side hustles, and personal finance. Use to find viral threads, "
        "case studies, and actionable advice people share on X."
    )

    def _run(self, query: str) -> str:
        """Execute X/Twitter search via web search (site:x.com)."""
        try:
            search = DuckDuckGoSearchRun()
            # Restrict to X/Twitter to get social proof and real discussions
            x_query = f"site:x.com OR site:twitter.com {query}"
            return search.run(x_query)
        except Exception as e:
            return f"X search error: {str(e)}"


def _extract_topic_summary(text: str, max_chars: int = 280) -> str:
    """Extract 1–2 sentence topic summary from script content (simple extraction, no LLM)."""
    if not text or not text.strip():
        return "(empty)"
    # Drop header block (title + Generated line) and SEO section
    lines = []
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("# ") or line.startswith("**Generated:**") or line == "---":
            continue
        if line.startswith("## SEO"):
            break
        if line:
            lines.append(line)
    text = " ".join(lines).strip()
    if not text:
        return "(no body)"
    # First 1–2 sentences
    sentences = []
    for s in text.replace("!", ".").replace("?", ".").split("."):
        s = s.strip()
        if s and len(s) > 10:
            sentences.append(s + ("." if not s.endswith(".") else ""))
            if len(sentences) >= 2:
                break
    if not sentences:
        return text[:max_chars] + ("..." if len(text) > max_chars else "")
    summary = " ".join(sentences).strip()
    return summary[:max_chars] + ("..." if len(summary) > max_chars else summary)


class ScanOutputsTool(BaseTool):
    """Scan outputs folder for existing script.md files and extract topic summaries."""

    name: str = "Scan Existing Scripts"
    description: str = (
        "Scan the outputs/ folder for all script.md files (e.g. outputs/2026-03-14_video1/script.md), "
        "read each file, and extract a 1–2 sentence topic summary per script. Use this before generating "
        "new ideas to avoid duplicate topics. Call with trigger='scan' or any string to run the scan. "
        "Returns a list of {file: path, topic_summary: summary}. If no script.md files exist (e.g. first run), returns empty list."
    )

    def _run(self, trigger: str = "scan") -> str:
        """Scan outputs/ for script.md files, read and summarize topics. Handles empty folder gracefully."""
        try:
            if not OUTPUTS_DIR.exists():
                return "No outputs folder found. Existing topics: (none) — first run, generate freely.\nMax video number: 0"
            script_paths = sorted(OUTPUTS_DIR.rglob("script.md"))
            if not script_paths:
                max_num = get_max_video_number_from_outputs()
                return f"No script.md files found in outputs/. Existing topics: (none) — first run, generate freely.\nMax video number: {max_num}"
            results = []
            for path in script_paths:
                try:
                    content = path.read_text(encoding="utf-8", errors="replace")
                    summary = _extract_topic_summary(content)
                    try:
                        rel = path.relative_to(OUTPUTS_DIR)
                    except ValueError:
                        rel = path
                    results.append({"file": str(rel), "topic_summary": summary})
                except Exception as e:
                    results.append({"file": str(path), "topic_summary": f"(read error: {e})"})
            if not results:
                return "Existing topics: (none).\nMax video number: 0"
            max_num = get_max_video_number_from_outputs()
            lines = ["EXISTING TOPICS TO AVOID (do not repeat verbatim):"]
            for i, r in enumerate(results, 1):
                lines.append(f"  {i}. File: {r['file']}")
                lines.append(f"     Topic/summary: {r['topic_summary']}")
            lines.append(f"Max video number: {max_num}")
            return "\n".join(lines)
        except Exception as e:
            return f"Scan error: {str(e)}. Proceed without memory. Max video number: {get_max_video_number_from_outputs()}"


# Instances for agents
duckduckgo_search = DuckDuckGoSearchTool()
web_search = WebSearchTool()
x_keyword_search = XKeywordSearchTool()
scan_outputs_tool = ScanOutputsTool()

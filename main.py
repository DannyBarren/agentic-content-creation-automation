"""
AI Money Machines Content Crew — Entry point.

Runs the crew and saves 7 short-form video pairs (script + visuals prompt) into
outputs/YYYY-MM-DD_videoN/ with sequential numbering (e.g. after video7, creates video8–14).
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime

# Load .env before any crew imports that might use env vars
from dotenv import load_dotenv
load_dotenv()

# Ensure project root is on path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.crew import create_crew, SCRIPT_CONFIG

OUTPUTS_DIR = PROJECT_ROOT / "outputs"
NUM_VIDEOS = SCRIPT_CONFIG.get("num_videos", 7)


def ensure_outputs_dir():
    """Create outputs/ if it doesn't exist."""
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def get_start_video_number() -> int:
    """Scan outputs/ for existing video* subfolders, return next available number (1 if none)."""
    if not OUTPUTS_DIR.exists():
        return 1
    numbers = []
    for path in OUTPUTS_DIR.iterdir():
        if not path.is_dir():
            continue
        match = re.search(r"video(\d+)$", path.name, re.IGNORECASE) or re.search(
            r"video(\d+)", path.name, re.IGNORECASE
        )
        if match:
            numbers.append(int(match.group(1)))
    max_num = max(numbers, default=0)
    return max_num + 1


def split_video_blocks(raw: str, num_blocks: int) -> list[str]:
    """
    Split task output into num_blocks by ## VIDEO 1, ## VIDEO 2, ... headers.
    Returns list of content strings (one per video); empty string if not found.
    """
    blocks = [""] * num_blocks
    for i in range(1, num_blocks + 1):
        header = f"## VIDEO {i}"
        next_header = f"## VIDEO {i + 1}" if i < num_blocks else None
        start = raw.find(header)
        if start == -1:
            continue
        start = raw.find("\n", start) + 1 if raw.find("\n", start) != -1 else start + len(header)
        if next_header and raw.find(next_header, start) != -1:
            end = raw.find(next_header, start)
            blocks[i - 1] = raw[start:end].strip()
        else:
            blocks[i - 1] = raw[start:].strip()
    return blocks


def main():
    print("=" * 60)
    print("AI Money Machines Content Crew")
    print("Niche: AI Tools for Making Money / Personal Finance + AI Side Hustles")
    print(f"Batch: {NUM_VIDEOS} short-form video pairs (script + visuals prompt) per run")
    print("=" * 60)

    if not os.getenv("OPENAI_API_KEY"):
        print("\n[WARN] OPENAI_API_KEY not set. Set it in .env or environment.")
        print("Create .env from .env.example and add your key.\n")

    try:
        ensure_outputs_dir()
        start_num = get_start_video_number()
        end_num = start_num + NUM_VIDEOS - 1
        print(f"[*] Next batch: video{start_num}–video{end_num} (sequential from existing outputs)\n")

        crew = create_crew()
        print("\n[*] Starting crew (memory scan first, then sequential)...\n")
        result = crew.kickoff()
        print("\n[+] Crew run finished.\n")

        if result is None:
            print("[ERROR] Crew returned no result.", file=sys.stderr)
            return 1

        # Task order: 0=memory, 1=trend (ideas), 2=script, 3=visuals_prompt, 4=SEO
        # Short-form: 500–800 words per script (strict); visuals prompt 500–1,000 words each
        tasks_out = getattr(result, "tasks_output", [])
        script_raw = tasks_out[2].raw if len(tasks_out) > 2 else ""
        visuals_raw = tasks_out[3].raw if len(tasks_out) > 3 else ""
        seo_raw = tasks_out[4].raw if len(tasks_out) > 4 else ""

        script_blocks = split_video_blocks(script_raw, NUM_VIDEOS)
        visuals_blocks = split_video_blocks(visuals_raw, NUM_VIDEOS)
        seo_blocks = split_video_blocks(seo_raw, NUM_VIDEOS)

        ensure_outputs_dir()
        date_str = datetime.now().strftime("%Y-%m-%d")

        for i in range(1, NUM_VIDEOS + 1):
            video_num = start_num + i - 1
            folder_name = f"{date_str}_video{video_num}"
            video_dir = OUTPUTS_DIR / folder_name
            video_dir.mkdir(parents=True, exist_ok=True)
            print(f"[*] Created folder: {video_dir} (video{video_num})")

            script_content = script_blocks[i - 1] if i <= len(script_blocks) else ""
            visuals_content = visuals_blocks[i - 1] if i <= len(visuals_blocks) else ""
            seo_content = seo_blocks[i - 1] if i <= len(seo_blocks) else ""

            script_path = video_dir / "script.md"
            script_body = script_content.strip()
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(f"# Video {video_num} — Short-Form Script\n\n")
                f.write(f"**Generated:** {datetime.now().isoformat()}\n\n---\n\n")
                f.write(script_body)
                if seo_content:
                    f.write("\n\n---\n\n## SEO\n\n")
                    f.write(seo_content.strip())
            print(f"    Saved: {script_path}")
            # Word count validation: target 500–800 words; warn if short
            word_count = len(script_body.split()) if script_body else 0
            min_required = SCRIPT_CONFIG.get("min_script_words", 500)
            print(f"    Script word count: {word_count} (target 500–800)")
            if word_count < min_required:
                print(f"    [WARN] Video {video_num} script is below minimum {min_required} words — consider re-running or editing for more substance.")

            visuals_path = video_dir / "visuals_prompt.md"
            with open(visuals_path, "w", encoding="utf-8") as f:
                f.write(f"# Video {video_num} — Unified Visuals Prompt\n\n")
                f.write(f"**Generated:** {datetime.now().isoformat()}\n\n---\n\n")
                f.write(visuals_content.strip())
            print(f"    Saved: {visuals_path}")

        print(f"\n[*] Done: video{start_num}–video{end_num} saved under {OUTPUTS_DIR}/")
        return 0

    except Exception as e:
        print(f"\n[ERROR] Crew run failed: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    sys.exit(main() or 0)

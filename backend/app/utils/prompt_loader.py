from pathlib import Path
from typing import Optional

PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"

def load_prompt(name: str, domain: Optional[str] = None) -> str:
    """
    Loads a prompt from the structured prompts directory.
    If domain is provided, looks in prompts/{domain}/{name}.
    Otherwise, searches recursively for the first match.
    """
    if domain:
        path = PROMPT_DIR / domain / name
        if not path.suffix:
            path = path.with_suffix(".txt")
        if path.exists():
            return path.read_text(encoding="utf-8")
            
    # Recursive search if not found or domain not provided
    for path in PROMPT_DIR.rglob("*.txt"):
        if path.name == name or path.stem == name:
            return path.read_text(encoding="utf-8")
            
    raise FileNotFoundError(f"Prompt not found: {name} (domain: {domain})")

from pathlib import Path


def load_rmk_rules(dir: str, file: str = "system.md", xml=True) -> str | None:
    """
    Load the rules from the .rmk/rules directory.
    """
    rules_file = Path(dir) / ".rmk" / "rules" / file
    if not rules_file.exists():
        return None
    rules_content = Path(rules_file).read_text().strip()
    if not rules_content:
        return None
    return f"<user_rules>\n{rules_content}\n</user_rules>"

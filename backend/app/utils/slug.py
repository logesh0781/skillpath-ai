import re
import secrets


def slugify(text: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return f"{base}-{secrets.token_hex(3)}"

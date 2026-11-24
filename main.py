"""Office Judge Joke — entry for make.fun's "Make the AI Judge Laugh: Office Jokes".

Writes a single one-line office joke to /output/entry.txt.
The gate requires UTF-8 text of 1 to 199 characters, not only whitespace.

The program validates the line against that gate (validate_entry: 1-199
chars, single line, non-blank), honours the grader's MAKEFUN_OUTPUT_DIR
(or legacy OUTPUT_DIR), and reads the file back after writing to confirm
the grader will see exactly the validated joke.
"""

import os

JOKE = "I blocked two hours to focus, and my calendar immediately scheduled a sync to discuss why I blocked two hours."


def output_path() -> str:
    """Where the entry goes: the grader's MAKEFUN_OUTPUT_DIR (or the
    legacy OUTPUT_DIR), falling back to /output."""
    out_dir = (
        os.environ.get("MAKEFUN_OUTPUT_DIR")
        or os.environ.get("OUTPUT_DIR")
        or "/output"
    )
    return os.path.join(out_dir, "entry.txt")


def validate_entry(text: str) -> str:
    """Enforce the kit gate from RULES.txt: 1-199 UTF-8 characters,
    a single line, not only whitespace. Returns the stripped line."""
    line = text.strip()
    if not line:
        raise ValueError("entry must not be empty or only whitespace")
    if len(line) > 199:
        raise ValueError(f"entry is {len(line)} chars, over the 199-char gate")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    line.encode("utf-8")  # raises if the text is not valid UTF-8
    return line


def main() -> None:
    text = validate_entry(JOKE)
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    # Round-trip: read it back and confirm the grader will see exactly
    # the validated joke, so a truncated or mangled write never slips
    # through silently.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != text:
        raise ValueError(f"wrote {written!r}, expected {text!r}")


if __name__ == "__main__":
    main()

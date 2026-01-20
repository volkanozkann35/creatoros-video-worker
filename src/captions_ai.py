from pathlib import Path

def generate_caption(video_path: Path) -> dict:
    """
    Şimdilik stabil, deterministic caption.
    (İstersen sonra OpenAI ile gerçek AI caption ekleriz.)
    """
    stem = video_path.stem.replace("_", " ").strip()
    title = stem[:80] if stem else "New Short"

    caption = (
        f"{title}\n\n"
        "⚡️ Daily boost • SolaraMade\n"
        "#shorts #reels #motivation #solaramade"
    )

    return {
        "title": title,
        "caption": caption,
        "description": caption,
        "tags": ["shorts", "reels", "motivation", "solaramade"]
    }

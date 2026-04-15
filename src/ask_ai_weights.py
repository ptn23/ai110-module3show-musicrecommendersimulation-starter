"""
Asks Claude to implement the load_songs function for the music recommender.

Usage (from project root):
    cd ai110-module3show-musicrecommendersimulation-starter
    python src/ask_ai_weights.py
"""

import anthropic


def ask_ai() -> None:
    client = anthropic.Anthropic()

    prompt = """
I am building a music recommender in Python. I need you to implement a function
called load_songs that reads a CSV file and returns a list of dictionaries.

Requirements:
- Use Python's built-in csv module (csv.DictReader) to read the file.
- The CSV has these columns:
    id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness
- Return a list of dicts, one per row.
- Convert numerical columns to the correct Python types so math works later:
    - id         → int
    - tempo_bpm  → int
    - energy     → float
    - valence    → float
    - danceability → float
    - acousticness → float
- Leave id, title, artist, genre, mood as their natural types (str / int).

Function signature:
    def load_songs(csv_path: str) -> list[dict]:

Please provide the complete implementation with a brief explanation of each step.
"""

    print("Asking Claude how to implement load_songs...\n")
    print("=" * 60)

    with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)

    print("\n" + "=" * 60)


if __name__ == "__main__":
    ask_ai()

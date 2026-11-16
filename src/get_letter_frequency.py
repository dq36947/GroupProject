import requests
from helpers import normalise_string
from pathlib import Path
import string

def save_book(url: str, filename: str) -> bool:
    """Saves the book at the given url to the data folder"""
    DATA_DIR = Path(__file__).resolve().parent / "data"
    DATA_DIR.mkdir(parents=True, exist_ok=True)     # create the folder if needed
    path = DATA_DIR / filename

    try:
        result = requests.get(url, timeout=10)
        result.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Download failed: {e}")
        return False

    result.encoding = result.apparent_encoding
    path.write_text(result.text, encoding="utf-8")
    print(f"Saved to {path.resolve()}")
    return True

def analyse_frequencies() -> list:
    """Calculates the frequency for every letter in the alphabet in the data dir and returns it as a list"""
    DATA_DIR = Path(__file__).resolve().parent / "data"     
    frequencies = [0] * 26

    for file in DATA_DIR.glob("*.txt"):
        text = normalise_string(file.read_text(encoding="utf-8"))
        text = text.lower()
        book_freqs = [text.count(c) for c in string.ascii_lowercase]
        for i, n in enumerate(book_freqs):
            frequencies[i] += n

    return [freq / sum(frequencies) for freq in frequencies]



# save_book("https://www.gutenberg.org/files/1342/1342-0.txt", "pride_and_prejudice.txt")
# save_book("https://www.gutenberg.org/files/2701/2701-0.txt", "moby_dick.txt")
# save_book("https://www.gutenberg.org/files/2600/2600-0.txt", "war_and_peace.txt")

for letter, freq in zip(string.ascii_lowercase, analyse_frequencies()):
    print(f"{letter}:   {freq:.4f}")

print(analyse_frequencies())
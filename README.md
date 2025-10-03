# Book Recommendation Portfolio Project

A Python-based application for the recommendation of series and standalone books based on book genres and filters for length, publication date, and rating. Created as the second of Codecademy's computer science career path portfolio projects, it is meant to showcase an understanding of a trie for genre searching as well as sorting algorithms (in this case, an in-place quicksort) for the sorting of results.

## Features
- Search books by one or more genres using a trie for efficient prefix matching (e.g., "h" for "horror" or "historical fiction").
- Filter results by minimum rating, book length, series length, and/or publication year.
- Sort results by Goodreads rating using an in-place quicksort algorithm.
- Display detailed book information, including information about the book series (as well as whether it is currently ongoing) and if it takes place in a shared universe with other books and series.
- Database includes 37 books and series from a variety of genres, ranging from books published in the early 19th century to books published recently.

## Installation
1. Ensure Python 3.x is installed.
2. Clone or download the project files: `booksearch.py`, `GenreTree.py`, and `books.py`.
3. Place all files in the same directory.
4. No additional dependencies are required (uses standard Python libraries).

## Usage
Run the program with:
```bash
python3 booksearch.py

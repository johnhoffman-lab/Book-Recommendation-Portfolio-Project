#Book search program utilizing a trie for searching genres, various filters to narrow the search, and a quicksort function for sorting matching books by rating.
from GenreTree import GenreTree
from books import booklist
import random

"""Runs the book search program, coordinating genre selection, filtering, and display.

Args: booklist (dict): Dictionary of books with their attributes.

Returns: None"""
def main(booklist):
    genre_tree = BuildTree(**booklist)
    user_continue = True
    while user_continue:
        genre_list = GenreList(genre_tree)
        books = BookSearch(genre_list, booklist.keys(), **booklist)
        sorted_books = FilterOptions(books, **booklist)
        PrintBooks(sorted_books, **booklist)
        user_continue = SearchAgain()

"""Builds a trie of genres for the user to search.

Args: booklist (dict): Dictionary of books with their attributes.

Returns: GenreTree: Trie containing all unique genres in the database."""
def BuildTree(**booklist):
    genre_tree = GenreTree()
    genre_set = set()
    for book in booklist.values():
        for genre in book["genres"]:
            genre_set.add(genre)
    for genre in genre_set:
        genre_tree.AddWord(genre)
    return genre_tree

"""Builds a list of genres based on the user's search terms. Restarts if the search terms are invalid.

Args: genre_tree (GenreTree): Trie containing all unique genres in the database.

Returns: list: A list of genres the user wishes to search."""
def GenreList(genre_tree):
    genre_list = []
    available_genres = sorted(genre_tree.ListGenres(genre_tree.root.children, "", []))
    options_list = "The available genres are: " + ", ".join(available_genres[:-1]) + f", and {available_genres[-1]}.\n"
    user_input = input("Please enter a genre to search or a partial word to search for genres starting with those letters. Press Enter to see a list of genres available.\n")
    while user_input == "":
        user_input = input(options_list)
    new_genre = SelectionConfirmation(genre_tree.SearchTree(user_input.lower()), genre_tree)
    if new_genre:
        genre_list.append(new_genre)
        more_searches = ""
        while more_searches.lower() not in ["n", "no"]:
            more_searches = input("Would you like to add more genres to the search?\n")
            if more_searches.lower() in ["y", "yes"]:
                user_input = input("Please enter another genre to add to the search or a partial word to search for genres starting with those letters. Press Enter to see a list of available genres.\n")
                while user_input == "":
                    user_input = input(options_list)
                new_genre = SelectionConfirmation(genre_tree.SearchTree(user_input.lower()), genre_tree)
                if new_genre:
                    genre_list.append(new_genre)
                else:
                    continue
    else:
        return GenreList(genre_tree) #Restarts the function if no genre matches the first search.
    return genre_list

"""Confirms the choice with the user, providing them a list of options if multiple genres match their search.

Args:   genre_list (list): List of genres matching the user's search
        genre_tree (GenreTree): Trie containing all unique genres in the database
        retries (int): Tracks retry attempts (default: 3)
        
Returns: str or bool: Selected genre or False if the search is invalid"""
def SelectionConfirmation(genre_list, genre_tree, retries = 3):
    if retries == 0: #Prevents infinite recursion by limiting retries
        print("Let's start over.")
        return False
    if not genre_list:
        print("It doesn't look like our books on file have a genre matching that selection. Try again.")
        return False
    elif len(genre_list) == 1:
        selection = input(f"Did you want to search for books in the {genre_list[0]} genre? yes/no\n")
        if selection.lower() in ["y", "yes"]:
            return genre_list[0]
        elif selection.lower() in ["n", "no"]:
            return False
        else:
            print("That is not a valid selection.")
            return SelectionConfirmation(genre_list, genre_tree, retries - 1)
    else:
        options = f"It looks like multiple genres match that search. The matching genres in our database are: " +  (f"{genre_list[0]} and {genre_list[1]}" if len(genre_list) == 2 else f"{', '.join(genre_list[:-1])}, and {genre_list[-1]}") + ". Which one would you like to search?\n"
        selection = input(options).lower()
        if selection in genre_list:
            return selection
        else:
            new_genre_search = genre_tree.SearchTree(selection)
            if new_genre_search:
                return SelectionConfirmation(new_genre_search, genre_tree, retries - 1)
            else:
                print("That's not a valid selection. Try again.")
                return False

"""Searches the database for books matching all searched genres (all books if no genres are entered).

Args:   genres (list): List of searched genres
        book_list (iterable): List of books in the database
        bookdict (dict): Dictionary of book attributes
        
Returns: list of book titles matching the genres"""
def BookSearch(genres, book_list, **bookdict):
    if len(genres) == 0:
        return list(book_list)
    new_list = [book for book in book_list if all(genre in bookdict[book]["genres"] for genre in genres)]
    return new_list

"""Filters books based on user preference

Args:   books (list): List of book titles matching the initial search
        bookdict (dict): Dictionary of book attributes
        
Returns: list: Filtered and sorted books"""
def FilterOptions(books, **bookdict):
    min_rating = min_size = max_size = min_series = max_series = oldest = newest = None
    options = ["rating", "length", "series length", "date"]
    user_choice = input(f"Would you like to filter books? You can filter the results by rating, length, series length, or date. Alternatively, type \"search\" to run the search.\n").lower()
    while user_choice not in options and user_choice != "search":
        user_choice = input("Invalid option. You can filter the results by rating, length, series length, or date. Alternatively, enter \"search\" to search without filters.\n")
    if user_choice == "search":
        filtered_books = BookFilter(books, min_rating, oldest, newest, min_size, max_size, min_series, max_series, **bookdict)
        if len(filtered_books) > 1:
            SortBooks(filtered_books, 0, len(filtered_books) - 1, **bookdict)
        return filtered_books
    while user_choice != "search" and len(options) > 0:
        if user_choice in options:
            if user_choice == "rating":
                min_rating = RatingsFilter()
                if min_rating is not None:
                    options.remove("rating")
            elif user_choice == "length":
                if min_size is None and max_size is None:
                    min_or_max = input("Would you like to filter by minimum or maximum length?\n").lower()
                    if min_or_max in ["min", "minimum"]:
                        min_size = SetMinimum(max_size)
                    elif min_or_max in ["max", "maximum"]:
                        max_size = SetMaximum(max_size)
                    else:
                        print("Please select minimum or maximum.")
                elif min_size is not None:
                    max_size = SetMaximum(min_size)
                    if max_size is not None: #Removes the option only if min and max are set.
                        options.remove("length")
                    #... similar for series length and date ...
                elif max_size is not None:
                    min_size = SetMinimum(max_size)
                    if min_size is not None:
                        options.remove("length")
            elif user_choice == "series length":
                if min_series is None and max_series is None:
                    min_or_max = input("Would you like to filter by minimum or maximum length?\n").lower()
                    if min_or_max in ["min", "minimum"]:
                        min_series = SetMinimum(max_series)
                    elif min_or_max in ["max", "maximum"]:
                        max_series = SetMaximum(max_series)
                    else:
                        print("Please select minimum or maximum.")
                elif min_series is not None:
                    max_series = SetMaximum(min_series)
                    if max_series is not None:
                        options.remove("series length")
                elif max_series is not None:
                    min_series = SetMinimum(max_series)
                    if min_series is not None:
                        options.remove("series length")
            elif user_choice == "date":
                if oldest is None and newest is None:
                    min_or_max = input("Would you like to filter by oldest or newest published year?\n").lower()
                    if min_or_max == "oldest":
                        oldest = SetOldest(newest)
                    elif min_or_max == "newest":
                        newest = SetNewest(oldest)
                    else:
                        print("Please select oldest or newest.")
                elif oldest is not None:
                    newest = SetNewest(oldest)
                    if newest is not None:
                        options.remove("date")
                elif newest is not None:
                    oldest = SetOldest(newest)
                    if oldest is not None:
                        options.remove("date")
        if len(options) > 0:
            options_string = (options[0] if len(options) == 1 else f"{options[0]} or {options[1]}" if len(options) == 2 else f"{', '.join(options[:-1])}, or {options[-1]}") #Format filter options for user prompt.
            user_choice = input(f"Would you like to add another filter? You can filter the results by {options_string}. Alternatively, type \"search\" to run the search.\n").lower()
            while user_choice not in options and user_choice != "search":
                user_choice = input(f"Invalid option. You can filter the results by {options_string} or enter \"search\" to search without any additional filters.\n")
    filtered_books = BookFilter(books, min_rating, oldest, newest, min_size, max_size, min_series, max_series, **bookdict)
    if len(filtered_books) > 1:
        SortBooks(filtered_books, 0, len(filtered_books) - 1, **bookdict)
    return filtered_books

"""Filters books based on the user's preference.

Args:   books (list): List of book titles matching the initial search
        min_rating (float or None): Minimum rating filter
        oldest (int or None): Earliest release year
        newest (int or None): Latest release year
        min_pages (int or None): Minimum page count
        max_pages (int or None): Maximum page count
        min_series (int or None): Minimum series length in pages
        max_series (int or None): Maximum series length in pages
        bookdict (dict): Dictionary of book attributes
        
Returns: list: Book titles matching all filters"""
def BookFilter(books, min_rating, oldest, newest, min_pages, max_pages, min_series, max_series, **bookdict):
    def matches(book):
        return ((min_rating is None or bookdict[book]["rating"] >= min_rating) and (oldest is None or bookdict[book]["release_date"] >= oldest) and (newest is None or bookdict[book]["release_date"] <= newest) and (min_pages is None or bookdict[book]["length"] >= min_pages) and (max_pages is None or bookdict[book]["length"] <= max_pages) and (min_series is None or bookdict[book]["series_length"] >= min_series) and (max_series is None or bookdict[book]["series_length"] <= max_series))
    return [book for book in books if matches(book)]

"""Gets and validates a minimum rating (0-5) from the user.

Returns: float or None: Valid rating or None if skipped"""
def RatingsFilter():
    while True:
        user_minimum = input("What should the minimum rating be? 0-5 or Enter to skip.\n")
        if user_minimum == "":
            return None
        try:
            min_rating = float(user_minimum)
            if 0 <= min_rating <= 5:
                return min_rating
            else:
                print("Minimum rating needs to be between 0 and 5.")
        except ValueError:
            print("That is not a valid rating.")

"""Gets and validates a minimum page count (either for the first book or for a series), ensures it's not greater than max_size.

Args: max_size (int or None): Maximum page count for validation

Returns: int or None: Valid minimum page count or None if skipped"""
def SetMinimum(max_size):
    while True:
        user_minimum = input("What should be the minimum length in pages? Press Enter to skip.\n")
        if user_minimum == "":
            return None
        try:
            min_size = int(user_minimum)
            if max_size is not None and min_size > max_size:
                print("You can't have a minimum size larger than the maximum!")
                continue
            if min_size < 0:
                print("This isn't your bank account. You can't have a negative number of pages.")
                continue
            return min_size
        except ValueError:
            print("That is not a valid amount.")

"""Gets and validates a maximum page count (either for the first book or for a series), ensures it's not less than min_size.

Args: min_size (int or None): Minimum page count for validation

Returns: int or None: Valid maximum page count or None if skipped"""
def SetMaximum(min_size):
    while True:
        user_maximum = input("What should be the maximum length in pages? Press Enter to skip.\n")
        if user_maximum == "":
            return None
        try:
            max_size = int(user_maximum)
            if min_size is not None and max_size < min_size:
                print("You can't have a maximum size smaller than the minimum!")
                continue
            if max_size < 0:
                print("This isn't your IQ score. You can't have a negative number of pages.")
                continue
            return max_size
        except ValueError:
            print("That is not a valid amount.")

"""Gets and validates an oldest release date, ensures it's not later than newest.

Args: newest (int or None): Most recent release date for validation

Returns: int or None: Valid oldest release date or None if skipped"""
def SetOldest(newest):
    while True:
        user_age = input("What should be the oldest year searched? Press Enter to skip.\n")
        if user_age == "":
            return None
        try:
            oldest = int(user_age)
            if newest is not None and oldest > newest:
                print("You can't have an oldest publishing date after the newest publishing date!")
                continue
            return oldest
        except ValueError:
            print("That is not a valid amount.")

"""Gets and validates a newest release date, ensures it's not earlier than oldest.

Args: oldest (int or None): Earliest release date for validation

Returns: int or None: Valid newest release date or None if skipped"""
def SetNewest(oldest):
    while True:
        user_age = input("What should be the newest year searched? Press Enter to skip.\n")
        if user_age == "":
            return None
        try:
            newest = int(user_age)
            if oldest is not None and newest < oldest:
                print("You can't have a newest publishing date before the oldest publishing date!")
                continue
            return newest
        except ValueError:
            print("That is not a valid amount.")

"""Sorts books in-place by rating (descending) using quicksort.

Args:   books (list): List of book titles to sort
        start (int): Starting index of the sublist
        end (int): Ending index of the sublist
        book_dict (dict): Dictionary of book attributes
        
Returns: None"""
def SortBooks(books, start, end, **book_dict):
    if start >= end:
        return
    pivot_idx = random.randrange(start, end + 1) #Picks a random pivot for better average-case performance.
    pivot_element = book_dict[books[pivot_idx]]["rating"]
    books[end], books[pivot_idx] = books[pivot_idx], books[end]
    lesser_than_pointer = start
    for idx in range(start, end):
        if book_dict[books[idx]]["rating"] >= pivot_element:
            books[idx], books[lesser_than_pointer] = books[lesser_than_pointer], books[idx]
            lesser_than_pointer += 1
    books[lesser_than_pointer], books[end] = books[end], books[lesser_than_pointer]
    SortBooks(books, start, lesser_than_pointer - 1, **book_dict)
    SortBooks(books, lesser_than_pointer + 1, end, **book_dict)

"""Displays books with formatted details and separators.

Args:   sorted_books (list): List of book titles to display
        bookdict (dict): Dictionary of book attributes
        
Returns: None"""
def PrintBooks(sorted_books, **bookdict):
    if len(sorted_books) == 0:
        print("No books in the database match your search.")
    else:
        for index, book in enumerate(sorted_books):
            print("/////////////////////////////////")
            print(BookDesc(book, **bookdict))
            print("/////////////////////////////////")
            if index < len(sorted_books) - 1:
                print("*********************************")

"""Formats a book's attributes into a user-friendly string.

Args:   bookname (str): Title of book or series
        bookdict (dict): Dictionary of book attributes
        
Returns: str: Formatted book description"""
def BookDesc(bookname, **bookdict):
    book = bookdict[bookname]
    if book["num_books"] > 1:
        book_desc = f"Series name: {book["series_name"]}\nFirst book: {book["first_book"]}\n"
    else:
        book_desc = f"Title: {book["first_book"]}\n"
    book_desc += f"Author: {book["author"]}\n"
    if book["shared_universe"]:
        book_desc += f"Collection: {book["shared_universe"]}\n"
    book_desc += f"Release date: {book["release_date"]}\nGoodreads rating: {book["rating"]:.2f}/5\nPages: {book["length"]}\n"
    if book["num_books"] > 1:
        book_desc += f"Series length: {book["series_length"]} pgs across {book["num_books"]} books\n"
    book_desc += "Genres: " + ", ".join(sorted(book["genres"])).title()
    if book["notes"]:
        book_desc += f"\nNotes: {book["notes"]}"
    return book_desc

"""Prompts the user to search again.

Returns: bool: True to search again, False to exit"""
def SearchAgain():
    user_selection = input("Would you like to search for more books?\n")
    if user_selection in ["y", "yes"]:
        return True
    elif user_selection in ["n", "no"]:
        return False
    else:
        print("That is not a valid option")
        return SearchAgain()

if __name__ == "__main__":
    main(booklist)
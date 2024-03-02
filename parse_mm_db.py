#!/usr/bin/env python3

import os
import requests
import json
import base64
from bs4 import BeautifulSoup
from collections import defaultdict
from langdetect import detect
from natsort import natsorted


class MechonMamreParser:
    def __init__(self):
        self.base_dir = os.getcwd() + "/pt/"
        self.bible_base = defaultdict(list)
        self.final_bible_db = defaultdict(dict)
        
        # Use this to order the books correctly.
        self.order_map = order_map = [
            "Genesis", 
            "Exodus", 
            "Leviticus", 
            "Numbers", 
            "Deuteronomy",
            "Joshua", 
            "Judges", 
            "1 Samuel", 
            "2 Samuel",
            "1 Kings", 
            "2 Kings", 
            "Isaiah", 
            "Jeremiah", 
            "Ezekiel", 
            "Hosea", 
            "Joel", 
            "Amos", 
            "Obadiah", 
            "Jonah", 
            "Micah", 
            "Nahum", 
            "Habakkuk", 
            "Zephaniah", 
            "Haggai", 
            "Zechariah", 
            "Malachi",
            "1 Chronicles", 
            "2 Chronicles", 
            "Psalms", 
            "Job", 
            "Proverbs", 
            "Ruth", 
            "Song of Songs", 
            "Ecclesiastes", 
            "Lamentations", 
            "Esther", 
            "Daniel", 
            "Ezra", 
            "Nehemiah"
        ]

    def find_bible_books(self):

        with open(self.base_dir + "pt0.htm", "r", encoding="windows-1255") as f:
            content = f.read().splitlines()

        for c in content:
            if '<A HREF="pt' in c and ".htm" in c and not "<P>" in c:
                soup = BeautifulSoup(c, "html.parser")
                for link in soup.find_all("a"):
                    link_href = link.get("href")

                    if "pt08a01" in link_href:
                        self.bible_base["1 Samuel"].append(link.get('href'))
                    if "pt09a01" in link_href:
                        self.bible_base["1 Kings"].append(link.get('href'))
                    if "pt25a01" in link_href:
                        self.bible_base["1 Chronicles"].append(link.get('href'))
                    if "pt35a01" in link_href:
                        self.bible_base["Ezra"].append(link.get('href'))
                    else:
                        self.bible_base[link.text].append(link.get('href'))

        # Now we apply corrections.

        # First, delete the duplicate keys
        del self.bible_base["Samuel"]
        del self.bible_base["Kings"]
        del self.bible_base["Chronicles"]

        # Second, add the second chapters of books such as Samuel, Kings, Chronicles and Nehemiah
        self.bible_base["2 Samuel"] = ["pt08b01.htm"]
        self.bible_base["2 Kings"] = ["pt09b01.htm"]
        self.bible_base["2 Chronicles"] = ["pt25b01.htm"]
        self.bible_base["Nehemiah"] = ["pt35b01.htm"]

    # This will get the contents of the main page of each book. 
    def get_book_chapters(self):
        for book, book_file in self.bible_base.items():
            with open(self.base_dir + book_file[0], "r", encoding="windows-1255", errors="ignore") as b:
                bk = b.read()
                soup = BeautifulSoup(bk, "html.parser")
                links = soup.find_all("a")
                for link in links:

                    g = link.get("href")

                    if g is not None and 'pt' in g and '.htm' in g and not 'pt0.htm' in g:

                        if "b" in g and "Ezra" == book and not "a" in g:
                            self.bible_base["Nehemiah"].append(g)

                        elif "a" in g and "Ezra" == book and not "b" in g:
                            self.bible_base["Ezra"].append(g)

                        elif "1" in book and "a" in g:
                            self.bible_base[book].append(g)

                        elif "2" in book and "b" in g:
                            new_book_name = book.replace("1", "2")
                            self.bible_base[new_book_name].append(g)


                        elif "1" not in book and "2" not in book and not "b" in g and not "Nehemiah" in book and not "Ezra" in book:
                            self.bible_base[book].append(g)

            # We probably got duplicate items. Just set the list to unique values. 
            self.bible_base[book] = natsorted(list(set(self.bible_base[book])))

    def parse_book_chapter(self, chapter_number, book_name, file_name):
        try:
            with open(self.base_dir + file_name, encoding="windows-1255", errors="ignore") as psalm:
                f = psalm.read().replace(u'\xa0', u' ')

            soup = BeautifulSoup(f, "html.parser")
            verses = soup.find_all("table")[1]

            table_rows = verses.find_all('td')


            # PIPE THIS INFORMATION TO A JSON DUMP

            for rows in table_rows:
                verse_number = rows.find_all("b")[0].text
                verse_content = rows.text.replace("\n", "").replace(verse_number, "", 1)
                
                if  self.final_bible_db[book_name].get(chapter_number) is None:
                    self.final_bible_db[book_name][chapter_number] = []
                
                if detect(verse_content) == "he":
                    self.final_bible_db[book_name][chapter_number].append({
                        "chapter_he": verse_number,
                        "verse_he": verse_content,
                    })
                else:
                    self.final_bible_db[book_name][chapter_number].append({
                        "chapter_en": verse_number,
                        "verse_en": verse_content,
                    })


        # We are ignoring errors, so this probably won't be triggering.
        except UnicodeDecodeError as ude:
            raise

    def generate_content(self):
        for book, book_info in self.bible_base.items():
            print(f"Parsing {book}")
            chapter_number = 1

            for file_name in book_info:
                self.parse_book_chapter(chapter_number, book, file_name)
                chapter_number += 1
                     
    def write_content(self):
        with open ("tanakh.json", "w") as w:
            w.write(json.dumps(self.final_bible_db, indent=1))

if __name__ == "__main__":
    mmp = MechonMamreParser()
    mmp.find_bible_books()
    mmp.get_book_chapters()
    mmp.generate_content()
    mmp.write_content()


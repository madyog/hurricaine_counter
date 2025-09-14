# myapp/management/commands/convert_html_to_csv.py
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

import os

class Command(BaseCommand):
    help = "Convert HTML table to CSV"

    def handle(self, *args, **kwargs):
        # Project root (where manage.py lives)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Paths
        html_path = os.path.join(BASE_DIR, "data", "HURDAT2.html")
        output_path = os.path.join(BASE_DIR, "data", "output.csv")

        # Read the first table from the HTML
        with open(html_path, "r", encoding="utf-8") as f:
            lxml = BeautifulSoup(f, "lxml")
        # Extract text inside <pre>
        pre_text = lxml.find("pre").get_text()

        # Split into lines
        lines = pre_text.strip().splitlines()

        hurricane_count = 0
        date = ""
        name = ""
        readings = ""
        i = 0
        hit_florida_already = False
        while i < len(lines):
            #remove all spaces
            clean_line = lines[i].replace(" ", "")
            split_line = clean_line.split(",")
            if len(split_line) == 4: #header line
                date = split_line[0]
                name = split_line[1]
                readings = int(split_line[2])
                hit_florida_already = False
                i += 1
                continue
            hit_florida = False
            for reading in range(readings):
                latitude =  split_line[4]
                longitude = split_line[5]
                print(latitude, longitude)
            i += 1


        self.stdout.write(self.style.SUCCESS(f"✅ Conversion complete! Saved as {output_path}"))

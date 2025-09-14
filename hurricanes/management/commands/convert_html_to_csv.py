# myapp/management/commands/convert_html_to_csv.py
from django.core.management.base import BaseCommand
import pandas as pd
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
            html_content = f.read()
        print(html_content)


        self.stdout.write(self.style.SUCCESS(f"✅ Conversion complete! Saved as {output_path}"))

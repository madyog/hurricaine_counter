# myapp/management/commands/convert_html_to_csv.py
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

import geopandas as gpd
from shapely.geometry import Point, Polygon

import os

class Command(BaseCommand):
    help = "Convert HTML table to CSV"

    def handle(self, *args, **kwargs):
        # Project root (where manage.py lives)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Paths
        html_path = os.path.join(BASE_DIR, "data", "HURDAT2.html")
        FLORIDA_BOUNDARY_PATH = os.path.join(BASE_DIR, "data", "tl_2019_12_place.shp")
        boundary = gpd.read_file(FLORIDA_BOUNDARY_PATH)

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
            latitude =  split_line[4]
            longitude = split_line[5]
            latitude = latitude.strip().upper()
            lat = 0
            long = 0
            if latitude[-1] in "NSEW":
                direction = latitude[-1]
                lat = float(latitude[:-1])
                if direction == "S" or direction == "W":
                    lat = -lat
            else:
                lat = float(latitude)
            if longitude[-1] in "NSEW":
                direction = longitude[-1]
                long = float(longitude[:-1])
                if direction == "S" or direction == "W":
                    long = -long
            else:
                long = float(longitude)
            point = Point(long, lat)
            hit_florida = False
            for index, row in boundary.iterrows():
                polygon = row.geometry
                if polygon.contains(point):
                    hit_florida = True
                    break
            if hit_florida and not hit_florida_already:
                hurricane_count += 1
                print(name)
                print(date)
            i += 1
        self.stdout.write(self.style.SUCCESS(f"✅ Conversion complete!"))

    # def is_in_florida(latitude, longitude, boundary):
    #     lat = float(latitude)
    #     long = float(longitude)
    #     point = Point(long, lat)
    #     is_in_file = False
    #     for index, row in boundary.iterrows():
    #         polygon = row.geometry
    #         if polygon.contains(point):
    #             is_in_shapefile = True
    #             break
    #     return is_in_shapefile



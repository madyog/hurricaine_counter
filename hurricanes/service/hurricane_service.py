import math

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

import geopandas as gpd
from shapely.geometry import Point, Polygon

import os

class HurricaneService:
    """
    Service class to process hurricane data blocks from HTML <pre> content.
    """

    def __init__(self):
        """
        data_lines: list of lines (strings) from the <pre> block
        """
        self.results = []  # store processed data

    def count_florida_hurricanes(self):
        # Paths
        html_path = os.path.join("/Users/madyogorek/PycharmProjects/django_getting_started/hurricaine_counter/hurricanes/data", "HURDAT2.html")
        FLORIDA_BOUNDARY_PATH = os.path.join("/Users/madyogorek/PycharmProjects/django_getting_started/hurricaine_counter/hurricanes/data", "tl_2019_12_place.shp")
        boundary = gpd.read_file(FLORIDA_BOUNDARY_PATH)
        fl_polygon = boundary.unary_union
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
        i = 0
        hit_florida = False
        max_speed = - math.inf
        date_of_landfall = 0
        while i < len(lines):
            # remove all spaces
            clean_line = lines[i].replace(" ", "")
            line = clean_line.split(",")
            if len(line) == 4:  # header line
                if hit_florida:
                    year = float(date[0:4])
                    if year > 1900:
                        hurricane_count += 1
                        self.results.append(name + ", " + date_of_landfall + ", " + str(max_speed) + "kn")
                name = line[1]
                hit_florida = False
                max_speed = -math.inf
                date_of_landfall = 0
                i += 1
                continue
            date = line[0]
            latitude = line[4]
            longitude = line[5]
            speed = float(line[6])
            max_speed = max(speed, max_speed)
            latitude = latitude.strip().upper()
            lat = self.convert_coordinate(latitude)
            long = self.convert_coordinate(longitude)
            hit = self.is_in_florida(lat, long, fl_polygon)
            if hit:
                date_of_landfall = date
            hit_florida = hit_florida or hit
            i += 1
        return self.results

    def convert_coordinate(self, coordinate):
        coordinate = coordinate.strip().upper()
        if coordinate[-1] in "NSEW":
            direction = coordinate[-1]
            number = float(coordinate[:-1])
            if direction == "S" or direction == "W":
                number = -number
            return number
        else:
            return float(coordinate)

    def is_in_florida(self, lat, long, fl_polygon):
        point = Point(long, lat)
        return fl_polygon.contains(point)
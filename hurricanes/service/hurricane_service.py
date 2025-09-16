import math

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

import geopandas as gpd
from shapely.geometry import Point, Polygon

import os

class HurricaneService:
    """
    Service class to process hurricane data from HURDAT2
    """

    def __init__(self):
        self.results = []  # store list of hurricanes

    def count_florida_hurricanes(self, use_boundary_box=False):
        html_path = os.path.join("/Users/madyogorek/PycharmProjects/django_getting_started/hurricaine_counter/hurricanes/data", "HURDAT2.html")
        fl_polygon = None
        if not use_boundary_box:
            fl_census_shp_path = os.path.join(
                "/Users/madyogorek/PycharmProjects/django_getting_started/hurricaine_counter/hurricanes/data",
                "tl_2019_12_place.shp")
            fl_census_shp = gpd.read_file(fl_census_shp_path)
            fl_polygon = fl_census_shp.unary_union #merges data points into shape of florida
        with open(html_path, "r", encoding="utf-8") as f: #read html file
            lxml = BeautifulSoup(f, "lxml")
        pre_text = lxml.find("pre").get_text() #extract text from <pre>
        lines = pre_text.strip().splitlines() #split into iterable lines
        hurricane_count, date_of_landfall = 0, 0
        date, name = "", ""
        i = 0
        hit_florida = False
        max_speed = -math.inf
        while i < len(lines):
            clean_line = lines[i].replace(" ", "") #remove spaces
            line = clean_line.split(",")
            if len(line) == 4:  # header line
                if hit_florida:
                    year = float(date[0:4])
                    if year > 1900:
                        hurricane_count += 1
                        self.results.append(name + ", Date: " + date_of_landfall + ", Max Speed: " + str(max_speed) + "kn")
                name = line[1]
                hit_florida = False
                max_speed = -math.inf
                date_of_landfall = 0
                i += 1
                continue
            date = line[0]
            speed = float(line[6])
            max_speed = max(speed, max_speed)
            lat = self.convert_coordinate(line[4])
            long = self.convert_coordinate(line[5])
            if use_boundary_box:
                hit = self.is_in_florida_box(lat, long)
            else:
                hit = self.is_in_florida(lat, long, fl_polygon)
            if hit:
                date_of_landfall = date
            hit_florida = hit_florida or hit #if this reading hit florida or a previous reading from this hurricane hit florida
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

    def is_in_florida_box(self, lat, long):
        if (24.39 <= lat <= 31.00 and -87.63 <= long <= -79.97):
            return True
        return False
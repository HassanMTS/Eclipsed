from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
    terrain_map = []
    with open(path, "r") as level_map:
        layout = reader(level_map, delimiter = ",")
        for row in layout:
            terrain_map.append(list(row))
    return terrain_map

def import_folder(path):
    surf_list = []
    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surf_list.append(image_surf)

    return surf_list

def import_text(path):
    text_dict = {}
    with open(path, "r") as f:
        for line in f.readlines():
            split_line = line.strip("\n").split("\t")
            ID = split_line[0]
            text = split_line[1]
            text_dict[ID] = text
    return text_dict

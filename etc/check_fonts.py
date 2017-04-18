#
# Utility to check availability and location of fonts
# for pygame
#
import pygame

pygame.font.init()  # Required or SysFont will break

candidates = [
    "Helvetica",
    "helvetica",
    # "helvetica.ttf", 
    "Avenir Next",
    "AvenirNext"
    ]
    
default = pygame.font.get_default_font()
print("System default font is '{}'".format(default))

for can in candidates:
    path = pygame.font.match_font(can)
    sysfont = pygame.font.SysFont(can, 12) # Breaks
    print("{} => {}".format(can, path))
    print("Sysfont {} => {}".format(can,sysfont))


print("Found fonts:")
fonts = pygame.font.get_fonts()
for font in fonts:
    print("-- {}".format(font))



'''
Python code to create an image mosaic
This particular implementation will not use repetition
We will read in images and crop/scale them so that there are enough to completely
    fill the background image
Carter Rhea
carterrhea93@gmail.com
12/14/18
'''
import os
import numpy as np
from PIL import Image, ImageOps, ImageSequence

##--------------------------------------------INPUTS------------------------------------------------------#
background_image = '/home/carterrhea/Documents/Photos/chandra1.jpeg'
photo_repo = '/home/carterrhea/Documents/Photos/16'
output_file = '/home/carterrhea/Documents/chandra_1_mosaique.png'


# ---------------------------------------------------------------------------------------------------------#
# ------------------------------------------------------#
# ------------------------------------------------------#
class image:
    def __init__(self, img_class):
        self.name = img_class  # keep as image class!
        self.width = self.name.size[0]
        self.height = self.name.size[1]
        self.avg_red = 0
        self.avg_green = 0
        self.avg_blue = 0

    def crop_im(self):
        global new_width, new_height, x_init, y_init
        if self.width > self.height:
            new_width = self.height
            new_height = self.height
            x_init = (self.width - self.height) / 2
            y_init = 0
        if self.width < self.height:
            new_width = self.width
            new_height = self.width
            x_init = 0
            y_init = (self.height - self.width) / 2
        self.name = self.name.crop((x_init, y_init, x_init + new_width, y_init + new_height))
        self.width = self.name.size[0]
        self.height = self.name.size[1]
        self.name.save('/home/carterrhea/Documents/temp.png')

    def rescale(self, scale_factor):
        new_size = (int(scale_factor), int(scale_factor))
        self.name = ImageOps.fit(self.name, new_size, Image.ANTIALIAS)

    def avg_color(self):
        # taken from masaicify
        hist = self.name.histogram()
        red = hist[0:256]
        green = hist[256:512]
        blue = hist[512:768]
        self.avg_red = weighted_avg(red)
        self.avg_green = weighted_avg(green)
        self.avg_blue = weighted_avg(blue)


# ------------------------------------------------------#
# ------------------------------------------------------#
class pixel:
    def __init__(self, x, y, r, g, b):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b

# ------------------------------------------------------#
# ------------------------------------------------------#
class pixel_group:
    def __init__(self,number):
        self.number = number
        self.pixels = []
        self.avg_red = 0
        self.avg_green = 0
        self.avg_blue = 0
        self.brightness = 0
        self.x = 0
        self.y = 0
    def add_pixel(self,pixel_):
        self.pixels.append(pixel_)
    def avg_color(self):
        r = []; g = []; b = []
        for pixel_ in self.pixels:
            r.append(pixel_.r)
            g.append(pixel_.g)
            b.append(pixel_.b)
        self.avg_red = weighted_avg(r)
        self.avg_green = weighted_avg(g)
        self.avg_blue = weighted_avg(b)
        self.brightness = (self.avg_red + self.avg_green + self.avg_blue) / 3
    def coord(self):
        xs = []; ys = []
        for pixel_ in self.pixels:
            xs.append(pixel_.x)
            ys.append(pixel_.y)
        self.x = np.mean(xs)
        self.y = np.mean(ys)
# ------------------------------------------------------#
# ------------------------------------------------------#
# Weighted average algo taken from mosaicify
def weighted_avg(color):
    weighted = sum(i * w for i, w in enumerate(color))
    total = sum(color)
    return int(weighted / float(total))


# ------------------------------------------------------#
# ------------------------------------------------------#
# Read in background image and get dimensions
def read_background(background_image):
    bkg = image(Image.open(background_image))
    # now lets also decide how to break up the background image
    #bkg.crop_im()
    # get pixels from background image
    pixels = []
    for x in range(bkg.width):
        for y in range(bkg.height):
            r, g, b = bkg.name.getpixel((x, y))
            pixels.append(pixel(x, y, r, g, b))
    return bkg,pixels


# ------------------------------------------------------#
# ------------------------------------------------------#
# Read in other images and crop and rescale
def read_images(photo_repo):
    total_num = len(next(os.walk(photo_repo))[2])
    scaling_factor = np.sqrt(total_num)
    images_list = []
    count = 0
    for (dirpath, dirnames, filenames) in os.walk(photo_repo):
        for filename in filenames:
            images_list.append(image(Image.open(photo_repo+'/'+filename)))
            #images_list[count].crop_im()
            images_list[count].rescale(scaling_factor)
            images_list[count].avg_color()
            #images_list[count].name.save('/home/carterrhea/Documents/'+str(count)+'.png')

            count += 1
    return images_list


# ------------------------------------------------------#
# ------------------------------------------------------#
# Create larger pixel groups
def grouping_pix(pixels,pix_per_tile):
    count_in = 0
    tile_number = 0
    new_tiles = {}
    for pixel_ in pixels:
        if tile_number not in new_tiles.keys():
            new_tiles[tile_number] = pixel_group(tile_number)
            new_tiles[tile_number].add_pixel(pixel_)
        if tile_number in new_tiles.keys() and count_in <= pix_per_tile:
            # we can add another
            new_tiles[tile_number].add_pixel(pixel_)
            count_in += 1
            if count_in == pix_per_tile+1:  # if we have filled group make new
                count_in = 0
                new_tiles[tile_number].avg_color()  # calculate filled groups color/brightness
                new_tiles[tile_number].coord() # calculate center coordinates of tile
                tile_number += 1
    new_tiles = [super_pix for key, super_pix in new_tiles.items()]
    for i in new_tiles:
        print(len(i.pixels))
        print(i.x,i.y)
    return new_tiles


# ------------------------------------------------------#
# ------------------------------------------------------#
# Find image with closest color
def closest_color(tiles_final,tile,images_left,tile_count):
    distance = [np.sqrt((tile.avg_red - im.avg_red)**2+(tile.avg_green - im.avg_green)**2+(tile.avg_blue - im.avg_blue)**2) for im in images_left]
    min_ind = distance.index(min(distance))
    tiles_final.append(images_left[min_ind]) #add image to tiles list!
    del images_left[min_ind] #get rid of image we just used
    return tiles_final,images_left
# ------------------------------------------------------#
# ------------------------------------------------------#
# Create final mosaique
def mosaique_final(bkg,images_brightness,coord_brightness,output_file):
    mosaique = Image.new(bkg.name.mode,(bkg.width,bkg.height))
    im_count = 0
    for img in images_brightness:
        #im = Image.new('RGB', (img.width,img.height))
        mosaique.paste(img.name,coord_brightness[im_count])
        im_count += 1
    mosaique.save(output_file)
    return None
# ------------------------------------------------------#
# ------------------------------------------------------#
# ------------------------------------------------------#
# ------------------------------------------------------#
def main():
    bkg,pixels = read_background(background_image)
    images = read_images(photo_repo)
    pix_per_tile = int(len(pixels)/len(images))
    #Now create the new tiles!
    new_tiles = grouping_pix(pixels,pix_per_tile)
    brightnes_ordered = sorted(new_tiles, key=lambda x: x.brightness) #set Reverse=True if you want the darkest
    #Now to assign an image to each tile based on 3d distance in color space (R,G,B)
    tiles_final = []
    images_left = images
    for tile in brightnes_ordered:
        tiles_final,images_left = closest_color(tiles_final,tile,images_left,tile.number)
    mosaique_final(bkg,tiles_final,[(int(tile.x),int(tile.y)) for tile in brightnes_ordered],output_file)



    return None


main()

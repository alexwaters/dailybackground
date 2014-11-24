from imgurpython import ImgurClient
import config
import urllib
import os
from imgurpython.imgur.models.gallery_album import GalleryAlbum
from imgurpython.imgur.models.gallery_image import GalleryImage
from itertools import count

client_id = config.client_id
client_secret = config.client_secret
client = ImgurClient(client_id, client_secret)
dir_name = 'images/'
new_imgs, cur_imgs, old_imgs, new_links, new_files = [], [], [], [], []
bg_width_max = 2880
bg_height_max = 1800

'''Get three lists: 1. recent images from imgur 2. images currently in the
local images directory 3. list of old images'''
def get_list():
    #Get list 1
    gallery = client.gallery('hot','time')
    for item in gallery:
        if isinstance(item, GalleryImage):
            new_imgs.append(item)
        if isinstance(item, GalleryAlbum):
            assert item.is_album == True
            alb_imgs = client.get_album_images(item.id)
            for img in alb_imgs: new_imgs.append(img)
    prune_new()
    for img in new_imgs: new_links.append(img.link)
    for img in new_imgs: new_files.append(img.link[-11:])
    
    #Get list 2
    i = 0
    dir_files = os.listdir(dir_name)
    for item in dir_files:
        i+=1
        if (len(item)  == 11) and (item[-4:] in ['.png', '.jpg', '.gif']):
            cur_imgs.append(item)
    print str(i) + ' files in ' + dir_name + ' directory'
    
    #Get list 3
    i = 0
    a = []
    for link in new_links:
        if link[-11:] in cur_imgs:
            a.append(link)
            i+=1
    for x in a: new_links.remove(x)
    
    for cur in cur_imgs:
        if cur not in new_files:
            old_imgs.append(cur)
    print  str(i) + ' images are current.'
            
'''Prune the list of images that are too big or animated'''
def prune_new():
    for img in new_imgs:
        if img.height > bg_height_max:
            new_imgs.remove(img)
        elif img.width > bg_width_max:
            new_imgs.remove(img)
        elif img.animated == True:
            new_imgs.remove(img)

'''Remove the old image files'''
def remove_old():
    i = 0
    for f in old_imgs:
        assert (len(f) == 11) and (f[-4:] in ['.png', '.jpg', '.gif'])
        os.remove(dir_name + f)
        i += 1
    print 'Removed ' + str(i) + ' old images.'
    
'''Save the new images'''
def save_new_imgs():
    i = 0
    for image in new_links:
        urllib.urlretrieve(image, dir_name + image[-11:])
        print image
        i+=1
    print 'Added ' + str(i) + ' new images.'

get_list()
remove_old()
save_new_imgs()
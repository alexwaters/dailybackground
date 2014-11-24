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
new_imgs, cur_imgs, old_imgs, new_links = [], [], [], []
bg_width_max = 2880
bg_height_max = 1800

'''Get three lists: 1. recent images from imgur 2. images currently in the
local images directory 3. list of old images'''
def get_list():
    #Get list 1
    gallery = client.gallery('hot','time')
    for item in gallery[0:30]:
        if isinstance(item, GalleryImage):
            new_imgs.append(item)
        if isinstance(item, GalleryAlbum):
            assert item.is_album == True
            alb_imgs = client.get_album_images(item.id)
            for img in alb_imgs: new_imgs.append(img)
    prune_new()
    
    #Get list 2
    dir_files = os.listdir('images')
    for item in dir_files:
        if (len(item)  == 11) and (item[-4:] in ['.png', '.jpg', '.gif']):
            cur_imgs.append(item)
    
    #Get list 3
    for img in new_imgs: new_links.append(img.link[-11:])
    for i in cur_imgs:
        if i in new_links:
            new_links.remove(i)
        else: old_imgs.append(file)
            
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
    for f in old_imgs:
        assert (len(f) == 11) and (f[-4:] in ['.png', '.jpg', '.gif'])
        os.remove(f)
    
'''Save the new images'''
def save_images():
    for image in new_imgs:
        urllib.urlretrieve(image, dir_name + image[-11:])

get_list()
remove_old()
print new_links
# print len(new_imgs)
# print cur_imgs
# print len(cur_imgs)

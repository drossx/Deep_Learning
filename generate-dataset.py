from PIL import Image, ImageDraw
import string
import numpy as np
import os

import json


def get_cat(word):

    categories = ['traffic light', 'traffic sign', 'car',
                  'truck', 'person', 'other']
    try:
        num = categories.index(word)
    except ValueError:
        num = 5 #set in other

    return num


cwd = os.getcwd()

g = open("%s/train.txt" % cwd, 'w+')


data = []
try:
    data = json.loads(open('%s/file.json' % cwd).read())
except JSONDecodeError:
    pass

count = 0
for i in data:
    jdata = data[count]
    count = count + 1

    name = jdata["name"]

    x1 = np.zeros(10)
    x2 = np.zeros(10)
    y1 = np.zeros(10)
    y2 = np.zeros(10)
    cat = list()

    for j in range(0, 10):
        try:
            for key, value in jdata["labels"][j]["box2d"].items():
                if key == 'x1':
                    x1[j] = value
                if key == 'x2':
                    x2[j] = value
                if key == 'y1':
                    y1[j] = value
                if key == 'y2':
                    y2[j] = value

            cat.append(get_cat(jdata["labels"][j]["category"]))

        except KeyError:
            break
        except IndexError:
            break


    with open('%s/YOLO/%s.txt' % (cwd, name[:-4]), 'w+') as f:
        for j in range(0, len(cat)):
            f.write('%s ' % cat[j])
            midx = x1[j] + abs(x2[j]-x1[j])/2
            midy = y1[j] + abs(y2[j]-y1[j])/2
            width = abs(x2[j]-x1[j])
            height = abs(y2[j]-y1[j])

            f.write('%f9 %f9 %f9 %f9\n' % (midx/1280, midy/720, width/1280, height/720)) #x y width height, ratios to pic size


        g.write('%s/images/%s\n' % (cwd,name))


g.close()

# for j in range(0,5000):
#     img = Image.new('RGB', (grid_w*cell_w,grid_h*cell_h))
#     d = ImageDraw.Draw(img)
#
#     with open('Labels/%d.txt' % j,'w+') as f:
#
#         for row in range(grid_w):
#             for col in range(grid_h):
#
#                 (digits, cat) = get_word(random.randint(0,2))
#
#                 width = len(digits)*6
#
#                 if(digits=='none'):
#                     f.write('%d %d %d\n' % (cat[0],cat[1],cat[2]) )
#                     f.write('%d %d %d %d\n' % ( col*cell_w+cell_w/2, row*cell_h+cell_h/2, cell_w, cell_h ))
#                     f.write('0\n') # confidence of object
#                     #print("None", (col,row), (col*cell_w+cell_w/2, row*cell_h+cell_h/2, cell_w, cell_h), 0)
#                 else:
#                     x = random.randrange(col*cell_w, (col+1)*cell_w)
#                     y = random.randrange(row*cell_w, min(67, (row+1)*cell_h))
#
#                     d.text((x-width/2, y-10/2), digits, fill=(255,255,255))
#                     f.write('%d %d %d\n' % (cat[0],cat[1],cat[2]))
#                     f.write('%d %d %d %d\n' % (x, y, width, 10) )
#                     f.write('1\n') # confidence of object
#                     #print("Objt", (col,row), (x, y, width, 10), 1)
#
#         f.write('---\n')

    #img.save('Images/%d.PNG' % j)



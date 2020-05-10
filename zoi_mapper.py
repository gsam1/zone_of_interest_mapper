import argparse
import numpy as np
import os
import json
import cv2

mouseX = 0
mouseY = 0
img = np.array([])
colormap = {}
ZONE = 0
ZONES = {}

def handle_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image')
    parser.add_argument('-s', '--scale')
    return vars(parser.parse_args())

def write_to_json():
    with open('export/zones.json', 'w') as f:
        json.dump(ZONES, f)

def add_points(img, colormap):
    global ZONES

    for key in ZONES.keys():
        for point in ZONES[key]:
            img = cv2.circle(img, (point[0], point[1]), 3, colormap[key], -1)

    return img

def get_mouse(event,x,y,flags,param):
    global mouseX, mouseY, img, colormap

    if event == cv2.EVENT_LBUTTONDBLCLK:
        if len(ZONES.keys()) == 0:
            print('No Zones Added')
        else:
            cv2.circle(img,(x,y),3,colormap[f'zone{ZONE}'],-1)
            if len(ZONES['zone' + str(ZONE)]) < 4:
                ZONES['zone' + str(ZONE)].append([x, y])
                print(f'Added to {ZONE}')
            else:
                print(f'No more points allowed in Zone {ZONE}')
            # print(x, y)
        
        mouseX, mouseY = x, y

def messages(msg_type):
    msg = {
        'head': 'Zone-of-Interest Mapper: For a new zone press "a". To clear all press "c". To save to json and exit press "s". To exit press "space".',
        'clear': 'Points cleared. To add new zone press "a". To exit press "space".',
        'zone-start': 'Map Zone Coordinates. 4 points required.',
        'zone-finish': 'Zone finished. For new zones press "a", to exit press "space".'
    }

    return msg[msg_type]

def scale_image(img, args):
    if args['scale'] == 'true':
        return cv2.resize(img, (1366, 768), interpolation = cv2.INTER_AREA)
    else:
        return img

def gen_colormap(clrmap_len):
    clrmap = {}

    for i in range(0, clrmap_len):
        if i % 3 == 0:
            if i == 0:
                clrmap[f'zone{i}'] = (0, 0, 255)
            else:
                clrmap[f'zone{i}'] = (0, 0, 255 // i)
        elif i % 3 == 1:
            if i == 1:
                clrmap[f'zone{i}'] = (0, 255, 0)
            else:
                clrmap[f'zone{i}'] = (0, 255 // i, 0)
        elif i % 3 == 2:
            if i == 2:
                clrmap[f'zone{i}'] = (255, 0, 0)
            else:
                clrmap[f'zone{i}'] = (255 // i, 0, 0)
        
    return clrmap

def main():
    global ZONE
    global ZONES
    global img
    global colormap

    args = handle_arguments()
    cv2.namedWindow('image')
    img = cv2.imread(args['image'])

    # temporary to fit in my laptops' screen
    img = scale_image(img, args)

    img = cv2.putText(img, messages('head'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.setMouseCallback('image', get_mouse)

    # generate color map
    colormap = gen_colormap(4)

    while True:
        cv2.imshow('image',img)
        k = cv2.waitKey(1)

        # if k%256 != 255:
        #     print(k%256)
        
        if k%256 == 97:
            img = cv2.imread(args['image'])
            img = cv2.putText(img, messages('zone-start'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 3)
            img = scale_image(img, args)
            
            img = add_points(img, colormap)

            if len(ZONES.keys()) == 0:
                ZONES['zone' + str(ZONE)] = []
            else:
                ZONE += 1
                ZONES['zone' + str(ZONE)] = []
        
        if (len(ZONES.keys()) > 0) and (len(ZONES['zone' + str(ZONE)]) >= 4):
                img = cv2.imread(args['image'])
                img = cv2.putText(img, messages('zone-finish'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 3)
                img = scale_image(img, args)
                img = add_points(img, colormap)
        
        if k%256 == 99:
            img = cv2.imread(args['image'])
            img = scale_image(img, args)
            img = img = cv2.putText(img, messages('clear'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 3)
            ZONES = {}
            ZONE = 0

        if k%256 == 115:
            print(ZONES)
            write_to_json()
            break

        if k%256 == 32:
            break
        # cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
import argparse
import numpy as np
import os
import json
import cv2

mouseX = 0
mouseY = 0
ZONE = 0
ZONES = {}

def handle_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image')
    return vars(parser.parse_args())

def write_to_json(coordinates, zone):
    pass

def get_mouse(event,x,y,flags,param):
    global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        if len(ZONES.keys()) == 0:
            print('No Zones Added')
        else:
            cv2.circle(img,(x,y),100,(255,0,0),-1)
            if len(ZONES['zone' + str(ZONE)]) <= 4:
                ZONES['zone' + str(ZONE)].append([x, y])
                print(f'Added to {ZONE}')
            else:
                print(f'No more points allowed in Zone {ZONE}')
            # print(x, y)
        
        mouseX, mouseY = x, y

def messages(msg_type):
    msg = {
        'head': 'Zone-of-Interest Mapper: For a new zone press "a". To exit press "space"',
        'zone-start': 'Map Zone Coordinates. 4 points required',
        'zone-finish': 'Zone finished. For new zones press "a", to exit press "space".'
    }

    return msg[msg_type]

def main():
    global ZONE
    global ZONES

    args = handle_arguments()
    cv2.namedWindow('image')
    img = cv2.imread(args['image'])

    # temporary to fit in my laptops' screen
    img = cv2.resize(img, (1366, 768), interpolation = cv2.INTER_AREA)

    img = cv2.putText(img, messages('head'), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    cv2.setMouseCallback('image',get_mouse)

    while True:
        cv2.imshow('image',img)
        k = cv2.waitKey(1)

        # if k%256 != 255:
        #     print(k%256)
        
        if k%256 == 97:
            img = cv2.imread(args['image'])
            img = cv2.putText(img, messages('zone-start'), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            img = cv2.resize(img, (1366, 768), interpolation = cv2.INTER_AREA)

            if len(ZONES.keys()) == 0:
                ZONES['zone' + str(ZONE)] = []
            else:
                ZONE += 1
                ZONES['zone' + str(ZONE)] = []
        
        if (len(ZONES.keys()) > 0) and (len(ZONES['zone' + str(ZONE)]) >= 4):
                img = cv2.imread(args['image'])
                img = cv2.putText(img, messages('zone-finish'), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                img = cv2.resize(img, (1366, 768), interpolation = cv2.INTER_AREA)

        if k%256 == 115:
            print(ZONES)

        if k%256 == 32:
            break
    # cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
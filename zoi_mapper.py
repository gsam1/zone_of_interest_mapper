import argparse
import numpy as np
import cv2

def handle_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image')
    return vars(parser.parse_args())

def main():
    image_path = handle_arguments()
    img = cv2.imread(image_path['image'])
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
import cv2 as cv
import numpy as np
import os
from configparser import *


def nothing():
    pass

def RaskRibas(img_path):
    arguments = ConfigParser()
    arguments.read(os.path.join(os.path.dirname(__file__), 'args.ini'))
    img = cv.imread(img_path)
    if img is None:
        return -1
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # sukuria langą ir trackbarus
    cv.namedWindow('Spalvų atrinkimas')
    cv.createTrackbar('Zemesnysis H', 'Spalvų atrinkimas', arguments.getint('Arguments', 'min_h'), 180, nothing)
    cv.createTrackbar('Zemesnysis S', 'Spalvų atrinkimas',  arguments.getint('Arguments', 'min_s'), 255, nothing)
    cv.createTrackbar('Zemesnysis V', 'Spalvų atrinkimas', arguments.getint('Arguments', 'min_v'), 255, nothing)
    cv.createTrackbar('Aukstesnysis H', 'Spalvų atrinkimas', arguments.getint('Arguments', 'max_h'), 180, nothing)
    cv.createTrackbar('Aukstesnysis S', 'Spalvų atrinkimas', arguments.getint('Arguments', 'max_s'), 255, nothing)
    cv.createTrackbar('Aukstesnysis V', 'Spalvų atrinkimas', arguments.getint('Arguments', 'max_v'), 255, nothing)

    try:
        while True:
            # gauna trackbar reikšmes
            l_h = cv.getTrackbarPos('Zemesnysis H', 'Spalvų atrinkimas')
            l_s = cv.getTrackbarPos('Zemesnysis S', 'Spalvų atrinkimas')
            l_v = cv.getTrackbarPos('Zemesnysis V', 'Spalvų atrinkimas')
            u_h = cv.getTrackbarPos('Aukstesnysis H', 'Spalvų atrinkimas')
            u_s = cv.getTrackbarPos('Aukstesnysis S', 'Spalvų atrinkimas')
            u_v = cv.getTrackbarPos('Aukstesnysis V', 'Spalvų atrinkimas')

            # Create mask with current ranges
            Zemesnysis = np.array([l_h, l_s, l_v])
            Aukstesnysis = np.array([u_h, u_s, u_v])
            mask = cv.inRange(hsv, Zemesnysis, Aukstesnysis)

            # rodyk
            cv.imshow('Spalvų atrinkimas', mask)

            # esc paspaudus išves
            key = cv.waitKey(1) & 0xFF
            if key == 27:  # ESC
                arguments.set('Arguments', 'min_h', str(l_h))
                arguments.set('Arguments', 'min_s', str(l_s))
                arguments.set('Arguments', 'min_v', str(l_v))
                arguments.set('Arguments', 'max_h', str(u_h))
                arguments.set('Arguments', 'max_s', str(u_s))
                arguments.set('Arguments', 'max_v', str(u_v))
                with open('args.ini', 'w') as args:
                    arguments.write(args)
                break
            
            # Check if window was closed
            if cv.getWindowProperty('Spalvų atrinkimas', cv.WND_PROP_VISIBLE) < 1:
                break
    finally:
        cv.destroyAllWindows()

def Balsu_atpazinimas(img_path):
    arguments = ConfigParser()
    arguments.read(os.path.join(os.path.dirname(__file__), 'args.ini'))
    img = cv.imread(img_path)
    if img is None:
        return -1
    
    # Vertimas į HSV spalvų erdvę
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    
    # Pagal ribas nustatome, kokias spalvas norime aptikti
    lower = np.array([arguments.getint('Arguments', 'min_h'), arguments.getint('Arguments', 'min_s'), arguments.getint('Arguments', 'min_v')])
    upper = np.array([arguments.getint('Arguments', 'max_h'), arguments.getint('Arguments', 'max_s'), arguments.getint('Arguments', 'max_v')])

    # Kurti maskę
    mask = cv.inRange(hsv, lower, upper)
    height = mask.shape[0]
    mask = mask[0:-1][abs(arguments.getint('Arguments', 'maxaukstis')-height):height-arguments.getint('Arguments', 'minaukstis')]

    # Medianinis įtempimas
    mask = cv.medianBlur(mask, 3)

    
    # Rasti sujungtas komponentes
    num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(
        mask, connectivity=8
    )
    
    h, w = mask.shape
    regions = []
    
    min_region_size = arguments.getint('Arguments', 'MinRegionSize') if arguments.has_option('Arguments', 'MinRegionSize') else 2
    
    for i in range(1, num_labels):
        x, y, ww, hh, area = stats[i]
        
        if area < min_region_size:
            continue
        
        if ww > 0.9 * w and hh > 0.9 * h:
            continue
        
        regions.append((x, y, ww, hh))
    
    # Išrūšiuoti pagal x
    regions = sorted(regions, key=lambda x: x[0])
    
    # Išsaugoti maskę
    output_path = os.path.join(os.path.dirname(__file__), "BWlygmuo.png")
    cv.imwrite(output_path, mask)

    # Išsaugoti rezultatus į failą
    with open(os.path.join(os.path.dirname(__file__), 'output.txt'), 'w') as output:
        for i, (x, y, ww, hh) in enumerate(regions):
            output.write(f"  Regionas {i+1}: x={x}, y={y}, plotis={ww}, aukstis={hh}\n")
    
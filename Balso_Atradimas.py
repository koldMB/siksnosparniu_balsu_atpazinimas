import cv2 as cv
import numpy as np
import os
from configparser import *


def nothing():
    pass

def RaskRibas(img_path):
    arguments = ConfigParser()
    arguments.read('args.ini')
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
        if cv.waitKey(1) == 27:
            arguments.set('Arguments', 'min_h', str(l_h))
            arguments.set('Arguments', 'min_s', str(l_s))
            arguments.set('Arguments', 'min_v', str(l_v))
            arguments.set('Arguments', 'max_h', str(u_h))
            arguments.set('Arguments', 'max_s', str(u_s))
            arguments.set('Arguments', 'max_v', str(u_v))
            with open('args.ini', 'w') as args:
                arguments.write(args)
            break

    cv.destroyAllWindows()

def Balsu_atpazinimas(img_path):
    arguments = ConfigParser()
    arguments.read('args.ini')
    img = cv.imread(img_path)
    if img is None:
        return -1
    ''' Nezinau kaip sita pakeisti, kad nebutu problemu
    #paveikslėlio apdorojimas
    imgtemp = img.copy()
    imgtemp = np.divide(imgtemp, 1/C_cof)
    imgtemp = np.roll(imgtemp, 1)
    height, _, channels = img.shape
    for i in range(0, height):
        for j in range(0, channels):
            imgtemp[i][0][j] = 0
    img = np.ndarray.round(np.subtract(img, imgtemp), 0)
    '''
    # Vertimas į HSV spalvų erdvę
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    # Pagal ribas nustatome, kokias spalvas norime aptikti
    lower = np.array([arguments.getint('Arguments', 'min_h'), arguments.getint('Arguments', 'min_s'), arguments.getint('Arguments', 'min_v')])
    upper = np.array([arguments.getint('Arguments', 'max_h'), arguments.getint('Arguments', 'max_s'), arguments.getint('Arguments', 'max_v')])

    # lygmuo
    mask = cv.inRange(hsv, lower, upper)
    
    # apkarpymas
    height = mask.shape[0]
    mask_cropped = mask[0:-1][abs(arguments.getint('Arguments', 'maxaukstis')-height):height-arguments.getint('Arguments', 'minaukstis')]

    # isaugok apkarpta vaizda
    output_path = os.path.join(os.path.dirname(__file__), "BWlygmuo.png")
    cv.imwrite(output_path, mask_cropped)

    #apversti balta i juduo ir juoda i balta, kad likusi dalis kodo veiktu

    for i in range(0, len(mask_cropped)):
        for j in range(0, len(mask_cropped[i])):
            if mask_cropped[i][j] == 0:
                mask_cropped[i][j] =  255
            else: 
                mask_cropped[i][j] = 0

    # isaugok invertuota apkarpta vaizda
    output_path = os.path.join(os.path.dirname(__file__), "BWlygmuo_Inverted.png")
    cv.imwrite(output_path, mask_cropped)

    # Rasti kontuorus
    contours, _ = cv.findContours(mask_cropped, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Filtruoti kontuorus pagal parametrus
    valid_contours = []

    aukstis = arguments.getint('Arguments', 'auksciotolerancija')
    ilgis = arguments.getint('Arguments', 'ilgiotolerancija')
    padengimas = arguments.getint('Arguments', 'plociotolerancija')
    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)

        # Patikrinti aukštį
        if h >= aukstis:
            # Patikrinti ilgį
            if w >= ilgis:
                # Patikrinti padengimą (area / bounding_rect)
                area = cv.contourArea(contour)
                rect_area = w * h
                coverage = (area / rect_area) * 100 if rect_area > 0 else 0
                
                if coverage <= padengimas:
                    valid_contours.append((x, y, w, h))
    
    #išrikuoti pagal x, o ne y
    valid_contours = sorted(valid_contours, key = lambda x: x[0])
    with open('output.txt', 'w') as output:
        for i, (x, y, w, h) in enumerate(valid_contours):
            output.write(f"  Regionas {i+1}: x={x}, y={y}, plotis={w}, aukstis={h}\n")
    
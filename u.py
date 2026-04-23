import cv2
import numpy as np
import os

def nothing(x):
    pass

if __name__ == '__main__':
    img = cv2.imread(os.path.join(os.path.dirname(__file__), "PIPPIP.png"))
    if img is None:
        print("Failas neatidarytas")
    else:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # sukuria langą ir trackbarus
        cv2.namedWindow('Spalvų atrinkimas')
        cv2.createTrackbar('Zemesnysis H', 'Spalvų atrinkimas', 0, 180, nothing)
        cv2.createTrackbar('Zemesnysis S', 'Spalvų atrinkimas', 0, 255, nothing)
        cv2.createTrackbar('Zemesnysis V', 'Spalvų atrinkimas', 0, 255, nothing)
        cv2.createTrackbar('Aukstesnysis H', 'Spalvų atrinkimas', 180, 180, nothing)
        cv2.createTrackbar('Aukstesnysis S', 'Spalvų atrinkimas', 255, 255, nothing)
        cv2.createTrackbar('Aukstesnysis V', 'Spalvų atrinkimas', 255, 255, nothing)
        
        while True:
            # gauna trackbar reikšmes
            l_h = cv2.getTrackbarPos('Zemesnysis H', 'Spalvų atrinkimas')
            l_s = cv2.getTrackbarPos('Zemesnysis S', 'Spalvų atrinkimas')
            l_v = cv2.getTrackbarPos('Zemesnysis V', 'Spalvų atrinkimas')
            u_h = cv2.getTrackbarPos('Aukstesnysis H', 'Spalvų atrinkimas')
            u_s = cv2.getTrackbarPos('Aukstesnysis S', 'Spalvų atrinkimas')
            u_v = cv2.getTrackbarPos('Aukstesnysis V', 'Spalvų atrinkimas')
            
            # Create mask with current ranges
            Zemesnysis = np.array([l_h, l_s, l_v])
            Aukstesnysis = np.array([u_h, u_s, u_v])
            mask = cv2.inRange(hsv, Zemesnysis, Aukstesnysis)
            
            # rodyk
            cv2.imshow('Spalvų atrinkimas', mask)
            
            # esc paspaudus išves
            if cv2.waitKey(1) == 27:
                print(f"Zemesnysis: {[l_h, l_s, l_v]}")
                print(f"Aukstesnysis: {[u_h, u_s, u_v]}")
                break
        
        cv2.destroyAllWindows()
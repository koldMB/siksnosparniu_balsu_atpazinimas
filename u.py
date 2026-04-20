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
        
        # Create window and trackbars
        cv2.namedWindow('Color Range Finder')
        cv2.createTrackbar('Lower H', 'Color Range Finder', 0, 180, nothing)
        cv2.createTrackbar('Lower S', 'Color Range Finder', 0, 255, nothing)
        cv2.createTrackbar('Lower V', 'Color Range Finder', 0, 255, nothing)
        cv2.createTrackbar('Upper H', 'Color Range Finder', 180, 180, nothing)
        cv2.createTrackbar('Upper S', 'Color Range Finder', 255, 255, nothing)
        cv2.createTrackbar('Upper V', 'Color Range Finder', 255, 255, nothing)
        
        while True:
            # Get trackbar values
            l_h = cv2.getTrackbarPos('Lower H', 'Color Range Finder')
            l_s = cv2.getTrackbarPos('Lower S', 'Color Range Finder')
            l_v = cv2.getTrackbarPos('Lower V', 'Color Range Finder')
            u_h = cv2.getTrackbarPos('Upper H', 'Color Range Finder')
            u_s = cv2.getTrackbarPos('Upper S', 'Color Range Finder')
            u_v = cv2.getTrackbarPos('Upper V', 'Color Range Finder')
            
            # Create mask with current ranges
            lower = np.array([l_h, l_s, l_v])
            upper = np.array([u_h, u_s, u_v])
            mask = cv2.inRange(hsv, lower, upper)
            
            # Show result
            cv2.imshow('Color Range Finder', mask)
            
            # Press ESC to exit and see ranges
            if cv2.waitKey(1) == 27:
                print(f"Lower: {[l_h, l_s, l_v]}")
                print(f"Upper: {[u_h, u_s, u_v]}")
                break
        
        cv2.destroyAllWindows()
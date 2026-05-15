import cv2
import numpy as np
import os

def process_vertical_strip_color(image, x, C=0.5):
    height, width, channels = image.shape
    result = image.copy()

    for c in range(channels):
        for y in range(height - 1):
            result[y + 1, x, c] = np.clip(result[y + 1, x, c] - result[y, x, c] * C, 0, 255)

    return result


print ("Visi dydžiai aprašomi pikseliais (px)")
minpavaukstis = int(input("minimalus paveikslėlio aukštis kad būtų fiksuojama koordinatės(ne 0): "))
maxpavaukstis = int(input("maksimalus paveikslėlio aukštis kad būtų fiksuojama koordinatės: "))
aukstis = int(input("Aukščio tolerancija (minimalus aukštis kad būtų fiksuojama koordinatės): "))
ilgis = int(input("Ilgio tolerancija (minimalus rėžio ilgis kad būtų fiksuojama koordinatės (rekomenduojama 3)):"))
padengimas = int(input("Kiek procentų aukščio ir ilgio turi būti padengta, kad būtų fiksuojama koordinatės (rekomenduojama 80):"))
garsas = int(input("Garso tolerancija (atstumas kiek po yra ignoruojama kiti rėžiai):"))
img = cv2.imread(os.path.join(os.path.dirname(__file__), "PIPPIP.png"))
if img is None:
    print("Failas neatidarytas")
else:
    # Vertimas į HSV spalvų erdvę
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Pagal ribas nustatome, kokias spalvas norime aptikti
    print("Atrinktos ribos: H min=17, S min=0, V min=248, H max=180, S max=184, V max=255")
    manoRibos = input("Įveskite ar norite savo HSV ribų (taip/ne): ")
    if manoRibos.lower() == "taip":
        h_min = int(input("Įveskite H min: "))
        s_min = int(input("Įveskite S min: "))
        v_min = int(input("Įveskite V min: "))
        h_max = int(input("Įveskite H max: "))
        s_max = int(input("Įveskite S max: "))
        v_max = int(input("Įveskite V max: "))
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
    else:
        print("Naudojamos numatytos ribos")
        lower = np.array([17, 0, 248])
        upper = np.array([180, 184, 255])
    
    # lygmuo
    mask = cv2.inRange(hsv, lower, upper)
    
    # apkarpymas
    height = mask.shape[0]
    mask_cropped = mask[0:-1][abs(maxpavaukstis-height):height-minpavaukstis]

    # isaugok apkarpta vaizda
    output_path = os.path.join(os.path.dirname(__file__), "BWlygmuo.png")
    cv2.imwrite(output_path, mask_cropped)

    #apversti balta i juduo ir juoda i balta, kad likusi dalis kodo veiktu

    for i in range(0, len(mask_cropped)):
        for j in range(0, len(mask_cropped[i])):
            if mask_cropped[i][j] == 0:
                mask_cropped[i][j] =  255
            else: 
                mask_cropped[i][j] = 0

    # isaugok invertuota apkarpta vaizda
    output_path = os.path.join(os.path.dirname(__file__), "BWlygmuo_Inverted.png")
    cv2.imwrite(output_path, mask_cropped)

    # Rasti kontuorus
    contours, _ = cv2.findContours(mask_cropped, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtruoti kontuorus pagal parametrus
    valid_contours = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Patikrinti aukštį
        if h >= aukstis:
            # Patikrinti ilgį
            if w >= ilgis:
                # Patikrinti padengimą (area / bounding_rect)
                area = cv2.contourArea(contour)
                rect_area = w * h
                coverage = (area / rect_area) * 100 if rect_area > 0 else 0
                
                if coverage >= padengimas:
                    valid_contours.append((x, y, w, h))
    
    #išrikuoti pagal x, o ne y
    valid_contours = sorted(valid_contours, key = lambda x: x[0])

    print(f"Rasti {len(valid_contours)} atitinkantys regionai:")
    for i, (x, y, w, h) in enumerate(valid_contours):
        print(f"  Regionas {i+1}: x={x}, y={y}, plotis={w}, aukštis={h}")
import cv2
from cvzone.HandTrackingModule import HandDetector
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
cap = cv2.VideoCapture(0)
detector = HandDetector()
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
min_distance = 20
max_distance = 180
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    print(hands)
    if hands:
        hand = hands[0]
        if hand["type"] == "Right":
            thumb_tip = hand["lmList"][4]
            index_tip = hand["lmList"][8]
            distance = math.hypot(thumb_tip[0] - index_tip[0], thumb_tip[1] - index_tip[1])
            distance = max(min_distance, min(distance, max_distance))
            volume_scaler = (distance - min_distance) / (max_distance - min_distance)
            volume.SetMasterVolumeLevelScalar(volume_scaler, None)
            volume_percent = int(volume_scaler * 100)
            cv2.line(img, (thumb_tip[0],thumb_tip[1]),(index_tip[0],index_tip[1]),(0,255,0),3)
            cv2.putText(img, f'Volume: {volume_percent}%', (50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)

    img = cv2.resize(img,(960,720))
    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows
import cv2
import winsound
import time
import pyttsx3

engine = pyttsx3.init()

def overlaps(x, y, w, h):
    if 240 < x < 400 or 240 < (x + w) < 400:
        return True
    else:
        return False


prevTime = int(round(time.time() * 1000))


widthImg = 640
heightImg = 480

cam = cv2.VideoCapture(0)

success, img = cam.read()

img = cv2.resize(img, (widthImg, heightImg))

cv2.rectangle(img, (240, 0), (400, 480), (0, 255, 0), 2)
cv2.imshow('Camera', img)

count = 0
prevOverlap = False

while cam.isOpened():
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()

    frame1 = cv2.flip(frame1, 1)
    frame2 = cv2.flip(frame2, 1)

    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dialated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dialated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(frame1, contours, -1, (0,255,0),2)

    for c in contours:
        area = cv2.contourArea(c)
        if area < 5000:
            continue

        x, y, w, h = cv2.boundingRect(c)

        if overlaps(x, y, w, h):
            currentTime = int(round(time.time() * 1000))
            timediff = currentTime - prevTime
            prevTime = currentTime
            if not prevOverlap and timediff > 2000:
                prevOverlap = True
                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                winsound.Beep(500, 200)
                count += 1
                engine.say(str(count))
                engine.runAndWait()
        else:
            #print('setting overlap false ', x, w)
            prevOverlap = False

        break

        # winsound.PlaySound('alert.wav', winsound.SND_ASYNC)

    cv2.rectangle(frame1, (240, 0), (400, 480), (0, 255, 0), 3)

    cv2.putText(frame1, str(count),
                (280, 200),
                cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 3)

    cv2.imshow('Camera', frame1)
    if cv2.waitKey(10) == ord('q'):
        break

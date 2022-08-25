import pygame
import cv2
#from mediapipe import *
from mediapipe.python import mediapipe as mp
import numpy as np
import time
import math

white = [255, 255, 255]
black = [0, 0, 0]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [80, 100, 255]
pygame.init()
screen_width = 800
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("AI FITNESS APP")
left = pygame.image.load("logo12.jpeg")
left = pygame.transform.scale(left, (70, 70))
right = pygame.image.load("logo11.jpeg")
right = pygame.transform.scale(right, (70, 70))
diet = pygame.image.load("one_week_plan.jpeg")
diet = pygame.transform.scale(diet, (screen_width, screen_height))
bmi = pygame.image.load("body_mas.jpeg")
bmi = pygame.transform.scale(bmi, (screen_width, screen_height))
pushups_photo = pygame.image.load("pushup.jpeg")
pushups_photo = pygame.transform.scale(pushups_photo, (190, 185))
squats_photo = pygame.image.load("scoot.jpeg")
squats_photo = pygame.transform.scale(squats_photo, (190, 190))
biceps_curls_photo = pygame.image.load("dubles.jpeg")
biceps_curls_photo = pygame.transform.scale(biceps_curls_photo, (190, 185))
clock = pygame.time.Clock()
pygame.display.update()

font = pygame.font.SysFont(None, 60)


def text_screen(text, color, x, y):
    a = font.render(text, True, color)
    gameWindow.blit(a, (x, y))


font1 = pygame.font.SysFont(None, 45)


def text_screen1(text, color, x, y):
    a = font1.render(text, True, color)
    gameWindow.blit(a, (x, y))


font2 = pygame.font.SysFont(None, 80)


def text_screen2(text, color, x, y):
    a = font2.render(text, True, color)
    gameWindow.blit(a, (x, y))


def pushups():
    cap = cv2.VideoCapture(0)
    ctime = 0
    ptime = 0
    width = 800
    height = 600
    count = 0
    dir = 0

    mpPose = mp.solutions.pose
    pose = mpPose.Pose()
    mpDraw = mp.solutions.drawing_utils

    def findAngle(img, p1, p2, p3, draw=True):
        x1, y1 = lmList[p1][1:]
        x2, y2 = lmList[p2][1:]
        x3, y3 = lmList[p3][1:]
        angle = math.degrees(math.atan2(y3-y1, x3-x1)-math.atan2(y1-y2, x1-x2))
        if angle < 0:
            angle += 360
        if draw:
            cv2.circle(img, (x1, y1), 6, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 6, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 6, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x1, y1), 10, (255, 0, 0), thickness=2)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), thickness=2)
            cv2.circle(img, (x3, y3), 10, (255, 0, 0), thickness=2)
            cv2.putText(img, str(int(angle)), (x2+10, y2),
                        fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(), thickness=3)
        return angle

    while True:
        success, img1 = cap.read()
        img = cv2.resize(img1, (width, height))
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        lmList = []
        if results.pose_landmarks:
            mpDraw.draw_landmarks(
                img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
        if len(lmList) != 0:
            angle = findAngle(img, 12, 14, 16)
            per = np.interp(angle, (100, 170), (100, 0))
            bar = np.interp(angle, (100, 170), (250, 500))
            angle1 = findAngle(img, 11, 13, 15)
            per1 = np.interp(angle1, (190, 260), (0, 100))
            bar1 = np.interp(angle1, (190, 260), (500, 250))
            if per == 100 and per1 == 100:
                if dir == 0:
                    count = count + 0.5
                    dir = 1
            if per == 0 and per1 == 0:
                if dir == 1:
                    count = count + 0.5
                    dir = 0
            cv2.putText(img, "COUNT : " + str(count), (570, 40),
                        fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(255, 0, 0), thickness=3)
            cv2.rectangle(img, (30, 250), (70, 500), color=(), thickness=3)
            cv2.rectangle(img, (30, int(bar)), (70, 500),
                          (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(int(per)) + "%", (30, 200),
                        fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(), thickness=3)
            cv2.rectangle(img, (730, 250), (770, 500), color=(), thickness=3)
            cv2.rectangle(img, (730, int(bar1)), (770, 500),
                          (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(int(per1)) + "%", (730, 200),
                        fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(), thickness=3)
        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime = ctime
        cv2.putText(img, "FPS : " + str(int(fps)), (15, 40),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(255, 0, 0), thickness=3)
        cv2.imshow("AI FITNESS APP", img)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def squats():
    cap = cv2.VideoCapture(0)
    ctime = 0
    ptime = 0
    width = 800
    height = 600
    count = 0
    dir = 0

    mpPose = mp.solutions.pose
    pose = mpPose.Pose()
    mpDraw = mp.solutions.drawing_utils

    def findAngle(img, p1, p2, p3, draw=True):
        x1, y1 = lmList[p1][1:]
        x2, y2 = lmList[p2][1:]
        x3, y3 = lmList[p3][1:]
        angle = math.degrees(math.atan2(y3-y1, x3-x1)-math.atan2(y1-y2, x1-x2))
        if angle < 0:
            angle += 360
        if draw:
            cv2.circle(img, (x1, y1), 6, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 6, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 6, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x1, y1), 10, (255, 0, 0), thickness=2)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), thickness=2)
            cv2.circle(img, (x3, y3), 10, (255, 0, 0), thickness=2)
            cv2.putText(img, str(int(angle)), (x2+10, y2),
                        fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(), thickness=3)
        return angle

    while True:
        success, img1 = cap.read()
        img = cv2.resize(img1, (width, height))
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        lmList = []
        if results.pose_landmarks:
            mpDraw.draw_landmarks(
                img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
        if len(lmList) != 0:
            angle = findAngle(img, 24, 26, 28)
            per = np.interp(angle, (140, 170), (100, 0))
            bar = np.interp(angle, (140, 170), (250, 500))
            if per == 100:
                if dir == 0:
                    count = count + 0.5
                    dir = 1
            if per == 0:
                if dir == 1:
                    count = count + 0.5
                    dir = 0
            cv2.putText(img, "COUNT : " + str(count), (570, 40),
                        fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(255, 0, 0), thickness=3)
            cv2.rectangle(img, (30, 250), (70, 500), color=(), thickness=3)
            cv2.rectangle(img, (30, int(bar)), (70, 500),
                          (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(int(per)) + "%", (30, 200),
                        fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(), thickness=3)
        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime = ctime
        cv2.putText(img, "FPS : " + str(int(fps)), (15, 40),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(255, 0, 0), thickness=3)
        cv2.imshow("AI FITNESS APP", img)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def biceps_curls():
    cap = cv2.VideoCapture(0)
    ctime = 0
    ptime = 0
    width = 800
    height = 600
    count = 0
    dir = 0

    mpPose = mp.solutions.pose
    pose = mpPose.Pose()
    mpDraw = mp.solutions.drawing_utils

    def findAngle(img, p1, p2, p3, draw=True):
        x1, y1 = lmList[p1][1:]
        x2, y2 = lmList[p2][1:]
        x3, y3 = lmList[p3][1:]
        angle = math.degrees(math.atan2(y3-y1, x3-x1)-math.atan2(y1-y2, x1-x2))
        if angle < 0:
            angle += 360
        if draw:
            cv2.circle(img, (x1, y1), 6, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 6, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 6, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x1, y1), 10, (255, 0, 0), thickness=2)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), thickness=2)
            cv2.circle(img, (x3, y3), 10, (255, 0, 0), thickness=2)
            cv2.putText(img, str(int(angle)), (x2+10, y2),
                        fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(), thickness=3)
        return angle

    while True:
        success, img1 = cap.read()
        img = cv2.resize(img1, (width, height))
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        lmList = []
        if results.pose_landmarks:
            mpDraw.draw_landmarks(
                img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
        if len(lmList) != 0:
            angle = findAngle(img, 12, 14, 16)
            per = np.interp(angle, (190, 245), (0, 100))
            bar = np.interp(angle, (190, 245), (500, 250))
            angle1 = findAngle(img, 11, 13, 15)
            per1 = np.interp(angle1, (115, 170), (100, 0))
            bar1 = np.interp(angle1, (115, 170), (250, 500))
            if per == 100 and per1 == 100:
                if dir == 0:
                    count = count + 0.5
                    dir = 1
            if per == 0 and per1 == 0:
                if dir == 1:
                    count = count + 0.5
                    dir = 0
            cv2.putText(img, "COUNT : " + str(count), (570, 40),
                        fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(255, 0, 0), thickness=3)
            cv2.rectangle(img, (30, 250), (70, 500), color=(), thickness=3)
            cv2.rectangle(img, (30, int(bar)), (70, 500),
                          (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(int(per)) + "%", (30, 200),
                        fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(), thickness=3)
            cv2.rectangle(img, (730, 250), (770, 500), color=(), thickness=3)
            cv2.rectangle(img, (730, int(bar1)), (770, 500),
                          (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(int(per1)) + "%", (730, 200),
                        fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(), thickness=3)
        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime = ctime
        cv2.putText(img, "FPS : " + str(int(fps)), (15, 40),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(255, 0, 0), thickness=3)
        cv2.imshow("AI FITNESS APP", img)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def start():
    exit_game = False
    gameWindow.fill(black)
    e = pygame.draw.rect(gameWindow, green, [0, 0, screen_width, 200])
    f = pygame.draw.rect(gameWindow, green, [0, 200, screen_width, 200])
    g = pygame.draw.rect(gameWindow, green, [0, 400, screen_width, 200])
    pygame.draw.rect(gameWindow, black, [0, 0, screen_width, 200], 5)
    pygame.draw.rect(gameWindow, black, [0, 200, screen_width, 200], 5)
    pygame.draw.rect(gameWindow, black, [0, 400, screen_width, 200], 5)
    pygame.draw.rect(gameWindow, black, [
                     0, 0, screen_width, screen_height], 10)
    pygame.draw.rect(gameWindow, black, [0, 0, 200, 200])
    pygame.draw.rect(gameWindow, black, [0, 200, 200, 200])
    pygame.draw.rect(gameWindow, black, [0, 400, 200, 200])
    text_screen2("PUSH-UPS", black, 350, 80)
    text_screen2("SQUATS", black, 380, 270)
    text_screen2("BICEPS CURLS", black, 300, 470)
    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_BACKSPACE:
                    game_loop()
            pos5 = pygame.mouse.get_pos()
            pos6 = pygame.mouse.get_pos()
            pos7 = pygame.mouse.get_pos()
            if e.collidepoint(pos5):
                if pygame.mouse.get_pressed()[0] == 1:
                    pushups()
            if f.collidepoint(pos6):
                if pygame.mouse.get_pressed()[0] == 1:
                    pygame.quit()
                    squats()
            if g.collidepoint(pos7):
                if pygame.mouse.get_pressed()[0] == 1:
                    pygame.quit()
                    biceps_curls()
        gameWindow.blit(pushups_photo, (10, 10))
        gameWindow.blit(squats_photo, (10, 205))
        gameWindow.blit(biceps_curls_photo, (10, 405))
        clock.tick(30)
        pygame.display.update()


def diet_plan():
    exit_game = False
    gameWindow.fill(black)
    gameWindow.blit(diet, (0, 0))
    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_BACKSPACE:
                    game_loop()
        clock.tick(30)
        pygame.display.update()


def bmi_report():
    exit_game = False
    gameWindow.fill(black)
    gameWindow.blit(bmi, (0, 0))
    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_BACKSPACE:
                    game_loop()
        clock.tick(30)
        pygame.display.update()


def game_loop():
    exit_game = False
    game_over = False
    while not exit_game:
        gameWindow.fill(black)
        c = pygame.draw.rect(gameWindow, white, [480, 230, 250, 50], 0, 10)
        d = pygame.draw.rect(gameWindow, white, [480, 380, 250, 50], 0, 10)
        a = pygame.draw.rect(gameWindow, white, [80, 230, 250, 50], 0, 10)
        b = pygame.draw.rect(gameWindow, white, [80, 380, 250, 50], 0, 10)
        text_screen("Fitness", white, 300, 25)
        text_screen("AI", blue, 470, 25)
        gameWindow.blit(left, (200, 10))
        gameWindow.blit(right, (540, 10))
        text_screen1("EXERCISES", black, 118, 242)
        text_screen1("DIETS", black, 154, 392)
        text_screen1("BMI REPORT", black, 514, 242)
        text_screen1("QUIT", black, 560, 392)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_BACKSPACE:
                    game_loop()
            pos1 = pygame.mouse.get_pos()
            pos2 = pygame.mouse.get_pos()
            pos3 = pygame.mouse.get_pos()
            pos4 = pygame.mouse.get_pos()
            if a.collidepoint(pos1):
                if pygame.mouse.get_pressed()[0] == 1:
                    start()
            if b.collidepoint(pos2):
                if pygame.mouse.get_pressed()[0] == 1:
                    diet_plan()
            if c.collidepoint(pos3):
                if pygame.mouse.get_pressed()[0] == 1:
                    bmi_report()
            if d.collidepoint(pos4):
                if pygame.mouse.get_pressed()[0] == 1:
                    pygame.quit()
                    quit()
        clock.tick(30)
        pygame.display.update()
    pygame.quit()
    quit()
game_loop()

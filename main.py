import pygame as pg
import random
from theme import *
from snake import Snake

SIZE, size = 800, 50
VERSION = '0.1.0'
CONTROLL_ENABLE = False

def generate_food(snake):
    isIn = True
    food = [random.randint(0, SIZE/size-1), random.randint(0, SIZE/size-1)]
    while isIn:
        for b in snake:
            if food in b:
                food = [random.randint(0, SIZE/size-1), random.randint(0, SIZE/size-1)]
                continue
        isIn = False
    return food

def draw_snake(window, snake):
    head = snake.body[0]
    body = snake.body[0:-1]
    tail = snake.body[-1]
    direct = snake.direct

    # Draw head
    if direct == 0:
        pg.draw.circle(window, SNAKE, (head[0]*size, (head[1]+0.5)*size), size/2)
    elif direct == 1:
        pg.draw.circle(window, SNAKE, ((head[0]+1)*size, (head[1]+0.5)*size), size/2)
    elif direct == 2:
        pg.draw.circle(window, SNAKE, ((head[0]+0.5)*size, head[1]*size), size/2)
    elif direct == 3:
        pg.draw.circle(window, SNAKE, ((head[0]+0.5)*size, (head[1]+1)*size), size/2)

    # Draw body
    for i in body:
        pg.draw.rect(window, SNAKE, (i[0] * size, i[1] * size, size, size))

    # Draw tail
    x = tail[0] - body[-1][0]
    y = tail[1] - body[-1][1]
    if x == 1:
        pg.draw.polygon(window, SNAKE, ((tail[0]*size, tail[1]*size), ((tail[0]+1)*size, (tail[1]+0.5)*size), (tail[0]*size, (tail[1]+1)*size)))
    elif x == -1:
        pg.draw.polygon(window, SNAKE, ((tail[0]*size, (tail[1]+0.5)*size), ((tail[0]+1)*size, tail[1]*size), ((tail[0]+1)*size, (tail[1]+1)*size)))
    elif y == 1:
        pg.draw.polygon(window, SNAKE, ((tail[0]*size, tail[1]*size), ((tail[0]+0.5)*size, (tail[1]+1)*size), ((tail[0]+1)*size, tail[1]*size)))
    elif y == -1:
        pg.draw.polygon(window, SNAKE, ((tail[0]*size, (tail[1]+1)*size), ((tail[0]+1)*size, (tail[1]+1)*size), ((tail[0]+0.5)*size, tail[1]*size)))

def draw_food(window, food):
    pg.draw.circle(window, RED, ((food[0]+0.5)*size, (food[1]+0.5)*size), size/2)

def isEaten(head, food):
    if head[0] == food[0] and head[1] == food[1]:
        return True
    else:
        return False

def collision(snake):
    head = snake.body[0]
    body = snake.body[1:]
    for b in body:
        if head[0] == b[0] and head[1] == b[1]:
            return True
    return False

def check_obj(snake, direct):
    head = snake.body[0]
    body = snake.body[1:]
    SPACE = 1
    for b in body:
        if direct == 0 or direct == 1:
            if head[1] == b[1] and abs(head[0]-b[0]) <= SPACE:
                return True
        elif direct == 2 or direct == 3:
            if head[0] == b[0] and abs(head[1]-b[1]) <= SPACE:
                return True
    return False

def auto_play(snake, food, direct):
    head = snake.body[0]
    x = head[0] - food[0]
    y = head[1] - food[1]
    temp = direct
    if direct == 0 or direct == 1:
        if -1 <= x and x <= 1:
            if check_obj(snake, direct):
                temp = random.randint(0, 1) + 2
            elif y > 0:
                temp = 2
            elif y < 0:
                temp = 3

    if direct == 2 or direct == 3:
        if -1 <= y and y <= 1:
            if check_obj(snake, direct):
                temp = random.randint(0, 1)
            elif x > 0:
                temp = 0
            elif x < 0:
                temp = 1
    return temp

def main(window):
    running = True
    clock = pg.time.Clock()
    time = 0
    fps, frame, speed = 120, 0, 12
    snake = Snake(5, int(SIZE/size-1))
    food = generate_food(snake.body)
    start = True
    direct = 0
    point = 0
    
    while running:
        clock.tick(fps)
        window.fill(BACKGROUND)

        if not CONTROLL_ENABLE:
            direct = auto_play(snake, food, direct)

        draw_food(window, food)
        draw_snake(window, snake)

        if start:
            start = not collision(snake)
            if frame == fps/speed:
                snake.move()
                snake.change_direct(direct)
                frame = 0
            else:
                frame += 1

        if isEaten(snake.body[0], food):
            snake.eat()
            food = generate_food(snake.body)
            point += 1
            time = 0
        else:
            time += 1
            if time >= fps*5:
                with open('score.txt', 'a') as f:
                    f.write('version: ' + VERSION + ', pts: ' + str(point)+'\n')
                snake = Snake(5, int(SIZE/size-1))
                food = generate_food(snake.body)
                point, time = 0, 0
                start = True

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                    break
                if CONTROLL_ENABLE:
                    if event.key == pg.K_LEFT or event.key == pg.K_a:
                        direct = 0
                    if event.key == pg.K_RIGHT or event.key == pg.K_d:
                        direct = 1
                    if event.key == pg.K_UP or event.key == pg.K_w:
                        direct = 2
                    if event.key == pg.K_DOWN or event.key == pg.K_s:
                        direct = 3

        pg.display.update()
    pg.quit()

if __name__ == '__main__':
    pg.init()
    window = pg.display.set_mode((SIZE, SIZE))
    pg.display.set_caption("Snake")
    main(window)
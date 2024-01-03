import pygame as pg
import sys
import random

wd = 800
hg = 800
block_size = 30
eye_size = block_size // 6
count_block = 1
game_speed = 8
white = (255, 255, 255)
twilight = (95, 0, 160)
yellow = (108, 186, 59)
black = (0, 0, 0)
red = (213, 50, 80)
green_grass = (128, 200, 80)
green_grass_black = (19, 109, 21)
blue = (50, 153, 213)
apple = 1
snake_lenght = 3
apple_radius = block_size // 2
snake_radius = block_size // 5
size_x = (wd // block_size - count_block * 2)
size_y = (hg // block_size - count_block * 2)
font_size = int(count_block * block_size * 0.75)


def main():
    dis, clock = initialize_pg()
    state = initizalize_pg_state()
    while state["prog_running"]:
        clock.tick(game_speed)
        events = get_events()
        upd_game_state(events, state)
        upd_display(dis, state)
    shutdown()


def initialize_pg():
    pg.init()
    dis = pg.display.set_mode((wd, hg))
    pg.display.set_caption('snake_for brother')
    clock = pg.time.Clock()
    return dis, clock


def initizalize_pg_state():
    state = {
        "prog_running": True,
        "game_running": False,
        "game_paused": False,
        'score': 0,
        'game_speed': game_speed
    }
    return state


def get_events():
    events = []
    for event in pg.event.get():
        if event.type == pg.QUIT:
            events.append('quit')
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                events.append('up')
            elif event.key == pg.K_DOWN:
                events.append('down')
            elif event.key == pg.K_LEFT:
                events.append('left')
            elif event.key == pg.K_RIGHT:
                events.append('right')
            elif event.key == pg.K_SPACE:
                events.append('space')
            elif event.key == pg.K_RETURN:
                events.append('enter')
            elif event.key == pg.K_ESCAPE:
                events.append('escape')

    return events


def upd_game_state(events, state):
    check_key_presses(events, state)

    if state['game_running'] and not state['game_paused']:
        snake_move(state)
        check_collision(state)
        check_apple_eat(state)


def snake_move(state):
    x = state['snake'][0][0] + state['directions'][0]
    y = state['snake'][0][1] + state['directions'][1]
    state['snake'].insert(0, (x, y))


def check_collision(state):
    x, y = state['snake'][0]
    if x < 0 or y < 0 or x >= size_x or y >= size_y:
        state['game_running'] = False
    if len(state['snake']) > len(set(state['snake'])):
        state['game_running'] = False


def check_apple_eat(state):
    apples_eaten = 0
    for apple in state['apples']:
        if apple == state['snake'][0]:
            state['apples'].remove(apple)
            place_apples(1, state)
            state['score'] += 1
            apples_eaten += 1
            state['game_speed'] = round(state['game_speed'] * 1.1)
        if apples_eaten == 0:
            state['snake'].pop()


def check_key_presses(events, state):
    if 'quit' in events:
        state['prog_running'] = False
    elif not state['game_running']:
        if 'escape' in events:
            state['prog_running'] = False
        elif 'enter' in events:
            initizalize_new_game(state)
            state['game_running'] = True
    elif state['game_paused']:
        if 'escape' in events:
            state['game_running'] = False
        elif 'space' in events:
            state['game_paused'] = False
    else:
        if 'escape' in events or 'space' in events:
            state['game_paused'] = True
        if 'up' in events:
            state['directions'] = (0, -1)
        if 'down' in events:
            state['directions'] = (0, 1)
        if 'left' in events:
            state['directions'] = (-1, 0)
        if 'right' in events:
            state['directions'] = (1, 0)


def initizalize_new_game(state):
    state['snake'] = []
    state['apples'] = []
    place_snake(snake_lenght, state)
    place_apples(apple, state)
    state['directions'] = (1, 0)
    state["game_paused"] = False
    state['score'] = 0
    state['game_speed'] = game_speed


def place_snake(lenght, state):
    x = size_x // 2
    y = size_y // 2
    state['snake'].append((x, y))
    for i in range(1, snake_lenght):
        state['snake'].append((x-i, y))


def place_apples(n, state):
    state['apples'] = []
    for i in range(apple):
        x = random.randint(0, size_x - 1)
        y = random.randint(0, size_y - 1)
        while (x, y) in state['apples'] or (x, y) in state['snake']:
            x = random.randint(0, size_x - 1)
            y = random.randint(0, size_y - 1)
        state['apples'].append((x, y))


def upd_display(dis, state):
    dis.fill(black)
    if not state['game_running']:
        print_new_game_message(dis)
    elif state['game_paused']:
        print_game_paused_message(dis)
    else:
        draw_apples(dis, state['apples'])
        draw_snake(dis, state['snake'], state['directions'])
    draw_walls(dis)
    print_score(dis, state['score'])
    pg.display.flip()


def print_new_game_message(dis):
    font = pg.font.SysFont("Ccurier New", font_size*2, bold=True)
    text1 = font.render("Нажмите ENTER: для продолжения: ", True, white)
    text2 = font.render("Нажмите ESCAPE для выхода: ", True, white)
    text_rect1 = text1.get_rect()
    text_rect2 = text2.get_rect()
    text_rect1.center = (wd // 2, hg//2-font_size)
    text_rect2.center = (wd // 2, hg//2+font_size)
    dis.blit(text1, text_rect1)
    dis.blit(text2, text_rect2)


def print_game_paused_message(dis):
    font = pg.font.SysFont("Ccurier New", font_size * 2, bold=True)
    text1 = font.render("Нажмите SPACE: для продолжения: ", True, white)
    text2 = font.render("Нажмите ESCAPE для старта новой игры: ", True, white)
    text_rect1 = text1.get_rect()
    text_rect2 = text2.get_rect()
    text_rect1.center = (wd // 2, hg // 2 - font_size)
    text_rect2.center = (wd // 2, hg // 2 + font_size)
    dis.blit(text1, text_rect1)
    dis.blit(text2, text_rect2)


def draw_snake(dis, snake, directions):
    for element in snake:
        x = element[0] * block_size + count_block * block_size
        y = element[1] * block_size + count_block * block_size
        rect = ((x, y), (block_size, block_size))
        pg.draw.rect(dis, yellow, rect, border_radius=snake_radius)
    draw_snake_eyes(dis, snake[0], directions)


def draw_snake_eyes(dis, head, directions):
    eye_offset = block_size // 4
    x, y = directions[0], directions[1]
    if x == -1 or y == -1:
        cord_x = head[0] * block_size + block_size * count_block + eye_offset
        cord_y = head[1] * block_size + block_size * count_block + eye_offset
        center = (cord_x, cord_y)
        pg.draw.circle(dis, black, center, eye_size)
    if x == -1 or y == 1:
        cord_x = head[0] * block_size + block_size * count_block + eye_offset
        cord_y = head[1] * block_size + block_size * count_block + (block_size - eye_offset)
        center = (cord_x, cord_y)
        pg.draw.circle(dis, black, center, eye_size)
    if x == 1 or y == -1:
        cord_x = head[0] * block_size + block_size * count_block + (block_size-eye_offset)
        cord_y = head[1] * block_size + block_size * count_block + eye_offset
        center = (cord_x, cord_y)
        pg.draw.circle(dis, black, center, eye_size)
    if x == 1 or y == 1:
        cord_x = head[0] * block_size + block_size * count_block + (block_size - eye_offset)
        cord_y = head[1] * block_size + block_size * count_block + (block_size - eye_offset)
        center = (cord_x, cord_y)
        pg.draw.circle(dis, black, center, eye_size)


def draw_walls(dis):
    pg.draw.rect(dis, twilight, ((0, 0), (wd, count_block*block_size)))
    pg.draw.rect(dis, twilight, ((0, 0), (count_block*block_size, hg)))
    pg.draw.rect(dis, twilight, ((0, hg - count_block*block_size), (wd, hg)))
    pg.draw.rect(dis, twilight, ((wd - count_block*block_size, 0), (wd, hg)))


def print_score(dis, score):
    font = pg.font.SysFont("Ccurier New", font_size, bold=True)
    text = font.render("Scor: " + str(score), True, white)
    text_rect = text.get_rect()
    text_rect.midleft = (block_size*count_block, block_size*count_block//2)
    dis.blit(text, text_rect)


def draw_apples(dis, apples):
    for apple in apples:
        x = apple[0] * block_size + count_block * block_size
        y = apple[1] * block_size + count_block * block_size
        rect = ((x, y), (block_size, block_size))
        pg.draw.rect(dis, red, rect, border_radius=apple_radius)


def shutdown():
    pg.quit()
    sys.exit()


main()
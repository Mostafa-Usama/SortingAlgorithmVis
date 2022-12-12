import pygame
import random
pygame.init()


class DrawInfo:

    orange = 255, 150, 0
    black = 0, 0, 0
    white = 255, 255, 255
    grey = 128, 128, 128
    red = 255, 0, 0
    green = 0, 255, 0
    background = white
    sidePad = 100
    topPad = 150
    greys = [grey,
             (160, 160, 160),
             (192, 192, 192)]
    font = pygame.font.SysFont("comicsans", 30)

    def __init__(self, width, height, lst):

        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.maxVal = max(lst)
        self.minVal = min(lst)
        self.block_width = round((self.width - self.sidePad) / len(lst))
        self.block_height = int((self.height-self.topPad) / (self.maxVal-self.minVal))
        self.start_x= self.sidePad // 2


def generate_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst


def draw(draw_info, algo_name):

    draw_info.window.fill(draw_info.background)

    controls = draw_info.font.render("R - Reset | SPACE - Start Sorting", 1, draw_info.black)
    sorting = draw_info.font.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort", 1, draw_info.black)
    title = draw_info.font.render(algo_name, 1, draw_info.orange)

    x_control = (draw_info.width - controls.get_width())/2
    x_sort = (draw_info.width - sorting.get_width())/2
    x_title = (draw_info.width - title.get_width())/2

    draw_info.window.blit(title, (x_title, 5))
    draw_info.window.blit(controls, (x_control, 35))
    draw_info.window.blit(sorting, (x_sort, 65))

    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.sidePad//2, draw_info.topPad, draw_info.width-draw_info.sidePad,
                      draw_info.height-draw_info.topPad)
        pygame.draw.rect(draw_info.window, draw_info.background, clear_rect)
    for i, val in enumerate(lst):
        x = draw_info.start_x + (i * draw_info.block_width)
        y = draw_info.height - (val - draw_info.minVal) * draw_info.block_height
        color = draw_info.greys[i % 3]
        if i in color_positions:
            color = color_positions[i]
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


def bubble_sort(draw_info):
    lst = draw_info.lst
    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            if lst[j] > lst[j+1]:
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_info, {j: draw_info.green, j+1: draw_info.red}, True)
                yield True
    return lst


def insertion_sort(draw_info):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]
        while True:
            if not (i > 0 and lst[i-1] > current):
                break
            lst[i] = lst[i-1]
            i -= 1
            lst[i] = current
            draw_list(draw_info, {i-1: draw_info.green, i: draw_info.red}, True)
            yield True
    return lst


def selection(draw_info):
    lst = draw_info.lst
    for i in range(0, len(lst)-1):
        p = 0
        mini = lst[-1]
        for j in range(i, len(lst)):
            if lst[j] <= mini:
                mini = lst[j]
                p = j
        lst[i], lst[p] = lst[p], lst[i]
        draw_list(draw_info, {p: draw_info.green, i: draw_info.red}, True)
        yield True
    return lst


def main():
    run = True
    sorting = False
    n = 50
    min_val = 0
    max_val = 100
    clock = pygame.time.Clock()
    lst = generate_list(n, min_val, max_val)
    info = DrawInfo(800, 600, lst)
    sorting_algorithm = bubble_sort
    sorting_algorithm_generator = None
    algorithm_name = "Bubble Sort"
    while run:
        clock.tick(30)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(info, algorithm_name)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_list(n, min_val, max_val)
                info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_b and not sorting:
                algorithm_name = "Bubble Sort"
                sorting_algorithm = bubble_sort
            elif event.key == pygame.K_i and not sorting:
                algorithm_name = "Insertion Sort"
                sorting_algorithm = insertion_sort
            elif event.key == pygame.K_s and not sorting:
                algorithm_name = "Selection Sort"
                sorting_algorithm = insertion_sort
            elif event.key == pygame.K_SPACE and not sorting:
                sorting_algorithm_generator = sorting_algorithm(info)
                sorting = True
    pygame.quit()


if __name__ == "__main__":
    main()

import pygame
import random
import time
import threading

pygame.init()

# WINDOW SIZE AND COLOUR CONSTANTS
WIDTH, HEIGHT = 1000, 700
BAR_WIDTH = 8
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)
DARK_GRAY = (100, 100, 100)

# GREY SEMI TRANSPARENT COLOUR
TRANSPARENT_GRAY = (150, 150, 150, 180)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Sorting Visualizer with Slider")

# DYNAMIC BAR CONSTANTS
min_bars, max_bars = 10, WIDTH // BAR_WIDTH
numberBars = min_bars


array = []
sorting_done = False
sorting_time = 0
current_algorithm = None

# SLIDER CONSTANTS
SLIDER_X, SLIDER_Y = 10, HEIGHT - 50
SLIDER_WIDTH, SLIDER_HEIGHT = 300, 20
HANDLE_WIDTH, HANDLE_HEIGHT = 10, 30
handle_x = SLIDER_X  # Initial handle position

# DICTIONNARY OF THE DIFFERENT SORTINGS AND THEIR SPACE-TIME COMPLEXITY IN O NOTATION
ALGORITHMS = {
    "Bubble Sort": {"func": "bubbleSort", "complexity": "O(n²)"},
    "Quick Sort": {"func": "quickSort", "complexity": "O(n log n)"},
    "Merge Sort": {"func": "mergeSort", "complexity": "O(n log n)"},
    "Insertion Sort": {"func": "insertionSort", "complexity": "O(n²)"},
}



# RANDOM ARRAY, WITH GIVEN NUMBER OF BARS
def generate_array(size=numberBars):
    return [random.randint(50, HEIGHT - 100) for _ in range(size)]



#DRAW ELEMENTS
def draw_array(array, colors=None):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 30)
    
    # UI ELEMENTS
    if sorting_done:
        reset_text = font.render("Press 'R' to Reset | Time: {:.2f}s".format(sorting_time), True, BLACK)
        screen.blit(reset_text, (10, 10))
    if current_algorithm:
        algo_text = font.render(f"Algorithm: {current_algorithm} ({ALGORITHMS[current_algorithm]['complexity']})", True, BLACK)
        screen.blit(algo_text, (10, 40))
    
    # DRAW THE BARS
    for i, value in enumerate(array):
        color = colors[i] if colors and i < len(colors) else BLACK
        pygame.draw.rect(screen, color, (i * BAR_WIDTH, HEIGHT - value, BAR_WIDTH - 1, value))
    
    



    for i, (algo, _) in enumerate(ALGORITHMS.items()):
        pygame.draw.rect(screen, GRAY, (WIDTH - 200, 10 + i * 40, 180, 30))
        text = font.render(algo, True, BLACK)
        screen.blit(text, (WIDTH - 190, 15 + i * 40))
    
    # DRAW SLIDER
    pygame.draw.rect(screen, GRAY, (SLIDER_X, SLIDER_Y, SLIDER_WIDTH, SLIDER_HEIGHT))
    pygame.draw.rect(screen, DARK_GRAY, (handle_x, SLIDER_Y - 5, HANDLE_WIDTH, HANDLE_HEIGHT))
    


    # SLIDER TEXT
    slider_text = font.render(f"Bars: {numberBars}", True, BLACK)
    text_rect = slider_text.get_rect(topleft=(SLIDER_X + SLIDER_WIDTH + 10, SLIDER_Y))
    background_rect = pygame.Rect(text_rect.left - 5, text_rect.top - 5, text_rect.width + 10, text_rect.height + 10)
    pygame.draw.rect(screen, TRANSPARENT_GRAY, background_rect)  # Semi-transparent background
    screen.blit(slider_text, (SLIDER_X + SLIDER_WIDTH + 10, SLIDER_Y))
    
    pygame.display.update()

# BUBBLE SORT
def bubbleSort(array):
    global sorting_done, sorting_time
    start_time = time.time()
    n = len(array)
    for i in range(n):

        for j in range(n - 1 - i):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                draw_array(array, [RED if x == j or x == j + 1 else BLACK for x in range(len(array))])
                pygame.time.delay(1)
    sorting_time = time.time() - start_time
    sorting_done = True
    return array

#QUICK SORT
def quickSort(array, low, high):
    if low < high:
        pivot = partition(array, low, high)
        quickSort(array, low, pivot - 1)
        quickSort(array, pivot + 1, high)
    return array


def partition(array, low, high):
    pivot = array[high]
    i = low - 1
    for j in range(low, high):

        if array[j] < pivot:
            i += 1
            array[i], array[j] = array[j], array[i]
            draw_array(array, [GREEN if x == i or x == j else BLACK for x in range(len(array))])
            pygame.time.delay(2)
    array[i + 1], array[high] = array[high], array[i + 1]
    return i + 1

#MERGE SORT
def mergeSort(array, left, right):
    if left < right:
        mid = (left + right) // 2
        mergeSort(array, left, mid)
        mergeSort(array, mid + 1, right)
        merge(array, left, mid, right)
    return array


# MERGE FOR MERGE SORT
def merge(array, left, mid, right):
    left_part = array[left:mid + 1]
    right_part = array[mid + 1:right + 1]
    i = j = 0
    k = left
    while i < len(left_part) and j < len(right_part):
        if left_part[i] < right_part[j]:
            array[k] = left_part[i]
            i += 1
        else:
            array[k] = right_part[j]
            j += 1
        draw_array(array, [GREEN if x == k else BLACK for x in range(len(array))])
        pygame.time.delay(2)
        k += 1
    while i < len(left_part):
        array[k] = left_part[i]
        i += 1
        k += 1
    while j < len(right_part):
        array[k] = right_part[j]
        j += 1
        k += 1



# INSERTION SORT
def insertionSort(array):
    global sorting_done, sorting_time
    start_time = time.time()
    n = len(array)
    for i in range(1, n):
        key = array[i]
        j = i - 1
        while j >= 0 and key < array[j]:
            array[j + 1] = array[j]
            j -= 1
            draw_array(array, [RED if x == j or x == j + 1 else BLACK for x in range(len(array))])
            pygame.time.delay(2)
        array[j + 1] = key
    sorting_time = time.time() - start_time
    sorting_done = True
    return array

# THREADED SORTING FUNCTION
def run_sorting(algo_name, array):
    global sorting_done, sorting_time, current_algorithm
    sorting_done = False
    current_algorithm = algo_name
    start_time = time.time()
    
    if algo_name == "Bubble Sort":
        sorted_array = bubbleSort(array)
    elif algo_name == "Quick Sort":
        sorted_array = quickSort(array, 0, len(array) - 1)
    elif algo_name == "Merge Sort":
        sorted_array = mergeSort(array, 0, len(array) - 1)
    elif algo_name == "Insertion Sort":
        sorted_array = insertionSort(array)
    
    sorting_time = time.time() - start_time
    sorting_done = True
    return sorted_array

# MAIN LOOP
array = generate_array()
running = True
dragging = False

while running:
    draw_array(array)
    
    # USE OF EVENT TYPE TO DETERMINE USER INPUTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                array = generate_array(numberBars)
                sorting_done = False
                sorting_time = 0
                current_algorithm = None




        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            
            if SLIDER_X <= x <= SLIDER_X + SLIDER_WIDTH and SLIDER_Y - 5 <= y <= SLIDER_Y + HANDLE_HEIGHT + 5:
                dragging = True
            

            if WIDTH - 200 <= x <= WIDTH - 20 and not sorting_done:
                for i, algo in enumerate(ALGORITHMS.keys()):
                    if 10 + i * 40 <= y <= 40 + i * 40:
                        sort_thread = threading.Thread(target=lambda: globals().update(array=run_sorting(algo, array.copy())))
                        sort_thread.start()



        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False



        elif event.type == pygame.MOUSEMOTION and dragging:
            x, _ = event.pos
            
            # INTERPOLATE THE MOUSE DRAGGING
            handle_x = max(SLIDER_X, min(x - HANDLE_WIDTH // 2, SLIDER_X + SLIDER_WIDTH - HANDLE_WIDTH))
            
            slider_range = SLIDER_WIDTH - HANDLE_WIDTH
            position_ratio = (handle_x - SLIDER_X) / slider_range
            numberBars = int(min_bars + (max_bars - min_bars) * position_ratio)
            array = generate_array(numberBars)
            sorting_done = False
            sorting_time = 0
            current_algorithm = None

pygame.quit()
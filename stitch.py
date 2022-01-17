
import pygame

def prepare_phrase(phrase):
    new_phrase = phrase
    new_phrase = remove_spaces(new_phrase)
    new_phrase = lowercase_phrase(new_phrase)
    return new_phrase

def remove_spaces(phrase):
    new_phrase = ''                                                                                 
    for ch in phrase:
        if not ord(ch) < 33:
            new_phrase += ch
    return new_phrase

def lowercase_phrase(phrase):
    new_phrase = ''
    for ch in phrase:
        new_phrase += character_lowercase_ascii(ch)
    return new_phrase

def character_lowercase_ascii(ch):
    if ord(ch) > 64 and ord(ch) < 91:
        return chr(ord(ch) + 32)
    else:
        return ch

def binarize_phrase(phrase):
    new_phrase = []
    for ch in phrase:
        new_phrase.append(is_character_vowel(ch))
    return new_phrase
        
def is_character_vowel(ch):
    if ch == 'a' or ch == 'e' or ch == 'i' or ch == 'o' or ch == 'u':
        return True
    else:
        return False

def is_vertical_line(col_number, cols_total):
    if col_number > 0 and col_number < cols_total - 2:
        return col_number % 2

def is_horizontal_line(col_number, cols_total):
    if col_number < cols_total - 1:
        return col_number % 2 == 0


def mark_vertical_line(phrase, coords):
    phrase_char = phrase[int((coords[0] - 1) / 2)]
    if phrase_char and coords[1] % 2 == 0:
        return True
    elif not phrase_char and coords[1] % 2 == 1:
        return True

def mark_horizontal_line(phrase, coords):
    if coords[1] > 0:
        phrase_char = phrase[coords[1] - 1]
        if phrase_char and coords[0] % 4 == 0:
            return True
        elif not phrase_char and coords[0] % 4 == 2:
            return True

phrase_x = 'phrase_1'
phrase_y = 'phrase_2'

phrase_1 = input('Enter phrase 1 (if blank default phrases are used): ')
if phrase_1:
    phrase_x = phrase_1
    phrase_y = input('Enter phrase 2: ')

phrase_x = prepare_phrase(phrase_x)
phrase_y = prepare_phrase(phrase_y)

len_x = len(phrase_x) * 2 + 2
len_y = len(phrase_y) + 1

binary_phrase_x = binarize_phrase(phrase_x)
binary_phrase_y = binarize_phrase(phrase_y)

rows = []
for row_number in range(0, len_y):
    row = ''
    for col_number in range(0, len_x):
        ch = ' '
        if is_vertical_line(col_number, len_x):
            if mark_vertical_line(binary_phrase_x, [col_number, row_number]):
                ch = '|'
        elif is_horizontal_line(col_number, len_x):
            if mark_horizontal_line(binary_phrase_y, [col_number, row_number]):
                ch = '_'
        row += ch
    rows.append(row)

rows.reverse()
for row in rows:
    print(row)


BLOCKS_X = len(phrase_x) + 1
BLOCKS_Y = len_y

class Blocks():
    blocks = []

    def __init__(self, blocks):
        self.blocks = blocks

class Block():

    fill_type = 0
    fill_row_start = 0

    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.is_n_border = None
        self.is_w_border = None
        self.fill = 0

    def set_fill(self, border):
        if border == True:
            Block.fill_type += 1
        self.fill = Block.fill_type


    def define_fill(self):
        if self.pos_x:
            self.set_fill(self.is_w_border)
        elif self.pos_y:
            Block.fill_type = Block.fill_row_start
            self.set_fill(self.is_n_border)
            Block.fill_row_start = self.fill
        else:
            self.set_fill(False)



    def check_barriers(self, string_group):
        self.check_n(string_group)
        self.check_w(string_group)

    def check_n(self, string_group):
        check_coords = self.check_n_coords()
        string_to_check = string_group[check_coords[1]]
        char_to_check = string_to_check[check_coords[0]]
        if not self.pos_y == 0:
            if char_to_check == ' ':
                self.is_n_border = False 
            else:
                self.is_n_border = True 

    def check_w(self, string_group):
        check_coords = self.check_w_coords()
        string_to_check = string_group[check_coords[1]]
        char_to_check = string_to_check[check_coords[0]]
        if not self.pos_x == 0:
            if char_to_check == ' ':
                self.is_w_border = False 
            else:
                self.is_w_border = True 

    def check_n_coords(self):
        check_x = self.pos_x * 2 
        check_y = self.pos_y - 1
        return (check_x, check_y)

    def check_w_coords(self):
        check_x = self.pos_x * 2 - 1
        check_y = self.pos_y
        return (check_x, check_y)

def print_lines():
    for i, row in enumerate(rows):
        for j, ch in enumerate(row):
            pos_x = int((j + 1) / 2) * BLOCK_SIZE
            pos_y = (i + 1) * BLOCK_SIZE
            pos_start = [pos_x , pos_y]
            pos_end = list(pos_start)
            if ch == '_':
                pos_end[0] += BLOCK_SIZE
            elif ch == '|':
                pos_end[1] -= BLOCK_SIZE
            pygame.draw.line(screen, LINE_COLOUR, pos_start, pos_end) 

def print_blocks():
    for key in blocks:
        block = blocks[key]
        # print(block.pos_x, block.pos_y, block.fill)
        pos_y = block.pos_y * BLOCK_SIZE
        pos_x = block.pos_x * BLOCK_SIZE
        if block.fill % 2:
            color = COLOUR_1
        else:
            color = COLOUR_2
        pygame.draw.rect(screen, color, (pos_x, pos_y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.flip()
        # input('test')
        
blocks = {}
for j in range(0, BLOCKS_Y):
    for i in range(0, BLOCKS_X):
        block = Block(i, j)
        block.check_barriers(rows)
        block.define_fill()
        blocks.update({(i, j): block}) 


mylist = []
for key in blocks:
    block = blocks[key]
    mylist.append(block)

    
BLOCK_SIZE = 32
LINE_COLOUR = (32,32,52)
COLOUR_1 = (22, 63, 88)
COLOUR_2 = (245, 181, 27)

WIDTH = BLOCKS_X * BLOCK_SIZE 
HEIGHT = BLOCKS_Y * BLOCK_SIZE 
FPS = 1
TITLE = "Hitomezashi stitches"

pygame.init()
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
all_sprites = pygame.sprite.Group()

screen.fill((240, 240, 240))

print_lines()
print_blocks()

running = True
while running:
    clock.tick(FPS)
    pygame.display.flip()
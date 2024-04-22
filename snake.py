import pygame, sys, random
from pygame.math import Vector2

class Snake:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
		
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.eat_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def draw_snake(self):
        self.insert_head_graphics()
        self.insert_tail_graphics()
        
        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            #pygame.draw.rect(screen, (183,111,122), block_rect)
            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block_relation = block - self.body[index + 1]
                next_block_relation = block - self.body[index - 1]
                if previous_block_relation.x == next_block_relation.x:
                    screen.blit(self.body_vertical,block_rect) 
                elif previous_block_relation.y == next_block_relation.y:
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block_relation.x == -1 and next_block_relation.y == -1 or previous_block_relation.y == -1 and next_block_relation.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block_relation.x == -1 and next_block_relation.y == 1 or previous_block_relation.y == 1 and next_block_relation.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block_relation.x == 1 and next_block_relation.y == -1 or previous_block_relation.y == -1 and next_block_relation.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block_relation.x == 1 and next_block_relation.y == 1 or previous_block_relation.y == 1 and next_block_relation.x == 1:
                        screen.blit(self.body_br,block_rect)
                    #pygame.draw.rect(screen, (183,111,122), block_rect)


    def insert_head_graphics(self):
        head_relation = self.body[0] - self.body[1]
        if head_relation == Vector2(1,0): self.head = self.head_right
        elif head_relation == Vector2(-1,0): self.head = self.head_left
        elif head_relation == Vector2(0,1): self.head = self.head_down
        elif head_relation == Vector2(0,-1): self.head = self.head_up

    def insert_tail_graphics(self):
        tail_relation = self.body[-1] - self.body[-2]
        if tail_relation == Vector2(1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(0,1): self.tail = self.tail_down
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_up

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy

    def add_block(self):
        self.new_block = True

    def play_eat_sound(self):
        self.eat_sound.play()

class Rabbit:
    def __init__(self):
        self.create_new_rabbit()

    def draw_rabbit(self):
        rabbit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(rabbit,rabbit_rect)
        #pygame.draw.rect(screen,(126,166,114),rabbit_rect)

    def create_new_rabbit(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number -1)
        self.pos = Vector2(self.x,self.y)

class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Rabbit()


    def update(self):
        self.snake.move_snake()
        self.check_collision()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_rabbit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.snake.body[0] == self.fruit.pos:
            self.fruit.create_new_rabbit()
            self.snake.add_block()
            self.snake.play_eat_sound()
        elif self.snake.body[0].x < 0 or self.snake.body[0].x >= cell_number:
            self.game_over()
        elif self.snake.body[0].y < 0 or self.snake.body[0].y >= cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()

    def draw_grass(self):
        grass_color = (167,209,61)
        for row in range(cell_number):
            if row % 2 == 0: 
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
    
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True,(56,74,12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        screen.blit(score_surface,score_rect)
        rabbit_rect = rabbit.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(rabbit_rect.left,rabbit_rect.top,rabbit_rect.width + score_rect.width + 6,rabbit_rect.height)

        pygame.draw.rect(screen,(167,209,61),bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(rabbit,rabbit_rect)
        pygame.draw.rect(screen,(56,74,12),bg_rect,2)

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
rabbit = pygame.image.load('Graphics/rabbit.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = Main()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)
            

    screen.fill((175,215,70))
    # draw all our elements
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
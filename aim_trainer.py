import pygame
import random
import time
import math

pygame.init()

WIDTH,HEIGHT = 800,600
TOP_BAR_HEIGHT = 50
LIVES = 3
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Aim Trainer")
TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30
BG_COLOR = (0,25,40)
LABEL_FONT = pygame.font.SysFont("comicsans",24)


class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    SECOND_COLOR = "white"

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size +=self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self,win):
        pygame.draw.circle(win,self.COLOR,(self.x,self.y),self.size)
        pygame.draw.circle(win,self.SECOND_COLOR,(self.x,self.y),self.size *0.8)
        pygame.draw.circle(win,self.COLOR,(self.x,self.y),self.size*0.6)
        pygame.draw.circle(win,self.SECOND_COLOR,(self.x,self.y),self.size*0.4)

    def collide(self,x,y):
        dis = math.sqrt((self.x - x) **2+(self.y-y)**2)
        #   100
        return dis <= self.size
        

class BottomHistorical:
    def __init__(self,win,x,y):
        self.win = win
        self.x = x
        self.y = y
        self.BOTTOM_COLOR = "red"

    def draw_bottom(self):
        pygame.draw.rect(self.win, self.BOTTOM_COLOR, (self.x, self.y, 150, 80))
        fonte = pygame.font.SysFont(None, 30)
        texto_surface = fonte.render("See Historical", True, "white")
        # Centraliza o texto no botão
        texto_rect = texto_surface.get_rect(center=(self.x + 150 / 2, self.y + 80 / 2))
        self.win.blit(texto_surface, texto_rect)

    def bottom_clicked(self, pos_mouse):
        # Verifica se a posição do mouse está dentro das coordenadas do botão
        if (self.x < pos_mouse[0] < self.x + 150 and
            self.y < pos_mouse[1] < self.y + 80):
            return True
        else:
            return False

def draw(win,targets):
    win.fill(BG_COLOR)
    for target in targets:
        target.draw(win)
    

def fomat_time(secs):
    milli = math.floor(int(secs*1000 % 1000 / 100))
    seconds = int(round(secs % 60,1))
    minutes = int(secs // 60)
    return f"{minutes:02d}:{seconds:02d}:{milli:02d}"

def draw_top_bar(win,elapsed_time,targets_pressed,misses):
    pygame.draw.rect(win,"grey",(0,0,WIDTH,TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(f"Time: {fomat_time(elapsed_time)}",1,"black")
    speed = round(targets_pressed / elapsed_time,1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s",1,"black")
    tg_label = LABEL_FONT.render(f"Hits: {targets_pressed}",1,"black")
    misses_label = LABEL_FONT.render(f"Misses: {misses}",1,"black")
    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}",1,"black")
    win.blit(time_label,(5,5))
    win.blit(speed_label,(200,5))
    win.blit(tg_label,(400,5))
    win.blit(misses_label,(550,5))
    win.blit(lives_label,(690,5))

def save_score(speed,hits,acuracy):
    with open("aim_trainer/score_historical.txt","a") as f:
        f.write(f"Speed: {speed}, Hits: {hits},Acuracy: {acuracy}\n")

def draw_historical_scores():
    with open("aim_trainer/score_historical.txt","r") as f:
        lines = f.readlines()
        lines
    return lines

def print_historical(win):
    win.fill(BG_COLOR)
    # Renderizar o texto "Historical Score"
    title_font = pygame.font.SysFont(None, 30)
    texto_surface = title_font.render("Historical Score", True, (255, 255, 255))
    # Posicione o texto na tela
    win.blit(texto_surface, (80, 5))
    historical = draw_historical_scores()
    lines_font = pygame.font.SysFont(None, 15)
    # Desenhar as pontuações históricas na tela
    re_index = 0
    for i, line in enumerate(historical):
        historical_text = lines_font.render(line.strip(), True, (255, 255, 255))
        # Posicionar cada linha abaixo do texto "Historical Score"
        line_height = 30  # Altura de cada linha de texto
        x_position = 80  # Posição x base para as linhas históricas
        y_position = 50 + i * line_height  # Posição y para a primeira linha histórica
        # Verificar se a posição y excede a altura da janela
        if y_position + line_height > HEIGHT:
            # Se exceder, alocar o texto em uma coluna ao lado
            x_position += 200  # Ajustar a posição x
            y_position = 50  + re_index * line_height  # Reiniciar a posição y para o topo
            re_index+=1
        
        win.blit(historical_text, (x_position, y_position))
    # Atualize a tela após desenhar todas as linhas
    pygame.display.update()


def end_screen(win,elapsed_time,targets_pressed,clicks):
    clock = pygame.time.Clock()
    win.fill(BG_COLOR)
    speed = round(targets_pressed / elapsed_time,1)
    time_label = LABEL_FONT.render(f"Time: {fomat_time(elapsed_time)}",1,"white")
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s",1,"white")
    tg_label = LABEL_FONT.render(f"Hits: {targets_pressed}",1,"white")
    try:
        accuracy = round(targets_pressed / clicks *100,1)
    except ZeroDivisionError:
        accuracy = 0
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%",1,"white")
    win.blit(time_label,(get_middle(time_label),100))
    win.blit(speed_label,(get_middle(speed_label),200))
    win.blit(tg_label,(get_middle(tg_label),300))
    win.blit(accuracy_label,(get_middle(accuracy_label),400))
    save_score(speed,targets_pressed,accuracy)
    
    historical_bottom = BottomHistorical(win,30,100)
    historical_bottom.draw_bottom()
     # Atualiza a tela
    pygame.display.update()

    # Loop do fim do jogo
    end_game = True
    while end_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Verifica se o botão foi clicado
                if historical_bottom.bottom_clicked(pygame.mouse.get_pos()):
                    print_historical(win)
                    pygame.display.update()
        clock.tick(15)  # Limita a taxa de atualização da tela

def get_middle(surface):
    return WIDTH / 2 -surface.get_width() / 2


def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    target_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT,TARGET_INCREMENT)
    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING,WIDTH-TARGET_PADDING)
                y = random.randint(TARGET_PADDING+TOP_BAR_HEIGHT,HEIGHT-TARGET_PADDING)
                target = Target(x,y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks+=1

        for target in targets:
            target.update()
            
            if target.size <=0:
                targets.remove(target)
                misses+=1
            
            if click and target.collide(*mouse_pos):
                targets.remove(target)
                target_pressed+=1

        if misses >= LIVES:
            end_screen(WIN,elapsed_time,target_pressed,clicks)
            pygame.display.update()

        draw(WIN,targets)
        draw_top_bar(WIN,elapsed_time,target_pressed,misses)
        pygame.display.update()

    pygame.quit()   

if __name__ == "__main__":
    main()
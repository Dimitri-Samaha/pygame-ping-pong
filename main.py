import pygame
import time
from game_mechanics import * 

class Button():
    def __init__(self, x : int, y : int, _image, _onclick, arguments : tuple, scale = (105, 95)):
        self.image = pygame.transform.scale(_image, scale) # change scale
        self.rect = self.image.get_rect() # create rect from image
        self.rect.topleft = (x, y) # coords of rect
        self.clicked = False
        self.action = _onclick
        self.arg = arguments

    def button_mechanics(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                if self.arg != None:                    
                    return self.action(self.arg)
                else:
                    return self.action()

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

    def draw(self, WINDOW):
        WINDOW.blit(self.image, (self.rect.x, self.rect.y)) # draw buttons
        return self.button_mechanics()


def create_landscape(WINDOW):
    # create and draw seperating line
    for i in range(0, int(HEIGHT/30)):
        line = pygame.Rect(WIDTH/2 -1, i*30, 2, 20)
        pygame.draw.rect(WINDOW, [255, 255, 255], line)

def button_press(int : int):
    return int


def main():
    players = "!"
    menu = True
    run = False
    end = False

    pygame.init() 
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT)) # create my window surface  
    pygame.display.set_caption("Ping Pong game")  # set window caption
    clock = pygame.time.Clock() # set clock depending on fps

    # Create buttons
    button_0 = Button(50, 250, pygame.image.load("images//button_0.JPG").convert_alpha(), button_press, (0))
    button_1 = Button(400, 250, pygame.image.load("images//button_1.JPG").convert_alpha(), button_press, (1))
    button_2 = Button(750, 250, pygame.image.load("images//button_2.JPG").convert_alpha(), button_press, (2))

    btn_list = [button_0, button_1, button_2]

    # Create menu loop
    while menu:
        WINDOW.fill([255, 255, 255])

        for b in btn_list:
            btn_ans = b.draw(WINDOW)
            if btn_ans != None:
                menu = False
                run = True
                players = str(btn_ans)

        # Create first text
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render("How many players want to play!", True, [0, 0, 255], [255, 255, 255])
        textRect = text.get_rect()
        textRect.center = (WIDTH//2, 100)    
        
        # Create second text
        font2 = pygame.font.Font('freesansbold.ttf', 16)
        text2 = font2.render('Controls: left player [W, S], right player [UP, DOWN]', True, [0, 0, 255], [255, 255, 255])
        textRect2 = text2.get_rect()
        textRect2.center = (WIDTH//2, 150)

        WINDOW.blit(text, textRect)
        WINDOW.blit(text2, textRect2)

        # Listen for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False

        pygame.display.update()
    

    # start game loop
    if run:
        start = False

        right_player = Player(1) # create player 1 from game_mechanics
        left_player = Player(0) # create player 0 from game_mechanics
        ball = Ball(right_player, left_player) # create ball from game_mechanics

        # Check if computer needed to be created from AI
        if players == "0":
            import AI
            right_computer = AI.Robot(right_player, ball)
            left_computer = AI.Robot(left_player, ball)
        elif players == "1":
            import AI
            right_computer = AI.Robot(right_player, ball)


        while run:
            clock.tick(FPS) # FPS

            # Draw everything
            WINDOW.fill([0, 0, 0]) # Black background
            create_landscape(WINDOW) # draw landscape
            right_player.draw(WINDOW) # draw player 1 from game_mechanics
            left_player.draw(WINDOW) # draw player 0 from game_mechanics         
            scored = ball.draw(WINDOW) # draw  ball from game_mechanics

            # CHeck if AI 
            if players == "0":
                right_computer.play()
                left_computer.play()
            elif players == "1":
                right_computer.play()

            # Check if scored
            if scored == True:
                run = False  
                end = True        
                message = "Lost, game ended! Want to play again?"  


            pygame.display.flip() # update the frames

            if not start:
                time.sleep(2)
                start = True

            # Listen for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    end = True
                    message = "Quit, game ended! Want to play again?"
                if event.type == pygame.KEYDOWN:
                    # Right
                    if players == "2":
                        if event.key == pygame.K_UP:
                            right_player.velocity = -VELOCITY
                        if event.key == pygame.K_DOWN:
                            right_player.velocity = VELOCITY
                    # Left
                    if players == "2" or players == "1":
                        if event.key == pygame.K_w:
                            left_player.velocity = -VELOCITY
                        if event.key == pygame.K_s:
                            left_player.velocity = VELOCITY
                if event.type == pygame.KEYUP:
                    # Right
                    if players == "2":
                        if event.key == pygame.K_UP:
                            right_player.velocity = 0
                        if event.key == pygame.K_DOWN:
                            right_player.velocity = 0
                    # Left
                    if players == "2" or players == "1":
                        if event.key == pygame.K_w:
                            left_player.velocity = 0
                        if event.key == pygame.K_s:
                            left_player.velocity = 0

        while end:
            try:
                WINDOW.fill([0, 0, 0])
            except:
                pass
            # Create text
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render(message , True, [0, 255, 0], [0, 0, 0])
            textRect = text.get_rect()
            textRect.center = (WIDTH//2, 100)
            
            btn_again = Button(250, HEIGHT-150, pygame.image.load("images/button_replay.JPG"), main, None, (350, 100))
            
            try:
                btn_again.draw(WINDOW)
                WINDOW.blit(text, textRect)                
            except:
                pass
            
            pygame.display.update()                                    

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = False
            

if __name__ == "__main__":
    main()    
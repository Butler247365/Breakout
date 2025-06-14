import pygame, random, simpleGE

class Paddle(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setSize(100, 20)
        self.colorRect((200, 200, 200), (100, 20))
        self.y = 450

    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= 10
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += 10
        self.left = max(self.left, 0)
        self.right = min(self.right, self.screenWidth)

class Ball(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setSize(20, 20)
        self.colorRect((240, 0, 20), (20, 20))
        self.x = random.randint(50, 590)
        self.y = 300
        self.dx = random.randint(2, 5)
        self.dy = -random.randint(2, 5)
        self.setBoundAction(self.BOUNCE)

    def process(self):
        self.x += self.dx
        self.y += self.dy

        if self.left <= 0 or self.right >= self.screenWidth:
            self.dx *= -1

        if self.top < 0:
            self.dy *= -1

        if self.bottom > self.screenHeight:
            print("Game Over!")
            elapsed = self.scene.timer.getElapsedTime()
            game_over = GameOverScene(last_time=elapsed)
            game_over.start()
            self.scene.stop()

        if self.collidesWith(self.scene.paddle):
            self.dy *= -1
            self.bottom = self.scene.paddle.top
            self.scene.paddleSound.play() 

        for block in self.scene.blocks:
            if self.collidesWith(block):
                self.dy *= -1
                block.hide()
                self.scene.blocks.remove(block)
                self.scene.hitSound.play()          

class Block(simpleGE.Sprite):
    def __init__(self, scene, x, y, color):
        super().__init__(scene)
        self.setSize(50, 20)
        self.colorRect(color, (50, 20))
        self.x = x
        self.y = y

class BreakoutGame(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.paddle = Paddle(self)
        
        self.ball = Ball(self)
        
        
        self.timer = simpleGE.Timer()
        self.timerLabel = simpleGE.Label()
        self.timerLabel.center = (540, 20)
        self.timerLabel.size = (180, 30)
        self.timerLabel.fgColor = (255, 255, 255)
        
        self.blocks = []

        self.hitSound = simpleGE.Sound("powerUp.wav")
        self.paddleSound = simpleGE.Sound("blipSelect.wav") 

        xStart = 40
        yStart = 50
        xGap = 15
        yGap = 10
        blockWidth = 50

        colors = [(255, 0, 0), 
                  (255, 128, 0), 
                  (255, 255, 0), 
                  (0, 255, 0), 
                  (0, 128, 255)]

        for row in range(5):
            for col in range(10):
                x = xStart + col * (blockWidth + xGap)
                y = yStart + row * (20 + yGap)
                color = colors[row % len(colors)]
                block = Block(self, x, y, color)
                self.blocks.append(block)

        self.sprites = [self.paddle, 
                        self.ball, 
                        self.timerLabel, 
                        self.blocks]

        self.timer.start()

    def process(self):
        self.timerLabel.text = f"Time: {self.timer.getElapsedTime():.1f}s"
        
        if not self.blocks:
            self.sceneResult = self.timer.getElapsedTime()
            GameOverScene(last_time=self.sceneResult, won=True).start()
            self.stop()

class MenuScene(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.titleLabel = simpleGE.Label()
        self.titleLabel.text = "Breakout Game"
        self.titleLabel.center = (320, 100)
        self.titleLabel.size = (300, 40)

        self.instructionLabel = simpleGE.MultiLabel()
        self.instructionLabel.textLines = [
            "Arrow keys to move paddle",
            "break all blocks to win",
            "don't let the ball fall"
        ]
        self.instructionLabel.center = (320, 200)
        self.instructionLabel.size = (400, 100)

        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play"
        self.btnPlay.center = (220, 350)

        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (420, 350)

        self.sprites = [self.titleLabel, 
                        self.instructionLabel, 
                        self.btnPlay, 
                        self.btnQuit]

    def process(self):
        if self.btnPlay.clicked:
            game = BreakoutGame()
            game.start()

        if self.btnQuit.clicked:
            self.stop()

class GameOverScene(simpleGE.Scene):
    def __init__(self, last_time=0.0, won=False):
        super().__init__()
        self.titleLabel = simpleGE.Label()
        self.titleLabel.text = "You Win!" if won else "Game Over, You Lose!"
        self.titleLabel.center = (320, 150)
        self.titleLabel.size = (300, 50)

        self.timeLabel = simpleGE.Label()
        self.timeLabel.text = f"Your time: {last_time:.2f} seconds"
        self.timeLabel.center = (320, 220)
        self.timeLabel.size = (300, 30)

        self.btnRestart = simpleGE.Button()
        self.btnRestart.text = "Restart"
        self.btnRestart.center = (220, 300)

        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (420, 300)

        self.sprites = [self.titleLabel,
                        self.timeLabel,
                        self.btnRestart,
                        self.btnQuit]

    def process(self):
        if self.btnRestart.clicked:
            game = BreakoutGame()
            game.start()

        if self.btnQuit.clicked:
            self.stop()

def main():
    menu = MenuScene()
    menu.start()

if __name__ == "__main__":
    main()

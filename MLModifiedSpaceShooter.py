# Modified from Space Shooter by Tyler Gray
# https://www.pygame.org/project-Space+Shooter-1292-.html
# tested
import os
import pygame
import random
from pygame.locals import *

FPS = 100
SCREENWIDTH  = 800
SCREENHEIGHT = 600

# os.environ['SDL_VIDEO_CENTERED'] = "1"
pygame.init()
FPSCLOCK = pygame.time.Clock()
pygame.display.set_caption("Space Shooter")
icon = pygame.image.load("game/Space Shooter.png")
icon = pygame.display.set_icon(icon)
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.mouse.set_visible(0)

# Background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))
GameNum = 0
file = open("scorelog.txt", "w", 1)
avg = 0

class GameState:
    def __init__(self):
        # Game Objects
        global player
        player = Player()
        global score
        score = Score()

        # Player/Enemy
        self.playerSprite = pygame.sprite.RenderPlain(player)

        global enemySprites
        enemySprites = pygame.sprite.RenderPlain(())
        enemySprites.add(Enemy(200))
        enemySprites.add(Enemy(300))
        enemySprites.add(Enemy(400))

        # Projectiles
        global laserSprites
        laserSprites = pygame.sprite.RenderPlain(())

        global bombSprites
        bombSprites = pygame.sprite.RenderPlain(())
        global enemyLaserSprites
        enemyLaserSprites = pygame.sprite.RenderPlain(())

        # Special FX
        # self.shieldSprites = pygame.sprite.RenderPlain(())

        # Score/and game over
        # self.scoreSprite = pygame.sprite.Group(score)


        # Set Clock
        self.keepGoing = True
        self.counter = 0

    def game_o(self):
        global GameNum
        global file
        global avg
        GameNum = GameNum + 1
        file.write(str(GameNum) + " " + str(score.score) + "\n")
        avg = avg + score.score
        if GameNum % 20 == 0:
            print(avg / 20)
            avg = 0
        self.__init__()


    def frame_step(self, input_actions):
        reward = 0
        terminal = False

        if sum(input_actions) != 1:
            raise ValueError('Multiple input actions!')

        screen.blit(background, (0, 0))

        if input_actions[0] == 1:  # Move Left
            player.dx = -10
        if input_actions[1] == 1:  # Move Right
            player.dx = 10
        if input_actions[2] == 1:  # Shoot
            self.playerSprite.update(True)
        else:
            self.playerSprite.update(False)

        # Update and draw on the screen

        # Update
        for enemy in enemySprites:
            reward += enemy.update()
        laserSprites.update()
        bombSprites.update()
        enemyLaserSprites.update()
       # self.shieldSprites.update()
       # self.scoreSprite.update()

        # Draw
        self.playerSprite.draw(screen)
        enemySprites.draw(screen)
        laserSprites.draw(screen)
        bombSprites.draw(screen)
        enemyLaserSprites.draw(screen)
        # self.scoreSprite.draw(screen)
        pygame.display.flip()

        # Spawn new enemies
        self.counter += 1
        if self.counter >= 20:
            enemySprites.add(Enemy(300))
            self.counter = 0

        # Check if enemy lasers hit player's ship
        for hit in pygame.sprite.groupcollide(enemyLaserSprites, self.playerSprite, 1, 0):
            # explosionSprites.add(Shield(player.rect.center))
            score.shield -= 10
            reward = -10
            if score.shield <= 0:
                self.game_o()
                terminal = True


        # Check if enemy collides with player
        for hit in pygame.sprite.groupcollide(enemySprites, self.playerSprite, 1, 0):
            score.shield -= 10
            reward = -10
            if score.shield <= 0:
                self.game_o()
                self.__init__()

        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        FPSCLOCK.tick(FPS)

        return image_data, reward, terminal


# Load Images
def load_image(name, colorkey=None):
    fullname = os.path.join('game/data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()



class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("sprites/player.png", -1)
        self.rect.center = (400, 500)
        self.dx = 0
        self.dy = 0
        self.reset()
        self.lasertimer = 0
        self.lasermax = 5
        # self.ammo = 100
        self.bombamount = 1
        self.bombtimer = 0
        self.bombmax = 10

    def update(self, fire):
        self.rect.move_ip((self.dx, self.dy))

        # Fire the laser
        if fire:
            self.lasertimer = self.lasertimer + 1
            if self.lasertimer == self.lasermax:  # self.ammo > 0:
                laserSprites.add(Laser(self.rect.midtop))
                # self.ammo = #self.ammo - 1
                self.lasertimer = 0

        # Player Boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800

        if self.rect.top <= 260:
            self.rect.top = 260
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600

    def reset(self):
        self.rect.bottom = 600


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("sprites/laser.png", -1)
        self.rect.center = pos

    def update(self):
        if self.rect.top < 0:
            self.kill()
        else:
            self.rect.move_ip(0, -15)


class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("sprites/elaser.png", -1)
        self.rect.center = pos

    def update(self):
        if self.rect.bottom < 0:
            self.kill()
        else:
            self.rect.move_ip(0, 15)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, centerx):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("sprites/enemy.png", -1)
        self.rect = self.image.get_rect()
        self.dy = 8
        self.reset()

    def update(self):
        reward = 0
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if self.rect.top > screen.get_height():
            self.reset()

        # random 1 - 60 determines if firing
        efire = random.randint(1, 60)
        if efire == 1:
            enemyLaserSprites.add(EnemyLaser(self.rect.midbottom))

        # Laser Collisions
        if pygame.sprite.groupcollide(enemySprites, laserSprites, 1, 1):
            # explosionSprites.add(EnemyExplosion(self.rect.center))
            score.score += 10
            reward = 1

        return reward

    def reset(self):
        self.rect.bottom = 0
        self.rect.centerx = random.randrange(0, screen.get_width())
        self.dy = random.randrange(5, 10)
        self.dx = random.randrange(-2, 2)


class Shield(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("sprites/shield.png", -1)
        self.rect.center = pos
        self.counter = 0
        self.maxcount = 2

    def update(self):
        self.counter = self.counter + 1
        if self.counter == self.maxcount:
            self.kill()


class EnemyExplosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("sprites/enemyexplosion.png", -1)
        self.rect.center = pos
        self.counter = 0
        self.maxcount = 10

    def update(self):
        self.counter = self.counter + 1
        if self.counter == self.maxcount:
            self.kill()


class ShieldPowerup(pygame.sprite.Sprite):
    def __init__(self, centerx):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("sprites/shieldpowerup.png", -1)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(0, screen.get_width())

    def update(self):
        if self.rect.top > screen.get_height():
            self.kill
        else:
            self.rect.move_ip(0, 6)


class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.shield = 100
        self.score = 0
        self.bomb = 1
        self.font = pygame.font.Font("game/data/fonts/arial.ttf", 28)

    def update(self):
        self.text = "Shield: %d                        Score: %d                        Torpedo: %d" % (
            self.shield, self.score, self.bomb)
        self.image = self.font.render(self.text, 1, (0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 20)


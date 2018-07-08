# Modified from Space Shooter by Tyler Gray
# https://www.pygame.org/project-Space+Shooter-1292-.html

# Import
import os, sys, pygame, random
from pygame.locals import *

os.environ['SDL_VIDEO_CENTERED'] = "1"
pygame.init()
pygame.display.set_caption("Space Shooter")
icon = pygame.image.load("game/Space Shooter.png")
icon = pygame.display.set_icon(icon)
screen = pygame.display.set_mode((800, 600))
pygame.mouse.set_visible(0)

# Background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))


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


# Sprites

# This class controls the arena background

class Arena(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("menu/arena.jpg", -1)
        self.dy = 5
        self.reset()

    def update(self):
        self.rect.bottom += self.dy
        if self.rect.bottom >= 1200:
            self.reset()

    def reset(self):
        self.rect.top = -600


# Player
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

    def update(self):
        self.rect.move_ip((self.dx, self.dy))

        # Fire the laser
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.lasertimer = self.lasertimer + 1
            if self.lasertimer == self.lasermax:  # self.ammo > 0:
                laserSprites.add(Laser(self.rect.midtop))
                # self.ammo = #self.ammo - 1
                self.lasertimer = 0

        # Fire the bomb
        if key[pygame.K_LCTRL]:
            self.bombtimer = self.bombtimer + 1
            if self.bombtimer == self.bombmax:
                self.bombtimer = 0
                if self.bombamount > 0:
                    self.bombamount = self.bombamount - 1
                    score.bomb += -1
                    bombSprites.add(Bomb(self.rect.midtop))

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

    # Laser class


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

        # Bomb class


class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("sprites/bomb.png", -1)
        self.rect.center = pos

    def update(self):
        if self.rect.top < 0:
            self.kill()
        else:
            self.rect.move_ip(0, -5)
        if pygame.sprite.groupcollide(enemySprites, bombSprites, 1, 1):
            bombExplosionSprites.add(BombExplosion(self.rect.center))


# Laser class
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

        # Enemy class


class Enemy(pygame.sprite.Sprite):
    def __init__(self, centerx):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("sprites/enemy.png", -1)
        self.rect = self.image.get_rect()
        self.dy = 8
        self.reset()

    def update(self):
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
            #explosionSprites.add(EnemyExplosion(self.rect.center))
            score.score += 10

        # Bomb Collisions
        if pygame.sprite.groupcollide(enemySprites, bombSprites, 1, 1):
            bombExplosionSprites.add(BombExplosion(self.rect.center))
            score.score += 10

        # Bomb Explosion Collisions
        if pygame.sprite.groupcollide(enemySprites, bombExplosionSprites, 1, 0):
            #explosionSprites.add(EnemyExplosion(self.rect.center))
            score.score += 10

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


class BombExplosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("sprites/bombexplosion.png", -1)
        self.rect.center = pos
        self.counter = 0
        self.maxcount = 5

    def update(self):
        self.counter = self.counter + 1
        if self.counter == self.maxcount:
            self.kill()


# Bomb Powerup
class BombPowerup(pygame.sprite.Sprite):
    def __init__(self, centerx):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("sprites/torpedopowerup.png", -1)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(0, screen.get_width())

    def update(self):
        if self.rect.top > screen.get_height():
            self.kill
        else:
            self.rect.move_ip(0, 6)

        # Shield Powerup


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


class Gameover(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font("game/data/fonts/planet5.ttf", 48)

    def update(self):
        self.text = ("GAME OVER")
        self.image = self.font.render(self.text, 1, (0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)


class Gameoveresc(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font("game/data/fonts/arial.ttf", 28)

    def update(self):
        self.text = "PRESS ESC TO RETURN"
        self.image = self.font.render(self.text, 1, (0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 400)


# Game Module
def game():
    # Game Objects
    global player
    player = Player()
    global score
    score = Score()

    # Game Groups

    # Player/Enemy
    playerSprite = pygame.sprite.RenderPlain((player))

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

    # Powerups
    global bombPowerups
    bombPowerups = pygame.sprite.RenderPlain(())
    global shieldPowerups
    shieldPowerups = pygame.sprite.RenderPlain(())

    # Special FX
    shieldSprites = pygame.sprite.RenderPlain(())

    global explosionSprites
    explosionSprites = pygame.sprite.RenderPlain(())

    global bombExplosionSprites
    bombExplosionSprites = pygame.sprite.RenderPlain(())

    # Score/and game over
    scoreSprite = pygame.sprite.Group(score)
    gameOverSprite = pygame.sprite.RenderPlain(())

    # Arena
    arena = Arena()
    arena = pygame.sprite.RenderPlain((arena))

    # Set Clock
    clock = pygame.time.Clock()
    keepGoing = True
    counter = 0

    # Main Loop
    while keepGoing:
        clock.tick(30)
        # input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                elif event.key == pygame.K_LEFT:
                    player.dx = -10
                elif event.key == K_RIGHT:
                    player.dx = 10
                #elif event.key == K_UP:
                #    player.dy = -10
                #elif event.key == K_DOWN:
                #    player.dy = 10
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    player.dx = 0
                elif event.key == K_RIGHT:
                    player.dx = 0
               # elif event.key == K_UP:
                #    player.dy = 0
                #elif event.key == K_DOWN:
                #    player.dy = 0

        # Update and draw on the screen

        # Update
        screen.blit(background, (0, 0))
        playerSprite.update()
        enemySprites.update()
        laserSprites.update()
        bombSprites.update()
        enemyLaserSprites.update()
        bombPowerups.update()
        shieldPowerups.update()
        shieldSprites.update()
        explosionSprites.update()
        bombExplosionSprites.update()
        arena.update()
        scoreSprite.update()
        gameOverSprite.update()

        # Draw
        arena.draw(screen)
        playerSprite.draw(screen)
        enemySprites.draw(screen)
        laserSprites.draw(screen)
        bombSprites.draw(screen)
        enemyLaserSprites.draw(screen)
        bombPowerups.draw(screen)
        shieldPowerups.draw(screen)
        shieldSprites.draw(screen)
        explosionSprites.draw(screen)
        bombExplosionSprites.draw(screen)
        scoreSprite.draw(screen)
        gameOverSprite.draw(screen)
        pygame.display.flip()

        # Spawn new enemies
        counter += 1
        if counter >= 20:
            enemySprites.add(Enemy(300))
            counter = 0

        # Spawn Shield Power up
        # shieldPowerupcounter += 1
        spawnShieldpowerup = random.randint(1, 500)
        if spawnShieldpowerup == 1:
            shieldPowerups.add(ShieldPowerup(300))

        # Spawn Bomb Power up
        spawnBombpowerup = random.randint(1, 500)
        if spawnBombpowerup == 1:
            bombPowerups.add(BombPowerup(300))
            bombPowerupcounter = 0

        # Check if enemy lasers hit player's ship
        for hit in pygame.sprite.groupcollide(enemyLaserSprites, playerSprite, 1, 0):
            explosionSprites.add(Shield(player.rect.center))
            score.shield -= 10
            if score.shield <= 0:
                gameOverSprite.add(Gameover())
                gameOverSprite.add(Gameoveresc())
                playerSprite.remove(player)

        # Check if enemy collides with player
        for hit in pygame.sprite.groupcollide(enemySprites, playerSprite, 1, 0):
            explosionSprites.add(Shield(player.rect.center))
            score.shield -= 10
            if score.shield <= 0:
                gameOverSprite.add(Gameover())
                gameOverSprite.add(Gameoveresc())
                playerSprite.remove(player)

        # Check if player collides with shield powerup
        for hit in pygame.sprite.groupcollide(shieldPowerups, playerSprite, 1, 0):
            if score.shield < 100:
                score.shield += 10

        # Check if player collides with bomb powerup
        for hit in pygame.sprite.groupcollide(bombPowerups, playerSprite, 1, 0):
            player.bombamount += 1
            score.bomb += 1


# Class Module




# Functions

# Main
def main():
    # Arena
    arena = Arena()
    arena = pygame.sprite.RenderPlain((arena))

    game()

    clock = pygame.time.Clock()
    keepGoing = True

    while 1:
        clock.tick(30)

        # Events
        events = pygame.event.get()



        # Quit Event
        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()
                return

        # Draw
        screen.blit(background, (0, 0))
        arena.update()
        arena.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()

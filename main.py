#!/user/bin/env python

import pygame
from game import *

try:
    import android
except ImportError:
    android = None


def main():
    pygame.init()
    if android:
        android.init()
        android.map_key(android.KEYCODE_BACK, pygame.K_r)
        android.map_key(android.KEYCODE_W, pygame.K_UP)
        android.map_key(android.KEYCODE_A, pygame.K_LEFT)
        android.map_key(android.KEYCODE_D, pygame.K_RIGHT)
        #android.mixer.pre_init(44100, 16, 2, 4096) ##i know this isnt correct
    else:
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.font.init()
    clock = pygame.time.Clock()

    game = Game(["server", "client"], levelFile, tilesetFile)
    #--- Main Loop
    while game.on:
        if android:
            if android.check_pause():
                android.wait_for_resume()
        game.tick()
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    if False:
        import cProfile
        cProfile.run('main()', sort='cumulative')
    else:
        main()

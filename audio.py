import pygame


def blow_up_sound():
    pygame.mixer.init()
    pygame.mixer.music.load('audio_files/explosion.mp3')
    pygame.mixer.music.play(loops=0)

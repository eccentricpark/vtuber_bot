import pygame


def play_sound(file):
    # pygame 라이브러리 초기화
    pygame.init()

    # 음악 파일 로드
    pygame.mixer.music.load(file)  # 실제 파일 경로로 교체해야 합니다.

    # 음악 재생
    pygame.mixer.music.play()

    # 음악이 재생될 동안 프로그램이 종료되지 않도록 대기
    while pygame.mixer.music.get_busy(): 
        pygame.time.Clock().tick(10)

    pygame.quit()

import pygame
import random
import sys

# Pygame 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("블럭깨기 게임")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# 시계 설정
clock = pygame.time.Clock()
FPS = 50

# 폰트 설정
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# 패들 클래스
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((300, 15))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

# 공 클래스
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x = 3
        self.speed_y = -3
        self.speed = 3
    
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # 좌우 벽 충돌
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x *= -1
        
        # 상단 벽 충돌
        if self.rect.top < 0:
            self.speed_y *= -1
        
        # 하단 벽 충돌 (게임 오버)
        if self.rect.bottom > SCREEN_HEIGHT:
            return False
        
        return True

# 블럭 클래스
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((75, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# 게임 상태 관리
class Game:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.score = 0
        self.lives = 3
        self.level = 1
        
        # 스프라이트 그룹 생성
        self.all_sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        
        # 패들과 공 생성
        self.paddle = Paddle()
        self.all_sprites.add(self.paddle)
        
        self.ball = Ball()
        self.all_sprites.add(self.ball)
        
        # 블럭 생성
        self.create_blocks()
    
    def create_blocks(self):
        colors = [RED, YELLOW, GREEN, CYAN, MAGENTA]
        self.blocks.empty()
        
        for row in range(3 + self.level):
            for col in range(10):
                x = col * 75 + 25
                y = row * 25 + 50
                color = colors[row % len(colors)]
                block = Block(x, y, color)
                self.all_sprites.add(block)
                self.blocks.add(block)
    
    def handle_collisions(self):
        # 패들과 공의 충돌
        if pygame.sprite.spritecollide(self.ball, [self.paddle], False):
            if self.ball.speed_y > 0:
                self.ball.speed_y *= -1
                self.ball.rect.bottom = self.paddle.rect.top
                # 패들의 어느 부분에 맞았는지에 따라 각도 조절
                paddle_center = self.paddle.rect.centerx
                ball_center = self.ball.rect.centerx
                offset = ball_center - paddle_center
                self.ball.speed_x = offset // 5
        
        # 블럭과 공의 충돌
        hit_blocks = pygame.sprite.spritecollide(self.ball, self.blocks, True)
        if hit_blocks:
            self.ball.speed_y *= -1
            self.score += len(hit_blocks) * 10
            
            # 모든 블럭이 깨졌는지 확인
            if len(self.blocks) == 0:
                self.level += 1
                self.create_blocks()
    
    def update(self):
        self.all_sprites.update()
        
        # 공이 화면을 벗어났는지 확인
        if not self.ball.update():
            self.lives -= 1
            if self.lives <= 0:
                return False  # 게임 오버
            else:
                # 공을 다시 시작 위치에
                self.ball.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                self.ball.speed_x = random.choice([-3, 3])
                self.ball.speed_y = -3
        
        self.handle_collisions()
        return True  # 계속 진행
    
    def draw(self):
        screen.fill(BLACK)
        self.all_sprites.draw(screen)
        
        # UI 정보 표시
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        lives_text = font.render(f"Lives: {self.lives}", True, WHITE)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - 200, 10))
        screen.blit(level_text, (SCREEN_WIDTH // 2 - 50, 10))
        
        # 남은 블럭 수
        blocks_left = small_font.render(f"Blocks: {len(self.blocks)}", True, WHITE)
        screen.blit(blocks_left, (10, SCREEN_HEIGHT - 30))
        
        pygame.display.flip()

# 메인 게임 루프
def main():
    game = Game()
    game_running = True
    game_over = False
    
    while game_running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = False
                if event.key == pygame.K_SPACE and game_over:
                    game = Game()
                    game_over = False
        
        if not game_over:
            if not game.update():
                game_over = True
            game.draw()
        else:
            # 게임 오버 화면
            screen.fill(BLACK)
            game_over_text = font.render("GAME OVER!", True, RED)
            final_score_text = font.render(f"Final Score: {game.score}", True, WHITE)
            final_level_text = font.render(f"Final Level: {game.level}", True, WHITE)
            restart_text = small_font.render("Press SPACE to restart or ESC to exit", True, WHITE)
            
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100))
            screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
            screen.blit(final_level_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 120))
            
            pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

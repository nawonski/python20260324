import pygame
import random
import math

# pygame 초기화
pygame.init()

# 상수 정의
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)

# 게임 상태
STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
STATE_WIN = 3


class Ball:
    """공 클래스"""
    def __init__(self, x, y, radius=5, speed=5):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.vx = speed * math.cos(math.radians(45))
        self.vy = -speed * math.sin(math.radians(45))
    
    def update(self):
        """공의 위치 업데이트"""
        self.x += self.vx
        self.y += self.vy
        
        # 벽 충돌 처리
        if self.x - self.radius <= 0 or self.x + self.radius >= SCREEN_WIDTH:
            self.vx *= -1
            self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))
        
        if self.y - self.radius <= 0:
            self.vy *= -1
            self.y = max(self.radius, self.y)
    
    def draw(self, screen):
        """공 그리기"""
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)
    
    def check_paddle_collision(self, paddle):
        """패들과의 충돌 감지"""
        if (self.y + self.radius >= paddle.y and 
            self.y - self.radius <= paddle.y + paddle.height and
            self.x >= paddle.x and 
            self.x <= paddle.x + paddle.width):
            
            # 공의 충돌 위치에 따라 각도 조정
            paddle_center = paddle.x + paddle.width / 2
            relative_pos = (self.x - paddle_center) / (paddle.width / 2)
            angle = relative_pos * 75  # -75도 ~ 75도 범위
            
            speed = math.hypot(self.vx, self.vy)
            self.vx = speed * math.sin(math.radians(angle))
            self.vy = -speed * math.cos(math.radians(angle))
            
            self.y = paddle.y - self.radius
            return True
        return False
    
    def check_block_collision(self, blocks):
        """블록과의 충돌 감지"""
        for block in blocks[:]:
            if block.check_collision(self):
                blocks.remove(block)
                
                # 공의 충돌 위치 계산
                dx = self.x - block.x
                dy = self.y - block.y
                
                # 블록의 가장 가까운 모서리까지의 거리
                if abs(dx) > abs(dy):
                    self.vx *= -1
                else:
                    self.vy *= -1
                
                return True
        return False
    
    def is_out_of_bounds(self):
        """공이 화면 아래로 벗어났는지 확인"""
        return self.y > SCREEN_HEIGHT


class Paddle:
    """패들(배) 클래스"""
    def __init__(self, x, y, width=160, height=15):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 6
    
    def update(self, keys):
        """패들 이동"""
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x + self.width < SCREEN_WIDTH:
            self.x += self.speed
    
    def draw(self, screen):
        """패들 그리기"""
        pygame.draw.rect(screen, CYAN, (self.x, self.y, self.width, self.height))


class Block:
    """블록 클래스"""
    def __init__(self, x, y, width=60, height=15, color=YELLOW):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    
    def draw(self, screen):
        """블록 그리기"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def check_collision(self, ball):
        """공과의 충돌 감지"""
        return (ball.x > self.x and 
                ball.x < self.x + self.width and
                ball.y > self.y - ball.radius and 
                ball.y < self.y + self.height + ball.radius)


class Game:
    """게임 메인 클래스"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("블록깨기 게임")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        
        self.state = STATE_MENU
        self.score = 0
        self.lives = 3
        
        self.init_game()
    
    def init_game(self):
        """게임 초기화"""
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.paddle = Paddle(SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT - 30)
        self.blocks = self.create_blocks()
        self.score = 0
        self.lives = 3
    
    def create_blocks(self):
        """블록 생성"""
        blocks = []
        colors = [RED, GREEN, BLUE, MAGENTA, YELLOW]
        block_width = 60
        block_height = 15
        padding = 10
        
        rows = 5
        cols = (SCREEN_WIDTH - padding) // (block_width + padding)
        
        for row in range(rows):
            for col in range(cols):
                x = col * (block_width + padding) + padding
                y = row * (block_height + padding) + 50
                color = colors[row % len(colors)]
                blocks.append(Block(x, y, block_width, block_height, color))
        
        return blocks
    
    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.state == STATE_MENU:
                        self.state = STATE_PLAYING
                    elif self.state == STATE_GAME_OVER or self.state == STATE_WIN:
                        self.init_game()
                        self.state = STATE_PLAYING
        
        return True
    
    def update(self):
        """게임 상태 업데이트"""
        if self.state != STATE_PLAYING:
            return
        
        keys = pygame.key.get_pressed()
        self.paddle.update(keys)
        self.ball.update()
        
        # 패들과의 충돌
        self.ball.check_paddle_collision(self.paddle)
        
        # 블록과의 충돌
        if self.ball.check_block_collision(self.blocks):
            self.score += 10
        
        # 공이 화면 아래로 벗어남
        if self.ball.is_out_of_bounds():
            self.lives -= 1
            if self.lives <= 0:
                self.state = STATE_GAME_OVER
            else:
                self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        
        # 모든 블록 제거됨
        if len(self.blocks) == 0:
            self.state = STATE_WIN
    
    def draw(self):
        """게임 화면 그리기"""
        self.screen.fill(BLACK)
        
        if self.state == STATE_MENU:
            self.draw_menu()
        elif self.state == STATE_PLAYING:
            self.draw_game()
        elif self.state == STATE_GAME_OVER:
            self.draw_game_over()
        elif self.state == STATE_WIN:
            self.draw_win()
        
        pygame.display.flip()
    
    def draw_menu(self):
        """메뉴 화면"""
        self.font = pygame.font.SysFont("malgungothic", 30)  # 윈도우: 맑은 고딕
        title = self.large_font.render("BLOCK BREAKER", True, CYAN)
        subtitle = self.font.render("SPACE 키를 눌러 게임 시작", True, WHITE)
        
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        
        self.screen.blit(title, title_rect)
        self.screen.blit(subtitle, subtitle_rect)
    
    def draw_game(self):
        """게임 화면"""
        # UI 그리기
        score_text = self.font.render(f"점수: {self.score}", True, WHITE)
        lives_text = self.font.render(f"생명: {self.lives}", True, WHITE)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (SCREEN_WIDTH - 200, 10))
        
        # 게임 객체 그리기
        self.ball.draw(self.screen)
        self.paddle.draw(self.screen)
        
        for block in self.blocks:
            block.draw(self.screen)
    
    def draw_game_over(self):
        """게임 오버 화면"""
        self.font = pygame.font.SysFont("malgungothic", 30)  # 윈도우: 맑은 고딕
        game_over = self.large_font.render("GAME OVER", True, RED)
        score_text = self.font.render(f"최종 점수: {self.score}", True, WHITE)
        restart_text = self.font.render("SPACE 키를 눌러 다시 시작", True, WHITE)
        
        game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        
        self.screen.blit(game_over, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
    
    def draw_win(self):
        """게임 승리 화면"""
        self.font = pygame.font.SysFont("malgungothic", 30)  # 윈도우: 맑은 고딕
        win = self.large_font.render("YOU WIN!", True, GREEN)
        score_text = self.font.render(f"최종 점수: {self.score}", True, WHITE)
        restart_text = self.font.render("SPACE 키를 눌러 다시 시작", True, WHITE)
        
        win_rect = win.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        
        self.screen.blit(win, win_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        """게임 메인 루프"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()

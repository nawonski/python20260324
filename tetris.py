"""
파이썬 테트리스 게임
Pygame을 사용하여 구현된 완전한 기능의 테트리스
"""

import pygame
import random
import sys
from enum import Enum
from typing import List, Tuple

# ============================================================================
# 상수 및 설정
# ============================================================================

# 화면 설정
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# 게임판 설정
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30

# 게임판 위치 (화면 상 위치)
BOARD_X = 50
BOARD_Y = 50
BOARD_WIDTH = GRID_WIDTH * CELL_SIZE
BOARD_HEIGHT = GRID_HEIGHT * CELL_SIZE

# 다음 블록 프리뷰 영역
PREVIEW_X = BOARD_X + BOARD_WIDTH + 50
PREVIEW_Y = BOARD_Y

# 정보 표시 영역
INFO_X = PREVIEW_X
INFO_Y = PREVIEW_Y + 150

# 색상
class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (50, 50, 50)
    LIGHT_GRAY = (200, 200, 200)
    RED = (255, 0, 0)
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    PURPLE = (128, 0, 128)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)
    PINK = (255, 192, 203)

# 테트로미노 색상 매핑
TETROMINO_COLORS = {
    'I': Color.CYAN,
    'O': Color.YELLOW,
    'T': Color.PURPLE,
    'S': Color.GREEN,
    'Z': Color.RED,
    'J': Color.BLUE,
    'L': Color.ORANGE,
}

# 테트로미노 모양 정의 (회전 포함)
# 각 블록은 (상대 좌표들의 리스트) 형태로 정의
TETROMINO_SHAPES = {
    'I': [
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(0, 0), (0, 1), (0, 2), (0, 3)],
    ],
    'O': [
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (0, 1), (1, 1)],
    ],
    'T': [
        [(0, 0), (1, 0), (2, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 1), (0, 2)],
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (0, 1), (1, 1), (1, 2)],
    ],
    'S': [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(0, 0), (0, 1), (1, 1), (1, 2)],
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(0, 0), (0, 1), (1, 1), (1, 2)],
    ],
    'Z': [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(1, 0), (0, 1), (1, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(1, 0), (0, 1), (1, 1), (0, 2)],
    ],
    'J': [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 0)],
        [(1, 0), (1, 1), (0, 2), (1, 2)],
    ],
    'L': [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
    ],
}


# ============================================================================
# 게임 상태 열거형
# ============================================================================

class GameState(Enum):
    RUNNING = 1
    PAUSED = 2
    GAME_OVER = 3


# ============================================================================
# 테트로미노 블록 클래스
# ============================================================================

class Block:
    """게임판에 떨어지는 테트로미노 블록"""
    
    def __init__(self, block_type: str):
        self.block_type = block_type
        self.rotation = 0
        self.x = GRID_WIDTH // 2 - 2  # 중앙에서 시작
        self.y = 0
        self.color = TETROMINO_COLORS[block_type]
    
    def get_cells(self) -> List[Tuple[int, int]]:
        """현재 회전 상태에서 블록이 차지하는 상대 좌표 반환"""
        return TETROMINO_SHAPES[self.block_type][self.rotation]
    
    def get_absolute_cells(self) -> List[Tuple[int, int]]:
        """절대 좌표로 변환하여 반환"""
        cells = self.get_cells()
        return [(self.x + cx, self.y + cy) for cx, cy in cells]
    
    def rotate(self):
        """블록을 시계방향으로 회전"""
        self.rotation = (self.rotation + 1) % 4
    
    def move_left(self):
        """블록을 왼쪽으로 이동"""
        self.x -= 1
    
    def move_right(self):
        """블록을 오른쪽으로 이동"""
        self.x += 1
    
    def move_down(self):
        """블록을 아래로 이동"""
        self.y += 1
    
    def copy(self):
        """블록의 복사본 반환"""
        new_block = Block(self.block_type)
        new_block.rotation = self.rotation
        new_block.x = self.x
        new_block.y = self.y
        return new_block


# ============================================================================
# 게임판 클래스
# ============================================================================

class Board:
    """테트리스 게임판"""
    
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.color_grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    
    def is_valid_position(self, block: Block) -> bool:
        """블록이 유효한 위치에 있는지 확인"""
        for x, y in block.get_absolute_cells():
            if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
                return False
            if y >= 0 and self.grid[y][x] != 0:
                return False
        return True
    
    def place_block(self, block: Block) -> bool:
        """블록을 게임판에 배치"""
        if not self.is_valid_position(block):
            return False
        
        for x, y in block.get_absolute_cells():
            if y >= 0:
                self.grid[y][x] = 1
                self.color_grid[y][x] = block.color
        
        return True
    
    def clear_lines(self) -> int:
        """완성된 행을 제거하고 제거된 행 수 반환"""
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        
        while y >= 0:
            if all(self.grid[y]):
                # 행이 완성됨
                del self.grid[y]
                del self.color_grid[y]
                self.grid.insert(0, [0] * GRID_WIDTH)
                self.color_grid.insert(0, [None] * GRID_WIDTH)
                lines_cleared += 1
            else:
                y -= 1
        
        return lines_cleared
    
    def is_game_over(self) -> bool:
        """게임 오버 확인 (맨 위 행에 블록이 있는지)"""
        return any(self.grid[0])
    
    def reset(self):
        """게임판 초기화"""
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.color_grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


# ============================================================================
# 게임 클래스
# ============================================================================

class Game:
    """테트리스 게임 메인 클래스"""
    
    def __init__(self):
        self.board = Board()
        self.current_block = self.spawn_block()
        self.next_block = self.spawn_block()
        self.state = GameState.RUNNING
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_speed = 30  # 프레임 수
        self.fall_counter = 0
        self.combo = 0
    
    def spawn_block(self) -> Block:
        """새로운 블록 생성"""
        block_types = list(TETROMINO_SHAPES.keys())
        return Block(random.choice(block_types))
    
    def update(self):
        """게임 상태 업데이트"""
        if self.state != GameState.RUNNING:
            return
        
        # 블록 낙하
        self.fall_counter += 1
        if self.fall_counter >= self.fall_speed:
            self.fall_counter = 0
            self.current_block.move_down()
            
            # 충돌 확인
            if not self.board.is_valid_position(self.current_block):
                self.current_block.move_down.__self__.y -= 1  # 한 칸 위로
                
                # 블록 배치
                if not self.board.place_block(self.current_block):
                    self.state = GameState.GAME_OVER
                    return
                
                # 새 블록 생성
                self.current_block = self.next_block
                self.next_block = self.spawn_block()
                
                # 라인 제거 및 점수 계산
                lines = self.board.clear_lines()
                if lines > 0:
                    # 점수 계산: 같은 턴에 여러 줄 제거 시 보너스
                    line_scores = {1: 100, 2: 300, 3: 500, 4: 800}
                    self.score += line_scores.get(lines, 800)
                    self.lines_cleared += lines
                    
                    # 레벨 업
                    new_level = self.lines_cleared // 10 + 1
                    if new_level > self.level:
                        self.level = new_level
                        self.fall_speed = max(5, 30 - (self.level - 1) * 2)
                
                # 게임 오버 확인
                if self.board.is_game_over():
                    self.state = GameState.GAME_OVER
    
    def move_left(self):
        """블록을 왼쪽으로 이동"""
        if self.state != GameState.RUNNING:
            return
        self.current_block.move_left()
        if not self.board.is_valid_position(self.current_block):
            self.current_block.move_right()
    
    def move_right(self):
        """블록을 오른쪽으로 이동"""
        if self.state != GameState.RUNNING:
            return
        self.current_block.move_right()
        if not self.board.is_valid_position(self.current_block):
            self.current_block.move_left()
    
    def rotate(self):
        """블록을 회전"""
        if self.state != GameState.RUNNING:
            return
        block_copy = self.current_block.copy()
        block_copy.rotate()
        if self.board.is_valid_position(block_copy):
            self.current_block.rotate()
    
    def hard_drop(self):
        """블록을 빠르게 낙하"""
        if self.state != GameState.RUNNING:
            return
        while self.board.is_valid_position(self.current_block):
            self.current_block.move_down()
        self.current_block.y -= 1
        self.fall_counter = 0
    
    def toggle_pause(self):
        """일시정지/재개"""
        if self.state == GameState.RUNNING:
            self.state = GameState.PAUSED
        elif self.state == GameState.PAUSED:
            self.state = GameState.RUNNING
    
    def reset(self):
        """게임 초기화"""
        self.board.reset()
        self.current_block = self.spawn_block()
        self.next_block = self.spawn_block()
        self.state = GameState.RUNNING
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_speed = 30


# ============================================================================
# 렌더러 클래스
# ============================================================================

class Renderer:
    """게임 화면 렌더링"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
    
    def draw(self, game: Game):
        """전체 게임 화면 그리기"""
        self.screen.fill(Color.BLACK)
        
        self.draw_board(game.board)
        self.draw_current_block(game.current_block, game.board)
        self.draw_preview(game.next_block)
        self.draw_info(game)
        
        self.draw_border()
        
        # 게임 상태 표시
        if game.state == GameState.PAUSED:
            self.draw_paused()
        elif game.state == GameState.GAME_OVER:
            self.draw_game_over(game)
        
        pygame.display.flip()
    
    def draw_board(self, board: Board):
        """게임판 그리기"""
        # 배경
        pygame.draw.rect(self.screen, Color.GRAY,
                        (BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT))
        
        # 배치된 블록들
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if board.grid[y][x] != 0:
                    self.draw_cell(x, y, board.color_grid[y][x])
        
        # 격자선
        for x in range(GRID_WIDTH + 1):
            pygame.draw.line(self.screen, Color.LIGHT_GRAY,
                           (BOARD_X + x * CELL_SIZE, BOARD_Y),
                           (BOARD_X + x * CELL_SIZE, BOARD_Y + BOARD_HEIGHT))
        for y in range(GRID_HEIGHT + 1):
            pygame.draw.line(self.screen, Color.LIGHT_GRAY,
                           (BOARD_X, BOARD_Y + y * CELL_SIZE),
                           (BOARD_X + BOARD_WIDTH, BOARD_Y + y * CELL_SIZE))
    
    def draw_current_block(self, block: Block, board: Board):
        """현재 낙하 중인 블록 그리기"""
        for x, y in block.get_absolute_cells():
            if y >= 0:
                self.draw_cell(x, y, block.color)
    
    def draw_cell(self, grid_x: int, grid_y: int, color):
        """격자 셀 하나 그리기"""
        screen_x = BOARD_X + grid_x * CELL_SIZE
        screen_y = BOARD_Y + grid_y * CELL_SIZE
        pygame.draw.rect(self.screen, color,
                        (screen_x + 1, screen_y + 1, CELL_SIZE - 2, CELL_SIZE - 2))
    
    def draw_preview(self, block: Block):
        """다음 블록 미리보기 그리기"""
        # 제목
        title_text = self.font_medium.render("NEXT", True, Color.WHITE)
        self.screen.blit(title_text, (PREVIEW_X, PREVIEW_Y))
        
        # 프리뷰 영역 배경
        pygame.draw.rect(self.screen, Color.GRAY,
                        (PREVIEW_X, PREVIEW_Y + 40, 120, 100), 2)
        
        # 블록 그리기 (작은 크기)
        preview_cell_size = 20
        for cx, cy in block.get_cells():
            px = PREVIEW_X + 30 + cx * preview_cell_size
            py = PREVIEW_Y + 60 + cy * preview_cell_size
            pygame.draw.rect(self.screen, block.color,
                           (px, py, preview_cell_size - 1, preview_cell_size - 1))
    
    def draw_info(self, game: Game):
        """게임 정보 표시"""
        y_offset = INFO_Y
        
        # 점수
        score_text = self.font_small.render(f"Score: {game.score}", True, Color.WHITE)
        self.screen.blit(score_text, (INFO_X, y_offset))
        y_offset += 40
        
        # 레벨
        level_text = self.font_small.render(f"Level: {game.level}", True, Color.WHITE)
        self.screen.blit(level_text, (INFO_X, y_offset))
        y_offset += 40
        
        # 라인
        lines_text = self.font_small.render(f"Lines: {game.lines_cleared}", True, Color.WHITE)
        self.screen.blit(lines_text, (INFO_X, y_offset))
        y_offset += 60
        
        # 조작법
        controls = [
            "← → : 좌우이동",
            "↑ : 회전",
            "↓ : 빠른낙하",
            "P : 일시정지",
            "R : 재시작"
        ]
        for control in controls:
            control_text = self.font_small.render(control, True, Color.LIGHT_GRAY)
            self.screen.blit(control_text, (INFO_X, y_offset))
            y_offset += 30
    
    def draw_border(self):
        """게임판 테두리 그리기"""
        pygame.draw.rect(self.screen, Color.WHITE,
                        (BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT), 3)
    
    def draw_paused(self):
        """일시정지 표시"""
        paused_text = self.font_large.render("PAUSED", True, Color.WHITE)
        text_rect = paused_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        
        # 반투명 배경
        pygame.draw.rect(self.screen, (0, 0, 0, 128), text_rect.inflate(40, 40))
        self.screen.blit(paused_text, text_rect)
    
    def draw_game_over(self, game: Game):
        """게임 오버 표시"""
        game_over_text = self.font_large.render("GAME OVER", True, Color.RED)
        final_score_text = self.font_medium.render(f"Final Score: {game.score}", True, Color.WHITE)
        restart_text = self.font_small.render("Press R to Restart or Q to Quit", True, Color.LIGHT_GRAY)
        
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
        
        # 반투명 배경
        popup_rect = game_over_rect.union(final_score_rect).union(restart_rect).inflate(40, 40)
        s = pygame.Surface((popup_rect.width, popup_rect.height))
        s.set_alpha(200)
        s.fill(Color.BLACK)
        self.screen.blit(s, popup_rect)
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(final_score_text, final_score_rect)
        self.screen.blit(restart_text, restart_rect)


# ============================================================================
# 메인 게임 루프
# ============================================================================

def main():
    """게임 메인 함수"""
    pygame.init()
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris - Python Edition")
    clock = pygame.time.Clock()
    
    game = Game()
    renderer = Renderer(screen)
    
    running = True
    while running:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_left()
                elif event.key == pygame.K_RIGHT:
                    game.move_right()
                elif event.key == pygame.K_UP:
                    game.rotate()
                elif event.key == pygame.K_DOWN:
                    game.hard_drop()
                elif event.key == pygame.K_p:
                    game.toggle_pause()
                elif event.key == pygame.K_r:
                    game.reset()
                elif event.key == pygame.K_q:
                    running = False
        
        # 게임 업데이트
        game.update()
        
        # 렌더링
        renderer.draw(game)
        
        # FPS 제어
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

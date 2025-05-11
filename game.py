import pygame
import random
import time
import math

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 800
GRID_SIZE = 6
CARD_SPACING = 10  # Added spacing between cards
CARD_SIZE = (WIDTH - (GRID_SIZE + 1) * CARD_SPACING) // GRID_SIZE  # Adjusted for spacing
FONT = pygame.font.Font(None, 60)
SMALL_FONT = pygame.font.Font(None, 36)
TITLE_FONT = pygame.font.Font(None, 72)
MENU_FONT = pygame.font.Font(None, 48)
BG_COLOR = (30, 30, 30)
CARD_COLOR = (200, 200, 200)
CARD_BACK_COLOR = (100, 149, 237)  # Cornflower blue
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (80, 120, 200)
BUTTON_HOVER_COLOR = (100, 140, 220)
SCORE_PANEL_HEIGHT = 50
WINDOW_HEIGHT = HEIGHT + SCORE_PANEL_HEIGHT

# Animation Constants
FLIP_SPEED = 10
MATCH_FADE_SPEED = 5
ANIMATION_DELAY = 30

# Create Game Window
screen = pygame.display.set_mode((WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Memory Match Game - 3 Card Matching")

# Game States
STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2

# Game Modes
MODE_VS_AI = 0
MODE_VS_PLAYER = 1

# Card animation states
CARD_STATE_HIDDEN = 0
CARD_STATE_FLIPPING_UP = 1
CARD_STATE_REVEALED = 2
CARD_STATE_FLIPPING_DOWN = 3
CARD_STATE_MATCHED_FADING = 4
CARD_STATE_MATCHED = 5

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False
        
    def draw(self, surface):
        color = BUTTON_HOVER_COLOR if self.is_hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 3, border_radius=10)
        
        text = MENU_FONT.render(self.text, True, TEXT_COLOR)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Card:
    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.state = CARD_STATE_HIDDEN
        self.flip_progress = 0  # 0 to 100
        self.fade_progress = 0  # 0 to 100
        
    def update_animation(self):
        # Update flipping animation
        if self.state == CARD_STATE_FLIPPING_UP:
            self.flip_progress += FLIP_SPEED
            if self.flip_progress >= 100:
                self.flip_progress = 100
                self.state = CARD_STATE_REVEALED
        elif self.state == CARD_STATE_FLIPPING_DOWN:
            self.flip_progress -= FLIP_SPEED
            if self.flip_progress <= 0:
                self.flip_progress = 0
                self.state = CARD_STATE_HIDDEN
        elif self.state == CARD_STATE_MATCHED_FADING:
            self.fade_progress += MATCH_FADE_SPEED
            if self.fade_progress >= 100:
                self.fade_progress = 100
                self.state = CARD_STATE_MATCHED
                
    def draw(self, surface):
        # Calculate position with spacing
        x = CARD_SPACING + self.col * (CARD_SIZE + CARD_SPACING)
        y = CARD_SPACING + self.row * (CARD_SIZE + CARD_SPACING)
        
        if self.state == CARD_STATE_HIDDEN:
            # Draw card back
            pygame.draw.rect(surface, CARD_BACK_COLOR, (x, y, CARD_SIZE, CARD_SIZE))
            pygame.draw.rect(surface, (0, 0, 0), (x, y, CARD_SIZE, CARD_SIZE), 3)
            
        elif self.state == CARD_STATE_REVEALED:
            # Draw card front
            pygame.draw.rect(surface, CARD_COLOR, (x, y, CARD_SIZE, CARD_SIZE))
            text = FONT.render(str(self.value), True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + CARD_SIZE//2, y + CARD_SIZE//2))
            surface.blit(text, text_rect)
            
        elif self.state == CARD_STATE_FLIPPING_UP or self.state == CARD_STATE_FLIPPING_DOWN:
            # Calculate width for flip animation
            flip_ratio = abs(50 - self.flip_progress) / 50
            width = max(1, int(CARD_SIZE * flip_ratio))
            
            # Draw card with animation
            card_x = x + (CARD_SIZE - width) // 2
            
            if self.flip_progress < 50:  # First half of flip (showing back)
                pygame.draw.rect(surface, CARD_BACK_COLOR, (card_x, y, width, CARD_SIZE))
            else:  # Second half of flip (showing front)
                pygame.draw.rect(surface, CARD_COLOR, (card_x, y, width, CARD_SIZE))
                if width > CARD_SIZE // 2:  # Only show text when card is wide enough
                    text = FONT.render(str(self.value), True, (0, 0, 0))
                    text_rect = text.get_rect(center=(x + CARD_SIZE//2, y + CARD_SIZE//2))
                    surface.blit(text, text_rect)
            
            # Draw border
            pygame.draw.rect(surface, (0, 0, 0), (card_x, y, width, CARD_SIZE), 3)
            
        elif self.state == CARD_STATE_MATCHED_FADING:
            # Draw fading card
            alpha = int(255 * (100 - self.fade_progress) / 100)
            card_surface = pygame.Surface((CARD_SIZE, CARD_SIZE), pygame.SRCALPHA)
            card_surface.fill((CARD_COLOR[0], CARD_COLOR[1], CARD_COLOR[2], alpha))
            surface.blit(card_surface, (x, y))
            
            # Draw fading text
            text = FONT.render(str(self.value), True, (0, 0, 0, alpha))
            text_rect = text.get_rect(center=(x + CARD_SIZE//2, y + CARD_SIZE//2))
            surface.blit(text, text_rect)
        
        # Matched cards are invisible - no drawing needed
            
    def is_animating(self):
        return self.state in [CARD_STATE_FLIPPING_UP, CARD_STATE_FLIPPING_DOWN, CARD_STATE_MATCHED_FADING]
    
    def is_revealed(self):
        return self.state in [CARD_STATE_REVEALED, CARD_STATE_FLIPPING_UP, CARD_STATE_FLIPPING_DOWN]
    
    def is_matched(self):
        return self.state in [CARD_STATE_MATCHED, CARD_STATE_MATCHED_FADING]
    
    def flip_up(self):
        if self.state == CARD_STATE_HIDDEN:
            self.state = CARD_STATE_FLIPPING_UP
            self.flip_progress = 0
            
    def flip_down(self):
        if self.state == CARD_STATE_REVEALED:
            self.state = CARD_STATE_FLIPPING_DOWN
            self.flip_progress = 100
            
    def set_matched(self):
        if self.state == CARD_STATE_REVEALED:
            self.state = CARD_STATE_MATCHED_FADING
            self.fade_progress = 0

# Set up the game state
def setup_game():
    # Generate Cards (Triplets of Numbers)
    # For a 6x6 grid with 3 matching cards, we need 12 unique values, each repeated 3 times
    card_values = list(range(1, (GRID_SIZE**2 // 3) + 1)) * 3
    random.shuffle(card_values)
    
    # Create Cards
    cards = []
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            index = i * GRID_SIZE + j
            cards.append(Card(card_values[index], i, j))
    
    # For the AI
    ai_memory = {}  # Will store {card_value: [card_obj, ...]}
    
    # Scores
    player1_score = 0
    player2_score = 0
    
    return cards, ai_memory, player1_score, player2_score

def draw_start_menu():
    """Draw the start menu with game mode options"""
    screen.fill(BG_COLOR)
    
    # Title
    title_text = TITLE_FONT.render("Memory Match Game", True, TEXT_COLOR)
    title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(title_text, title_rect)
    
    # Create buttons
    vs_ai_button = Button(WIDTH//2 - 150, HEIGHT//2 - 50, 300, 80, "Play vs AI")
    vs_player_button = Button(WIDTH//2 - 150, HEIGHT//2 + 50, 300, 80, "Play vs Friend")
    
    # Draw buttons
    vs_ai_button.draw(screen)
    vs_player_button.draw(screen)
    
    pygame.display.flip()
    
    return vs_ai_button, vs_player_button

def draw_board(cards, player1_score, player2_score, current_player, game_mode):
    """Draws the current state of the game board with scores."""
    # Clear the screen
    screen.fill(BG_COLOR)
    
    # Draw all cards
    for card in cards:
        card.draw(screen)
    
    # Draw score panel
    pygame.draw.rect(screen, (50, 50, 50), (0, HEIGHT, WIDTH, SCORE_PANEL_HEIGHT))
    
    # Draw scores based on game mode
    if game_mode == MODE_VS_AI:
        player_text = SMALL_FONT.render(f"Player: {player1_score}", True, TEXT_COLOR)
        ai_text = SMALL_FONT.render(f"AI: {player2_score}", True, TEXT_COLOR)
        screen.blit(player_text, (20, HEIGHT + 15))
        screen.blit(ai_text, (WIDTH - 20 - ai_text.get_width(), HEIGHT + 15))
        
        # Draw turn indicator
        turn_text = SMALL_FONT.render("Player's Turn" if current_player == 1 else "AI's Turn", True, TEXT_COLOR)
    else:  # VS_PLAYER mode
        player1_text = SMALL_FONT.render(f"Player 1: {player1_score}", True, TEXT_COLOR)
        player2_text = SMALL_FONT.render(f"Player 2: {player2_score}", True, TEXT_COLOR)
        screen.blit(player1_text, (20, HEIGHT + 15))
        screen.blit(player2_text, (WIDTH - 20 - player2_text.get_width(), HEIGHT + 15))
        
        # Draw turn indicator
        turn_text = SMALL_FONT.render(f"Player {current_player}'s Turn", True, TEXT_COLOR)
    
    turn_rect = turn_text.get_rect(center=(WIDTH//2, HEIGHT + 25))
    screen.blit(turn_text, turn_rect)
    
    pygame.display.flip()

def get_card_at_position(cards, position):
    """Get card at the given position."""
    x, y = position
    
    for card in cards:
        # Calculate card position with spacing
        card_x = CARD_SPACING + card.col * (CARD_SIZE + CARD_SPACING)
        card_y = CARD_SPACING + card.row * (CARD_SIZE + CARD_SPACING)
        
        # Check if position is within card bounds
        if (card_x <= x <= card_x + CARD_SIZE and 
            card_y <= y <= card_y + CARD_SIZE):
            return card
            
    return None

def get_revealed_cards(cards):
    """Get list of currently revealed cards."""
    return [card for card in cards if card.is_revealed() and not card.is_matched()]

def animate_cards(cards):
    """Update card animations and return True if any card is animating."""
    animating = False
    for card in cards:
        if card.is_animating():
            card.update_animation()
            animating = True
    return animating

def wait_for_animations(cards, player1_score, player2_score, current_player, game_mode):
    """Wait until all card animations are complete."""
    while animate_cards(cards):
        draw_board(cards, player1_score, player2_score, current_player, game_mode)
        pygame.time.delay(ANIMATION_DELAY)
        
        # Keep processing events to allow quitting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def player_turn_handler(cards, ai_memory, game_mode):
    """Handle player's turn with fancy animations."""
    revealed_cards = get_revealed_cards(cards)
    
    # Wait for player to select cards
    while len(revealed_cards) < 3:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Only check board area, not score panel
                if event.pos[1] < HEIGHT:
                    clicked_card = get_card_at_position(cards, event.pos)
                    if clicked_card and not clicked_card.is_revealed() and not clicked_card.is_matched():
                        clicked_card.flip_up()
                        
                        # Remember card for AI (if in AI mode)
                        if game_mode == MODE_VS_AI:
                            if clicked_card.value not in ai_memory:
                                ai_memory[clicked_card.value] = []
                            if clicked_card not in ai_memory[clicked_card.value]:
                                ai_memory[clicked_card.value].append(clicked_card)
        
        # Update animations
        animate_cards(cards)
        draw_board(cards, player1_score, player2_score, current_player, game_mode)
        pygame.time.delay(ANIMATION_DELAY)
        
        # Update revealed cards
        revealed_cards = get_revealed_cards(cards)
        
        # If we have 3 revealed cards and they're done animating, we're done
        if len(revealed_cards) >= 3:
            wait_for_animations(cards, player1_score, player2_score, current_player, game_mode)
            break
    
    # Check for match
    if len(revealed_cards) >= 3:
        card1, card2, card3 = revealed_cards[0], revealed_cards[1], revealed_cards[2]
        
        if card1.value == card2.value == card3.value:
            # We have a match
            card1.set_matched()
            card2.set_matched()
            card3.set_matched()
            wait_for_animations(cards, player1_score, player2_score, current_player, game_mode)
            
            # Remove from AI memory if in AI mode
            if game_mode == MODE_VS_AI and card1.value in ai_memory:
                ai_memory.pop(card1.value)
                
            return True, 1  # Player gets another turn and 1 point
        else:
            # No match, hide cards after delay
            pygame.time.delay(1000)  # Wait a second before flipping back
            for card in revealed_cards:
                card.flip_down()
            wait_for_animations(cards, player1_score, player2_score, current_player, game_mode)
            return False, 0  # Switch turns, no points
    
    return True, 0  # Just in case

def ai_turn_handler(cards, ai_memory):
    """Handle AI's turn with fancy animations."""
    # First look for matches in memory
    potential_match = None
    for value, card_list in ai_memory.items():
        valid_cards = [card for card in card_list if not card.is_matched()]
        if len(valid_cards) >= 3:
            potential_match = (valid_cards[0], valid_cards[1], valid_cards[2])
            break
    
    # Flip cards based on AI knowledge or random selection
    flipped_cards = []
    
    if potential_match:
        # AI knows a match
        card1, card2, card3 = potential_match
        card1.flip_up()
        flipped_cards.append(card1)
        wait_for_animations(cards, player1_score, player2_score, current_player, MODE_VS_AI)
        
        pygame.time.delay(500)  # Add delay between flips
        
        card2.flip_up()
        flipped_cards.append(card2)
        wait_for_animations(cards, player1_score, player2_score, current_player, MODE_VS_AI)
        
        pygame.time.delay(500)  # Add delay between flips
        
        card3.flip_up()
        flipped_cards.append(card3)
        wait_for_animations(cards, player1_score, player2_score, current_player, MODE_VS_AI)
    else:
        # Need to flip cards randomly
        
        # First card: random selection
        available_cards = [card for card in cards if not card.is_revealed() and not card.is_matched()]
        
        if not available_cards:
            return True, 0  # No cards left to flip
        
        # Flip first card
        card1 = random.choice(available_cards)
        card1.flip_up()
        flipped_cards.append(card1)
        
        # Remember this card
        if card1.value not in ai_memory:
            ai_memory[card1.value] = []
        if card1 not in ai_memory[card1.value]:
            ai_memory[card1.value].append(card1)
            
        wait_for_animations(cards, player1_score, player2_score, current_player, MODE_VS_AI)
        pygame.time.delay(500)  # Add delay between flips
        
        # Second card: check memory for potential match
        found_match = False
        second_card = None
        
        if card1.value in ai_memory:
            for card2 in ai_memory[card1.value]:
                if card2 != card1 and not card2.is_revealed() and not card2.is_matched():
                    card2.flip_up()
                    flipped_cards.append(card2)
                    second_card = card2
                    found_match = True
                    break
        
        # If no match in memory, pick randomly
        if not found_match:
            available_cards = [card for card in cards if not card.is_revealed() and not card.is_matched() and card != card1]
            
            if available_cards:
                card2 = random.choice(available_cards)
                card2.flip_up()
                flipped_cards.append(card2)
                second_card = card2
                
                # Remember this card
                if card2.value not in ai_memory:
                    ai_memory[card2.value] = []
                if card2 not in ai_memory[card2.value]:
                    ai_memory[card2.value].append(card2)
                    
        wait_for_animations(cards, player1_score, player2_score, current_player, MODE_VS_AI)
        pygame.time.delay(500)  # Add delay between flips
        
        # Third card: check memory for potential match
        found_match = False
        
        if second_card and card1.value == second_card.value and card1.value in ai_memory:
            for card3 in ai_memory[card1.value]:
                if card3 != card1 and card3 != second_card and not card3.is_revealed() and not card3.is_matched():
                    card3.flip_up()
                    flipped_cards.append(card3)
                    found_match = True
                    break
        
        # If no match in memory, pick randomly
        if not found_match:
            available_cards = [card for card in cards if not card.is_revealed() and not card.is_matched() and card not in flipped_cards]
            
            if available_cards:
                card3 = random.choice(available_cards)
                card3.flip_up()
                flipped_cards.append(card3)
                
                # Remember this card
                if card3.value not in ai_memory:
                    ai_memory[card3.value] = []
                if card3 not in ai_memory[card3.value]:
                    ai_memory[card3.value].append(card3)
        
        wait_for_animations(cards, player1_score, player2_score, current_player, MODE_VS_AI)
    
    # Check for match if we flipped three cards
    if len(flipped_cards) == 3:
        card1, card2, card3 = flipped_cards
        
        if card1.value == card2.value == card3.value:
            # We have a match
            pygame.time.delay(500)  # Short delay before marking as matched
            card1.set_matched()
            card2.set_matched()
            card3.set_matched()
            wait_for_animations(cards, player1_score, player2_score, current_player, MODE_VS_AI)
            
            # Remove from memory
            if card1.value in ai_memory:
                ai_memory.pop(card1.value)
                
            return True, 1  # AI gets another turn and 1 point
        else:
            # No match
            pygame.time.delay(1000)  # Wait a second before flipping back
            for card in flipped_cards:
                card.flip_down()
            wait_for_animations(cards, player1_score, player2_score, current_player, MODE_VS_AI)
            return False, 0  # Switch to player turn, no points
    
    return False, 0  # Just in case

def show_game_over(player1_score, player2_score, game_mode):
    """Display game over screen with final scores and replay option."""
    overlay = pygame.Surface((WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Semi-transparent overlay
    screen.blit(overlay, (0, 0))
    
    # Game over text
    game_over_font = pygame.font.Font(None, 72)
    game_over_text = game_over_font.render("Game Over!", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(game_over_text, game_over_rect)
    
    # Final scores
    score_font = pygame.font.Font(None, 48)
    
    if game_mode == MODE_VS_AI:
        player_text = score_font.render(f"Player: {player1_score}", True, (255, 255, 255))
        opponent_text = score_font.render(f"AI: {player2_score}", True, (255, 255, 255))
    else:  # VS_PLAYER mode
        player_text = score_font.render(f"Player 1: {player1_score}", True, (255, 255, 255))
        opponent_text = score_font.render(f"Player 2: {player2_score}", True, (255, 255, 255))
    
    player_rect = player_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(player_text, player_rect)
    
    opponent_rect = opponent_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))
    screen.blit(opponent_text, opponent_rect)
    
    # Winner
    winner_font = pygame.font.Font(None, 54)
    if player1_score > player2_score:
        if game_mode == MODE_VS_AI:
            winner_text = winner_font.render("You Win!", True, (0, 255, 0))
        else:
            winner_text = winner_font.render("Player 1 Wins!", True, (0, 255, 0))
    elif player2_score > player1_score:
        if game_mode == MODE_VS_AI:
            winner_text = winner_font.render("AI Wins!", True, (255, 0, 0))
        else:
            winner_text = winner_font.render("Player 2 Wins!", True, (255, 0, 0))
    else:
        winner_text = winner_font.render("It's a Tie!", True, (255, 255, 0))
    
    winner_rect = winner_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 120))
    screen.blit(winner_text, winner_rect)
    
    # Play again button
    play_again_button = Button(WIDTH//2 - 150, HEIGHT//2 + 200, 300, 80, "Play Again")
    play_again_button.draw(screen)
    
    pygame.display.flip()
    
    # Wait for user response
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Exit game
            
            if event.type == pygame.MOUSEMOTION:
                play_again_button.check_hover(event.pos)
                pygame.display.update()
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_again_button.is_clicked(event.pos):
                    return True  # Start new game
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False  # Exit game
    
    return False  # Default to exit

def main():
    global player1_score, player2_score, current_player
    
    game_state = STATE_MENU
    game_mode = MODE_VS_AI  # Default to AI mode
    
    while True:
        if game_state == STATE_MENU:
            # Show start menu
            vs_ai_button, vs_player_button = draw_start_menu()
            
            # Wait for mode selection
            selecting = True
            while selecting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    
                    if event.type == pygame.MOUSEMOTION:
                        vs_ai_button.check_hover(event.pos)
                        vs_player_button.check_hover(event.pos)
                        pygame.display.update()
                        
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if vs_ai_button.is_clicked(event.pos):
                            game_mode = MODE_VS_AI
                            selecting = False
                        elif vs_player_button.is_clicked(event.pos):
                            game_mode = MODE_VS_PLAYER
                            selecting = False
            
            # Set up the game
            cards, ai_memory, player1_score, player2_score = setup_game()
            current_player = 1  # Player 1 or human player goes first
            game_state = STATE_PLAYING
            
        elif game_state == STATE_PLAYING:
            # Draw current state
            draw_board(cards, player1_score, player2_score, current_player, game_mode)
            
            # Handle events (even when AI is playing)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            
            # Check for game over
            matches = sum(1 for card in cards if card.is_matched())
            if matches == len(cards):
                # Game over - wait for animations to finish
                wait_for_animations(cards, player1_score, player2_score, current_player, game_mode)
                game_state = STATE_GAME_OVER
                continue
            
            # Take turn based on whose turn it is and game mode
            if game_mode == MODE_VS_AI:
                if current_player == 1:  # Human player
                    continue_turn, points = player_turn_handler(cards, ai_memory, game_mode)
                    player1_score += points
                    if not continue_turn:
                        current_player = 2  # Switch to AI
                else:  # AI player
                    continue_turn, points = ai_turn_handler(cards, ai_memory)
                    player2_score += points
                    if not continue_turn:
                        current_player = 1  # Switch to human player
            else:  # VS_PLAYER mode
                continue_turn, points = player_turn_handler(cards, ai_memory, game_mode)
                if current_player == 1:
                    player1_score += points
                    if not continue_turn:
                        current_player = 2  # Switch to player 2
                else:
                    player2_score += points
                    if not continue_turn:
                        current_player = 1  # Switch to player 1
                        
        elif game_state == STATE_GAME_OVER:
            # Show game over screen and check if player wants to play again
            if show_game_over(player1_score, player2_score, game_mode):
                game_state = STATE_MENU  # Go back to menu
            else:
                pygame.quit()
                return

if __name__ == "__main__":
    player1_score = 0
    player2_score = 0
    current_player = 1
    main()
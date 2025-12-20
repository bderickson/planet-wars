"""
Planet Wars - A browser-based strategy game
Main entry point for the game
"""
import asyncio
import sys
import logging
import pygame
from game.logger import setup_logging, get_logger
from game.game_state import GameState
from game.renderer import Renderer
from game.input_handler import InputHandler
from game.menus import Menu, GameConfigMenu, ScoreboardMenu
from game.game_over import GameOver
from game.config import Config
from game.scoreboard import Scoreboard

# Setup logging first thing
setup_logging(level=logging.DEBUG)  # DEBUG for troubleshooting
logger = get_logger(__name__)


class Game:
    """Main game class that manages the game loop"""
    
    def __init__(self):
        logger.info("Initializing Planet Wars game...")
        
        pygame.init()
        logger.debug("Pygame initialized")
        
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Planet Wars")
        logger.debug(f"Screen created: {self.screen_width}x{self.screen_height}")
        
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True
        
        # Detect if running in browser
        self.is_browser = sys.platform == "emscripten"
        logger.info(f"Platform: {sys.platform} (browser: {self.is_browser})")
        
        # Start with click-to-start screen in browser, menu otherwise
        self.state = "start_screen" if self.is_browser else "menu"
        logger.info(f"Initial state: {self.state}")
        
        # Load configuration and scoreboard
        self.config = Config()
        self.scoreboard = Scoreboard()
        logger.debug("Config and scoreboard loaded")
        
        # Initialize menus
        self.menu = Menu(self.screen_width, self.screen_height, self.config)
        self.scoreboard_menu = ScoreboardMenu(self.screen_width, self.screen_height, self.scoreboard)
        self.config_menu = GameConfigMenu(self.screen_width, self.screen_height)
        logger.debug("Menus initialized")
        
        # Game components (initialized when starting a new game)
        self.game_state = None
        self.renderer = None
        self.input_handler = None
        self.game_over_screen = None
        
        logger.info("Game initialization complete")

    async def run(self):
        """Main game loop - async for pygbag compatibility"""
        logger.info("Starting game loop")
        
        while self.running:
            # Handle events
            for event in pygame.event.get():
                try:
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif self.state == "start_screen":
                        self._handle_start_screen_event(event)
                    elif self.state == "menu":
                        self._handle_menu_event(event)
                    elif self.state == "scoreboard":
                        self._handle_scoreboard_event(event)
                    elif self.state == "config":
                        self._handle_config_event(event)
                    elif self.state == "playing":
                        self._handle_game_event(event)
                    elif self.state == "game_over":
                        self._handle_game_over_event(event)
                except Exception as e:
                    logger.error(f"Error handling event in state '{self.state}': {e}", exc_info=True)
                    # Don't crash the game, just log the error and continue

            # Update and render based on state
            try:
                if self.state == "start_screen":
                    self._render_start_screen()
                elif self.state == "menu":
                    self.menu.render(self.screen)
                elif self.state == "scoreboard":
                    self.scoreboard_menu.render(self.screen)
                elif self.state == "config":
                    self.config_menu.render(self.screen)
                elif self.state == "playing":
                    # Update game state
                    dt = self.clock.tick(self.fps) / 1000.0  # Delta time in seconds
                    self.game_state.update(dt)

                    # Check for game over
                    game_result = self.game_state.check_game_over()
                    if game_result:
                        # Stop all playing sounds
                        self.game_state.sound_manager.stop_all()

                        # Play victory or defeat sound
                        if game_result == "victory":
                            self.game_state.sound_manager.play_game_victory()
                        else:
                            self.game_state.sound_manager.play_game_defeat()

                        # Get final stats
                        is_victory = (game_result == "victory")
                        stats = self.game_state.player_stats_tracker if is_victory else self.game_state.enemy_stats_tracker
                        planet_count = len([p for p in self.game_state.planets if p.owner == ("Player" if is_victory else "Enemy")])

                        # Calculate final score
                        if is_victory:
                            final_score = self.game_state.calculate_final_score()
                        else:
                            final_score = 0  # Defeat = 0 score

                        # Save to scoreboard
                        self.scoreboard.add_score(
                            player_name=self.config.player_name,
                            score=final_score,
                            planets_controlled=planet_count,
                            ships_produced=stats['ships_produced'],
                            battles_won=stats['battles_won'],
                            battles_lost=stats['battles_lost'],
                            victory=is_victory,
                            is_cheater=False
                        )

                        self.game_over_screen = GameOver(
                            self.screen_width,
                            self.screen_height,
                            victory=is_victory,
                            planets_controlled=planet_count,
                            ships_produced=stats['ships_produced'],
                            battles_won=stats['battles_won'],
                            battles_lost=stats['battles_lost'],
                            score=final_score,
                            is_cheater=False,
                            game_time=self.game_state.game_time
                        )
                        self.state = "game_over"

                    # Render
                    self.renderer.render(self.game_state)
                elif self.state == "game_over":
                    self.game_over_screen.render(self.screen)
            except Exception as e:
                logger.error(f"Error in update/render loop (state='{self.state}'): {e}", exc_info=True)
                # Try to continue running despite the error

            pygame.display.flip()
            self.clock.tick(self.fps)

            # Required for pygbag - allows browser to handle events
            await asyncio.sleep(0)

        pygame.quit()

    def _handle_start_screen_event(self, event):
        """Handle events in the start screen state"""
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            logger.info("User interaction on start screen, initializing audio")
            
            # Initialize mixer after user interaction (required for browser)
            try:
                if not pygame.mixer.get_init():
                    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                    logger.info("Audio mixer initialized successfully")
                else:
                    logger.info("Audio mixer already initialized")
            except Exception as e:
                logger.error(f"Failed to initialize audio mixer: {e}", exc_info=True)
            
            logger.info("Transitioning to menu")
            self.state = "menu"

    def _render_start_screen(self):
        """Render the 'Click to Start' screen"""
        import math
        
        self.screen.fill((0, 0, 0))  # Black background

        title_font = pygame.font.Font(None, 100)
        start_font = pygame.font.Font(None, 50)

        title_surface = title_font.render("PLANET WARS", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        self.screen.blit(title_surface, title_rect)

        # Pulsing effect for "Click to Start"
        pulse_factor = (pygame.time.get_ticks() % 1000) / 1000.0  # 0 to 1 over 1 second
        brightness = 150 + int(100 * abs(math.sin(pulse_factor * math.pi)))  # 150 to 250
        start_color = (brightness, brightness, brightness)

        start_text = "Click or Press Any Key to Start"
        start_surface = start_font.render(start_text, True, start_color)
        start_rect = start_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
        self.screen.blit(start_surface, start_rect)

    def _handle_menu_event(self, event):
        """Handle events in the menu state"""
        # Handle text input first (for player name)
        self.menu.handle_text_input(event)
        
        if event.type == pygame.MOUSEMOTION:
            self.menu.handle_mouse_motion(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            action = self.menu.handle_click(event.pos)
            if action == "new_game":
                self.state = "config"
            elif action == "scoreboard":
                self.state = "scoreboard"
            elif action == "quit":
                self.running = False

    def _handle_scoreboard_event(self, event):
        """Handle events in the scoreboard state"""
        if event.type == pygame.MOUSEMOTION:
            self.scoreboard_menu.handle_mouse_motion(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            logger.debug(f"Scoreboard: mouse click at {event.pos}")
            action = self.scoreboard_menu.handle_click(event.pos)
            logger.debug(f"Scoreboard: action returned = {action}")
            if action == "back":
                logger.info("Returning to menu from scoreboard")
                self.state = "menu"

    def _handle_config_event(self, event):
        """Handle events in the config menu state"""
        if event.type == pygame.MOUSEMOTION:
            self.config_menu.handle_mouse_motion(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            logger.debug(f"Config menu: mouse click at {event.pos}")
            result = self.config_menu.handle_click(event.pos)
            logger.debug(f"Config menu: result returned = {result}")
            
            if result:
                if result.get('action') == 'back':
                    logger.info("Returning to menu from config")
                    self.state = "menu"
                elif result.get('action') == 'start':
                    logger.info(f"Starting game with config: {result}")
                    # Start new game with selected configuration
                    self.start_new_game(
                        map_size=result.get('map_size', 'medium'),
                        difficulty=result.get('difficulty', 'medium'),
                        sound_pack=result.get('sound_pack', 'default')
                    )
                    self.state = "playing"
            else:
                logger.debug("Config menu: No result from click")

    def start_new_game(self, map_size='medium', difficulty='medium', sound_pack='default'):
        """Initialize a new game with given settings"""
        logger.info(f"Starting new game: map={map_size}, difficulty={difficulty}, sound={sound_pack}")
        
        self.game_state = GameState(
            self.screen_width,
            self.screen_height,
            player_name=self.config.player_name,
            map_size=map_size,
            ai_difficulty=difficulty,  # Note: GameState parameter is 'ai_difficulty'
            sound_pack=sound_pack
        )
        self.renderer = Renderer(self.screen)  # Renderer only takes screen
        self.input_handler = InputHandler(self.game_state)  # InputHandler needs game_state
        
        logger.info("Game started successfully")

    def _handle_game_event(self, event):
        """Handle events during gameplay"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check for UI button clicks first
            if self.renderer.is_quit_button_clicked(event.pos):
                self.state = "menu"
                return
            
            # Check for ability buttons
            ability_name = self.renderer.get_ability_clicked(event.pos)
            if ability_name:
                self._handle_ability_activation(ability_name)
                return
            
            # Check for win button (debug)
            if self.renderer.is_win_button_clicked(event.pos):
                self._handle_win_button()
                return
        
        # Handle input events (mouse clicks, motion, etc)
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            self.input_handler.handle_event(event, self.renderer)
        
        # Also handle mouse motion for UI hover effects
        if event.type == pygame.MOUSEMOTION:
            self.renderer.handle_mouse_motion(event.pos)

    def _handle_ability_activation(self, ability_name):
        """Handle activation of player abilities"""
        try:
            if ability_name == "recall":
                self.game_state.activate_recall()
            elif ability_name == "production":
                self.game_state.activate_production_surge()
            elif ability_name == "shield":
                # Shield requires a selected planet
                if self.game_state.selected_planet is not None:
                    if self.game_state.selected_planet.owner == "Player":
                        self.game_state.activate_shield(self.game_state.selected_planet)
        except Exception as e:
            logger.error(f"Failed to activate ability '{ability_name}': {e}", exc_info=True)

    def _handle_win_button(self):
        """Handle win button click (debug feature)"""
        # Mark as cheater
        stats = self.game_state.player_stats_tracker
        planet_count = len([p for p in self.game_state.planets if p.owner == "Player"])
        
        # Save cheater score
        self.scoreboard.add_score(
            player_name=self.config.player_name,
            score=0,
            planets_controlled=planet_count,
            ships_produced=stats['ships_produced'],
            battles_won=stats['battles_won'],
            battles_lost=stats['battles_lost'],
            victory=True,
            is_cheater=True
        )
        
        self.game_over_screen = GameOver(
            self.screen_width,
            self.screen_height,
            victory=True,
            planets_controlled=planet_count,
            ships_produced=stats['ships_produced'],
            battles_won=stats['battles_won'],
            battles_lost=stats['battles_lost'],
            score=0,
            is_cheater=True,
            game_time=self.game_state.game_time
        )
        self.state = "game_over"

    def _handle_game_over_event(self, event):
        """Handle events on the game over screen"""
        if event.type == pygame.MOUSEMOTION:
            self.game_over_screen.handle_mouse_motion(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            action = self.game_over_screen.handle_click(event.pos)
            if action == "menu":
                self.state = "menu"


async def main():
    """Entry point"""
    logger.info("=" * 60)
    logger.info("Planet Wars starting...")
    logger.info("=" * 60)
    
    game = Game()
    await game.run()
    
    logger.info("Game ended")


# Run the game
logger.info("Calling asyncio.run(main())")
asyncio.run(main())

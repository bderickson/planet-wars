"""
Input handling - mouse and keyboard events
"""
import pygame
from game.entities import Ship


class InputHandler:
    """Handles user input events"""
    
    def __init__(self, game_state):
        self.game_state = game_state
        self.dragging_slider = False
    
    def handle_event(self, event, renderer=None):
        """
        Process a pygame event
        
        Args:
            event: pygame.Event to process
            renderer: Renderer instance for slider interaction
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_down(event.pos, renderer)
        elif event.type == pygame.MOUSEBUTTONUP:
            self._handle_mouse_up(event.pos, renderer)
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event.pos, renderer)
    
    def _handle_mouse_down(self, pos, renderer):
        """Handle mouse button down"""
        # Check if clicking on slider
        if renderer and renderer.slider_rect:
            expanded_rect = renderer.slider_rect.inflate(0, renderer.slider_handle_radius * 2)
            if expanded_rect.collidepoint(pos[0], pos[1]):
                self.dragging_slider = True
                renderer.handle_slider_interaction(pos, dragging=True)
                return
        
        # Otherwise handle planet clicks
        self._handle_click(pos, renderer)
    
    def _handle_mouse_up(self, pos, renderer):
        """Handle mouse button up"""
        self.dragging_slider = False
    
    def _handle_mouse_motion(self, pos, renderer):
        """Handle mouse motion"""
        if self.dragging_slider and renderer:
            renderer.handle_slider_interaction(pos, dragging=True)
    
    def _handle_click(self, pos, renderer):
        """
        Handle a mouse click
        
        Args:
            pos: Tuple of (x, y) click position
            renderer: Renderer instance for slider access
        """
        clicked_planet = self.game_state.get_planet_at(pos[0], pos[1])
        
        if clicked_planet is None:
            # Clicked empty space - deselect
            self.game_state.selected_planet = None
            return
        
        # If no planet selected, select this one (if it's owned by player)
        if self.game_state.selected_planet is None:
            if clicked_planet.owner == "Player":
                self.game_state.selected_planet = clicked_planet
                # Reset slider to 50% when selecting a new planet
                if renderer:
                    renderer.slider_value = 0.5
        else:
            # We have a selected planet - send ships to clicked planet
            source = self.game_state.selected_planet
            target = clicked_planet
            
            # Can only send from player's planets
            if source.owner == "Player" and source.ship_count >= 1:
                # Get ship count from slider
                if renderer:
                    ships_to_send = renderer.get_ships_to_send(source)
                else:
                    ships_to_send = max(1, source.ship_count // 2)
                
                # Ensure we don't send more than we have
                ships_to_send = min(ships_to_send, source.ship_count)
                
                if ships_to_send > 0:
                    source.ship_count -= ships_to_send
                    
                    # Create ship fleet
                    ship = Ship(source, target, "Player", fleet_size=ships_to_send)
                    self.game_state.add_ship(ship)
                    
                    # Play launch sound
                    self.game_state.sound_manager.play_fleet_launched()
            
            # Deselect after sending
            self.game_state.selected_planet = None


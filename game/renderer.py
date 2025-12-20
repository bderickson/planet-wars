"""
Rendering logic - draws the game state to the screen
"""
import pygame
import math
import random


class Renderer:
    """Handles all rendering of game entities"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        # Colors
        self.bg_color = (10, 10, 30)  # Dark space blue
        self.text_color = (255, 255, 255)
        
        # UI Buttons - aligned on the right side
        button_width = 110
        button_height = 50
        button_spacing = 10
        gap_between_sections = 30  # Larger gap to prevent accidental clicks
        right_margin = 10
        start_x = self.screen.get_width() - button_width - right_margin
        
        # Main Menu button (quit) at top
        self.quit_button_rect = pygame.Rect(start_x, 10, button_width, button_height)
        self.quit_button_hovered = False
        
        # Ability buttons - start below Main Menu with a gap
        ability_start_y = 10 + button_height + gap_between_sections
        
        self.ability_buttons = {
            'recall': pygame.Rect(start_x, ability_start_y, button_width, button_height),
            'production': pygame.Rect(start_x, ability_start_y + button_height + button_spacing, button_width, button_height),
            'shield': pygame.Rect(start_x, ability_start_y + (button_height + button_spacing) * 2, button_width, button_height)
        }
        self.ability_hovered = {key: False for key in self.ability_buttons}
        
        # Win button (for testing) - below abilities with a gap
        win_button_y = ability_start_y + (button_height + button_spacing) * 3 + gap_between_sections
        self.win_button_rect = pygame.Rect(start_x, win_button_y, button_width, button_height)
        self.win_button_hovered = False
        
        # Ship count slider
        self.slider_rect = None  # Will be positioned when planet selected
        self.slider_track_height = 8
        self.slider_handle_radius = 12
        self.slider_value = 0.5  # 0.0 to 1.0 (percentage)
        self.slider_active = False
        
        # Background theme (randomly selected)
        self._star_rng = random.Random(random.randint(0, 999999))
        self._background_theme = random.choice([
            "purple_nebula",
            "blue_nebula",
            "orange_nebula",
            "green_cosmic",
            "pink_stardust",
            "red_giant",
            "teal_void",
            "golden_aurora"
        ])
        self._stars = None  # Cache star positions
        self._space_objects = None  # Cache background space objects (planets, asteroids, etc.)
    
    def render(self, game_state):
        """
        Render the entire game state
        
        Args:
            game_state: The current GameState to render
        """
        # Clear screen
        self.screen.fill(self.bg_color)
        
        # Draw stars background (simple effect)
        self._draw_stars()
        
        # Draw player stats at top
        self._draw_player_stats(game_state)
        
        # Draw planets
        for planet in game_state.planets:
            is_selected = (planet == game_state.selected_planet)
            is_shielded = self._is_planet_shielded(planet, game_state)
            self._draw_planet(planet, is_selected, is_shielded)
        
        # Draw ships
        for ship in game_state.ships:
            self._draw_ship(ship)
        
        # Draw UI
        self._draw_ui(game_state)
        
        # Draw ship count slider if planet is selected
        if game_state.selected_planet and game_state.selected_planet.owner == "Player":
            self._draw_slider(game_state.selected_planet)
        
        # Draw ability buttons
        self._draw_ability_buttons(game_state)
        
        # Draw win button (testing)
        self._draw_win_button()
        
        # Draw quit button
        self._draw_quit_button()
    
    def _draw_stars(self):
        """Draw background based on theme"""
        if self._background_theme == "purple_nebula":
            self._draw_colored_space((25, 10, 45), (60, 20, 90), (100, 40, 150))
        elif self._background_theme == "blue_nebula":
            self._draw_colored_space((10, 20, 40), (20, 50, 100), (40, 80, 160))
        elif self._background_theme == "orange_nebula":
            self._draw_colored_space((40, 20, 10), (90, 50, 20), (150, 80, 30))
        elif self._background_theme == "green_cosmic":
            self._draw_colored_space((10, 30, 20), (20, 70, 40), (40, 120, 70))
        elif self._background_theme == "pink_stardust":
            self._draw_colored_space((40, 15, 30), (90, 30, 70), (140, 60, 110))
        elif self._background_theme == "red_giant":
            self._draw_colored_space((45, 10, 10), (100, 20, 20), (160, 40, 30))
        elif self._background_theme == "teal_void":
            self._draw_colored_space((10, 30, 35), (20, 60, 70), (30, 100, 110))
        elif self._background_theme == "golden_aurora":
            self._draw_colored_space((40, 35, 10), (80, 70, 30), (130, 110, 50))
    
    def _draw_colored_space(self, color1, color2, color3):
        """Draw a colorful space background with nebula clouds and objects"""
        # Generate and cache space objects
        if self._space_objects is None:
            self._generate_space_objects()
        
        # Draw large nebula clouds
        for obj in self._space_objects:
            if obj['type'] == 'nebula_cloud':
                self._draw_nebula_cloud(obj, color1, color2)
            elif obj['type'] == 'nebula_streak':
                self._draw_nebula_streak(obj, color2, color3)
        
        # Draw background space objects
        for obj in self._space_objects:
            if obj['type'] == 'background_planet':
                self._draw_background_planet(obj, color2, color3)
            elif obj['type'] == 'asteroid':
                self._draw_asteroid(obj)
            elif obj['type'] == 'comet':
                self._draw_comet(obj, color3)
            elif obj['type'] == 'distant_star':
                self._draw_distant_star(obj, color3)
        
        # Draw stars on top
        if self._stars is None:
            self._stars = []
            for _ in range(150):
                x = self._star_rng.randint(0, self.screen.get_width())
                y = self._star_rng.randint(0, self.screen.get_height())
                brightness = self._star_rng.randint(150, 255)
                size = 1 if self._star_rng.random() < 0.9 else 2
                twinkle = self._star_rng.random() < 0.3  # Some stars twinkle
                self._stars.append((x, y, brightness, size, twinkle))
        
        for x, y, brightness, size, twinkle in self._stars:
            color = (brightness, brightness, brightness)
            pygame.draw.circle(self.screen, color, (x, y), size)
    
    def _generate_space_objects(self):
        """Generate various space objects for the background"""
        self._space_objects = []
        
        # Large nebula clouds (3-5)
        for _ in range(self._star_rng.randint(3, 5)):
            self._space_objects.append({
                'type': 'nebula_cloud',
                'x': self._star_rng.randint(-200, self.screen.get_width() + 200),
                'y': self._star_rng.randint(-200, self.screen.get_height() + 200),
                'radius': self._star_rng.randint(150, 350),
                'alpha': self._star_rng.randint(25, 55)
            })
        
        # Nebula streaks (2-4)
        for _ in range(self._star_rng.randint(2, 4)):
            self._space_objects.append({
                'type': 'nebula_streak',
                'x': self._star_rng.randint(0, self.screen.get_width()),
                'y': self._star_rng.randint(0, self.screen.get_height()),
                'width': self._star_rng.randint(300, 600),
                'height': self._star_rng.randint(80, 150),
                'angle': self._star_rng.randint(0, 360),
                'alpha': self._star_rng.randint(30, 60)
            })
        
        # Background planets (1-3 small distant planets)
        for _ in range(self._star_rng.randint(1, 3)):
            self._space_objects.append({
                'type': 'background_planet',
                'x': self._star_rng.randint(0, self.screen.get_width()),
                'y': self._star_rng.randint(0, self.screen.get_height()),
                'radius': self._star_rng.randint(15, 35),
                'has_ring': self._star_rng.random() < 0.4
            })
        
        # Asteroids (2-5)
        for _ in range(self._star_rng.randint(2, 5)):
            self._space_objects.append({
                'type': 'asteroid',
                'x': self._star_rng.randint(0, self.screen.get_width()),
                'y': self._star_rng.randint(0, self.screen.get_height()),
                'size': self._star_rng.randint(3, 8)
            })
        
        # Comets (0-2)
        for _ in range(self._star_rng.randint(0, 2)):
            self._space_objects.append({
                'type': 'comet',
                'x': self._star_rng.randint(0, self.screen.get_width()),
                'y': self._star_rng.randint(0, self.screen.get_height()),
                'tail_length': self._star_rng.randint(50, 150),
                'angle': self._star_rng.randint(0, 360)
            })
        
        # Distant stars/galaxies (2-4)
        for _ in range(self._star_rng.randint(2, 4)):
            self._space_objects.append({
                'type': 'distant_star',
                'x': self._star_rng.randint(0, self.screen.get_width()),
                'y': self._star_rng.randint(0, self.screen.get_height()),
                'size': self._star_rng.randint(20, 50),
                'intensity': self._star_rng.randint(40, 80)
            })
    
    def _draw_nebula_cloud(self, obj, color1, color2):
        """Draw a nebula cloud"""
        cloud_surface = pygame.Surface((obj['radius'] * 2, obj['radius'] * 2))
        cloud_surface.set_alpha(obj['alpha'])
        color = color1 if self._star_rng.random() < 0.5 else color2
        pygame.draw.circle(cloud_surface, color, (obj['radius'], obj['radius']), obj['radius'])
        self.screen.blit(cloud_surface, (obj['x'] - obj['radius'], obj['y'] - obj['radius']))
    
    def _draw_nebula_streak(self, obj, color2, color3):
        """Draw an elongated nebula streak"""
        streak_surface = pygame.Surface((obj['width'], obj['height']))
        streak_surface.set_alpha(obj['alpha'])
        streak_surface.fill(color2)
        # Rotate the surface
        rotated = pygame.transform.rotate(streak_surface, obj['angle'])
        rect = rotated.get_rect(center=(obj['x'], obj['y']))
        self.screen.blit(rotated, rect)
    
    def _draw_background_planet(self, obj, color2, color3):
        """Draw a small background planet"""
        # Draw planet
        pygame.draw.circle(self.screen, color2, (obj['x'], obj['y']), obj['radius'])
        # Add shading
        shade_color = tuple(max(0, c - 30) for c in color2)
        pygame.draw.circle(self.screen, shade_color, (obj['x'] + 3, obj['y'] + 3), obj['radius'] - 2)
        
        # Draw ring if it has one
        if obj['has_ring']:
            ring_rect = pygame.Rect(obj['x'] - obj['radius'] * 1.5, 
                                    obj['y'] - obj['radius'] * 0.3,
                                    obj['radius'] * 3, 
                                    obj['radius'] * 0.6)
            pygame.draw.ellipse(self.screen, color3, ring_rect, 2)
    
    def _draw_asteroid(self, obj):
        """Draw a small asteroid"""
        gray = self._star_rng.randint(60, 100)
        pygame.draw.circle(self.screen, (gray, gray, gray), (obj['x'], obj['y']), obj['size'])
    
    def _draw_comet(self, obj, color3):
        """Draw a comet with tail"""
        import math
        # Comet head
        pygame.draw.circle(self.screen, (200, 220, 255), (obj['x'], obj['y']), 4)
        pygame.draw.circle(self.screen, (255, 255, 255), (obj['x'], obj['y']), 2)
        
        # Comet tail
        angle_rad = math.radians(obj['angle'])
        tail_end_x = obj['x'] - math.cos(angle_rad) * obj['tail_length']
        tail_end_y = obj['y'] - math.sin(angle_rad) * obj['tail_length']
        
        # Draw tail as fading line
        for i in range(5):
            t = i / 5.0
            x = int(obj['x'] - math.cos(angle_rad) * obj['tail_length'] * t)
            y = int(obj['y'] - math.sin(angle_rad) * obj['tail_length'] * t)
            alpha = int(100 * (1 - t))
            tail_surface = pygame.Surface((6, 6))
            tail_surface.set_alpha(alpha)
            tail_surface.fill(color3)
            self.screen.blit(tail_surface, (x - 3, y - 3))
    
    def _draw_distant_star(self, obj, color3):
        """Draw a distant star or small galaxy"""
        glow_surface = pygame.Surface((obj['size'] * 2, obj['size'] * 2))
        glow_surface.set_alpha(obj['intensity'])
        pygame.draw.circle(glow_surface, color3, (obj['size'], obj['size']), obj['size'])
        self.screen.blit(glow_surface, (obj['x'] - obj['size'], obj['y'] - obj['size']))
    
    def _draw_planet(self, planet, is_selected=False, is_shielded=False):
        """Draw a single planet"""
        # Draw shield effect if active
        if is_shielded:
            # Pulsing blue shield circle
            import time
            pulse = abs(math.sin(time.time() * 3))  # Pulse between 0 and 1
            shield_radius = planet.radius + 8 + int(pulse * 4)
            shield_alpha = int(100 + pulse * 100)  # Alpha between 100-200
            
            # Create a surface for the shield with transparency
            shield_surface = pygame.Surface((shield_radius * 2 + 10, shield_radius * 2 + 10), pygame.SRCALPHA)
            shield_color = (100, 150, 255, shield_alpha)  # Blue with alpha
            pygame.draw.circle(shield_surface, shield_color, (shield_radius + 5, shield_radius + 5), shield_radius, 3)
            
            # Blit shield to screen
            self.screen.blit(shield_surface, (int(planet.x) - shield_radius - 5, int(planet.y) - shield_radius - 5))
        
        # Draw planet circle
        pygame.draw.circle(self.screen, planet.get_color(), 
                         (int(planet.x), int(planet.y)), planet.radius)
        
        # Draw planet outline (thicker if selected)
        outline_width = 3 if is_selected else 1
        pygame.draw.circle(self.screen, (255, 255, 255), 
                         (int(planet.x), int(planet.y)), planet.radius, outline_width)
        
        # Draw ship count
        text = self.font.render(str(planet.ship_count), True, self.text_color)
        text_rect = text.get_rect(center=(int(planet.x), int(planet.y)))
        self.screen.blit(text, text_rect)
        
        # Draw planet name below the planet
        name_text = self.small_font.render(planet.name, True, self.text_color)
        name_rect = name_text.get_rect(center=(int(planet.x), int(planet.y + planet.radius + 15)))
        self.screen.blit(name_text, name_rect)
    
    def _is_planet_shielded(self, planet, game_state):
        """Check if a planet has an active shield"""
        # Check player shield
        player_shield = game_state.player_abilities['shield']
        if player_shield.is_active() and player_shield.target == planet:
            return True
        
        # Check enemy shield
        enemy_shield = game_state.enemy_abilities['shield']
        if enemy_shield.is_active() and enemy_shield.target == planet:
            return True
        
        return False
    
    def _draw_ship(self, ship):
        """Draw a single ship as a triangle pointing towards target"""
        # Calculate angle to target
        dx = ship.target_x - ship.x
        dy = ship.target_y - ship.y
        angle = math.atan2(dy, dx)
        
        # Triangle size
        size = 30
        
        # Calculate triangle points (pointing right by default, then rotated)
        # Front point, back-top point, back-bottom point
        points = [
            (size, 0),      # Front tip
            (-size/2, -size/2),  # Back top
            (-size/2, size/2)    # Back bottom
        ]
        
        # Rotate and translate points
        rotated_points = []
        for px, py in points:
            # Rotate
            rotated_x = px * math.cos(angle) - py * math.sin(angle)
            rotated_y = px * math.sin(angle) + py * math.cos(angle)
            # Translate to ship position
            rotated_points.append((
                int(ship.x + rotated_x),
                int(ship.y + rotated_y)
            ))
        
        # Draw filled triangle
        pygame.draw.polygon(self.screen, ship.get_color(), rotated_points)
        
        # Draw outline
        pygame.draw.polygon(self.screen, (255, 255, 255), rotated_points, 2)
        
        # Draw fleet size number
        fleet_text = self.small_font.render(str(ship.fleet_size), True, (255, 255, 255))
        text_rect = fleet_text.get_rect(center=(int(ship.x), int(ship.y)))
        
        # Draw the text directly (no background)
        self.screen.blit(fleet_text, text_rect)
    
    def _draw_ui(self, game_state):
        """Draw UI elements like instructions and fleet status"""
        instructions = [
            "Click a planet to select it",
            "Click another planet to send half your ships",
            "",
        ]
        
        y_offset = 60  # Start below player stats
        for line in instructions:
            text = self.small_font.render(line, True, self.text_color)
            self.screen.blit(text, (10, y_offset))
            y_offset += 25
        
        # Draw active fleets section
        if game_state.ships:
            y_offset += 10
            header = self.small_font.render("Active Fleets:", True, (200, 200, 255))
            self.screen.blit(header, (10, y_offset))
            y_offset += 25
            
            for ship in game_state.ships:
                # Format: "Alpha: 25 ships -> Blobby Prime"
                fleet_info = f"{ship.fleet_id}: {ship.fleet_size} ships -> {ship.target_planet.name}"
                color = ship.get_color()
                text = self.small_font.render(fleet_info, True, color)
                self.screen.blit(text, (20, y_offset))
                y_offset += 20
        else:
            y_offset += 10
            text = self.small_font.render("No active fleets", True, (150, 150, 150))
            self.screen.blit(text, (10, y_offset))
    
    def _draw_player_stats(self, game_state):
        """Draw player statistics at the top of the screen"""
        # Get stats for both players
        player_stats = game_state.get_player_stats("Player")
        enemy_stats = game_state.get_player_stats("Enemy")
        
        # Player stats (left side, blue) - use custom name
        player_text = f"{game_state.player_name} - {player_stats['planet_count']} Planets, {player_stats['total_ships']} Ships (+{int(player_stats['production_rate'])})"
        player_surface = self.font.render(player_text, True, (100, 150, 255))
        self.screen.blit(player_surface, (10, 10))
        
        # Enemy stats (right side, red)
        enemy_text = f"Enemy - {enemy_stats['planet_count']} Planets, {enemy_stats['total_ships']} Ships (+{int(enemy_stats['production_rate'])})"
        enemy_surface = self.font.render(enemy_text, True, (255, 100, 100))
        enemy_rect = enemy_surface.get_rect(topright=(self.screen.get_width() - 140, 10))  # More space for buttons
        self.screen.blit(enemy_surface, enemy_rect)
    
    def _draw_quit_button(self):
        """Draw the quit button in the top right"""
        # Button colors
        button_color = (70, 70, 140) if self.quit_button_hovered else (50, 50, 100)
        
        # Draw button background
        pygame.draw.rect(self.screen, button_color, self.quit_button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.quit_button_rect, 2)  # Border
        
        # Draw text
        text = self.small_font.render("Main Menu", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.quit_button_rect.center)
        self.screen.blit(text, text_rect)
    
    def _draw_win_button(self):
        """Draw the win button (for testing)"""
        # Button colors - gold theme for victory
        button_color = (200, 150, 50) if self.win_button_hovered else (150, 100, 20)
        
        # Draw button background
        pygame.draw.rect(self.screen, button_color, self.win_button_rect)
        pygame.draw.rect(self.screen, (255, 215, 0), self.win_button_rect, 2)  # Gold border
        
        # Draw text
        text = self.small_font.render("Win", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.win_button_rect.center)
        self.screen.blit(text, text_rect)
    
    def handle_mouse_motion(self, pos):
        """Handle mouse motion for button hover effects"""
        self.quit_button_hovered = self.quit_button_rect.collidepoint(pos[0], pos[1])
        self.win_button_hovered = self.win_button_rect.collidepoint(pos[0], pos[1])
        
        # Check all ability buttons
        for key, rect in self.ability_buttons.items():
            self.ability_hovered[key] = rect.collidepoint(pos[0], pos[1])
    
    def is_quit_button_clicked(self, pos):
        """Check if the quit button was clicked"""
        return self.quit_button_rect.collidepoint(pos[0], pos[1])
    
    def is_win_button_clicked(self, pos):
        """Check if the win button was clicked"""
        return self.win_button_rect.collidepoint(pos[0], pos[1])
    
    def get_ability_clicked(self, pos):
        """Check if an ability button was clicked, return ability name or None"""
        for key, rect in self.ability_buttons.items():
            if rect.collidepoint(pos[0], pos[1]):
                return key
        return None
    
    def _draw_ability_buttons(self, game_state):
        """Draw all three ability buttons"""
        abilities = game_state.player_abilities
        
        # Recall button
        self._draw_single_ability_button(
            'recall',
            abilities['recall'],
            "Recall",
            self.ability_buttons['recall'],
            self.ability_hovered['recall']
        )
        
        # Production Surge button
        self._draw_single_ability_button(
            'production',
            abilities['production'],
            "Production",
            self.ability_buttons['production'],
            self.ability_hovered['production']
        )
        
        # Shield Generator button
        self._draw_single_ability_button(
            'shield',
            abilities['shield'],
            "Shield",
            self.ability_buttons['shield'],
            self.ability_hovered['shield']
        )
    
    def _draw_single_ability_button(self, key, ability, label, rect, hovered):
        """Draw a single ability button"""
        # Determine button color based on state
        if not ability.available and not ability.active:
            # Used up
            button_color = (60, 60, 60)
            text_color = (120, 120, 120)
        elif ability.active:
            # Currently active
            button_color = (100, 200, 100)
            text_color = (255, 255, 255)
        elif hovered:
            # Available and hovered
            button_color = (100, 100, 200)
            text_color = (255, 255, 255)
        else:
            # Available but not hovered
            button_color = (70, 70, 150)
            text_color = (255, 255, 255)
        
        # Draw button background
        pygame.draw.rect(self.screen, button_color, rect)
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)  # Border
        
        # Draw label
        label_surface = self.small_font.render(label, True, text_color)
        label_rect = label_surface.get_rect(center=(rect.centerx, rect.centery - 10))
        self.screen.blit(label_surface, label_rect)
        
        # Draw status/timer
        if ability.active and ability.duration > 0:
            timer_text = f"{ability.time_remaining:.1f}s"
            timer_surface = self.small_font.render(timer_text, True, text_color)
            timer_rect = timer_surface.get_rect(center=(rect.centerx, rect.centery + 10))
            self.screen.blit(timer_surface, timer_rect)
        elif not ability.available:
            used_surface = self.small_font.render("Used", True, text_color)
            used_rect = used_surface.get_rect(center=(rect.centerx, rect.centery + 10))
            self.screen.blit(used_surface, used_rect)
    
    def _draw_slider(self, selected_planet):
        """Draw the ship count slider for selected planet"""
        # Position slider below the selected planet
        slider_width = 200
        slider_x = selected_planet.x - slider_width // 2
        slider_y = selected_planet.y + selected_planet.radius + 60
        
        # Clamp to screen bounds
        slider_x = max(20, min(slider_x, self.screen.get_width() - slider_width - 20))
        slider_y = max(100, min(slider_y, self.screen.get_height() - 80))
        
        self.slider_rect = pygame.Rect(slider_x, slider_y, slider_width, self.slider_track_height)
        
        # Calculate ship count
        max_ships = selected_planet.ship_count
        ships_to_send = max(1, int(max_ships * self.slider_value))
        
        # Draw background panel
        panel_rect = pygame.Rect(slider_x - 10, slider_y - 35, slider_width + 20, 70)
        panel_surface = pygame.Surface((panel_rect.width, panel_rect.height))
        panel_surface.set_alpha(200)
        panel_surface.fill((20, 20, 50))
        self.screen.blit(panel_surface, panel_rect.topleft)
        pygame.draw.rect(self.screen, (100, 100, 150), panel_rect, 2)
        
        # Draw label
        label = self.small_font.render(f"Ships to send: {ships_to_send} / {max_ships}", True, (255, 255, 255))
        label_rect = label.get_rect(center=(slider_x + slider_width // 2, slider_y - 20))
        self.screen.blit(label, label_rect)
        
        # Draw slider track
        pygame.draw.rect(self.screen, (100, 100, 150), self.slider_rect)
        pygame.draw.rect(self.screen, (200, 200, 255), self.slider_rect, 2)
        
        # Draw filled portion
        filled_width = int(slider_width * self.slider_value)
        filled_rect = pygame.Rect(slider_x, slider_y, filled_width, self.slider_track_height)
        pygame.draw.rect(self.screen, (100, 150, 255), filled_rect)
        
        # Draw handle
        handle_x = slider_x + int(slider_width * self.slider_value)
        handle_y = slider_y + self.slider_track_height // 2
        pygame.draw.circle(self.screen, (150, 200, 255), (handle_x, handle_y), self.slider_handle_radius)
        pygame.draw.circle(self.screen, (255, 255, 255), (handle_x, handle_y), self.slider_handle_radius, 2)
        
        # Draw instruction
        instruction = self.small_font.render("Drag slider, then click target planet", True, (200, 200, 200))
        instruction_rect = instruction.get_rect(center=(slider_x + slider_width // 2, slider_y + 25))
        self.screen.blit(instruction, instruction_rect)
    
    def handle_slider_interaction(self, pos, dragging=False):
        """
        Handle slider mouse interaction
        
        Args:
            pos: Mouse position (x, y)
            dragging: Whether mouse button is held down
            
        Returns:
            True if slider was interacted with, False otherwise
        """
        if self.slider_rect is None:
            return False
        
        # Check if mouse is near the slider
        expanded_rect = self.slider_rect.inflate(0, self.slider_handle_radius * 2)
        
        if expanded_rect.collidepoint(pos[0], pos[1]) and dragging:
            # Update slider value based on mouse position
            relative_x = pos[0] - self.slider_rect.x
            self.slider_value = max(0.0, min(1.0, relative_x / self.slider_rect.width))
            # Ensure minimum of 1 ship
            if self.slider_value < 0.01:
                self.slider_value = 0.01
            return True
        
        return False
    
    def get_ships_to_send(self, selected_planet):
        """
        Get the number of ships to send based on slider value
        
        Args:
            selected_planet: The planet ships are being sent from
            
        Returns:
            Number of ships to send (at least 1)
        """
        if selected_planet is None:
            return 0
        return max(1, int(selected_planet.ship_count * self.slider_value))


"""
Special abilities system for players
"""


class Ability:
    """Base class for special abilities"""
    
    def __init__(self, name, duration=0):
        self.name = name
        self.available = True
        self.active = False
        self.duration = duration  # How long the ability lasts (0 = instant)
        self.time_remaining = 0
        self.target = None  # For abilities that target a specific planet
    
    def activate(self, target=None):
        """Activate the ability"""
        if self.available and not self.active:
            self.available = False
            self.active = True
            self.time_remaining = self.duration
            self.target = target
            return True
        return False
    
    def update(self, dt):
        """Update ability state"""
        if self.active and self.duration > 0:
            self.time_remaining -= dt
            if self.time_remaining <= 0:
                self.active = False
                self.time_remaining = 0
                self.target = None
    
    def is_active(self):
        """Check if ability is currently active"""
        return self.active
    
    def is_available(self):
        """Check if ability can be used"""
        return self.available


class RecallAbility(Ability):
    """Recalls all player fleets back to their origin planets"""
    
    def __init__(self):
        super().__init__("Recall", duration=0)  # Instant ability
    
    def get_description(self):
        """Get ability description"""
        if self.available:
            return "Recall: Call back all fleets"
        else:
            return "Recall: Used"


class ProductionSurgeAbility(Ability):
    """Doubles ship production rate for 10 seconds"""
    
    def __init__(self):
        super().__init__("Production Surge", duration=10.0)
        self.production_multiplier = 2.0
    
    def get_description(self):
        """Get ability description"""
        if self.available:
            return "Production Surge: 2x production (10s)"
        elif self.active:
            return f"Surge Active: {self.time_remaining:.1f}s"
        else:
            return "Production Surge: Used"


class ShieldGeneratorAbility(Ability):
    """Fortifies a planet with +50% defense for 15 seconds"""
    
    def __init__(self):
        super().__init__("Shield Generator", duration=15.0)
        self.defense_multiplier = 0.5  # Ships take 50% less damage
    
    def get_description(self):
        """Get ability description"""
        if self.available:
            return "Shield: +50% defense (15s)"
        elif self.active:
            return f"Shield Active: {self.time_remaining:.1f}s"
        else:
            return "Shield: Used"

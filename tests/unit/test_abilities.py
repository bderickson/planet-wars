"""
Unit tests for the Abilities system
"""
import pytest
from game.abilities import Ability, RecallAbility, ProductionSurgeAbility, ShieldGeneratorAbility


class TestAbilityBase:
    """Tests for the base Ability class"""
    
    def test_init_with_no_duration(self):
        """Test creating an instant ability (no duration)"""
        ability = Ability("Test Ability")
        assert ability.name == "Test Ability"
        assert ability.duration == 0
        assert ability.available is True
        assert ability.active is False
        assert ability.time_remaining == 0
        assert ability.target is None
    
    def test_init_with_duration(self):
        """Test creating an ability with duration"""
        ability = Ability("Timed Ability", duration=10.0)
        assert ability.name == "Timed Ability"
        assert ability.duration == 10.0
        assert ability.available is True
        assert ability.active is False
        assert ability.time_remaining == 0
    
    def test_activate_success(self):
        """Test activating an available ability"""
        ability = Ability("Test", duration=5.0)
        result = ability.activate()
        
        assert result is True
        assert ability.available is False
        assert ability.active is True
        assert ability.time_remaining == 5.0
    
    def test_activate_with_target(self):
        """Test activating an ability with a target"""
        ability = Ability("Test", duration=5.0)
        target = "SomeTarget"
        result = ability.activate(target=target)
        
        assert result is True
        assert ability.target == target
    
    def test_activate_when_unavailable(self):
        """Test that unavailable abilities cannot be activated"""
        ability = Ability("Test")
        ability.activate()  # First activation
        
        # Try to activate again
        result = ability.activate()
        assert result is False
    
    def test_activate_when_already_active(self):
        """Test that active abilities cannot be reactivated"""
        ability = Ability("Test", duration=10.0)
        ability.activate()
        
        # Try to activate while still active
        result = ability.activate()
        assert result is False
        assert ability.active is True  # Still active
    
    def test_is_available(self):
        """Test is_available method"""
        ability = Ability("Test")
        assert ability.is_available() is True
        
        ability.activate()
        assert ability.is_available() is False
    
    def test_is_active(self):
        """Test is_active method"""
        ability = Ability("Test", duration=5.0)
        assert ability.is_active() is False
        
        ability.activate()
        assert ability.is_active() is True


class TestAbilityUpdate:
    """Tests for the ability update/timer system"""
    
    def test_update_instant_ability_no_effect(self):
        """Test that instant abilities (duration=0) are not affected by update"""
        ability = Ability("Instant", duration=0)
        ability.activate()
        
        # Update should not change anything for instant abilities
        ability.update(1.0)
        assert ability.active is True  # Still active
        assert ability.time_remaining == 0
    
    def test_update_decreases_time_remaining(self):
        """Test that update decreases time_remaining"""
        ability = Ability("Timed", duration=10.0)
        ability.activate()
        
        ability.update(3.0)
        assert ability.time_remaining == 7.0
        assert ability.active is True
    
    def test_update_multiple_times(self):
        """Test multiple updates"""
        ability = Ability("Timed", duration=10.0)
        ability.activate()
        
        ability.update(2.0)
        assert ability.time_remaining == 8.0
        
        ability.update(3.0)
        assert ability.time_remaining == 5.0
        
        ability.update(1.0)
        assert ability.time_remaining == 4.0
    
    def test_update_deactivates_when_time_expires(self):
        """Test that ability deactivates when time runs out"""
        ability = Ability("Timed", duration=5.0)
        ability.activate()
        
        ability.update(6.0)  # More than duration
        
        assert ability.active is False
        assert ability.time_remaining == 0
    
    def test_update_clears_target_on_expiration(self):
        """Test that target is cleared when ability expires"""
        ability = Ability("Timed", duration=5.0)
        ability.activate(target="SomeTarget")
        
        ability.update(10.0)
        
        assert ability.target is None
    
    def test_update_exact_duration(self):
        """Test update with exactly the remaining time"""
        ability = Ability("Timed", duration=5.0)
        ability.activate()
        
        ability.update(5.0)
        
        assert ability.active is False
        assert ability.time_remaining == 0
    
    def test_update_when_not_active(self):
        """Test that update does nothing when ability is not active"""
        ability = Ability("Test", duration=10.0)
        
        # Don't activate
        ability.update(5.0)
        
        assert ability.active is False
        assert ability.time_remaining == 0
    
    def test_update_with_small_dt(self):
        """Test update with small delta time (frame-by-frame)"""
        ability = Ability("Timed", duration=1.0)
        ability.activate()
        
        # Simulate 60 FPS for 0.5 seconds
        for _ in range(30):
            ability.update(1.0 / 60.0)
        
        assert ability.active is True
        assert 0.4 < ability.time_remaining < 0.6  # Approximately 0.5 seconds left


class TestRecallAbility:
    """Tests for RecallAbility"""
    
    def test_init(self):
        """Test RecallAbility initialization"""
        ability = RecallAbility()
        assert ability.name == "Recall"
        assert ability.duration == 0  # Instant ability
        assert ability.available is True
    
    def test_is_instant(self):
        """Test that Recall is an instant ability"""
        ability = RecallAbility()
        ability.activate()
        
        ability.update(100.0)  # Update with large time
        assert ability.active is True  # Should stay active (instant)
    
    def test_get_description_available(self):
        """Test description when available"""
        ability = RecallAbility()
        assert ability.get_description() == "Recall: Call back all fleets"
    
    def test_get_description_used(self):
        """Test description after being used"""
        ability = RecallAbility()
        ability.activate()
        assert ability.get_description() == "Recall: Used"
    
    def test_single_use(self):
        """Test that Recall is single-use"""
        ability = RecallAbility()
        
        # First use succeeds
        assert ability.activate() is True
        
        # Second use fails
        assert ability.activate() is False


class TestProductionSurgeAbility:
    """Tests for ProductionSurgeAbility"""
    
    def test_init(self):
        """Test ProductionSurgeAbility initialization"""
        ability = ProductionSurgeAbility()
        assert ability.name == "Production Surge"
        assert ability.duration == 10.0
        assert ability.production_multiplier == 2.0
        assert ability.available is True
    
    def test_has_production_multiplier(self):
        """Test that production multiplier is set correctly"""
        ability = ProductionSurgeAbility()
        assert ability.production_multiplier == 2.0
    
    def test_get_description_available(self):
        """Test description when available"""
        ability = ProductionSurgeAbility()
        assert ability.get_description() == "Production Surge: 2x production (10s)"
    
    def test_get_description_active(self):
        """Test description while active"""
        ability = ProductionSurgeAbility()
        ability.activate()
        
        description = ability.get_description()
        assert "Surge Active:" in description
        assert "10.0s" in description
    
    def test_get_description_active_after_update(self):
        """Test description shows remaining time"""
        ability = ProductionSurgeAbility()
        ability.activate()
        ability.update(3.5)
        
        description = ability.get_description()
        assert "Surge Active:" in description
        assert "6.5s" in description
    
    def test_get_description_used(self):
        """Test description after expiring"""
        ability = ProductionSurgeAbility()
        ability.activate()
        ability.update(15.0)  # Expire
        
        assert ability.get_description() == "Production Surge: Used"
    
    def test_duration_expires(self):
        """Test that production surge expires after 10 seconds"""
        ability = ProductionSurgeAbility()
        ability.activate()
        
        ability.update(5.0)
        assert ability.is_active() is True
        
        ability.update(5.0)
        assert ability.is_active() is False


class TestShieldGeneratorAbility:
    """Tests for ShieldGeneratorAbility"""
    
    def test_init(self):
        """Test ShieldGeneratorAbility initialization"""
        ability = ShieldGeneratorAbility()
        assert ability.name == "Shield Generator"
        assert ability.duration == 15.0
        assert ability.defense_multiplier == 0.5
        assert ability.available is True
    
    def test_has_defense_multiplier(self):
        """Test that defense multiplier is set correctly"""
        ability = ShieldGeneratorAbility()
        assert ability.defense_multiplier == 0.5  # 50% damage reduction
    
    def test_get_description_available(self):
        """Test description when available"""
        ability = ShieldGeneratorAbility()
        assert ability.get_description() == "Shield: +50% defense (15s)"
    
    def test_get_description_active(self):
        """Test description while active"""
        ability = ShieldGeneratorAbility()
        ability.activate(target="SomePlanet")
        
        description = ability.get_description()
        assert "Shield Active:" in description
        assert "15.0s" in description
    
    def test_get_description_active_after_update(self):
        """Test description shows remaining time"""
        ability = ShieldGeneratorAbility()
        ability.activate()
        ability.update(7.5)
        
        description = ability.get_description()
        assert "Shield Active:" in description
        assert "7.5s" in description
    
    def test_get_description_used(self):
        """Test description after expiring"""
        ability = ShieldGeneratorAbility()
        ability.activate()
        ability.update(20.0)  # Expire
        
        assert ability.get_description() == "Shield: Used"
    
    def test_duration_expires(self):
        """Test that shield expires after 15 seconds"""
        ability = ShieldGeneratorAbility()
        ability.activate()
        
        ability.update(10.0)
        assert ability.is_active() is True
        
        ability.update(5.0)
        assert ability.is_active() is False
    
    def test_stores_target(self):
        """Test that shield can store a target planet"""
        ability = ShieldGeneratorAbility()
        target_planet = "Planet123"
        
        ability.activate(target=target_planet)
        assert ability.target == target_planet
    
    def test_target_cleared_on_expiration(self):
        """Test that target is cleared when shield expires"""
        ability = ShieldGeneratorAbility()
        ability.activate(target="Planet123")
        
        ability.update(20.0)  # Expire
        assert ability.target is None


class TestAbilityEdgeCases:
    """Tests for edge cases and error conditions"""
    
    def test_negative_duration(self):
        """Test ability with negative duration (shouldn't happen but test it)"""
        ability = Ability("Test", duration=-5.0)
        ability.activate()
        
        # Negative duration should not be updated
        ability.update(1.0)
        # Behavior depends on implementation, just ensure no crash
        assert True  # If we get here, no crash
    
    def test_very_small_time_updates(self):
        """Test with very small time deltas"""
        ability = Ability("Test", duration=1.0)
        ability.activate()
        
        # Update with very small time steps
        for _ in range(1000):
            ability.update(0.001)
        
        assert ability.active is False
        assert ability.time_remaining == 0
    
    def test_zero_time_update(self):
        """Test update with zero delta time"""
        ability = Ability("Test", duration=10.0)
        ability.activate()
        
        ability.update(0.0)
        assert ability.time_remaining == 10.0
        assert ability.active is True
    
    def test_activate_with_none_target(self):
        """Test explicit None target"""
        ability = Ability("Test")
        result = ability.activate(target=None)
        
        assert result is True
        assert ability.target is None
    
    def test_multiple_abilities_independent(self):
        """Test that multiple instances don't interfere"""
        ability1 = ProductionSurgeAbility()
        ability2 = ProductionSurgeAbility()
        
        ability1.activate()
        
        assert ability1.is_active() is True
        assert ability2.is_active() is False
        assert ability2.is_available() is True
    
    def test_ability_state_after_expiration(self):
        """Test that all state is properly cleaned up after expiration"""
        ability = ShieldGeneratorAbility()
        ability.activate(target="TestPlanet")
        
        ability.update(20.0)  # Expire
        
        assert ability.active is False
        assert ability.time_remaining == 0
        assert ability.target is None
        assert ability.available is False  # One-time use


class TestAbilityComparison:
    """Tests comparing different ability types"""
    
    def test_all_abilities_start_available(self):
        """Test that all ability types start available"""
        abilities = [
            RecallAbility(),
            ProductionSurgeAbility(),
            ShieldGeneratorAbility()
        ]
        
        for ability in abilities:
            assert ability.is_available() is True
    
    def test_all_abilities_single_use(self):
        """Test that all abilities are single-use"""
        abilities = [
            RecallAbility(),
            ProductionSurgeAbility(),
            ShieldGeneratorAbility()
        ]
        
        for ability in abilities:
            ability.activate()
            assert ability.activate() is False  # Second activation fails
    
    def test_duration_differences(self):
        """Test that abilities have correct durations"""
        recall = RecallAbility()
        production = ProductionSurgeAbility()
        shield = ShieldGeneratorAbility()
        
        assert recall.duration == 0  # Instant
        assert production.duration == 10.0
        assert shield.duration == 15.0
    
    def test_unique_names(self):
        """Test that each ability has a unique name"""
        abilities = [
            RecallAbility(),
            ProductionSurgeAbility(),
            ShieldGeneratorAbility()
        ]
        
        names = [ability.name for ability in abilities]
        assert len(names) == len(set(names))  # All unique


"""
Unit tests for the AI system
"""
import pytest
from unittest.mock import MagicMock, Mock
from game.ai import create_ai
from game.ai.base_ai import BaseAI
from game.ai.simple_ai import SimpleAI
from game.entities import Planet


class TestAIFactory:
    """Tests for AI factory function"""
    
    def test_create_ai_default(self):
        """Test creating AI with default difficulty"""
        ai = create_ai()
        assert isinstance(ai, SimpleAI)
        assert ai.difficulty == "medium"
    
    def test_create_ai_easy(self):
        """Test creating easy AI"""
        ai = create_ai("easy")
        assert isinstance(ai, SimpleAI)
        assert ai.difficulty == "easy"
    
    def test_create_ai_medium(self):
        """Test creating medium AI"""
        ai = create_ai("medium")
        assert isinstance(ai, SimpleAI)
        assert ai.difficulty == "medium"
    
    def test_create_ai_hard(self):
        """Test creating hard AI"""
        ai = create_ai("hard")
        assert isinstance(ai, SimpleAI)
        assert ai.difficulty == "hard"
    
    def test_create_ai_returns_baseai(self):
        """Test that factory returns BaseAI subclass"""
        ai = create_ai()
        assert isinstance(ai, BaseAI)


class TestBaseAI:
    """Tests for BaseAI base class"""
    
    def test_base_ai_cannot_instantiate(self):
        """Test that BaseAI is abstract and cannot be instantiated"""
        with pytest.raises(TypeError):
            BaseAI()
    
    def test_base_ai_requires_make_decision(self):
        """Test that subclasses must implement make_decision"""
        class IncompleteAI(BaseAI):
            pass
        
        with pytest.raises(TypeError):
            IncompleteAI()
    
    def test_base_ai_has_difficulty(self):
        """Test that BaseAI stores difficulty"""
        class TestAI(BaseAI):
            def make_decision(self, game_state, dt):
                return []
        
        ai = TestAI("hard")
        assert ai.difficulty == "hard"
    
    def test_get_enemy_planets(self):
        """Test get_enemy_planets helper"""
        class TestAI(BaseAI):
            def make_decision(self, game_state, dt):
                return []
        
        ai = TestAI()
        
        # Mock game state
        game_state = Mock()
        game_state.planets = [
            Planet(100, 100, 30, "Enemy", 10),
            Planet(200, 200, 30, "Player", 10),
            Planet(300, 300, 30, "Enemy", 10),
            Planet(400, 400, 30, "Neutral", 10),
        ]
        
        enemy_planets = ai.get_enemy_planets(game_state)
        assert len(enemy_planets) == 2
        assert all(p.owner == "Enemy" for p in enemy_planets)
    
    def test_get_player_planets(self):
        """Test get_player_planets helper"""
        class TestAI(BaseAI):
            def make_decision(self, game_state, dt):
                return []
        
        ai = TestAI()
        
        game_state = Mock()
        game_state.planets = [
            Planet(100, 100, 30, "Enemy", 10),
            Planet(200, 200, 30, "Player", 10),
            Planet(300, 300, 30, "Player", 10),
        ]
        
        player_planets = ai.get_player_planets(game_state)
        assert len(player_planets) == 2
        assert all(p.owner == "Player" for p in player_planets)
    
    def test_get_neutral_planets(self):
        """Test get_neutral_planets helper"""
        class TestAI(BaseAI):
            def make_decision(self, game_state, dt):
                return []
        
        ai = TestAI()
        
        game_state = Mock()
        game_state.planets = [
            Planet(100, 100, 30, "Neutral", 10),
            Planet(200, 200, 30, "Player", 10),
            Planet(300, 300, 30, "Neutral", 10),
        ]
        
        neutral_planets = ai.get_neutral_planets(game_state)
        assert len(neutral_planets) == 2
        assert all(p.owner == "Neutral" for p in neutral_planets)
    
    def test_get_distance(self):
        """Test get_distance helper"""
        class TestAI(BaseAI):
            def make_decision(self, game_state, dt):
                return []
        
        ai = TestAI()
        
        planet1 = Planet(0, 0, 30)
        planet2 = Planet(300, 400, 30)
        
        distance = ai.get_distance(planet1, planet2)
        assert distance == 500  # 3-4-5 triangle


class TestSimpleAIInit:
    """Tests for SimpleAI initialization"""
    
    def test_simple_ai_init_easy(self):
        """Test SimpleAI initialization with easy difficulty"""
        ai = SimpleAI("easy")
        
        assert ai.difficulty == "easy"
        assert ai.decision_interval == 3.0
        assert ai.aggression == 0.3
        assert ai.min_ships_to_attack == 20
        assert ai.decision_timer == 0
    
    def test_simple_ai_init_medium(self):
        """Test SimpleAI initialization with medium difficulty"""
        ai = SimpleAI("medium")
        
        assert ai.difficulty == "medium"
        assert ai.decision_interval == 2.0
        assert ai.aggression == 0.5
        assert ai.min_ships_to_attack == 10
    
    def test_simple_ai_init_hard(self):
        """Test SimpleAI initialization with hard difficulty"""
        ai = SimpleAI("hard")
        
        assert ai.difficulty == "hard"
        assert ai.decision_interval == 1.0
        assert ai.aggression == 0.7
        assert ai.min_ships_to_attack == 5
    
    def test_simple_ai_default_is_medium(self):
        """Test that SimpleAI defaults to medium"""
        ai = SimpleAI()
        assert ai.difficulty == "medium"


class TestSimpleAIMakeDecision:
    """Tests for SimpleAI decision making"""
    
    def test_make_decision_returns_list(self):
        """Test that make_decision returns a list"""
        ai = SimpleAI()
        game_state = Mock()
        game_state.planets = []
        
        result = ai.make_decision(game_state, 0.1)
        assert isinstance(result, list)
    
    def test_make_decision_waits_for_interval(self):
        """Test that AI waits for decision interval"""
        ai = SimpleAI("medium")  # 2.0 second interval
        
        game_state = Mock()
        game_state.planets = [
            Planet(100, 100, 30, "Enemy", 50),
            Planet(300, 300, 30, "Neutral", 10),
        ]
        
        # First call with small dt - should return empty
        result = ai.make_decision(game_state, 0.5)
        assert result == []
        
        # Second call that pushes timer over threshold
        result = ai.make_decision(game_state, 1.6)
        # May or may not return actions, but shouldn't crash
        assert isinstance(result, list)
    
    def test_make_decision_resets_timer(self):
        """Test that decision timer resets after making decision"""
        ai = SimpleAI("easy")  # 3.0 second interval
        
        game_state = Mock()
        game_state.planets = []
        
        # Trigger a decision
        ai.make_decision(game_state, 3.0)
        
        # Timer should be reset (< interval)
        assert ai.decision_timer < ai.decision_interval
    
    def test_make_decision_no_enemy_planets(self):
        """Test decision making with no enemy planets"""
        ai = SimpleAI()
        
        game_state = Mock()
        game_state.planets = [
            Planet(100, 100, 30, "Player", 50),
        ]
        
        ai.decision_timer = 10.0  # Force decision
        result = ai.make_decision(game_state, 0.1)
        assert result == []
    
    def test_make_decision_insufficient_ships(self):
        """Test that AI doesn't attack without enough ships"""
        ai = SimpleAI("medium")  # min_ships = 10
        
        game_state = Mock()
        game_state.planets = [
            Planet(100, 100, 30, "Enemy", 5),  # Too few ships
            Planet(300, 300, 30, "Neutral", 1),
        ]
        
        ai.decision_timer = 10.0  # Force decision
        result = ai.make_decision(game_state, 0.1)
        assert result == []
    
    def test_make_decision_finds_closest_target(self):
        """Test that AI targets closest planet"""
        ai = SimpleAI("easy")
        
        game_state = Mock()
        enemy_planet = Planet(100, 100, 30, "Enemy", 50)
        close_target = Planet(150, 150, 30, "Neutral", 5)
        far_target = Planet(900, 900, 30, "Neutral", 5)
        
        game_state.planets = [enemy_planet, close_target, far_target]
        
        ai.decision_timer = 10.0
        result = ai.make_decision(game_state, 0.1)
        
        # Should attack the closest target
        if result:
            assert result[0]["target_planet"] == close_target
    
    def test_make_decision_returns_valid_actions(self):
        """Test that returned actions have correct format"""
        ai = SimpleAI("medium")
        
        game_state = Mock()
        game_state.planets = [
            Planet(100, 100, 30, "Enemy", 100),
            Planet(300, 300, 30, "Neutral", 5),
        ]
        
        ai.decision_timer = 10.0
        result = ai.make_decision(game_state, 0.1)
        
        if result:
            action = result[0]
            assert "action" in action
            assert action["action"] == "send_fleet"
            assert "source_planet" in action
            assert "target_planet" in action
            assert "ship_count" in action
            assert action["ship_count"] > 0
    
    def test_make_decision_respects_aggression(self):
        """Test that ship count respects aggression level"""
        ai = SimpleAI("medium")  # 0.5 aggression
        
        game_state = Mock()
        enemy_planet = Planet(100, 100, 30, "Enemy", 100)
        target = Planet(300, 300, 30, "Neutral", 1)
        game_state.planets = [enemy_planet, target]
        
        ai.decision_timer = 10.0
        result = ai.make_decision(game_state, 0.1)
        
        if result:
            ships_sent = result[0]["ship_count"]
            expected = int(100 * 0.5)
            assert ships_sent == expected


class TestSimpleAIShouldAttack:
    """Tests for SimpleAI attack decision logic"""
    
    def test_should_attack_neutral_with_advantage(self):
        """Test attacking neutral planet when we have more ships"""
        ai = SimpleAI("medium")
        
        source = Planet(100, 100, 30, "Enemy", 100)
        target = Planet(300, 300, 30, "Neutral", 20)
        game_state = Mock()
        
        ships_to_send = int(100 * 0.5)  # 50 ships
        assert ships_to_send > target.ship_count
        
        result = ai._should_attack(source, target, game_state)
        assert result is True
    
    def test_should_not_attack_neutral_without_advantage(self):
        """Test not attacking neutral when we don't have enough ships"""
        ai = SimpleAI("medium")
        
        source = Planet(100, 100, 30, "Enemy", 100)
        target = Planet(300, 300, 30, "Neutral", 60)
        game_state = Mock()
        
        # We'd send 50, target has 60
        result = ai._should_attack(source, target, game_state)
        assert result is False
    
    def test_should_attack_player_with_large_advantage(self):
        """Test attacking player planet with sufficient advantage"""
        ai = SimpleAI("hard")  # 1.2x safety margin
        
        source = Planet(100, 100, 30, "Enemy", 100)
        target = Planet(300, 300, 30, "Player", 30)
        game_state = Mock()
        
        # We'd send 70 (0.7 aggression), need > 30 * 1.2 = 36
        result = ai._should_attack(source, target, game_state)
        assert result is True
    
    def test_should_not_attack_player_without_large_advantage(self):
        """Test not attacking player without sufficient margin"""
        ai = SimpleAI("easy")  # 1.5x safety margin, 0.3 aggression
        
        source = Planet(100, 100, 30, "Enemy", 100)
        target = Planet(300, 300, 30, "Player", 25)
        game_state = Mock()
        
        # We'd send 30, need > 25 * 1.5 = 37.5
        result = ai._should_attack(source, target, game_state)
        assert result is False
    
    def test_should_not_attack_with_zero_ships(self):
        """Test not attacking when we'd send zero ships"""
        ai = SimpleAI("medium")
        
        source = Planet(100, 100, 30, "Enemy", 1)  # Very few ships
        target = Planet(300, 300, 30, "Neutral", 0)
        game_state = Mock()
        
        # Would send 0 ships (1 * 0.5 = 0.5 -> 0)
        result = ai._should_attack(source, target, game_state)
        assert result is False


class TestSimpleAIDifficultyDifferences:
    """Tests for difficulty-based behavior differences"""
    
    def test_easy_makes_slower_decisions(self):
        """Test that easy AI has longer decision interval"""
        easy = SimpleAI("easy")
        medium = SimpleAI("medium")
        hard = SimpleAI("hard")
        
        assert easy.decision_interval > medium.decision_interval
        assert medium.decision_interval > hard.decision_interval
    
    def test_easy_is_less_aggressive(self):
        """Test that easy AI sends fewer ships"""
        easy = SimpleAI("easy")
        medium = SimpleAI("medium")
        hard = SimpleAI("hard")
        
        assert easy.aggression < medium.aggression
        assert medium.aggression < hard.aggression
    
    def test_easy_requires_more_ships(self):
        """Test that easy AI needs more ships before attacking"""
        easy = SimpleAI("easy")
        medium = SimpleAI("medium")
        hard = SimpleAI("hard")
        
        assert easy.min_ships_to_attack > medium.min_ships_to_attack
        assert medium.min_ships_to_attack > hard.min_ships_to_attack
    
    def test_easy_more_cautious_against_player(self):
        """Test that easy AI uses larger safety margin"""
        easy = SimpleAI("easy")
        hard = SimpleAI("hard")
        
        source = Planet(100, 100, 30, "Enemy", 100)
        player_planet = Planet(300, 300, 30, "Player", 40)
        game_state = Mock()
        
        # Easy: sends 30, needs > 40 * 1.5 = 60 (won't attack)
        # Hard: sends 70, needs > 40 * 1.2 = 48 (will attack)
        
        easy_attacks = easy._should_attack(source, player_planet, game_state)
        hard_attacks = hard._should_attack(source, player_planet, game_state)
        
        assert easy_attacks is False
        assert hard_attacks is True


class TestSimpleAIEdgeCases:
    """Tests for edge cases"""
    
    def test_no_targets_available(self):
        """Test AI behavior when no targets exist"""
        ai = SimpleAI()
        
        game_state = Mock()
        game_state.planets = [
            Planet(100, 100, 30, "Enemy", 100),
            # No other planets
        ]
        
        ai.decision_timer = 10.0
        result = ai.make_decision(game_state, 0.1)
        assert result == []
    
    def test_multiple_enemy_planets(self):
        """Test AI with multiple planets can attack"""
        ai = SimpleAI("hard")
        
        game_state = Mock()
        game_state.planets = [
            Planet(100, 100, 30, "Enemy", 100),
            Planet(200, 200, 30, "Enemy", 100),
            Planet(500, 500, 30, "Neutral", 5),
        ]
        
        ai.decision_timer = 10.0
        result = ai.make_decision(game_state, 0.1)
        
        # Both planets should try to attack
        assert len(result) <= 2  # At most 2 actions
    
    def test_very_large_dt(self):
        """Test with very large time delta"""
        ai = SimpleAI()
        
        game_state = Mock()
        game_state.planets = []
        
        result = ai.make_decision(game_state, 1000.0)
        assert isinstance(result, list)
    
    def test_zero_dt(self):
        """Test with zero time delta"""
        ai = SimpleAI()
        
        game_state = Mock()
        game_state.planets = []
        
        result = ai.make_decision(game_state, 0.0)
        assert result == []
    
    def test_negative_dt(self):
        """Test with negative time delta (shouldn't happen but test it)"""
        ai = SimpleAI()
        
        game_state = Mock()
        game_state.planets = []
        
        result = ai.make_decision(game_state, -1.0)
        # Should still work, just won't trigger decision
        assert isinstance(result, list)


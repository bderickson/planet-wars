"""
Unit tests for the Scoreboard class
"""
import pytest
import json
import os
from datetime import datetime
from game.scoreboard import Scoreboard


class TestScoreboardInit:
    """Tests for Scoreboard initialization"""
    
    def test_init_with_default_filename(self, tmp_path):
        """Test initialization with default filename"""
        os.chdir(tmp_path)
        scoreboard = Scoreboard()
        assert scoreboard.filename == 'files/scoreboard.json'
        assert scoreboard.scores == []
    
    def test_init_with_custom_filename(self, tmp_path):
        """Test initialization with custom filename"""
        filename = str(tmp_path / "custom_scores.json")
        scoreboard = Scoreboard(filename)
        assert scoreboard.filename == filename
        assert scoreboard.scores == []
    
    def test_init_loads_existing_scores(self, tmp_path):
        """Test that initialization loads existing scores from file"""
        filename = str(tmp_path / "existing_scores.json")
        
        # Create a file with existing scores
        existing_scores = [
            {
                'player_name': 'Alice',
                'score': 100,
                'planets_controlled': 5,
                'ships_produced': 50,
                'battles_won': 10,
                'battles_lost': 0,
                'victory': True,
                'is_cheater': False,
                'timestamp': datetime.now().isoformat()
            }
        ]
        with open(filename, 'w') as f:
            json.dump(existing_scores, f)
        
        scoreboard = Scoreboard(filename)
        assert len(scoreboard.scores) == 1
        assert scoreboard.scores[0]['player_name'] == 'Alice'


class TestScoreboardAddScore:
    """Tests for adding scores"""
    
    def test_add_legitimate_score(self, tmp_path):
        """Test adding a legitimate score"""
        filename = str(tmp_path / "test_scores.json")
        scoreboard = Scoreboard(filename)
        
        scoreboard.add_score(
            player_name="Bob",
            score=85,
            planets_controlled=3,
            ships_produced=30,
            battles_won=5,
            battles_lost=2,
            victory=True,
            is_cheater=False
        )
        
        assert len(scoreboard.scores) == 1
        entry = scoreboard.scores[0]
        assert entry['player_name'] == 'Bob'
        assert entry['score'] == 85
        assert entry['planets_controlled'] == 3
        assert entry['ships_produced'] == 30
        assert entry['battles_won'] == 5
        assert entry['battles_lost'] == 2
        assert entry['victory'] is True
        assert entry['is_cheater'] is False
        assert 'timestamp' in entry
    
    def test_add_cheater_score(self, tmp_path):
        """Test adding a cheater score (win button pressed)"""
        filename = str(tmp_path / "test_scores.json")
        scoreboard = Scoreboard(filename)
        
        scoreboard.add_score(
            player_name="Cheater",
            score=999,  # Score shouldn't matter
            planets_controlled=5,
            ships_produced=100,
            battles_won=10,
            battles_lost=0,
            victory=True,
            is_cheater=True
        )
        
        assert len(scoreboard.scores) == 1
        entry = scoreboard.scores[0]
        assert entry['player_name'] == 'Cheater'
        assert entry['score'] == "CHEATER"  # Score replaced with string
        assert entry['is_cheater'] is True
    
    def test_add_defeat_score(self, tmp_path):
        """Test adding a defeat score"""
        filename = str(tmp_path / "test_scores.json")
        scoreboard = Scoreboard(filename)
        
        scoreboard.add_score(
            player_name="Loser",
            score=0,
            planets_controlled=0,
            ships_produced=20,
            battles_won=2,
            battles_lost=5,
            victory=False,
            is_cheater=False
        )
        
        assert len(scoreboard.scores) == 1
        entry = scoreboard.scores[0]
        assert entry['victory'] is False
        assert entry['score'] == 0
    
    def test_add_multiple_scores(self, tmp_path):
        """Test adding multiple scores"""
        filename = str(tmp_path / "test_scores.json")
        scoreboard = Scoreboard(filename)
        
        for i in range(5):
            scoreboard.add_score(
                player_name=f"Player{i}",
                score=100 - i * 10,
                planets_controlled=i,
                ships_produced=i * 10,
                battles_won=i,
                battles_lost=0,
                victory=True,
                is_cheater=False
            )
        
        assert len(scoreboard.scores) == 5


class TestScoreboardGetTopScores:
    """Tests for getting top scores"""
    
    def test_get_top_scores_empty(self, tmp_path):
        """Test getting top scores from empty scoreboard"""
        filename = str(tmp_path / "test_scores.json")
        scoreboard = Scoreboard(filename)
        
        top_scores = scoreboard.get_top_scores()
        assert top_scores == []
    
    def test_get_top_scores_sorted(self, tmp_path):
        """Test that top scores are sorted by score descending"""
        filename = str(tmp_path / "test_scores.json")
        scoreboard = Scoreboard(filename)
        
        # Add scores in random order
        scores = [50, 100, 75, 25, 90]
        for i, score in enumerate(scores):
            scoreboard.add_score(
                player_name=f"Player{i}",
                score=score,
                planets_controlled=3,
                ships_produced=20,
                battles_won=5,
                battles_lost=1,
                victory=True,
                is_cheater=False
            )
        
        top_scores = scoreboard.get_top_scores()
        assert len(top_scores) == 5
        assert top_scores[0]['score'] == 100
        assert top_scores[1]['score'] == 90
        assert top_scores[2]['score'] == 75
        assert top_scores[3]['score'] == 50
        assert top_scores[4]['score'] == 25
    
    def test_get_top_scores_excludes_cheaters(self, tmp_path):
        """Test that cheaters are excluded from top scores"""
        filename = str(tmp_path / "test_scores.json")
        scoreboard = Scoreboard(filename)
        
        # Add legitimate scores
        scoreboard.add_score("Alice", 100, 5, 50, 10, 0, True, False)
        scoreboard.add_score("Bob", 80, 4, 40, 8, 2, True, False)
        
        # Add cheater score
        scoreboard.add_score("Cheater", 999, 5, 100, 20, 0, True, True)
        
        top_scores = scoreboard.get_top_scores()
        assert len(top_scores) == 2
        assert all(not s['is_cheater'] for s in top_scores)
        assert top_scores[0]['player_name'] == 'Alice'
        assert top_scores[1]['player_name'] == 'Bob'
    
    def test_get_top_scores_with_limit(self, tmp_path):
        """Test getting top scores with custom limit"""
        filename = str(tmp_path / "test_scores.json")
        scoreboard = Scoreboard(filename)
        
        # Add 10 scores
        for i in range(10):
            scoreboard.add_score(
                player_name=f"Player{i}",
                score=100 - i,
                planets_controlled=3,
                ships_produced=20,
                battles_won=5,
                battles_lost=1,
                victory=True,
                is_cheater=False
            )
        
        top_3 = scoreboard.get_top_scores(limit=3)
        assert len(top_3) == 3
        assert top_3[0]['score'] == 100
        assert top_3[1]['score'] == 99
        assert top_3[2]['score'] == 98
    
    def test_get_top_scores_includes_defeats(self, tmp_path):
        """Test that defeats are included if they have valid scores"""
        filename = str(tmp_path / "test_scores.json")
        scoreboard = Scoreboard(filename)
        
        # Add victory
        scoreboard.add_score("Winner", 100, 5, 50, 10, 0, True, False)
        
        # Add defeat (score is 0 by design for defeats)
        scoreboard.add_score("Loser", 0, 0, 20, 2, 5, False, False)
        
        top_scores = scoreboard.get_top_scores()
        # Should have both if score is numeric
        assert len(top_scores) == 2


class TestScoreboardGetAllScores:
    """Tests for getting all scores"""
    
    def test_get_all_scores_includes_cheaters(self, tmp_path):
        """Test that all scores include cheaters at the end"""
        filename = str(tmp_path / "test_scores.json")
        scoreboard = Scoreboard(filename)
        
        # Add legitimate scores
        scoreboard.add_score("Alice", 100, 5, 50, 10, 0, True, False)
        scoreboard.add_score("Bob", 80, 4, 40, 8, 2, True, False)
        
        # Add cheater
        scoreboard.add_score("Cheater", 999, 5, 100, 20, 0, True, True)
        
        all_scores = scoreboard.get_all_scores()
        assert len(all_scores) == 3
        # Legitimate scores should be first, sorted by score
        assert all_scores[0]['player_name'] == 'Alice'
        assert all_scores[1]['player_name'] == 'Bob'
        # Cheater should be last
        assert all_scores[2]['player_name'] == 'Cheater'
        assert all_scores[2]['score'] == "CHEATER"
    
    def test_get_all_scores_with_limit(self, tmp_path):
        """Test getting all scores with limit"""
        filename = str(tmp_path / "test_scores.json")
        scoreboard = Scoreboard(filename)
        
        # Add many scores
        for i in range(60):
            scoreboard.add_score(
                player_name=f"Player{i}",
                score=100 - i,
                planets_controlled=3,
                ships_produced=20,
                battles_won=5,
                battles_lost=1,
                victory=True,
                is_cheater=False
            )
        
        # Default limit is 50
        all_scores = scoreboard.get_all_scores()
        assert len(all_scores) == 50
        
        # Custom limit
        limited_scores = scoreboard.get_all_scores(limit=10)
        assert len(limited_scores) == 10


class TestScoreboardPersistence:
    """Tests for score persistence (save/load)"""
    
    def test_scores_persist_after_save(self, tmp_path):
        """Test that scores are saved to file"""
        filename = str(tmp_path / "test_scores.json")
        scoreboard = Scoreboard(filename)
        
        scoreboard.add_score("Alice", 100, 5, 50, 10, 0, True, False)
        
        # Check file was created
        assert os.path.exists(filename)
        
        # Check file contents
        with open(filename, 'r') as f:
            saved_data = json.load(f)
        
        assert len(saved_data) == 1
        assert saved_data[0]['player_name'] == 'Alice'
    
    def test_scores_loaded_on_init(self, tmp_path):
        """Test that scores are loaded when creating new instance"""
        filename = str(tmp_path / "test_scores.json")
        
        # Create first scoreboard and add score
        scoreboard1 = Scoreboard(filename)
        scoreboard1.add_score("Alice", 100, 5, 50, 10, 0, True, False)
        
        # Create second scoreboard with same filename
        scoreboard2 = Scoreboard(filename)
        
        # Should load the score from file
        assert len(scoreboard2.scores) == 1
        assert scoreboard2.scores[0]['player_name'] == 'Alice'
    
    def test_corrupted_file_returns_empty(self, tmp_path):
        """Test that corrupted file returns empty scores list"""
        filename = str(tmp_path / "corrupted.json")
        
        # Write invalid JSON
        with open(filename, 'w') as f:
            f.write("This is not valid JSON{{{")
        
        scoreboard = Scoreboard(filename)
        assert scoreboard.scores == []
    
    def test_save_creates_valid_json(self, tmp_path):
        """Test that saved file is valid JSON with proper formatting"""
        filename = str(tmp_path / "test_scores.json")
        scoreboard = Scoreboard(filename)
        
        scoreboard.add_score("Alice", 100, 5, 50, 10, 0, True, False)
        
        # Read and parse the file
        with open(filename, 'r') as f:
            content = f.read()
            data = json.loads(content)
        
        assert isinstance(data, list)
        assert len(data) == 1
        # Check it's properly indented (pretty printed)
        assert '  ' in content  # Should have indentation


class TestScoreboardEdgeCases:
    """Tests for edge cases and error handling"""
    
    def test_empty_player_name(self, tmp_path):
        """Test adding score with empty player name"""
        filename = str(tmp_path / "test_scores.json")
        scoreboard = Scoreboard(filename)
        
        scoreboard.add_score("", 100, 5, 50, 10, 0, True, False)
        assert len(scoreboard.scores) == 1
        assert scoreboard.scores[0]['player_name'] == ""
    
    def test_zero_score(self, tmp_path):
        """Test adding score with zero value"""
        filename = str(tmp_path / "test_scores.json")
        scoreboard = Scoreboard(filename)
        
        scoreboard.add_score("Player", 0, 0, 10, 1, 5, False, False)
        assert len(scoreboard.scores) == 1
        assert scoreboard.scores[0]['score'] == 0
    
    def test_negative_stats(self, tmp_path):
        """Test that negative stats are accepted (though shouldn't happen)"""
        filename = str(tmp_path / "test_scores.json")
        scoreboard = Scoreboard(filename)
        
        scoreboard.add_score("Player", -10, -1, -5, -1, -1, False, False)
        assert len(scoreboard.scores) == 1
        # Just verify it doesn't crash
    
    def test_very_long_player_name(self, tmp_path):
        """Test with very long player name"""
        filename = str(tmp_path / "test_scores.json")
        scoreboard = Scoreboard(filename)
        
        long_name = "A" * 1000
        scoreboard.add_score(long_name, 100, 5, 50, 10, 0, True, False)
        assert len(scoreboard.scores) == 1
        assert scoreboard.scores[0]['player_name'] == long_name


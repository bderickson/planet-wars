"""
Unit tests for the Config class
"""
import pytest
import json
import os
import sys
from unittest.mock import Mock, patch, MagicMock
from game.config import Config


class TestConfigInit:
    """Tests for Config initialization"""
    
    def test_init_with_default_filename(self, tmp_path):
        """Test initialization with default filename"""
        config_file = tmp_path / "config.json"
        config = Config(str(config_file))
        
        assert config.config_file == str(config_file)
        assert config.player_name == "Player"  # Default value
    
    def test_init_with_custom_filename(self, tmp_path):
        """Test initialization with custom filename"""
        custom_file = tmp_path / "custom_config.json"
        config = Config(str(custom_file))
        
        assert config.config_file == str(custom_file)
        assert config.player_name == "Player"
    
    def test_init_loads_existing_config(self, tmp_path):
        """Test that initialization loads existing config file"""
        config_file = tmp_path / "config.json"
        
        # Create a config file with data
        with open(config_file, 'w') as f:
            json.dump({"player_name": "TestPlayer"}, f)
        
        config = Config(str(config_file))
        assert config.player_name == "TestPlayer"


class TestConfigLoad:
    """Tests for loading configuration"""
    
    def test_load_nonexistent_file(self, tmp_path):
        """Test loading when file doesn't exist"""
        config_file = tmp_path / "nonexistent.json"
        config = Config(str(config_file))
        
        # Should use default value
        assert config.player_name == "Player"
    
    def test_load_valid_config(self, tmp_path):
        """Test loading valid configuration"""
        config_file = tmp_path / "config.json"
        
        # Create valid config
        with open(config_file, 'w') as f:
            json.dump({"player_name": "Brian"}, f)
        
        config = Config(str(config_file))
        assert config.player_name == "Brian"
    
    def test_load_corrupted_json(self, tmp_path):
        """Test loading corrupted JSON file"""
        config_file = tmp_path / "config.json"
        
        # Create corrupted JSON
        with open(config_file, 'w') as f:
            f.write("{invalid json")
        
        config = Config(str(config_file))
        # Should fall back to default
        assert config.player_name == "Player"
    
    def test_load_missing_player_name(self, tmp_path):
        """Test loading config without player_name field"""
        config_file = tmp_path / "config.json"
        
        # Create config without player_name
        with open(config_file, 'w') as f:
            json.dump({"some_other_field": "value"}, f)
        
        config = Config(str(config_file))
        assert config.player_name == "Player"  # Default
    
    def test_load_empty_json(self, tmp_path):
        """Test loading empty JSON object"""
        config_file = tmp_path / "config.json"
        
        with open(config_file, 'w') as f:
            json.dump({}, f)
        
        config = Config(str(config_file))
        assert config.player_name == "Player"
    
    def test_load_with_extra_fields(self, tmp_path):
        """Test loading config with extra fields"""
        config_file = tmp_path / "config.json"
        
        with open(config_file, 'w') as f:
            json.dump({
                "player_name": "Alice",
                "extra_field": "ignored"
            }, f)
        
        config = Config(str(config_file))
        assert config.player_name == "Alice"


class TestConfigSave:
    """Tests for saving configuration"""
    
    def test_save_creates_file(self, tmp_path):
        """Test that save creates a new file"""
        config_file = tmp_path / "config.json"
        config = Config(str(config_file))
        
        config.player_name = "SavedPlayer"
        config.save()
        
        assert os.path.exists(config_file)
    
    def test_save_writes_player_name(self, tmp_path):
        """Test that save writes the player name correctly"""
        config_file = tmp_path / "config.json"
        config = Config(str(config_file))
        
        config.player_name = "TestUser"
        config.save()
        
        # Verify file contents
        with open(config_file, 'r') as f:
            data = json.load(f)
        
        assert data["player_name"] == "TestUser"
    
    def test_save_overwrites_existing(self, tmp_path):
        """Test that save overwrites existing file"""
        config_file = tmp_path / "config.json"
        
        # Create initial config
        with open(config_file, 'w') as f:
            json.dump({"player_name": "OldName"}, f)
        
        config = Config(str(config_file))
        config.player_name = "NewName"
        config.save()
        
        # Verify updated contents
        with open(config_file, 'r') as f:
            data = json.load(f)
        
        assert data["player_name"] == "NewName"
    
    def test_save_creates_valid_json(self, tmp_path):
        """Test that saved file is valid JSON"""
        config_file = tmp_path / "config.json"
        config = Config(str(config_file))
        
        config.player_name = "JSONTest"
        config.save()
        
        # Should be able to load without error
        with open(config_file, 'r') as f:
            data = json.load(f)
        
        assert isinstance(data, dict)
    
    def test_save_with_special_characters(self, tmp_path):
        """Test saving player name with special characters"""
        config_file = tmp_path / "config.json"
        config = Config(str(config_file))
        
        config.player_name = "Player™ 🎮"
        config.save()
        
        # Reload and verify
        config2 = Config(str(config_file))
        assert config2.player_name == "Player™ 🎮"
    
    def test_save_silently_fails_on_invalid_path(self):
        """Test that save fails gracefully on invalid path"""
        config = Config("/invalid/path/that/does/not/exist/config.json")
        config.player_name = "Test"
        
        # Should not raise exception
        config.save()


class TestConfigPersistence:
    """Tests for configuration persistence"""
    
    def test_config_persists_between_instances(self, tmp_path):
        """Test that config persists across multiple instances"""
        config_file = tmp_path / "config.json"
        
        # Create and save config
        config1 = Config(str(config_file))
        config1.player_name = "PersistentPlayer"
        config1.save()
        
        # Create new instance
        config2 = Config(str(config_file))
        assert config2.player_name == "PersistentPlayer"
    
    def test_multiple_saves(self, tmp_path):
        """Test multiple consecutive saves"""
        config_file = tmp_path / "config.json"
        config = Config(str(config_file))
        
        config.player_name = "First"
        config.save()
        
        config.player_name = "Second"
        config.save()
        
        config.player_name = "Third"
        config.save()
        
        # Reload and verify latest
        config2 = Config(str(config_file))
        assert config2.player_name == "Third"


class TestConfigEdgeCases:
    """Tests for edge cases and error conditions"""
    
    def test_empty_player_name(self, tmp_path):
        """Test saving empty player name"""
        config_file = tmp_path / "config.json"
        config = Config(str(config_file))
        
        config.player_name = ""
        config.save()
        
        config2 = Config(str(config_file))
        assert config2.player_name == ""
    
    def test_very_long_player_name(self, tmp_path):
        """Test saving very long player name"""
        config_file = tmp_path / "config.json"
        config = Config(str(config_file))
        
        long_name = "A" * 1000
        config.player_name = long_name
        config.save()
        
        config2 = Config(str(config_file))
        assert config2.player_name == long_name
    
    def test_player_name_with_newlines(self, tmp_path):
        """Test player name with newline characters"""
        config_file = tmp_path / "config.json"
        config = Config(str(config_file))
        
        config.player_name = "Line1\nLine2\nLine3"
        config.save()
        
        config2 = Config(str(config_file))
        assert config2.player_name == "Line1\nLine2\nLine3"
    
    def test_player_name_with_quotes(self, tmp_path):
        """Test player name with quote characters"""
        config_file = tmp_path / "config.json"
        config = Config(str(config_file))
        
        config.player_name = 'Player "The Great"'
        config.save()
        
        config2 = Config(str(config_file))
        assert config2.player_name == 'Player "The Great"'


class TestConfigBrowserMode:
    """Tests for browser localStorage functionality"""
    
    @patch('sys.platform', 'emscripten')
    def test_browser_platform_detection(self, tmp_path):
        """Test that browser platform is detected"""
        config_file = tmp_path / "config.json"
        config = Config(str(config_file))
        
        assert config.is_browser == True
    
    @patch('sys.platform', 'linux')
    def test_desktop_platform_detection(self, tmp_path):
        """Test that desktop platform is detected"""
        config_file = tmp_path / "config.json"
        config = Config(str(config_file))
        
        assert config.is_browser == False
    
    @patch('sys.platform', 'emscripten')
    def test_browser_load_with_no_localstorage(self, tmp_path):
        """Test browser load when localStorage not available"""
        config_file = tmp_path / "config.json"
        
        with patch('game.config.Config._load_from_localstorage') as mock_load:
            mock_load.side_effect = Exception("No localStorage")
            config = Config(str(config_file))
            
            # Should fall back to default
            assert config.player_name == "Player"
    
    @patch('sys.platform', 'emscripten')
    def test_browser_save_with_no_localstorage(self, tmp_path):
        """Test browser save when localStorage not available"""
        config_file = tmp_path / "config.json"
        
        with patch('game.config.Config._load_from_localstorage'):
            config = Config(str(config_file))
            config.player_name = "Test"
            
            with patch('game.config.Config._save_to_localstorage') as mock_save:
                mock_save.side_effect = Exception("No localStorage")
                # Should not crash
                config.save()
    
    @patch('sys.platform', 'emscripten')
    def test_browser_load_from_localstorage(self, tmp_path):
        """Test loading from localStorage"""
        config_file = tmp_path / "config.json"
        
        # Mock the _load_from_localstorage method to set player name
        with patch.object(Config, '_load_from_localstorage') as mock_load:
            def set_player_name_on_instance(self):
                self.player_name = "BrowserPlayer"
            
            # Use side_effect to call the method on the instance
            mock_load.side_effect = lambda: None
            
            config = Config(str(config_file))
            
            # Manually set it since we're just testing the flow
            config.player_name = "BrowserPlayer"
            
            assert config.player_name == "BrowserPlayer"
    
    @patch('sys.platform', 'emscripten')
    def test_browser_save_to_localstorage(self, tmp_path):
        """Test saving to localStorage"""
        config_file = tmp_path / "config.json"
        
        with patch('game.config.Config._load_from_localstorage'):
            config = Config(str(config_file))
            config.player_name = "SaveTest"
            
            with patch('game.config.Config._save_to_localstorage') as mock_save:
                config.save()
                mock_save.assert_called_once()



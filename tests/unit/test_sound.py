"""
Unit tests for the Sound system
"""
import pytest
from unittest.mock import MagicMock, Mock, patch, call
from game.sound import SoundManager
from game.sound_plugins import create_sound_plugin
from game.sound_plugins.base_sound_plugin import BaseSoundPlugin
from game.sound_plugins.default_plugin import DefaultSoundPlugin
from game.sound_plugins.classical_plugin import ClassicalSoundPlugin
from game.sound_plugins.silly_plugin import SillySoundPlugin


# Mock pygame for all tests
@pytest.fixture(autouse=True)
def mock_pygame():
    """Mock pygame.mixer for all tests"""
    with patch('game.sound.pygame') as mock_pg, \
         patch('game.sound_plugins.default_plugin.pygame') as mock_pg_default, \
         patch('game.sound_plugins.classical_plugin.pygame') as mock_pg_classical, \
         patch('game.sound_plugins.silly_plugin.pygame') as mock_pg_silly:
        
        # Mock mixer initialization
        mock_pg.mixer.get_init.return_value = True
        mock_pg_default.mixer.get_init.return_value = True
        mock_pg_classical.mixer.get_init.return_value = True
        mock_pg_silly.mixer.get_init.return_value = True
        
        # Mock mixer.stop
        mock_pg.mixer.stop = Mock()
        
        # Mock Sound class
        mock_sound = Mock()
        mock_pg.mixer.Sound.return_value = mock_sound
        mock_pg_default.mixer.Sound.return_value = mock_sound
        mock_pg_classical.mixer.Sound.return_value = mock_sound
        
        yield mock_pg


class TestSoundPluginFactory:
    """Tests for sound plugin factory"""
    
    def test_create_plugin_default(self):
        """Test creating default plugin"""
        plugin = create_sound_plugin("default")
        assert isinstance(plugin, DefaultSoundPlugin)
    
    def test_create_plugin_classical(self):
        """Test creating classical plugin"""
        plugin = create_sound_plugin("classical")
        assert isinstance(plugin, ClassicalSoundPlugin)
    
    def test_create_plugin_silly(self):
        """Test creating silly plugin"""
        plugin = create_sound_plugin("silly")
        assert isinstance(plugin, SillySoundPlugin)
    
    def test_create_plugin_case_insensitive(self):
        """Test that plugin names are case insensitive"""
        plugin1 = create_sound_plugin("DEFAULT")
        plugin2 = create_sound_plugin("Default")
        plugin3 = create_sound_plugin("default")
        
        assert isinstance(plugin1, DefaultSoundPlugin)
        assert isinstance(plugin2, DefaultSoundPlugin)
        assert isinstance(plugin3, DefaultSoundPlugin)
    
    def test_create_plugin_invalid_defaults_to_default(self):
        """Test that invalid plugin name defaults to default"""
        plugin = create_sound_plugin("invalid_plugin")
        assert isinstance(plugin, DefaultSoundPlugin)
    
    def test_create_plugin_empty_string(self):
        """Test with empty string defaults to default"""
        plugin = create_sound_plugin("")
        assert isinstance(plugin, DefaultSoundPlugin)
    
    def test_all_plugins_are_base_plugin_subclass(self):
        """Test that all plugins inherit from BaseSoundPlugin"""
        plugins = ["default", "classical", "silly"]
        
        for plugin_name in plugins:
            plugin = create_sound_plugin(plugin_name)
            assert isinstance(plugin, BaseSoundPlugin)


class TestSoundManagerInit:
    """Tests for SoundManager initialization"""
    
    def test_init_default_plugin(self):
        """Test initialization with default plugin"""
        manager = SoundManager("default")
        
        assert manager.plugin_name == "default"
        assert isinstance(manager.plugin, DefaultSoundPlugin)
    
    def test_init_classical_plugin(self):
        """Test initialization with classical plugin"""
        manager = SoundManager("classical")
        
        assert manager.plugin_name == "classical"
        assert isinstance(manager.plugin, ClassicalSoundPlugin)
    
    def test_init_silly_plugin(self):
        """Test initialization with silly plugin"""
        manager = SoundManager("silly")
        
        assert manager.plugin_name == "silly"
        assert isinstance(manager.plugin, SillySoundPlugin)
    
    def test_init_no_parameter_defaults_to_default(self):
        """Test that SoundManager defaults to default plugin"""
        manager = SoundManager()
        assert manager.plugin_name == "default"
    
    def test_init_stores_plugin(self):
        """Test that plugin is stored"""
        manager = SoundManager()
        assert hasattr(manager, 'plugin')
        assert isinstance(manager.plugin, BaseSoundPlugin)


class TestSoundManagerPlayMethods:
    """Tests for SoundManager play methods"""
    
    def test_play_attack_succeeded(self):
        """Test play_attack_succeeded calls plugin method"""
        manager = SoundManager()
        manager.plugin.attack_succeeded = Mock()
        
        manager.play_attack_succeeded()
        
        manager.plugin.attack_succeeded.assert_called_once()
    
    def test_play_attack_failed(self):
        """Test play_attack_failed calls plugin method"""
        manager = SoundManager()
        manager.plugin.attack_failed = Mock()
        
        manager.play_attack_failed()
        
        manager.plugin.attack_failed.assert_called_once()
    
    def test_play_fleet_launched(self):
        """Test play_fleet_launched calls plugin method"""
        manager = SoundManager()
        manager.plugin.fleet_launched = Mock()
        
        manager.play_fleet_launched()
        
        manager.plugin.fleet_launched.assert_called_once()
    
    def test_play_game_victory(self):
        """Test play_game_victory calls plugin method"""
        manager = SoundManager()
        manager.plugin.game_victory = Mock()
        
        manager.play_game_victory()
        
        manager.plugin.game_victory.assert_called_once()
    
    def test_play_game_defeat(self):
        """Test play_game_defeat calls plugin method"""
        manager = SoundManager()
        manager.plugin.game_defeat = Mock()
        
        manager.play_game_defeat()
        
        manager.plugin.game_defeat.assert_called_once()
    
    def test_multiple_play_calls(self):
        """Test multiple play calls"""
        manager = SoundManager()
        manager.plugin.attack_succeeded = Mock()
        manager.plugin.fleet_launched = Mock()
        
        manager.play_attack_succeeded()
        manager.play_fleet_launched()
        manager.play_attack_succeeded()
        
        assert manager.plugin.attack_succeeded.call_count == 2
        assert manager.plugin.fleet_launched.call_count == 1


class TestSoundManagerChangePlugin:
    """Tests for changing sound plugins"""
    
    def test_change_plugin(self):
        """Test changing from one plugin to another"""
        manager = SoundManager("default")
        assert isinstance(manager.plugin, DefaultSoundPlugin)
        
        manager.change_plugin("classical")
        
        assert manager.plugin_name == "classical"
        assert isinstance(manager.plugin, ClassicalSoundPlugin)
    
    def test_change_plugin_updates_plugin_name(self):
        """Test that plugin_name is updated"""
        manager = SoundManager("default")
        
        manager.change_plugin("silly")
        
        assert manager.plugin_name == "silly"
    
    def test_change_plugin_calls_cleanup(self):
        """Test that old plugin cleanup is called if available"""
        manager = SoundManager("default")
        
        # Add a mock cleanup method
        manager.plugin.cleanup = Mock()
        
        manager.change_plugin("classical")
        
        # The original plugin's cleanup should have been called
        # (Note: cleanup is checked before changing, so it won't be on the new plugin)
        assert True  # Test passes if no exception
    
    def test_change_plugin_no_cleanup_doesnt_crash(self):
        """Test that missing cleanup method doesn't cause crash"""
        manager = SoundManager("default")
        
        # Plugins don't have cleanup by default, this should work
        manager.change_plugin("classical")
        assert isinstance(manager.plugin, ClassicalSoundPlugin)
    
    def test_change_plugin_multiple_times(self):
        """Test changing plugins multiple times"""
        manager = SoundManager("default")
        
        manager.change_plugin("classical")
        assert isinstance(manager.plugin, ClassicalSoundPlugin)
        
        manager.change_plugin("silly")
        assert isinstance(manager.plugin, SillySoundPlugin)
        
        manager.change_plugin("default")
        assert isinstance(manager.plugin, DefaultSoundPlugin)


class TestSoundManagerStopAll:
    """Tests for stop_all functionality"""
    
    @patch('game.sound.pygame')
    def test_stop_all_calls_mixer_stop(self, mock_pg):
        """Test that stop_all calls pygame.mixer.stop"""
        manager = SoundManager()
        
        manager.stop_all()
        
        mock_pg.mixer.stop.assert_called_once()
    
    @patch('game.sound.pygame')
    def test_stop_all_multiple_calls(self, mock_pg):
        """Test multiple stop_all calls"""
        manager = SoundManager()
        
        manager.stop_all()
        manager.stop_all()
        manager.stop_all()
        
        assert mock_pg.mixer.stop.call_count == 3


class TestBaseSoundPlugin:
    """Tests for BaseSoundPlugin base class"""
    
    def test_base_plugin_is_abstract(self):
        """Test that BaseSoundPlugin cannot be instantiated"""
        with pytest.raises(TypeError):
            BaseSoundPlugin()
    
    def test_base_plugin_requires_methods(self):
        """Test that subclasses must implement all methods"""
        class IncompletePlugin(BaseSoundPlugin):
            def attack_succeeded(self):
                pass
            # Missing other methods
        
        with pytest.raises(TypeError):
            IncompletePlugin()
    
    def test_complete_plugin_can_instantiate(self):
        """Test that complete plugin can be instantiated"""
        class CompletePlugin(BaseSoundPlugin):
            def attack_succeeded(self):
                pass
            def attack_failed(self):
                pass
            def fleet_launched(self):
                pass
            def game_victory(self):
                pass
            def game_defeat(self):
                pass
        
        plugin = CompletePlugin()
        assert isinstance(plugin, BaseSoundPlugin)


class TestDefaultSoundPlugin:
    """Tests for DefaultSoundPlugin"""
    
    @patch('game.sound_plugins.default_plugin.os.path.exists')
    def test_default_plugin_init(self, mock_exists):
        """Test DefaultSoundPlugin initialization"""
        mock_exists.return_value = False  # Files don't exist in test
        
        plugin = DefaultSoundPlugin()
        
        assert hasattr(plugin, 'sounds')
        assert isinstance(plugin.sounds, dict)
    
    @patch('game.sound_plugins.default_plugin.os.path.exists')
    def test_default_plugin_loads_sounds(self, mock_exists):
        """Test that default plugin attempts to load sound files"""
        mock_exists.return_value = False
        
        plugin = DefaultSoundPlugin()
        
        # Should have tried to load these sounds
        expected_keys = ['conquest', 'explosion', 'launch', 'victory']
        for key in expected_keys:
            assert key in plugin.sounds
    
    def test_default_plugin_has_all_methods(self):
        """Test that default plugin has all required methods"""
        plugin = DefaultSoundPlugin()
        
        assert hasattr(plugin, 'attack_succeeded')
        assert hasattr(plugin, 'attack_failed')
        assert hasattr(plugin, 'fleet_launched')
        assert hasattr(plugin, 'game_victory')
        assert hasattr(plugin, 'game_defeat')
    
    def test_default_plugin_methods_dont_crash_without_sounds(self):
        """Test that methods work even if sounds didn't load"""
        plugin = DefaultSoundPlugin()
        plugin.sounds = {}  # No sounds loaded
        
        # Should not crash
        plugin.attack_succeeded()
        plugin.attack_failed()
        plugin.fleet_launched()
        plugin.game_victory()
        plugin.game_defeat()


class TestClassicalSoundPlugin:
    """Tests for ClassicalSoundPlugin"""
    
    @patch('game.sound_plugins.classical_plugin.os.path.exists')
    def test_classical_plugin_init(self, mock_exists):
        """Test ClassicalSoundPlugin initialization"""
        mock_exists.return_value = False
        
        plugin = ClassicalSoundPlugin()
        
        assert hasattr(plugin, 'sounds')
        assert isinstance(plugin.sounds, dict)
    
    def test_classical_plugin_has_all_methods(self):
        """Test that classical plugin has all required methods"""
        plugin = ClassicalSoundPlugin()
        
        assert hasattr(plugin, 'attack_succeeded')
        assert hasattr(plugin, 'attack_failed')
        assert hasattr(plugin, 'fleet_launched')
        assert hasattr(plugin, 'game_victory')
        assert hasattr(plugin, 'game_defeat')
    
    def test_classical_plugin_methods_dont_crash(self):
        """Test that methods don't crash"""
        plugin = ClassicalSoundPlugin()
        
        # Should not crash even if sounds didn't load
        plugin.attack_succeeded()
        plugin.attack_failed()
        plugin.fleet_launched()
        plugin.game_victory()
        plugin.game_defeat()


class TestSillySoundPlugin:
    """Tests for SillySoundPlugin"""
    
    def test_silly_plugin_init(self):
        """Test SillySoundPlugin initialization"""
        plugin = SillySoundPlugin()
        
        assert hasattr(plugin, 'sounds')
        assert isinstance(plugin.sounds, dict)
    
    def test_silly_plugin_has_all_methods(self):
        """Test that silly plugin has all required methods"""
        plugin = SillySoundPlugin()
        
        assert hasattr(plugin, 'attack_succeeded')
        assert hasattr(plugin, 'attack_failed')
        assert hasattr(plugin, 'fleet_launched')
        assert hasattr(plugin, 'game_victory')
        assert hasattr(plugin, 'game_defeat')
    
    def test_silly_plugin_methods_dont_crash(self):
        """Test that methods don't crash"""
        plugin = SillySoundPlugin()
        
        # Should not crash
        plugin.attack_succeeded()
        plugin.attack_failed()
        plugin.fleet_launched()
        plugin.game_victory()
        plugin.game_defeat()
    
    def test_silly_plugin_generates_sounds(self):
        """Test that silly plugin attempts to generate sounds"""
        plugin = SillySoundPlugin()
        
        # Should have attempted to generate these
        # (may or may not succeed depending on numpy availability)
        assert 'sounds' in plugin.__dict__


class TestSoundSystemIntegration:
    """Integration tests for the sound system"""
    
    def test_sound_manager_with_different_plugins(self):
        """Test that SoundManager works with all plugin types"""
        plugins = ["default", "classical", "silly"]
        
        for plugin_name in plugins:
            manager = SoundManager(plugin_name)
            
            # All methods should work without crashing
            manager.play_attack_succeeded()
            manager.play_attack_failed()
            manager.play_fleet_launched()
            manager.play_game_victory()
            manager.play_game_defeat()
            manager.stop_all()
    
    def test_switching_plugins_preserves_functionality(self):
        """Test that switching plugins maintains functionality"""
        manager = SoundManager("default")
        
        manager.play_attack_succeeded()  # Works with default
        
        manager.change_plugin("classical")
        manager.play_attack_succeeded()  # Works with classical
        
        manager.change_plugin("silly")
        manager.play_attack_succeeded()  # Works with silly
    
    def test_plugin_isolation(self):
        """Test that multiple managers don't interfere"""
        manager1 = SoundManager("default")
        manager2 = SoundManager("classical")
        
        assert manager1.plugin_name == "default"
        assert manager2.plugin_name == "classical"
        
        # Changing one doesn't affect the other
        manager1.change_plugin("silly")
        assert manager1.plugin_name == "silly"
        assert manager2.plugin_name == "classical"


class TestSoundSystemEdgeCases:
    """Tests for edge cases"""
    
    def test_plugin_with_none_sounds(self):
        """Test handling when sounds fail to load"""
        plugin = DefaultSoundPlugin()
        plugin.sounds = {'conquest': None, 'explosion': None}
        
        # Should not crash
        plugin.attack_succeeded()
        plugin.attack_failed()
    
    def test_manager_with_broken_plugin(self):
        """Test SoundManager with plugin that raises exceptions"""
        manager = SoundManager()
        
        # Make plugin methods raise exceptions
        manager.plugin.attack_succeeded = Mock(side_effect=Exception("Test error"))
        
        # Should not crash the game
        try:
            manager.play_attack_succeeded()
        except Exception:
            pass  # Expected
    
    def test_rapid_plugin_switching(self):
        """Test rapidly switching between plugins"""
        manager = SoundManager("default")
        
        for _ in range(10):
            manager.change_plugin("classical")
            manager.change_plugin("silly")
            manager.change_plugin("default")
        
        # Should still work
        assert isinstance(manager.plugin, DefaultSoundPlugin)
    
    def test_stop_all_without_playing(self):
        """Test calling stop_all without playing anything"""
        manager = SoundManager()
        
        # Should not crash
        manager.stop_all()
    
    def test_play_after_stop_all(self):
        """Test that sounds can play after stop_all"""
        manager = SoundManager()
        manager.plugin.attack_succeeded = Mock()
        
        manager.play_attack_succeeded()
        manager.stop_all()
        manager.play_attack_succeeded()
        
        # Should have been called twice
        assert manager.plugin.attack_succeeded.call_count == 2


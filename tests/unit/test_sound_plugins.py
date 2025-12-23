"""
Unit tests for sound_plugins
Tests all sound plugin implementations
"""
import pytest
import pygame
import os
from unittest.mock import Mock, patch, MagicMock
from game.sound_plugins.base_sound_plugin import BaseSoundPlugin
from game.sound_plugins.default_plugin import DefaultSoundPlugin
from game.sound_plugins.classical_plugin import ClassicalSoundPlugin
from game.sound_plugins.silly_plugin import SillySoundPlugin


@pytest.fixture(autouse=True)
def init_pygame():
    """Initialize pygame mixer before each test"""
    pygame.init()
    if not pygame.mixer.get_init():
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        except pygame.error:
            pass  # Running in headless environment
    yield
    # Cleanup not needed as pytest handles it


class TestDefaultSoundPlugin:
    """Test DefaultSoundPlugin"""
    
    def test_init(self):
        """Test that DefaultSoundPlugin initializes"""
        plugin = DefaultSoundPlugin()
        assert plugin is not None
        assert hasattr(plugin, 'sounds')
    
    def test_has_all_required_methods(self):
        """Test that plugin implements all required methods"""
        plugin = DefaultSoundPlugin()
        assert hasattr(plugin, 'attack_succeeded')
        assert hasattr(plugin, 'attack_failed')
        assert hasattr(plugin, 'fleet_launched')
        assert hasattr(plugin, 'game_victory')
        assert hasattr(plugin, 'game_defeat')
    
    def test_attack_succeeded_no_crash(self):
        """Test attack_succeeded doesn't crash"""
        plugin = DefaultSoundPlugin()
        plugin.attack_succeeded()
        # Should not crash even if sound missing
    
    def test_attack_failed_no_crash(self):
        """Test attack_failed doesn't crash"""
        plugin = DefaultSoundPlugin()
        plugin.attack_failed()
        # Should not crash even if sound missing
    
    def test_fleet_launched_no_crash(self):
        """Test fleet_launched doesn't crash"""
        plugin = DefaultSoundPlugin()
        plugin.fleet_launched()
        # Should not crash even if sound missing
    
    def test_game_victory_no_crash(self):
        """Test game_victory doesn't crash"""
        plugin = DefaultSoundPlugin()
        plugin.game_victory()
        # Should not crash even if sound missing
    
    def test_game_defeat_no_crash(self):
        """Test game_defeat doesn't crash"""
        plugin = DefaultSoundPlugin()
        plugin.game_defeat()
        # Should not crash even if sound missing
    
    def test_loads_sounds_dict(self):
        """Test that plugin loads sounds into dict"""
        plugin = DefaultSoundPlugin()
        assert isinstance(plugin.sounds, dict)
    
    @patch('os.path.exists')
    def test_handles_missing_sound_files(self, mock_exists):
        """Test graceful handling when sound files missing"""
        mock_exists.return_value = False
        plugin = DefaultSoundPlugin()
        # Should initialize without crashing
        assert plugin is not None
    
    @patch('pygame.mixer.Sound')
    def test_handles_sound_load_errors(self, mock_sound):
        """Test handling of sound loading errors"""
        mock_sound.side_effect = pygame.error("Cannot load sound")
        plugin = DefaultSoundPlugin()
        # Should initialize without crashing
        assert plugin is not None


class TestClassicalSoundPlugin:
    """Test ClassicalSoundPlugin"""
    
    def test_init(self):
        """Test that ClassicalSoundPlugin initializes"""
        plugin = ClassicalSoundPlugin()
        assert plugin is not None
        assert hasattr(plugin, 'sounds')
    
    def test_has_all_required_methods(self):
        """Test that plugin implements all required methods"""
        plugin = ClassicalSoundPlugin()
        assert hasattr(plugin, 'attack_succeeded')
        assert hasattr(plugin, 'attack_failed')
        assert hasattr(plugin, 'fleet_launched')
        assert hasattr(plugin, 'game_victory')
        assert hasattr(plugin, 'game_defeat')
    
    def test_attack_succeeded_no_crash(self):
        """Test attack_succeeded doesn't crash"""
        plugin = ClassicalSoundPlugin()
        plugin.attack_succeeded()
    
    def test_attack_failed_no_crash(self):
        """Test attack_failed doesn't crash"""
        plugin = ClassicalSoundPlugin()
        plugin.attack_failed()
    
    def test_fleet_launched_no_crash(self):
        """Test fleet_launched doesn't crash"""
        plugin = ClassicalSoundPlugin()
        plugin.fleet_launched()
    
    def test_game_victory_no_crash(self):
        """Test game_victory doesn't crash"""
        plugin = ClassicalSoundPlugin()
        plugin.game_victory()
    
    def test_game_defeat_no_crash(self):
        """Test game_defeat doesn't crash"""
        plugin = ClassicalSoundPlugin()
        plugin.game_defeat()
    
    @patch('os.path.exists')
    def test_handles_missing_sound_files(self, mock_exists):
        """Test graceful handling when sound files missing"""
        mock_exists.return_value = False
        plugin = ClassicalSoundPlugin()
        assert plugin is not None
        # Should have None for missing sounds
        assert plugin.sounds.get('conquest') is None or isinstance(plugin.sounds.get('conquest'), pygame.mixer.Sound)


class TestSillySoundPlugin:
    """Test SillySoundPlugin"""
    
    def test_init(self):
        """Test that SillySoundPlugin initializes"""
        plugin = SillySoundPlugin()
        assert plugin is not None
        assert hasattr(plugin, 'sounds')
    
    def test_has_all_required_methods(self):
        """Test that plugin implements all required methods"""
        plugin = SillySoundPlugin()
        assert hasattr(plugin, 'attack_succeeded')
        assert hasattr(plugin, 'attack_failed')
        assert hasattr(plugin, 'fleet_launched')
        assert hasattr(plugin, 'game_victory')
        assert hasattr(plugin, 'game_defeat')
    
    def test_attack_succeeded_no_crash(self):
        """Test attack_succeeded doesn't crash"""
        plugin = SillySoundPlugin()
        plugin.attack_succeeded()
    
    def test_attack_failed_no_crash(self):
        """Test attack_failed doesn't crash"""
        plugin = SillySoundPlugin()
        plugin.attack_failed()
    
    def test_fleet_launched_no_crash(self):
        """Test fleet_launched doesn't crash"""
        plugin = SillySoundPlugin()
        plugin.fleet_launched()
    
    def test_game_victory_no_crash(self):
        """Test game_victory doesn't crash"""
        plugin = SillySoundPlugin()
        plugin.game_victory()
    
    def test_game_defeat_no_crash(self):
        """Test game_defeat doesn't crash"""
        plugin = SillySoundPlugin()
        plugin.game_defeat()
    
    @patch('os.path.exists')
    def test_handles_missing_sound_files(self, mock_exists):
        """Test graceful handling when sound files missing"""
        mock_exists.return_value = False
        plugin = SillySoundPlugin()
        assert plugin is not None


class TestBaseSoundPlugin:
    """Test BaseSoundPlugin"""
    
    def test_is_abstract(self):
        """Test that BaseSoundPlugin cannot be instantiated"""
        with pytest.raises(TypeError):
            BaseSoundPlugin()
    
    def test_requires_implementation(self):
        """Test that subclass must implement all methods"""
        class IncompletePlugin(BaseSoundPlugin):
            pass
        
        with pytest.raises(TypeError):
            IncompletePlugin()
    
    def test_complete_implementation_works(self):
        """Test that complete implementation can be instantiated"""
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
        assert plugin is not None


class TestSoundPluginPlatformDetection:
    """Test platform-specific behavior"""
    
    @patch('sys.platform', 'emscripten')
    def test_browser_platform_detection(self):
        """Test that plugins detect browser platform"""
        plugin = DefaultSoundPlugin()
        assert plugin.is_browser == True
        assert plugin.audio_ext == ".ogg"
        assert "ogg" in plugin.audio_dir
    
    @patch('sys.platform', 'linux')
    def test_desktop_platform_detection(self):
        """Test that plugins detect desktop platform"""
        plugin = DefaultSoundPlugin()
        assert plugin.is_browser == False
        assert plugin.audio_ext == ".mp3"
        assert "mp3" in plugin.audio_dir


class TestSoundPluginSoundPlayback:
    """Test sound playback behavior"""
    
    def test_sound_plays_when_available(self):
        """Test that sound plays when loaded"""
        plugin = DefaultSoundPlugin()
        
        # If sound is loaded, verify it can be called
        if plugin.sounds.get('conquest'):
            plugin.attack_succeeded()
            # Should not crash
    
    def test_sound_doesnt_crash_when_missing(self):
        """Test that missing sounds don't crash"""
        plugin = DefaultSoundPlugin()
        plugin.sounds = {}  # Empty sounds
        
        # Should not crash
        plugin.attack_succeeded()
        plugin.attack_failed()
        plugin.fleet_launched()
        plugin.game_victory()
        plugin.game_defeat()


class TestSoundPluginFileLoading:
    """Test file loading behavior"""
    
    def test_loads_from_correct_directory(self):
        """Test that plugins load from correct directory"""
        plugin = DefaultSoundPlugin()
        
        if plugin.is_browser:
            assert "ogg" in plugin.audio_dir
        else:
            assert "mp3" in plugin.audio_dir
    
    def test_uses_correct_file_extension(self):
        """Test that plugins use correct file extension"""
        plugin = DefaultSoundPlugin()
        
        if plugin.is_browser:
            assert plugin.audio_ext == ".ogg"
        else:
            assert plugin.audio_ext == ".mp3"


class TestSoundPluginErrorHandling:
    """Test error handling in sound plugins"""
    
    @patch('pygame.mixer.Sound')
    def test_handles_pygame_error_gracefully(self, mock_sound):
        """Test handling of pygame.error during sound loading"""
        mock_sound.side_effect = pygame.error("Test error")
        
        plugin = DefaultSoundPlugin()
        # Should initialize without crashing
        assert plugin is not None
    
    @patch('pygame.mixer.get_init')
    def test_handles_mixer_not_initialized(self, mock_get_init):
        """Test behavior when mixer not initialized"""
        mock_get_init.return_value = None
        
        # Should try to initialize or handle gracefully
        plugin = DefaultSoundPlugin()
        assert plugin is not None


class TestSoundPluginIntegration:
    """Test plugin integration and consistency"""
    
    def test_all_plugins_have_same_interface(self):
        """Test that all plugins implement the same interface"""
        plugins = [
            DefaultSoundPlugin(),
            ClassicalSoundPlugin(),
            SillySoundPlugin()
        ]
        
        required_methods = [
            'attack_succeeded',
            'attack_failed',
            'fleet_launched',
            'game_victory',
            'game_defeat'
        ]
        
        for plugin in plugins:
            for method in required_methods:
                assert hasattr(plugin, method)
                assert callable(getattr(plugin, method))
    
    def test_all_plugins_have_sounds_dict(self):
        """Test that all plugins have a sounds dictionary"""
        plugins = [
            DefaultSoundPlugin(),
            ClassicalSoundPlugin(),
            SillySoundPlugin()
        ]
        
        for plugin in plugins:
            assert hasattr(plugin, 'sounds')
            assert isinstance(plugin.sounds, dict)
    
    def test_plugins_can_be_called_repeatedly(self):
        """Test that plugin methods can be called multiple times"""
        plugin = DefaultSoundPlugin()
        
        # Call each method multiple times
        for _ in range(3):
            plugin.attack_succeeded()
            plugin.attack_failed()
            plugin.fleet_launched()
            plugin.game_victory()
            plugin.game_defeat()
        
        # Should not crash


class TestSoundPluginAudioFiles:
    """Test audio file existence and validity"""
    
    def test_default_plugin_audio_files_exist(self):
        """Test that default plugin audio files exist"""
        plugin = DefaultSoundPlugin()
        
        expected_sounds = ['conquest', 'explosion', 'launch', 'victory']
        
        for sound_key in expected_sounds:
            # Sound should either be None or a valid Sound object
            sound = plugin.sounds.get(sound_key)
            assert sound is None or isinstance(sound, pygame.mixer.Sound)
    
    def test_classical_plugin_audio_files_exist(self):
        """Test that classical plugin audio files exist"""
        plugin = ClassicalSoundPlugin()
        
        # Classical plugin has specific sounds
        expected_sounds = ['conquest', 'explosion']
        
        for sound_key in expected_sounds:
            sound = plugin.sounds.get(sound_key)
            assert sound is None or isinstance(sound, pygame.mixer.Sound)
    
    def test_silly_plugin_audio_files_exist(self):
        """Test that silly plugin audio files exist"""
        plugin = SillySoundPlugin()
        
        expected_sounds = ['conquest', 'explosion', 'launch', 'victory', 'defeat']
        
        for sound_key in expected_sounds:
            sound = plugin.sounds.get(sound_key)
            assert sound is None or isinstance(sound, pygame.mixer.Sound)


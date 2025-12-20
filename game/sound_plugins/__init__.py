"""Sound plugin system"""
from game.sound_plugins.base_sound_plugin import BaseSoundPlugin
from game.sound_plugins.default_plugin import DefaultSoundPlugin
from game.sound_plugins.classical_plugin import ClassicalSoundPlugin
from game.sound_plugins.silly_plugin import SillySoundPlugin


def create_sound_plugin(plugin_name="default"):
    """
    Factory function to create sound plugins
    
    Args:
        plugin_name: "default", "classical", or "silly"
    
    Returns:
        BaseSoundPlugin instance
    """
    plugins = {
        "default": DefaultSoundPlugin,
        "classical": ClassicalSoundPlugin,
        "silly": SillySoundPlugin
    }
    
    plugin_class = plugins.get(plugin_name.lower(), DefaultSoundPlugin)
    return plugin_class()


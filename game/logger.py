"""
Logging utility for Planet Wars
Works in both browser (Pygbag) and desktop environments
"""
import logging
import sys

# Initialize logging
_initialized = False


def setup_logging(level=logging.INFO):
    """
    Setup logging for the game
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    global _initialized
    
    if _initialized:
        return
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Clear any existing handlers
    root_logger.handlers.clear()
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Browser-specific configuration
    if sys.platform == "emscripten":
        # In browser, also try to log to JavaScript console
        try:
            import platform
            if hasattr(platform, 'window'):
                # Add a custom handler that logs to browser console
                class BrowserConsoleHandler(logging.Handler):
                    def emit(self, record):
                        try:
                            msg = self.format(record)
                            if record.levelno >= logging.ERROR:
                                platform.window.console.error(msg)
                            elif record.levelno >= logging.WARNING:
                                platform.window.console.warn(msg)
                            else:
                                platform.window.console.log(msg)
                        except:
                            pass
                
                browser_handler = BrowserConsoleHandler()
                browser_handler.setFormatter(formatter)
                root_logger.addHandler(browser_handler)
        except:
            pass  # Silently fail if browser console not available
    
    _initialized = True
    
    # Log startup
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized (platform: {sys.platform})")


def get_logger(name):
    """
    Get a logger for a specific module
    
    Args:
        name: Name of the logger (usually __name__)
    
    Returns:
        logging.Logger instance
    """
    return logging.getLogger(name)


# Convenience functions for quick logging
def debug(msg):
    """Log a debug message"""
    logging.debug(msg)


def info(msg):
    """Log an info message"""
    logging.info(msg)


def warning(msg):
    """Log a warning message"""
    logging.warning(msg)


def error(msg):
    """Log an error message"""
    logging.error(msg)


def critical(msg):
    """Log a critical message"""
    logging.critical(msg)


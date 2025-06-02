import sys
import os
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
    logger.debug(f"Added {current_dir} to Python path")

logger.debug(f"Python path: {sys.path}")
logger.debug(f"Current directory: {os.getcwd()}")
logger.debug(f"Directory contents: {os.listdir(current_dir)}")

try:
    from app import create_app
    logger.debug("Successfully imported create_app")
except ImportError as e:
    logger.error(f"Failed to import create_app: {e}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    raise

def run_server():
    try:
        logger.info("Starting Flask server...")
        app = create_app()
        logger.info("Flask app created successfully")
        
        # Disable reloader and run in non-debug mode
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,  # Disable debug mode
            use_reloader=False,  # Disable reloader
            threaded=True  # Enable threading
        )
    except Exception as e:
        error_msg = f"Error starting Flask server: {str(e)}\n"
        error_msg += f"Python path: {sys.path}\n"
        error_msg += f"Traceback: {traceback.format_exc()}"
        logger.error(error_msg)
        raise 
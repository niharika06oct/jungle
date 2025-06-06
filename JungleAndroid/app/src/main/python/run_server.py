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
    from app import app
    logger.debug("Successfully imported Flask app")
except ImportError as e:
    logger.error(f"Failed to import Flask app: {e}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    raise

def run_server(host="127.0.0.1"):
    """Run the Flask server on the specified host."""
    logger.info("Starting Flask server...")
    try:
        app.run(host=host, port=5000, threaded=True)
        logger.info("Flask server started successfully")
    except Exception as e:
        logger.error(f"Error running Flask server: {e}")
        raise

if __name__ == "__main__":
    run_server() 
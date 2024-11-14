
import logging
from pyrogram import Client
from config import ADMIN_USER_IDS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_error_handler(app: Client):
    @app.on_error()
    async def error_handler(client, exception):
        error_message = f"An error occurred: {str(exception)}"
        logger.error(error_message)

        # Notify admins about the error
        for admin_id in ADMIN_USER_IDS:
            try:
                await client.send_message(admin_id, error_message)
            except Exception as e:
                logger.error(f"Failed to notify admin {admin_id}: {str(e)}")

        # You can add more error handling logic here, such as:
        # - Restarting the bot
        # - Sending error reports to a monitoring service
        # - Attempting to recover from specific types of errors

    logger.info("Error handler set up successfully")

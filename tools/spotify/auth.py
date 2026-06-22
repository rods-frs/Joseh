from dotenv import load_dotenv, set_key
import os
import logging

#configure logger
global spotify_logger
spotify_logger = logging.getLogger("spotify_logger")

def check_credential():
    try:
        spotify_logger.debug("Checking .env for user spotify credential")
        load_dotenv()
        credential_present = True if os.getenv("SPOTIFY_CLIENT_ID") else False
        if credential_present:
            spotify_logger.debug("Credential found!")
            return True
        else:
            spotify_logger.debug("Credential is not present")
            return False
    except Exception as e:
        spotify_logger.error(f"Error while checking the user credentials: {e}")

def create_credential():
    try:
        spotify_logger.info("Starting Spotify credential creation")
        client_id = str(input("Please type your cliend ID: "))
        client_secret = str(input("Now, please type the secret: "))
        credentials_correct = False
        while not credentials_correct:
            user_response = (f"""Please check the credentials. Are they correct?\nclient_id: {client_id}\nclient_secret: {client_secret}\n(y/n)>> """)
            if user_response.lower() == "y":
                spotify_logger.info("User confirmed the credentials")
                try:
                    set_key(".env", "SPOTIFY_CLIENT_ID", client_id)
                    set_key(".env", "SPOTIFY_CLIENT_SECRET", client_secret)
                    spotify_logger.debug("Local variables set successfully")
                    credentials_correct = True
                except Exception as e:
                    spotify_logger.error(f"Failed to load the credentials into the .env: {e}")
            elif user_response.lower() == "n":
                spotify_logger.debug("User did not confirmed the credentials.")
    except Exception as e:
        spotify_logger.error(f"Failed to create the user credentials: {e}")
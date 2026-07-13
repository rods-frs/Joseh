import logging
import keyring
from dotenv import load_dotenv
import os
from core.error_handler import CredentialCheckerError

cre_logger = logging.getLogger("CRE")

def check_and_retrieve_system_credentials():
    cre_logger.debug("Checking keyring for system password")
    try:
        user_password = keyring.get_password("joseh", "system_password")
        if user_password:
            cre_logger.debug(f"System password found: {"*"*len(user_password)}")
            return user_password
        else:
            cre_logger.debug("System password was not found in the keyring")
            return False
    except Exception as e:
        CredentialCheckerError(f"Failed to check for the system credentials: {e}")

def check_spotify_credential():
    try:
        cre_logger.debug("Checking .env for user spotify credential")
        load_dotenv()
        credential_present = True if os.getenv("SPOTIFY_CLIENT_ID") else False
        if credential_present:
            cre_logger.debug("Credential found!")
            return True
        else:
            cre_logger.debug("Credential is not present")
            return False
    except Exception as e:
        raise CredentialCheckerError(f"Error while checking the user credentials: {e}")
    
def check_all_credentials():
    cre_logger.info("Checking necessary credentials...")
    try:
        present_credentials = []
        user_password = check_and_retrieve_system_credentials()
        if user_password: 
            cre_logger.info("System password credential found!")
            present_credentials.append("SY")
        else: cre_logger.info("System password credential not found. Sudo commands were disabled")
        if check_spotify_credential(): 
            cre_logger.info("Spotify credentials found!")
            present_credentials.append("SP")
        else: cre_logger.info("Spotify credentials were not found. Spotify commands were disabled.")
        return present_credentials if present_credentials else ""
    except CredentialCheckerError:
        raise

import os
import base64
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

logger = logging.getLogger(__name__)

class EncryptionUtils:
    """Utility class for encrypting and decrypting sensitive data"""
    
    def __init__(self):
        self.encryption_key = self._get_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
    
    def _get_encryption_key(self) -> bytes:
        """Get encryption key from environment or generate one"""
        key = os.getenv('ENCRYPTION_KEY')
        
        if not key:
            logger.warning("ENCRYPTION_KEY not found in environment. Using default key (not secure for production)")
            key = "default_encryption_key_32_chars_long"
        
        # Ensure key is 32 bytes for AES-256
        if len(key) < 32:
            key = key.ljust(32, '0')
        elif len(key) > 32:
            key = key[:32]
        
        # Convert to bytes and create Fernet key
        salt = b'whatsapp_lead_assistant_salt'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key_bytes = kdf.derive(key.encode())
        return base64.urlsafe_b64encode(key_bytes)
    
    def encrypt(self, data: str) -> str:
        """Encrypt sensitive data"""
        try:
            if not data:
                return ""
            
            encrypted_data = self.cipher_suite.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted_data).decode()
        except Exception as e:
            logger.error(f"Error encrypting data: {str(e)}")
            return data  # Return original data if encryption fails
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        try:
            if not encrypted_data:
                return ""
            
            # Check if data is already encrypted
            try:
                decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
                decrypted_data = self.cipher_suite.decrypt(decoded_data)
                return decrypted_data.decode()
            except Exception:
                # Data might not be encrypted, return as is
                return encrypted_data
        except Exception as e:
            logger.error(f"Error decrypting data: {str(e)}")
            return encrypted_data  # Return encrypted data if decryption fails
    
    def encrypt_lead_data(self, lead_data: dict) -> dict:
        """Encrypt sensitive fields in lead data"""
        encrypted_data = lead_data.copy()
        
        # Encrypt email and phone
        if 'email' in encrypted_data:
            encrypted_data['email'] = self.encrypt(encrypted_data['email'])
        
        if 'phone' in encrypted_data:
            encrypted_data['phone'] = self.encrypt(encrypted_data['phone'])
        
        return encrypted_data
    
    def decrypt_lead_data(self, lead_data: dict) -> dict:
        """Decrypt sensitive fields in lead data"""
        decrypted_data = lead_data.copy()
        
        # Decrypt email and phone
        if 'email' in decrypted_data:
            decrypted_data['email'] = self.decrypt(decrypted_data['email'])
        
        if 'phone' in decrypted_data:
            decrypted_data['phone'] = self.decrypt(decrypted_data['phone'])
        
        return decrypted_data 
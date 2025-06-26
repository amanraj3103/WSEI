#!/usr/bin/env python3
"""
Rasa training script for WhatsApp Lead Assistant
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_rasa_installation():
    """Check if Rasa is installed"""
    try:
        import rasa
        logger.info(f"Rasa version: {rasa.__version__}")
        return True
    except ImportError:
        logger.error("Rasa is not installed. Please install it first.")
        return False

def train_rasa_model():
    """Train the Rasa model"""
    try:
        # Change to rasa_bot directory
        rasa_dir = Path("rasa_bot")
        if not rasa_dir.exists():
            logger.error("rasa_bot directory not found!")
            return False
        
        os.chdir(rasa_dir)
        logger.info(f"Changed to directory: {os.getcwd()}")
        
        # Check if training data exists
        data_files = ["data/nlu.yml", "data/stories.yml", "data/rules.yml"]
        for file_path in data_files:
            if not Path(file_path).exists():
                logger.error(f"Training data file not found: {file_path}")
                return False
        
        logger.info("Training data files found. Starting training...")
        
        # Run Rasa train command
        result = subprocess.run(
            ["rasa", "train"],
            capture_output=True,
            text=True,
            cwd=rasa_dir
        )
        
        if result.returncode == 0:
            logger.info("Rasa model trained successfully!")
            logger.info("Training output:")
            logger.info(result.stdout)
            return True
        else:
            logger.error("Rasa training failed!")
            logger.error("Error output:")
            logger.error(result.stderr)
            return False
            
    except Exception as e:
        logger.error(f"Error training Rasa model: {str(e)}")
        return False

def test_rasa_model():
    """Test the trained Rasa model"""
    try:
        rasa_dir = Path("rasa_bot")
        if not rasa_dir.exists():
            logger.error("rasa_bot directory not found!")
            return False
        
        os.chdir(rasa_dir)
        
        # Test with sample messages
        test_messages = [
            "hello",
            "I want to schedule a consultation",
            "I need help with visa",
            "My name is John Doe",
            "My email is john@example.com",
            "help"
        ]
        
        logger.info("Testing Rasa model with sample messages...")
        
        for message in test_messages:
            result = subprocess.run(
                ["rasa", "shell", "--model", "models", "--quiet"],
                input=message,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                logger.info(f"Test message '{message}': OK")
            else:
                logger.warning(f"Test message '{message}': Failed")
        
        return True
        
    except Exception as e:
        logger.error(f"Error testing Rasa model: {str(e)}")
        return False

def start_rasa_server():
    """Start Rasa server for testing"""
    try:
        rasa_dir = Path("rasa_bot")
        if not rasa_dir.exists():
            logger.error("rasa_bot directory not found!")
            return False
        
        os.chdir(rasa_dir)
        
        logger.info("Starting Rasa server...")
        logger.info("Server will be available at: http://localhost:5005")
        logger.info("Press Ctrl+C to stop the server")
        
        # Start Rasa server
        subprocess.run([
            "rasa", "run",
            "--model", "models",
            "--enable-api",
            "--cors", "*",
            "--port", "5005"
        ])
        
    except KeyboardInterrupt:
        logger.info("Rasa server stopped by user")
    except Exception as e:
        logger.error(f"Error starting Rasa server: {str(e)}")
        return False

def main():
    """Main function"""
    logger.info("Starting Rasa training process...")
    
    # Check Rasa installation
    if not check_rasa_installation():
        return 1
    
    # Train model
    if not train_rasa_model():
        logger.error("Training failed!")
        return 1
    
    # Test model
    if not test_rasa_model():
        logger.warning("Model testing failed!")
    
    logger.info("Rasa training process completed!")
    
    # Ask if user wants to start server
    try:
        response = input("Do you want to start the Rasa server for testing? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            start_rasa_server()
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
    
    return 0

if __name__ == "__main__":
    exit(main()) 
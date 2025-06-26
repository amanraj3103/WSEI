#!/bin/bash

# WhatsApp Lead Assistant Deployment Script
# This script helps deploy the application to various platforms

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check environment variables
check_env_vars() {
    print_status "Checking environment variables..."
    
    required_vars=(
        "TWILIO_ACCOUNT_SID"
        "TWILIO_AUTH_TOKEN"
        "TWILIO_PHONE_NUMBER"
        "HUBSPOT_API_KEY"
        "HUBSPOT_PORTAL_ID"
        "CALENDLY_API_KEY"
        "CALENDLY_USER_URI"
        "ENCRYPTION_KEY"
    )
    
    missing_vars=()
    
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing_vars+=("$var")
        fi
    done
    
    if [ ${#missing_vars[@]} -ne 0 ]; then
        print_error "Missing required environment variables:"
        for var in "${missing_vars[@]}"; do
            echo "  - $var"
        done
        return 1
    fi
    
    print_success "All required environment variables are set"
    return 0
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found!"
        return 1
    fi
    
    pip install -r requirements.txt
    print_success "Dependencies installed successfully"
}

# Function to setup database
setup_database() {
    print_status "Setting up database..."
    
    if command_exists python3; then
        python3 scripts/setup_database.py
    else
        print_error "Python 3 is required but not installed"
        return 1
    fi
}

# Function to train Rasa model
train_rasa() {
    print_status "Training Rasa model..."
    
    if command_exists python3; then
        python3 scripts/train_rasa.py
    else
        print_error "Python 3 is required but not installed"
        return 1
    fi
}

# Function to run tests
run_tests() {
    print_status "Running tests..."
    
    if command_exists pytest; then
        pytest tests/ -v
    else
        print_warning "pytest not found, skipping tests"
    fi
}

# Function to build Docker image
build_docker() {
    print_status "Building Docker image..."
    
    if ! command_exists docker; then
        print_error "Docker is required but not installed"
        return 1
    fi
    
    docker build -f docker/Dockerfile -t whatsapp-lead-assistant .
    print_success "Docker image built successfully"
}

# Function to deploy with Docker Compose
deploy_docker_compose() {
    print_status "Deploying with Docker Compose..."
    
    if ! command_exists docker-compose; then
        print_error "Docker Compose is required but not installed"
        return 1
    fi
    
    docker-compose up -d
    print_success "Application deployed with Docker Compose"
}

# Function to deploy to Railway
deploy_railway() {
    print_status "Deploying to Railway..."
    
    if ! command_exists railway; then
        print_error "Railway CLI is required but not installed"
        print_status "Install Railway CLI: npm install -g @railway/cli"
        return 1
    fi
    
    railway login
    railway up
    print_success "Application deployed to Railway"
}

# Function to deploy to Render
deploy_render() {
    print_status "Deploying to Render..."
    
    print_warning "Render deployment requires manual setup:"
    echo "1. Connect your repository to Render"
    echo "2. Set environment variables in Render dashboard"
    echo "3. Set build command: pip install -r requirements.txt"
    echo "4. Set start command: python main.py"
    echo "5. Deploy automatically on push to main branch"
}

# Function to check application health
check_health() {
    print_status "Checking application health..."
    
    # Wait for application to start
    sleep 10
    
    if command_exists curl; then
        response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health || echo "000")
        
        if [ "$response" = "200" ]; then
            print_success "Application is healthy"
        else
            print_error "Application health check failed (HTTP $response)"
            return 1
        fi
    else
        print_warning "curl not found, skipping health check"
    fi
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  local       - Deploy locally with Python"
    echo "  docker      - Deploy with Docker Compose"
    echo "  railway     - Deploy to Railway"
    echo "  render      - Show Render deployment instructions"
    echo "  setup       - Setup database and train Rasa model"
    echo "  test        - Run tests"
    echo "  health      - Check application health"
    echo "  help        - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 local"
    echo "  $0 docker"
    echo "  $0 railway"
}

# Main deployment function
main() {
    case "${1:-help}" in
        "local")
            print_status "Starting local deployment..."
            check_env_vars || exit 1
            install_dependencies
            setup_database
            train_rasa
            run_tests
            print_status "Starting application..."
            python main.py
            ;;
        "docker")
            print_status "Starting Docker deployment..."
            check_env_vars || exit 1
            build_docker
            deploy_docker_compose
            check_health
            ;;
        "railway")
            print_status "Starting Railway deployment..."
            check_env_vars || exit 1
            install_dependencies
            setup_database
            train_rasa
            run_tests
            deploy_railway
            ;;
        "render")
            deploy_render
            ;;
        "setup")
            print_status "Setting up application..."
            install_dependencies
            setup_database
            train_rasa
            print_success "Setup completed successfully"
            ;;
        "test")
            run_tests
            ;;
        "health")
            check_health
            ;;
        "help"|*)
            show_usage
            ;;
    esac
}

# Run main function with all arguments
main "$@" 
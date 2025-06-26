# WhatsApp Lead Assistant

A fully automated WhatsApp-based lead assistant using Rasa, HubSpot Smart CRM, and Calendly, deployed via Twilio WhatsApp Business API.

## 🚀 Features

- **Intelligent Lead Capture**: Rasa-powered NLP to understand and collect lead information
- **Secure Data Processing**: Encrypted handling of sensitive information (email & phone)
- **CRM Integration**: Automatic lead creation in HubSpot Smart CRM
- **Meeting Scheduling**: Personalized Calendly booking links
- **Smart Reminders**: Automated WhatsApp reminders (5h and 1h before meetings)
- **Reporting**: PDF/Excel summary generation for each lead conversation

## 🏗️ Architecture

```
whatsapp-lead-assistant/
├── rasa_bot/                 # Rasa chatbot configuration
│   ├── actions/              # Custom actions for integrations
│   ├── data/                 # Training data
│   ├── models/               # Trained models
│   └── config.yml           # Rasa configuration
├── integrations/             # External service integrations
│   ├── hubspot/             # HubSpot CRM integration
│   ├── calendly/            # Calendly scheduling
│   ├── twilio/              # Twilio WhatsApp API
│   └── encryption/          # Data encryption utilities
├── scheduling/              # Reminder scheduling system
├── reporting/               # PDF/Excel report generation
├── docker/                  # Docker configuration
└── scripts/                 # Utility scripts
```

## 🛠️ Tech Stack

- **Rasa** (latest stable) - NLP/NLU engine
- **Python 3.9+** - Backend logic and integrations
- **Twilio** - WhatsApp Business API
- **HubSpot** - Smart CRM integration
- **Calendly** - Meeting scheduling
- **APScheduler** - Background job scheduling
- **Docker** - Containerization
- **fpdf/reportlab** - PDF generation
- **pandas/xlsxwriter** - Excel report generation

## 📋 Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Twilio Account with WhatsApp Business API
- HubSpot Developer Account
- Calendly Account
- Railway/Render account (for deployment)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd whatsapp-lead-assistant
```

### 2. Environment Configuration

```bash
cp .env.example .env
```

Edit `.env` with your API keys and configuration:

```env
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=whatsapp:+1234567890

# HubSpot Configuration
HUBSPOT_API_KEY=your_hubspot_api_key
HUBSPOT_PORTAL_ID=your_portal_id

# Calendly Configuration
CALENDLY_API_KEY=your_calendly_api_key
CALENDLY_USER_URI=your_calendly_user_uri

# Encryption
ENCRYPTION_KEY=your_32_character_encryption_key

# Database
DATABASE_URL=sqlite:///leads.db

# Admin Email
ADMIN_EMAIL=admin@yourcompany.com
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Train Rasa Model

```bash
cd rasa_bot
rasa train
```

### 5. Run the Application

```bash
# Start all services
docker-compose up -d

# Or run locally
python main.py
```

## 📱 Usage

1. **Lead Initiation**: User sends a message to your WhatsApp number
2. **Data Collection**: Bot collects lead information through conversation
3. **CRM Creation**: Lead is automatically created in HubSpot
4. **Meeting Scheduling**: Calendly link is sent to user
5. **Reminders**: Automated reminders sent before meeting
6. **Reporting**: PDF/Excel summary generated and sent to admin

## 🔧 Configuration

### Rasa Configuration

Edit `rasa_bot/config.yml` to customize:
- Pipeline configuration
- Policies
- Language settings

### Form Configuration

Modify `rasa_bot/domain.yml` to adjust:
- Required lead fields
- Form validation rules
- Response templates

### Integration Settings

Configure integrations in respective modules:
- `integrations/hubspot/config.py`
- `integrations/calendly/config.py`
- `integrations/twilio/config.py`

## 🚀 Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f
```

### Railway/Render Deployment

1. Connect your repository to Railway/Render
2. Set environment variables in the platform dashboard
3. Deploy automatically on push to main branch

### Manual Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Set up database
python scripts/setup_database.py

# Start services
python main.py
```

## 🔒 Security

- All sensitive data (email, phone) is encrypted using AES-256
- API keys are stored securely in environment variables
- HTTPS endpoints for all external communications
- Regular security audits and updates

## 📊 Monitoring

- Application logs in `logs/` directory
- Health check endpoint: `/health`
- Metrics dashboard: `/metrics`
- Error tracking and alerting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact: support@yourcompany.com
- Documentation: [Wiki Link]

## 🔄 Updates

- **v1.0.0**: Initial release with core functionality
- **v1.1.0**: Added advanced reporting features
- **v1.2.0**: Enhanced security and monitoring 
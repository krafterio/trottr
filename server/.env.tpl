# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/smashr

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=30

# LOGGER
LOG_LEVEL=info
LOG_OUTPUT=console
LOG_FORMAT=text_light
LOG_FILE=

# SMTP
SMTP_HOST=your-smtp-host
SMTP_PORT=587
SMTP_USE_TLS=True
SMTP_USERNAME=your-smtp-username
SMTP_PASSWORD=your-smtp-password
SMTP_DEFAULT_FROM=Smashr <noreply@smashr.tech>

# BASE URL
BASE_URL=https://domain.tld/api
BASE_URL_EMAIL=https://domain.tld

# WORKERS
HTTP_WORKERS

# Preview Access
MODE_PREVIEW=False
MODE_PREVIEW_NOTIF_EMAIL=

# Data
DATA_PATH=

# PILOTERR
PILOTERR_API_KEY=ta_cle_api_piloterr_ici

# DROPCONTACT
DROPCONTACT_API_KEY=votre_clé_api_dropcontact

# DEBUG
DEBUG_ADMIN=False
DEBUG_SIMULATE_CONTACT_ENRICHMENT=False
DEBUG_SIMULATE_COMPANY_ENRICHMENT=False

# Recaptcha
RECAPTCHA_ENABLED=False
RECAPTCHA_SITE_KEY=
RECAPTCHA_SECRET_KEY=
RECAPTCHA_MIN_SCORE=0.5

# Tokens
AVAILABLE_CREDITS_BY_USER=100
AVAILABLE_CREDITS_TOTAL_TRIAL=50

# OPEN_AI
OPENAI_API_KEY=your_api_key_here

# MISTRAL AI
MISTRAL_API_KEY=ta_clé_api_mistral_ici

# GOOGLE
GOOGLE_CLIENT_ID=your_api_key_here
GOOGLE_CLIENT_SECRET=your_api_key_here
GOOGLE_REDIRECT_URI=http://localhost:8000/api/integrations/gmail/callback

# BENCHMARKR
BENCHMARKR_URL=https://benchmarkr.app
BENCHMARKR_API_KEY=

# SXNG
SXNG_URL=https://searxng.brihx.fr

# ASSEMBLY AI
ASSEMBLY_AI_TOKEN=your_api_key_here

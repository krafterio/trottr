# Trottr

Trottr is a SaaS platform made for Field Services Management. It helps companies with on site job management.


## Prerequisites

- Python 3.13+
- PIP 25.0+ (Python Package Manager)
- PostgreSQL 15.0+ (with CLI Tools in PATH)
- NVM for Node.js 22.0+ (see the [installation doc](https://github.com/nvm-sh/nvm?tab=readme-ov-file#installing-and-updating))


## Installation

1. Clone the project:
```bash
git clone git@github.com:krafterio/smashr.git
```

2. Create and activate virtual environment:
```bash
python3.13 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

3. Install server dependencies:
```bash
pip install -r server/requirements.txt
pip install -r server/requirements-dev.txt
```

4. Install app dependencies:
```bash
cd app
nvm install 22
nvm use 22
npm install
```

5. Configure environment variables:
```bash
cp server/.env.tpl server/.env
cp app/.env.tpl app/.env
# Edit .env files with your configurations
```


## Database Setup

1. Create PostgreSQL database:
```bash
./kt db createdb
```

2. Initialize Alembic:
```bash
./kt db migrate
```

3. Initialize data of database (countries and languages):
```bash
./kt db init-data
```


## Starting the Server

### Via CLI
```bash
./kt serve
```

### Via VS Code
1. Open the project in VS Code
2. Launch the server (Backend)


## Starting the App

### Via CLI
```bash
cd app
npm run dev 
```

### Via VS Code
1. Open the project in VS Code
2. Launch the app (Frontend) or the app and the server (Fullstack)


## API Endpoints

Swagger Documentation: http://localhost:8000/docs


## Usage

### CLI Commands

The project includes a custom CLI (`kt`) to facilitate common tasks.

#### Start the Server

```bash
./kt serve
```

Available options:
- `--host`: Server host (default: 0.0.0.0)
- `--port`: Server port (default: 8000)
- `--reload/--no-reload`: Enable/disable hot reload (default: enabled)

Example:
```bash
./kt serve --port 8080 --no-reload
```

#### Launch tasks

Send email welcome:
```bash
./kt task send-email-welcome <user_email>
```

#### Database Management

Initialize Alembic (if no migration versions exist):
```bash
./kt db init
```

Create a new migration:
```bash
./kt db makemigrations -m "migration description"
```

Apply pending migrations:
```bash
./kt db migrate
```

Revert the last migration:
```bash
./kt db downgrade
```

View migration history:
```bash
./kt db history
```

### API Documentation

Once the server is running, you can access:
- Swagger UI Documentation: http://localhost:8000/docs
- ReDoc Documentation: http://localhost:8000/redoc


### Service dependencies

1. Google reCaptcha: https://www.google.com/recaptcha/admin/create


## Stripe Configuration (Development)

### Prerequisites

1. Install Stripe CLI:
   Read the official documentation to install [Stripe CLI](https://docs.stripe.com/stripe-cli).

### Setup

1. **Login to Stripe CLI:**
   ```bash
   stripe login
   ```
   Follow the prompts to authenticate with your Stripe account.

2. **Configure environment variables** in `server/.env`:
   ```bash
   STRIPE_ENABLED=True
   STRIPE_PUBLISHABLE_KEY=pk_*****
   STRIPE_SECRET_KEY=sk_*****
   STRIPE_WEBHOOK_SECRET=
   ```

3. **Setup webhook endpoint** for local development:
   ```bash
   # Forward Stripe webhooks to your local server
   stripe listen --forward-to localhost:8003/api/webhooks/stripe
   ```

   This command will output a webhook signing secret like `whsec_...`. Copy this value to your `STRIPE_WEBHOOK_SECRET` environment variable.

4. **Keep the webhook listener running** during development. You can run it in a separate terminal:
   ```bash
   # Terminal 1: Start your server
   ./kt serve

   # Terminal 2: Start webhook forwarding
   stripe listen --forward-to localhost:8003/api/webhooks/stripe
   ```

### Testing Payments

You can use Stripe's test card numbers for testing:
- **Successful payment:** `4242 4242 4242 4242`
- **Payment requires authentication:** `4000 0025 0000 3155`
- **Payment is declined:** `4000 0000 0000 9995`

Use any future expiration date and any 3-digit CVC.

### Important Notes

- The webhook listener must be running to receive subscription events
- Test mode keys start with `sk_test_` and `pk_test_`
- Never commit real API keys to version control
- For production, configure webhooks directly in the Stripe Dashboard


## Development

### Development Workflow

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/feature-name
   ```
2. Make your changes
3. Create a migration if you modify models:
   ```bash
   ./kt db migrate "description of changes"
   ./kt db upgrade
   ```
4. Test your changes
5. Create a pull request


## Commit message format convention

This project uses the **[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0)** naming convention.

### Basic structure of a Conventional commit

```
<type>(<scope>): <description>
```

- **type**: the type of modification made (required)
- **scope**: the scope (optional, but recommended)
- **description**: a short explanation (imperative, no capital letters, no period)

### Conventional Commits Types used

| Type     | Description                                                                    |
|----------|--------------------------------------------------------------------------------|
| feat     | New feature                                                                    |
| fix      | Bug fix                                                                        |
| docs     | Change in documentation                                                        |
| style    | Change of format (indentation, spaces, etc.) without functional impact         |
| refactor | Refactoring the code without adding or correcting functionality                |
| test     | Adding or modifying tests                                                      |
| chore    | Miscellaneous tasks without direct impact (build, dependencies, configs, etc.) |
| perf     | Performance improvement                                                        |
| build    | Change in build system or dependencies                                         |
| ci       | Changes to CI/CD files (GitHub Actions, GitLab CI, etc.)                       |

## License

This project is licensed under Proprietary License. See the `LICENSE` file for details.

# Master .env Configuration Status

**Total Variables Configured**: 116  
**Repository**: `/Users/jackagnew/projects/jckagnew-agents`

## Environment Variables by Category

| Category | Variable Name | Status | Notes |
|----------|--------------|--------|-------|
| **Supabase** | `SUPABASE_URL` | ✅ Configured | Main Supabase project URL |
| | `SUPABASE_ANON_KEY` | ✅ Configured | Anonymous key for client access |
| | `SUPABASE_SERVICE_ROLE_KEY` | ✅ Configured | Service role key for admin operations |
| | `SUPABASE_API_URL` | ✅ Configured | API endpoint URL |
| | `SUPABASE_DB_URL` | ✅ Configured | Direct database connection string |
| | `SUPABASE_RESPONSES_BUCKET` | ✅ Configured | Storage bucket for responses |
| | `EXPO_PUBLIC_SUPABASE_URL` | ✅ Configured | Public URL for Expo apps |
| | `EXPO_PUBLIC_SUPABASE_ANON_KEY` | ✅ Configured | Public anon key for Expo |
| | `NEXT_PUBLIC_SUPABASE_URL` | ✅ Configured | Public URL for Next.js |
| | `NEXT_PUBLIC_SUPABASE_ANON_KEY` | ✅ Configured | Public anon key for Next.js |
| | `FACTORY_SUPABASE_URL` | ✅ Configured | Factory-specific Supabase URL |
| | `FACTORY_SUPABASE_ANON_KEY` | ✅ Configured | Factory-specific anon key |
| | `EXPO_PUBLIC_FACTORY_SUPABASE_URL` | ✅ Configured | Factory Supabase URL for Expo |
| | `EXPO_PUBLIC_FACTORY_SUPABASE_ANON_KEY` | ✅ Configured | Factory anon key for Expo |
| **AI Services** | `OPENAI_API_KEY` | ✅ Configured | OpenAI API key |
| | `OPENAI_MODEL` | ✅ Configured | Default OpenAI model |
| | `ANTHROPIC_API_KEY` | ✅ Configured | Anthropic/Claude API key |
| | `ANTHROPIC_MODEL` | ✅ Configured | Default Anthropic model |
| | `GEMINI_API_KEY` | ✅ Configured | Google Gemini API key |
| | `GOOGLE_AI_API_KEY` | ✅ Configured | Google AI Studio API key |
| | `GOOGLE_AI_MODEL` | ✅ Configured | Google AI model |
| | `GOOGLE_API_KEY` | ✅ Configured | General Google API key |
| | `DEEPSEEK_API_KEY` | ✅ Configured | DeepSeek API key |
| | `GROQ_API_KEY` | ✅ Configured | Groq API key |
| | `GROK_API_KEY` | ✅ Configured | Grok API key |
| | `HF_TOKEN` | ✅ Configured | Hugging Face token |
| | `LLM_DEFAULT_PROVIDER` | ✅ Configured | Default LLM provider |
| **Stripe** | `STRIPE_SECRET_KEY` | ✅ Configured | Stripe secret key |
| | `STRIPE_PUBLISHABLE_KEY` | ✅ Configured | Stripe publishable key |
| | `STRIPE_WEBHOOK_SECRET` | ✅ Configured | Webhook signing secret |
| | `STRIPE_PRO_MONTHLY_PRICE_ID` | ✅ Configured | Monthly subscription price ID |
| | `STRIPE_PRO_YEARLY_PRICE_ID` | ✅ Configured | Yearly subscription price ID |
| | `STRIPE_ONE_TIME_CREDITS_PRICE_ID` | ✅ Configured | One-time credits price ID |
| **Database** | `DATABASE_URL` | ✅ Configured | PostgreSQL connection string |
| | `DATABASE_HOST` | ✅ Configured | Database host |
| | `DATABASE_PORT` | ✅ Configured | Database port |
| | `DATABASE_NAME` | ✅ Configured | Database name |
| | `DATABASE_USER` | ✅ Configured | Database user |
| | `DATABASE_PASSWORD` | ✅ Configured | Database password |
| **Redis** | `REDIS_URL` | ✅ Configured | Redis connection URL |
| | `REDIS_HOST` | ✅ Configured | Redis host |
| | `REDIS_PORT` | ✅ Configured | Redis port |
| | `UPSTASH_REDIS_URL` | ✅ Configured | Upstash Redis URL |
| | `UPSTASH_REDIS_TOKEN` | ✅ Configured | Upstash Redis token |
| | `UPSTASH_REDIS_REST_URL` | ✅ Configured | Upstash REST API URL |
| | `UPSTASH_REDIS_REST_TOKEN` | ✅ Configured | Upstash REST API token |
| **Email Services** | `RESEND_API_KEY` | ✅ Configured | Resend API key |
| | `SENDGRID_API_KEY` | ✅ Configured | SendGrid API key |
| | `SENDGRID_SENDER_EMAIL` | ✅ Configured | SendGrid sender email |
| | `EMAIL_SMTP_HOST` | ✅ Configured | SMTP server host |
| | `EMAIL_SMTP_PORT` | ✅ Configured | SMTP server port |
| | `EMAIL_SMTP_USER` | ✅ Configured | SMTP username |
| | `EMAIL_SMTP_PASSWORD` | ✅ Configured | SMTP password |
| | `EMAIL_SMTP_SECURE` | ✅ Configured | SMTP secure flag |
| | `EMAIL_FROM` | ✅ Configured | Default sender email |
| | `EMAIL_SUBJECT_PREFIX` | ✅ Configured | Email subject prefix |
| **Gmail Integration** | `GMAIL_USER` | ✅ Configured | Gmail account |
| | `GMAIL_APP_PASSWORD` | ✅ Configured | Gmail app password |
| | `GMAIL_AUTH_MODE` | ✅ Configured | Authentication mode (oauth) |
| | `GMAIL_OAUTH_CLIENT_PATH` | ✅ Configured | OAuth client credentials path |
| | `GMAIL_OAUTH_TOKEN_PATH` | ✅ Configured | OAuth token path |
| | `GMAIL_OAUTH_AUTO_AUTHORIZE` | ✅ Configured | Auto-authorize flag |
| | `GMAIL_SYNC_CONTACTS` | ✅ Configured | Contacts to sync |
| | `GMAIL_SYNC_QUERY` | ✅ Configured | Gmail search query |
| **Authentication** | `NEXTAUTH_SECRET` | ✅ Configured | NextAuth secret |
| | `NEXTAUTH_URL` | ✅ Configured | NextAuth URL |
| | `JWT_SECRET` | ✅ Configured | JWT signing secret |
| | `JWT_EXPIRES_IN` | ✅ Configured | JWT expiration time |
| | `SESSION_SECRET` | ✅ Configured | Session secret |
| | `ADMIN_USERNAME` | ✅ Configured | Admin username |
| | `ADMIN_PASSWORD_HASH_B64` | ✅ Configured | Admin password hash (base64) |
| **Storage Buckets** | `DESIGNS_BUCKET` | ✅ Configured | Designs storage bucket |
| | `DELIVERABLES_BUCKET` | ✅ Configured | Deliverables storage bucket |
| | `AVATARS_BUCKET` | ✅ Configured | Avatars storage bucket |
| **Admin Console** | `ALLOWED_ORIGINS` | ✅ Configured | CORS allowed origins |
| | `CORS_ORIGIN` | ✅ Configured | CORS origin |
| | `BCRYPT_ROUNDS` | ✅ Configured | Bcrypt rounds for hashing |
| **Monitoring & Logging** | `LOG_LEVEL` | ✅ Configured | Logging level |
| | `LOG_FORMAT` | ✅ Configured | Log format |
| | `LOG_FILE` | ✅ Configured | Log file path |
| | `GRAFANA_PORT` | ✅ Configured | Grafana port |
| | `GRAFANA_PASSWORD` | ✅ Configured | Grafana password |
| | `PROMETHEUS_PORT` | ✅ Configured | Prometheus port |
| **Notifications** | `NTFY_SERVER_URL` | ✅ Configured | Ntfy server URL |
| | `NTFY_SERVER_IP` | ✅ Configured | Ntfy server IP |
| | `NTFY_TOPIC` | ✅ Configured | Ntfy topic |
| | `PUSHOVER_TOKEN` | ✅ Configured | Pushover token |
| | `PUSHOVER_USER` | ✅ Configured | Pushover user |
| **Rate Limiting** | `RATE_LIMIT_MAX_REQUESTS` | ✅ Configured | Max requests per window |
| | `RATE_LIMIT_WINDOW_MS` | ✅ Configured | Rate limit window (ms) |
| **Background Jobs** | `BULL_CONCURRENCY` | ✅ Configured | Bull queue concurrency |
| | `BULL_MAX_RETRIES` | ✅ Configured | Bull max retries |
| **Development** | `NODE_ENV` | ✅ Configured | Node environment |
| | `DEBUG` | ✅ Configured | Debug mode |
| | `HOT_RELOAD` | ✅ Configured | Hot reload enabled |
| | `MOCK_EXTERNAL_SERVICES` | ✅ Configured | Mock external services flag |
| **Server Config** | `HOST` | ✅ Configured | Server host |
| | `PORT` | ✅ Configured | Server port |
| | `API_BASE_URL` | ✅ Configured | API base URL |
| | `API_VERSION` | ✅ Configured | API version |
| | `NEXT_PUBLIC_BASE_URL` | ✅ Configured | Next.js public base URL |
| | `NEXT_PUBLIC_APP_URL` | ✅ Configured | Next.js app URL |
| **Project Info** | `PROJECT_NAME` | ✅ Configured | Project name |
| | `PROJECT_VERSION` | ✅ Configured | Project version |
| | `CURRENT_DATE` | ✅ Configured | Current date |
| | `CURRENT_DATETIME` | ✅ Configured | Current datetime |
| **Google Services** | `GOOGLE_APPLICATION_CREDENTIALS` | ✅ Configured | Google service account path |
| | `GOOGLE_APP_PW` | ✅ Configured | Google app password |
| | `GOOGLE_MAPS_API_KEY` | ✅ Configured | Google Maps API key |
| **Figma** | `FIGMA_ACCESS_TOKEN` | ✅ Configured | Figma API access token |
| | `FIGMA_FILE_KEY` | ✅ Configured | Figma file key |
| **GitHub** | `GH_TOKEN` | ✅ Configured | GitHub personal access token |
| **Search** | `SERPER_API_KEY` | ✅ Configured | Serper API key for search |
| **Docker** | `DOCKER_COMPOSE_FILE` | ✅ Configured | Docker Compose file path |
| **Analytics** | `NEXT_PUBLIC_GA4_BESPOKE_ID` | ✅ Configured | GA4 Bespoke tracking ID |
| | `NEXT_PUBLIC_GA4_CONSUMER_ID` | ✅ Configured | GA4 Consumer tracking ID |
| | `NEXT_PUBLIC_GA4_ENTERPRISE_ID` | ✅ Configured | GA4 Enterprise tracking ID |

## Summary by Category

- **Supabase**: 14 variables
- **AI Services**: 13 variables (OpenAI, Anthropic, Google/Gemini, DeepSeek, Groq, Grok, HuggingFace)
- **Stripe**: 6 variables
- **Database**: 6 variables
- **Redis**: 7 variables
- **Email Services**: 10 variables (Resend, SendGrid, SMTP, Gmail)
- **Authentication**: 6 variables
- **Storage Buckets**: 3 variables
- **Admin Console**: 3 variables
- **Monitoring & Logging**: 5 variables
- **Notifications**: 5 variables
- **Rate Limiting**: 2 variables
- **Background Jobs**: 2 variables
- **Development**: 4 variables
- **Server Config**: 5 variables
- **Project Info**: 4 variables
- **Google Services**: 3 variables
- **Figma**: 2 variables
- **GitHub**: 1 variable
- **Search**: 1 variable
- **Docker**: 1 variable
- **Analytics**: 3 variables

**Total**: 116 environment variables configured


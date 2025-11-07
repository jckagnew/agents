# Stitch Workflow Implementation Guide

## Overview

This document describes the complete implementation of the Stitch-integrated Design-First Software Factory workflow. The implementation supports the human-in-the-loop design process using Google's Stitch tool for iterative UI design.

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    User Intake                               │
│  - App concept                                               │
│  - 3 inspiration websites (1 lockable as brand guideline)   │
│  - Service tier selection                                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Gemini: Problem Deconstruction                  │
│  - Screenshot inspiration websites                           │
│  - Analyze design patterns                                   │
│  - Generate user stories & features                          │
│  - Create design system                                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Gemini: Screen Mapping                          │
│  - Map features → screens                                    │
│  - Generate Stitch prompts for each screen                   │
│  - Define screen states (empty, loading, error, etc.)       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│           Human: Stitch Iteration                            │
│  - User pastes prompts into stitch.withgoogle.com            │
│  - Iterates on designs (annotate, reprompt, refine)         │
│  - Exports HTML for each approved screen                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│            User: Upload & Approve                            │
│  - Upload HTML files for each screen                         │
│  - Review generated designs                                  │
│  - Approve or request iteration                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│       Claude/Cursor: HTML → Expo (universal React Native)    │
│  - Convert HTML to TypeScript Expo components                │
│  - Apply design system                                       │
│  - Generate navigation structure                             │
│  - Package complete Expo project (iOS, Android, Web)         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  Project Handoff                             │
│  - Download ZIP file with complete project                   │
│  - Run npm install && expo start                             │
│  - Deploy to App Store / Play Store                          │
└─────────────────────────────────────────────────────────────┘
```

## Database Schema

### Key Tables

#### `projects`
Tracks each project through the workflow:
- `status`: intake → problem_deconstruction → screen_mapping → stitch_iteration → html_upload → code_generation → complete
- `service_tier`: express | concierge | premium
- `metadata`: Additional project context

#### `inspiration_websites`
Stores up to 3 inspiration websites per project:
- `url`: Website URL
- `locked`: Boolean (true = brand guideline, must follow exactly)
- `screenshot_url`: Captured screenshot
- `analysis`: Gemini's design analysis (JSONB)
- **Constraint**: Max 3 per project (enforced by trigger)

#### `problem_deconstructions`
AI-generated analysis of the project:
- `user_stories`: Array of user story objects
- `features`: Array of feature objects
- `ux_requirements`: UX requirements
- `design_system`: Complete design system (colors, typography, spacing)

#### `screen_mappings`
Features mapped to screens with Stitch prompts:
- `screen_name`: e.g., "Login", "Dashboard"
- `screen_type`: authentication | onboarding | main | detail | form | settings
- `stitch_prompt`: Ready-to-paste prompt for Stitch
- `state_variations`: Array of states (empty, loading, error, success)

#### `stitch_designs`
HTML exports from Stitch:
- `html_content`: Full HTML from Stitch export
- `approved`: Boolean (user approval gate)
- `iteration_number`: Tracks design iterations
- `parent_design_id`: Links to previous iteration

#### `code_generation_jobs`
Background processing queue:
- `status`: queued → processing → completed | failed
- `job_type`: html_to_react_native | full_project_generation
- `retry_count`: Automatic retry on failure

#### `code_artifacts`
Generated code files:
- `artifact_type`: component | screen | navigation | full_project
- `file_path`: Relative path in generated project
- `conversion_confidence`: 0.0 to 1.0 quality score
- `warnings`: Array of conversion issues

## Frontend Components

### 1. ProjectIntakeScreen

**Purpose**: Capture user requirements and inspiration websites

**Features**:
- App name and concept inputs
- Service tier selection (Express, Concierge, Premium)
- Up to 3 inspiration website inputs
- Locking mechanism for brand guideline (only 1 can be locked)
- Notes field for each inspiration website
- Form validation

**Location**: `src/screens/ProjectIntakeScreen.tsx`

### 2. StitchUploadScreen

**Purpose**: Guide users through uploading Stitch HTML exports

**Features**:
- Display generated Stitch prompts for each screen
- HTML file upload per screen/state
- Progress tracking (uploaded, approved)
- Design approval workflow
- Re-upload capability for iterations
- Generate code button (enabled when all approved)

**Location**: `src/screens/StitchUploadScreen.tsx`

## Backend Services

### 1. GeminiService

**Purpose**: AI-powered analysis and prompt generation

**Methods**:

#### `analyzeInspirationWebsite(screenshot, url, isLocked)`
- Analyzes screenshot of inspiration website
- Extracts color palette, typography, layout patterns
- If locked, extracts brand guidelines (must-follow rules)
- Returns structured DesignAnalysis object

#### `generateProblemDeconstruction(intake, inspirationAnalyses)`
- Takes app concept + inspiration analyses
- Generates 8-12 user stories
- Identifies 6-10 core features
- Creates 10-15 UX requirements
- Builds complete design system incorporating inspiration aesthetics
- **Special handling**: Locked brand guidelines are strictly followed

#### `generateScreenMappings(problemDeconstruction)`
- Maps features to 6-12 screens
- Defines screen types and navigation
- Generates detailed Stitch prompts per screen
- Lists state variations (empty, loading, error, etc.)

#### `generateStitchPrompt(screenMapping, designSystem, stateVariation)`
- Creates highly detailed, Stitch-optimized prompt
- References exact design system values
- Specifies state-specific UI elements
- 3-5 paragraphs, actionable for Stitch AI

**Location**: `src/services/gemini.service.ts`

### 2. SupabaseService

**Purpose**: Database operations and workflow orchestration

**Methods**:

#### `createProjectFromIntake(intake)`
Main workflow orchestrator:
1. Check user quota
2. Create project record
3. Capture & analyze inspiration websites
4. Generate problem deconstruction
5. Generate screen mappings
6. Update project status to `stitch_iteration`
7. Track AI costs

#### `getProjectWithDetails(projectId)`
- Fetches project with all related data
- Includes inspiration websites, deconstruction, screens, designs

#### `uploadStitchDesign(projectId, screenMappingId, screenName, htmlContent, stateVariation)`
- Uploads HTML to Supabase Storage
- Creates stitch_designs record
- Returns design ID for approval tracking

#### `approveStitchDesign(designId, feedback)`
- Marks design as approved
- Optional feedback for iteration

#### `generateCodeFromStitchDesigns(projectId)`
- Gets all approved designs
- Creates code generation job
- Triggers background worker
- Returns job ID for status tracking

**Location**: `src/services/supabase.service.ts`

## Edge Functions

### 1. capture-screenshot

**Purpose**: Capture website screenshots for design analysis

**Endpoint**: `POST /capture-screenshot`

**Request**:
```json
{
  "url": "https://example.com",
  "width": 1280,
  "height": 720,
  "fullPage": false
}
```

**Response**:
```json
{
  "screenshot": "base64-encoded-png",
  "url": "https://example.com",
  "timestamp": "2025-11-06T..."
}
```

**Implementation**: Uses ScreenshotAPI.net or similar service

**Location**: `supabase/functions/capture-screenshot/index.ts`

### 2. convert-html-to-react-native

**Purpose**: Convert single Stitch HTML export to Expo component (universal React Native)

**Endpoint**: `POST /convert-html-to-react-native`

**Request**:
```json
{
  "design_id": "uuid",
  "target_framework": "expo"
}
```

**Response**:
```json
{
  "success": true,
  "artifact_id": "uuid",
  "component_code": "// TypeScript component code",
  "style_code": "// StyleSheet styles",
  "dependencies": ["react-native-svg"],
  "warnings": ["Manual review needed for complex gradient"],
  "confidence": 0.95
}
```

**AI Provider**: Claude Sonnet 4.5 (via Anthropic API)

**Location**: `supabase/functions/convert-html-to-react-native/index.ts`

### 3. process-code-generation

**Purpose**: Background job for generating complete Expo projects

**Endpoint**: `POST /process-code-generation`

**Request**:
```json
{
  "job_id": "uuid"
}
```

**Workflow**:
1. Get all approved Stitch designs
2. Convert each to Expo screen (iOS, Android, Web compatible)
3. Generate navigation structure
4. Generate theme file from design system
5. Generate package.json with Expo dependencies
6. Package all as ZIP file
7. Upload to storage
8. Update job status to `completed`
9. Notify user

**Response**:
```json
{
  "success": true,
  "job_id": "uuid",
  "screen_count": 8,
  "zip_url": "https://storage.supabase.co/..."
}
```

**Location**: `supabase/functions/process-code-generation/index.ts`

## User Flow

### Concierge Tier (Human-in-the-Loop)

#### Step 1: Intake (2 minutes)
1. User fills out ProjectIntakeScreen
2. Enters app name and concept
3. Adds up to 3 inspiration websites
4. Locks 1 as brand guideline (optional)
5. Selects "Concierge" tier
6. Submits

#### Step 2: AI Analysis (1-2 minutes, automated)
1. System captures screenshots of inspiration websites
2. Gemini analyzes each screenshot:
   - Color palette extraction
   - Typography identification
   - Layout pattern analysis
   - Brand guideline extraction (if locked)
3. Gemini generates problem deconstruction:
   - User stories
   - Features
   - UX requirements
   - Design system (incorporating inspiration aesthetics)
4. Gemini generates screen mappings:
   - 6-12 screens identified
   - Features mapped to screens
   - Stitch prompts generated

#### Step 3: Stitch Iteration (10-30 minutes, human)
1. User opens StitchUploadScreen
2. For each screen:
   - Copy the generated Stitch prompt
   - Paste into stitch.withgoogle.com
   - Review generated design
   - Annotate for changes (if needed)
   - Reprompt for refinement
   - Export HTML when satisfied
3. User uploads each HTML file
4. Reviews in app
5. Approves or re-uploads

#### Step 4: Code Generation (2-5 minutes, automated)
1. User clicks "Generate Code"
2. Background job starts:
   - Converts each HTML to Expo (universal React Native)
   - Generates navigation
   - Generates theme file
   - Packages complete Expo project (iOS, Android, Web)
3. User receives notification
4. Downloads ZIP file

#### Step 5: Handoff (5 minutes)
1. Extract ZIP file
2. Run `npm install`
3. Run `expo start`
4. Test on device/simulator
5. Deploy to app stores

### Express Tier (Fully Automated)

Skips Step 3 (Stitch iteration):
- Gemini generates design tokens directly
- Code generation happens immediately
- No HTML intermediary
- Faster but less user control

### Premium Tier (Professional Design)

Enhanced workflow:
1. Complete Steps 1-3 (Stitch rapid prototype)
2. Optional: Export to Figma for professional refinement
3. Figma API extracts final design
4. Continue to code generation

## Environment Variables

### Required

```bash
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# AI Services
GEMINI_API_KEY=your-gemini-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key

# Screenshot Service
SCREENSHOT_API_KEY=your-screenshot-api-key
```

### Optional

```bash
# Development
NODE_ENV=development
ENABLE_DEBUG_LOGGING=true
```

## Deployment

### Database Setup

```bash
# Run migrations
supabase migration up

# Verify tables created
supabase db dump --schema public
```

### Edge Functions Deployment

```bash
# Deploy all functions
supabase functions deploy capture-screenshot
supabase functions deploy convert-html-to-react-native
supabase functions deploy process-code-generation

# Set secrets
supabase secrets set ANTHROPIC_API_KEY=your-key
supabase secrets set SCREENSHOT_API_KEY=your-key
```

### Frontend Deployment

```bash
# Install dependencies
npm install

# Run locally
expo start

# Build for web
expo build:web

# Deploy to hosting (Vercel, Netlify, etc.)
```

## Cost Tracking

All AI operations are tracked in the `ai_generations` table:

- **Gemini 1.5 Pro Pricing**:
  - Input: $3.50 per 1M tokens
  - Output: $10.50 per 1M tokens

- **Claude Sonnet 4.5 Pricing**:
  - Input: $3.00 per 1M tokens
  - Output: $15.00 per 1M tokens

Example project costs:
- Inspiration analysis (3 sites): ~$0.10
- Problem deconstruction: ~$0.15
- Screen mapping (8 screens): ~$0.20
- Code generation (8 screens): ~$0.80
- **Total**: ~$1.25 per project

## Testing

### Unit Tests

```bash
npm run test
```

### Integration Tests

```bash
# Test complete workflow
npm run test:integration

# Test Stitch upload
npm run test:stitch-upload

# Test code generation
npm run test:code-gen
```

### Manual Testing Checklist

- [ ] Create project with 3 inspiration websites
- [ ] Verify screenshots captured
- [ ] Check Gemini analysis quality
- [ ] Review generated Stitch prompts
- [ ] Test Stitch workflow (paste, iterate, export)
- [ ] Upload HTML files
- [ ] Approve designs
- [ ] Generate code
- [ ] Download and run project
- [ ] Verify screens match Stitch designs

## Monitoring

### Key Metrics

- **Project creation rate**: Projects per day
- **Completion rate**: % of projects reaching `complete` status
- **Average time to completion**: Intake → handoff
- **Stitch iteration count**: Avg iterations per screen
- **Code conversion quality**: Avg confidence scores
- **Cost per project**: Total AI spend

### Alerts

- Failed code generation jobs
- Low conversion confidence (<0.7)
- High iteration count (>5 per screen)
- Quota exceeded errors

## Troubleshooting

### Common Issues

#### "No approved designs found"
- Ensure all screens have uploaded and approved HTML
- Check `stitch_designs` table for `approved = true`

#### "Code generation job failed"
- Check job error message in `code_generation_jobs`
- Verify Anthropic API key is set
- Check Edge Function logs

#### "Screenshot capture failed"
- Verify Screenshot API key
- Check if URL is accessible
- Try with `fullPage: false`

#### "Conversion confidence too low"
- Review HTML structure (complex layouts may need manual refinement)
- Check design system application
- Consider Premium tier for Figma refinement

## Future Enhancements

### Planned Features

1. **Real-time collaboration**: Multiple users on same project
2. **Design iteration history**: Visual diff of Stitch iterations
3. **Component library**: Reusable components across projects
4. **A/B testing**: Generate variants for testing
5. **Analytics integration**: Built-in analytics setup
6. **CI/CD pipeline**: Automated deployment to app stores
7. **Design tokens sync**: Export to Figma/Sketch
8. **Multi-language support**: i18n code generation

### Experimental

- **Voice input**: Describe app concept via voice
- **Video demos**: Generate demo videos from screens
- **AI code review**: Automated quality checks
- **Performance optimization**: AI-suggested optimizations

## Support

### Documentation

- [Stitch Documentation](https://stitch.withgoogle.com/docs)
- [Expo Documentation](https://docs.expo.dev)
- [Supabase Documentation](https://supabase.com/docs)
- [Gemini API Documentation](https://ai.google.dev/docs)

### Contact

- GitHub Issues: [design-first-software-factory/issues](https://github.com/your-org/design-first-software-factory/issues)
- Email: support@yourcompany.com
- Discord: [Community Server](https://discord.gg/yourserver)

## License

Proprietary - See LICENSE file for details

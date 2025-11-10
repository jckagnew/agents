# Admin Console

**Design-First Software Factory**
**Version**: 1.0.0
**Tech Stack**: Expo SDK 54 + React Native 0.81.5

---

## Overview

Admin Console for managing Design Factory customers, projects, and operations. Built with Expo and React Native to match the tech stack of generated apps.

### Features

- **Customer Management**: View, search, and manage all customers
- **Project Tracking**: Monitor projects across all stages (INTAKE → DESIGN → DEV → QA → COMPLETE)
- **Authentication**: Secure admin login with Supabase Auth
- **Role-Based Access**: super_admin, admin, and viewer roles
- **Real-time Data**: Direct integration with Supabase backend APIs

---

## Prerequisites

- Node.js 18+ installed
- Expo CLI installed: `npm install -g expo-cli`
- Supabase project set up (see backend setup in `/supabase`)
- iOS Simulator (for Mac) or Android Emulator, or Expo Go app on physical device

---

## Setup

### 1. Install Dependencies

```bash
cd admin-console
npm install
```

### 2. Configure Environment

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your Supabase credentials:

```bash
EXPO_PUBLIC_SUPABASE_URL=https://your-project-ref.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

### 3. Start Development Server

```bash
npm start
```

This will open Expo DevTools in your browser.

### 4. Run on Device

**iOS Simulator** (Mac only):
```bash
npm run ios
```

**Android Emulator**:
```bash
npm run android
```

**Physical Device**:
1. Install Expo Go app from App Store or Google Play
2. Scan the QR code shown in terminal

---

## Login Credentials

For development/testing, use the seeded admin account:

- **Email**: `admin@designfactory.dev`
- **Password**: `SupabaseShouldReset!`

⚠️ **Change this password in production!**

---

## Project Structure

```
admin-console/
├── app/
│   ├── (tabs)/              # Tab navigation screens
│   │   ├── customers.tsx    # Customer list
│   │   ├── projects.tsx     # Project list
│   │   └── settings.tsx     # Settings & account info
│   ├── _layout.tsx          # Root layout with auth protection
│   └── login.tsx            # Login screen
├── contexts/
│   └── AuthContext.tsx      # Authentication context & hooks
├── lib/
│   └── supabase.ts          # Supabase client configuration
├── hooks/                   # Custom React hooks
├── components/              # Reusable UI components
├── assets/                  # Images, fonts, etc.
└── package.json
```

---

## Tech Stack Details

### Core Technologies
- **Expo SDK 54** - Universal React Native framework
- **React 19.1.0** - UI library
- **React Native 0.81.5** - Cross-platform mobile framework
- **TypeScript 5.9.3** - Type safety

### Backend Integration
- **Supabase Client** - Database and auth
- **Expo SecureStore** - Secure token storage
- **Expo Router** - File-based navigation

### UI Components
- **@expo/vector-icons** - Feather icons
- **React Native built-ins** - View, Text, FlatList, etc.

---

## Features Implemented

### Week 3 MVP (Current)

✅ **Authentication**
- Login with email/password
- Secure token storage with SecureStore
- Admin role verification
- Protected routes

✅ **Customer Management**
- List all customers with search
- View customer details (name, email, company)
- See subscription status and MRR
- Project count per customer
- Filter by status (active, trial, past_due, cancelled)

✅ **Project Tracking**
- List all projects with filters
- Filter by status (INTAKE, DESIGN, DEV, QA, COMPLETE)
- View project details (name, customer, product type)
- Visual QA scores
- Estimated delivery dates
- Product type indicators (express, concierge, website_refresh)

✅ **Settings**
- View account info (name, email, role)
- App version and tech stack info
- Sign out

---

## Backend Integration

This app connects to the Admin Console backend deployed in `/supabase`. See backend documentation:

- [API Reference](/design-first-software-factory/docs/admin-console/API_REFERENCE.md)
- [Test Data](/design-first-software-factory/docs/admin-console/TEST_DATA.md)
- [Backend README](/supabase/README.md)

### API Endpoints Used

- **Auth**: `supabase.auth.signInWithPassword()`
- **Customers**: `supabase.from('customers').select()`
- **Projects**: `supabase.from('projects').select()`
- **Admin Users**: `supabase.from('admin_users').select()`

---

## Next Steps (Week 4-5)

### Week 4: Enhanced Features
- [ ] Customer detail screens with edit capability
- [ ] Project detail screens with notes
- [ ] Create new customer flow
- [ ] Create new project flow
- [ ] File upload for design files
- [ ] Invoice viewing

### Week 5: Polish & Deploy
- [ ] Error handling improvements
- [ ] Loading states
- [ ] Optimistic updates
- [ ] Offline support
- [ ] Push notifications setup
- [ ] EAS Build configuration
- [ ] Production deployment

---

## Development Tips

### Debugging

```bash
# View logs
npx expo start --dev-client

# Clear cache
npx expo start -c

# Reset metro bundler
npx expo start --reset-cache
```

### TypeScript

All files use TypeScript with strict mode enabled. Types for Supabase tables should be generated from the database schema.

### Styling

Uses React Native's StyleSheet API. Design system:
- Primary color: `#007AFF` (iOS blue)
- Background: `#f5f5f5`
- Card background: `#fff`
- Border: `#E5E5EA`
- Text colors: `#1a1a1a`, `#8E8E93`

---

## Deployment

### Build for Production

```bash
# Install EAS CLI
npm install -g eas-cli

# Configure EAS
eas build:configure

# Build iOS
eas build --platform ios

# Build Android
eas build --platform android
```

### Environment Variables

For production, set environment variables in `eas.json` or use EAS Secrets:

```bash
eas secret:create --name EXPO_PUBLIC_SUPABASE_URL --value <url>
eas secret:create --name EXPO_PUBLIC_SUPABASE_ANON_KEY --value <key>
```

---

## Testing

### Manual Testing Checklist

- [ ] Login with admin credentials
- [ ] View customers list
- [ ] Search customers by name/email
- [ ] View projects list
- [ ] Filter projects by status
- [ ] Search projects by name
- [ ] View settings screen
- [ ] Sign out

### Test Data

Use the seeded test data (5 customers, 5 projects). See [TEST_DATA.md](/design-first-software-factory/docs/admin-console/TEST_DATA.md) for details.

---

## Troubleshooting

### Issue: "Supabase URL not configured"
**Solution**: Ensure `.env` file exists with correct `EXPO_PUBLIC_SUPABASE_URL`

### Issue: "Not an admin user"
**Solution**: Check that your user email is in the `admin_users` table with an active admin role

### Issue: "Can't connect to backend"
**Solution**: Verify Supabase project is running and RLS policies are deployed

### Issue: "Module not found"
**Solution**: Run `npm install` and restart with `npx expo start -c`

---

## Support

For backend issues, see `/supabase/README.md`
For API issues, see `/design-first-software-factory/docs/admin-console/API_REFERENCE.md`

---

**Status**: ✅ Week 3 MVP Complete - Ready for testing and enhancement

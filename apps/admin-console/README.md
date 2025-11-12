# Admin Console

**Branch**: `claude/security-fixes-011CV4GmG4H3M7Seg9KC2ZcP`

The Admin Console code exists on a separate branch. To merge it into this consolidated structure:

```bash
git checkout claude/security-fixes-011CV4GmG4H3M7Seg9KC2ZcP
git mv admin-console/* apps/admin-console/
git checkout claude/expo-factory-web-deployment-011CV4GmG4H3M7Seg9KC2ZcP
git merge claude/security-fixes-011CV4GmG4H3M7Seg9KC2ZcP
```

## About Admin Console

Universal Expo React Native app for managing customers, projects, and invoices.

**Platforms**: iOS, Android, Web
**Status**: ✅ Security-hardened, ready for deployment

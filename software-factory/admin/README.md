# Factory Admin

Admin interface for managing software factory projects, health alerts, and capability launches.

## Features

- **Dashboard** highlighting project count, health alerts, and quick links
- **Project registry** with create/edit support and design-token editing
- **Health alert feed** sourced from `software-factory/data/health-alerts.json`
- **Splash creator launchpad** linking to the interactive splash workflow

## Development (future)

```bash
npm install
npm run dev
```

The admin runs alongside other factory apps (splash creator, weight tracker, etc.). Update `software-factory/data/projects.json` to seed new entries until full CRUD services are in place.

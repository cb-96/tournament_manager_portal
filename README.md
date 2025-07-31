# Tournament Manager Portal

A custom Odoo 18.0 addon to manage tournaments for a sports federation. This module provides a public-facing portal for club managers to create teams, manage lineups, and follow tournament progress — all from within Odoo.

## 🏆 Features

- Organize and manage tournaments
- View current standings and upcoming gamedays
- Schedule matches per tournament
- Portal access for club managers:
  - Create and manage teams
  - Set and update lineups
- Mobile-friendly interface for on-the-go access

## 🚀 Installation

This module is designed to run inside an Odoo 18.0 Docker environment.

### Prerequisites
- Docker & Docker Compose installed
- Odoo 18.0 running via `docker-compose.yml`
- PostgreSQL service configured in Docker

### Steps

1. Clone the repository into your Odoo addons folder:

   ```bash
   git clone https://github.com/cb-96/tournament_manager_portal.git
   ```

2. Add the module path to your Odoo configuration (addons_path).

3. Restart your Odoo container:
   ```
   docker compose restart odoo
   ```

4. Activate the module in Odoo:
    - Go to __Apps__
    - Click __Update Apps List__
    - Search for __Tournament Manager Portal__
    - Click __Install__

## 🧑‍💼 Portal Access

Club managers can log in to the portal to:
- Register teams for tournaments
- Manage player lineups
- View tournament schedules and standings

Access is granted via Odoo's portal user system. Make sure club managers are assigned the correct portal group.

## 📁 Repository Structure

```
tournament_manager_portal/
├── models/
│   └── *.py               # Business logic and data models
├── views/
│   └── *.xml              # UI definitions for backend and portal
├── security/
│   └── ir.model.access.csv  # Access control rules
├── static/
│   └── src/               # Assets (JS, CSS, images)
├── __manifest__.py        # Module metadata
└── README.md              # You're reading it!
```

## 🛠 Development Notes

Built for Odoo 18.0
Tested in Dockerized environments
Designed with mobile usability in mind

## 📸 Screenshots
Add screenshots or GIFs here to showcase the portal interface.

## 📬 Feedback & Contributions
Feel free to open issues or submit pull requests. Feedback is welcome!
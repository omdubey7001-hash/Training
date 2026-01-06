# Next.js Dashboard Application

A modern, responsive dashboard application built using **Next.js App Router** and **Tailwind CSS**.  
The project follows a clean folder structure, reusable components, and layout-based architecture for scalability and performance.

---

## 🚀 Features

- App Router based routing (`app/` directory)
- Root Layout for global UI (Navbar + Sidebar)
- Responsive dashboard layout
- Modular and reusable UI components
- Clean and scalable folder structure
- Tailwind CSS for fast styling

---

## 📸 Screenshots

> _Screenshots of the application UI_

### Dashboard View
![Dashboard Screenshot](./screenshots/dashboard.png)

### Sidebar & Navigation
![Sidebar Screenshot](./screenshots/sidebar.png)

### Tables / Pages
![Tables Screenshot](./screenshots/tables.png)

> 📌 **Note:** Add your screenshots inside a `screenshots/` folder at the project root and update filenames if needed.

---

## 📁 Folder Structure

```
project-root/
│
├── app/
│   ├── layout.jsx        # Root Layout (global layout)
│   ├── page.jsx          # Home page
│   ├── globals.css       # Global styles
│   │
│   ├── dashboard/
│   │   └── page.jsx      # Dashboard page
│   │
│   └── tables/
│       └── page.jsx      # Tables page
│
├── components/
│   └── ui/
│       ├── Navbar.jsx
│       ├── Sidebar.jsx
│       ├── Card.jsx
│       └── Table.jsx
│
├── public/
│   └── assets/           # Images, icons, static files
│
├── screenshots/          # Application screenshots
│
├── package.json
├── tailwind.config.js
└── README.md
```

## 🧩 Components List

### Layout Components
- **RootLayout**  
  Acts as the top-level wrapper for the entire application. It defines the global HTML structure and ensures persistent UI elements such as the Navbar and Sidebar remain consistent across all routes.

- **Navbar**  
  A top navigation component used for displaying page titles, user actions, and global controls. It remains visible across all pages.

- **Sidebar**  
  A persistent side navigation component that provides links to different sections of the dashboard. It helps in structured and intuitive navigation.

---

### UI Components
- **Card**  
  A reusable UI component used to display metrics, summaries, or grouped content within the dashboard.

- **Table**  
  A reusable component responsible for rendering tabular data in a clean and responsive manner.

---

### Page Components
- **Dashboard Page**  
  The main dashboard view that aggregates cards, tables, and key application data.

- **Tables Page**  
  Displays structured data using the Table component and demonstrates reusable component patterns.

---

### Utility & Styling
- **globals.css**  
  Contains global styles and Tailwind CSS base configuration used across the entire application.

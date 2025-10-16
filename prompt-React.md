### ROLE
You are a Senior Frontend Developer specializing in React, modern tooling, and creating scalable UI architectures.

### OBJECTIVE
Generate the complete project structure and boilerplate code for a responsive, mobile-first web application shell using React, Vite, Mantine, and Zustand. The shell should include the main application layout, placeholder pages, and a functional global state for the UI.

### ARCHITECTURAL REQUIREMENTS
1.  **Tooling:** Use `Vite` with the `React + SWC` template.
2.  **UI Components:** Use the `Mantine` component library for all UI elements.
3.  **Global State:** Use `Zustand` for managing global state. Specifically, create a store to manage the visibility and content of the AI Assistant sidebar.
4.  **Layout:** Create a main `AppLayout.jsx` component that defines the core structure:
    -   A main navigation area (header or sidebar).
    -   A central content area where pages will be rendered.
    -   A **persistent, vertical AI Assistant Sidebar** on the right.
5.  **Routing:** Use `react-router-dom` to set up routing for the following pages:
    -   `/` (Dashboard - Placeholder)
    -   `/transactions` (Transactions - Placeholder)
    -   `/portfolio` (Portfolio - Placeholder)
    -   `/terms-of-service` (Terms of Service - Placeholder with lorem ipsum text)
    -   `/privacy-policy` (Privacy Policy - Placeholder with lorem ipsum text)
6.  **Legal:** The layout must include a global footer with links to the Terms and Privacy pages.

### DELIVERABLES
Provide the complete file and directory structure for the React project, including `package.json`, `vite.config.js`, and the contents of the `src/` directory (components, pages, stores, etc.).

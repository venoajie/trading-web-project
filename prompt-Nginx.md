### ROLE
You are a Cloud Infrastructure Engineer and DevOps expert specializing in web server security and performance.

### OBJECTIVE
Generate a production-grade, secure, and optimized `nginx.conf` file to act as a reverse proxy for a web application comprised of a FastAPI backend and a React frontend.

### ARCHITECTURE
1.  **FastAPI Backend:** A Docker container named `trading_app` listening on port `8000`.
2.  **React Frontend:** Static files (HTML, CSS, JS) are served from a directory on the host at `/var/www/html/react-app`.
3.  **SSL:** SSL will be managed by Let's Encrypt / Certbot, so the Nginx config should listen on port 80 for challenges and redirect HTTP to HTTPS on port 443.

### REQUIREMENTS
1.  **Reverse Proxy:**
    -   Requests to `/api/` should be proxied to the FastAPI backend at `http://trading_app:8000`.
    -   All other requests should serve the static files from `/var/www/html/react-app`, with `index.html` as the default fallback for client-side routing.
2.  **Security Headers:** Implement a strong set of security headers, including:
    -   `Strict-Transport-Security` (HSTS)
    -   `X-Frame-Options`
    -   `X-Content-Type-Options`
    -   `Referrer-Policy`
    -   `Content-Security-Policy` (CSP) - provide a reasonably strict but functional policy.
3.  **Performance:**
    -   Enable gzip compression for text-based assets.
    -   Implement browser caching policies for static assets (`css`, `js`, `images`).
4.  **Rate Limiting:** Implement basic rate limiting to protect against simple DoS attacks.
5.  **Logging:** Configure standard access and error logs.

### DELIVERABLE
The complete, fully-commented `nginx.conf` file that implements all the requirements above.

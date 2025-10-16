
#!/bin/bash
#
# deploy.sh: A script to automate the deployment of the Trading App.
# This script should be run from the project's root directory on the deployment host.
#

# Stop execution if any command fails
set -e

# --- Configuration Variables ---
APP_NAME="trading_app"
FRONTEND_DIR="trading-app-frontend"
NGINX_STATIC_ROOT="/var/www/tradingapp/static"
DOCKER_COMPOSE_FILE="docker-compose.yml"

echo "--- [Step 1/6] Pulling latest changes from Git ---"
# In a real CI/CD, this might be a checkout step. For manual deployment, it's a pull.
git pull origin main
echo "Git pull complete."
echo ""

echo "--- [Step 2/6] Building the React frontend application ---"
# Check if the frontend directory exists
if [ ! -d "$FRONTEND_DIR" ]; then
    echo "Error: Frontend directory '$FRONTEND_DIR' not found."
    exit 1
fi
# Navigate into the frontend directory, install dependencies, and run the build
(cd "$FRONTEND_DIR" && npm install && npm run build)
echo "Frontend build complete. Artifacts are in '$FRONTEND_DIR/dist'."
echo ""

echo "--- [Step 3/6] Building and recreating the backend Docker container ---"
# Build the Docker image with the linux/arm64 platform specified for OCI Ampere VMs.
# --no-cache can be added for a clean build if needed.
docker compose -f "$DOCKER_COMPOSE_FILE" build --build-arg PLATFORM=linux/arm64
# Stop and remove the old container, then start the new one.
# The '--force-recreate' flag ensures the new image is used.
docker compose -f "$DOCKER_COMPOSE_FILE" up -d --force-recreate
echo "Docker container has been rebuilt and started."
echo ""

echo "--- [Step 4/6] Applying database migrations ---"
# Execute the 'alembic upgrade head' command inside the newly running container.
# This ensures the database schema is up-to-date with the new code.
docker compose -f "$DOCKER_COMPOSE_FILE" exec -T "$APP_NAME" alembic upgrade head
echo "Database migrations applied successfully."
echo ""

echo "--- [Step 5/6] Syncing static frontend assets to Nginx root ---"
# Ensure the Nginx root directory exists
sudo mkdir -p "$NGINX_STATIC_ROOT"
# Use rsync to efficiently and safely copy the built files.
# The '--delete' flag removes old files from the destination.
# The trailing slash on the source directory is important for rsync's behavior.
sudo rsync -av --delete "$FRONTEND_DIR/dist/" "$NGINX_STATIC_ROOT/"
echo "Static assets synced to $NGINX_STATIC_ROOT."
echo ""

echo "--- [Step 6/6] Cleaning up Docker build cache ---"
# Optional: Prune the build cache to save disk space.
docker buildx prune -f
echo "Docker build cache pruned."
echo ""

echo "======================================================"
echo "✅ DEPLOYMENT COMPLETE"
echo "The Trading App has been successfully deployed."
echo "======================================================"
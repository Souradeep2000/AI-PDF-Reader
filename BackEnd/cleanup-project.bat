@echo off
echo ===============================
echo  AI Project Docker Cleanup
echo ===============================

echo Stopping containers...
docker compose down

echo Removing stopped containers...
docker container prune -f

echo Removing dangling images...
docker image prune -f

echo Clearing build cache...
docker builder prune -f

echo Removing unused networks/layers...
docker system prune -f

echo Done! Keeping volumes safe (DB preserved)
pause
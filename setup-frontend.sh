# Create frontend directory structure
mkdir -p lang-portal/frontend/src/{components,stores,services,utils,views,types}

# Move existing files to their new locations
mv src/types/models.ts lang-portal/frontend/src/types/
mv src/services/api.ts lang-portal/frontend/src/services/
mv src/services/api.types.ts lang-portal/frontend/src/services/
mv src/stores/app.ts lang-portal/frontend/src/stores/
mv src/utils/index.ts lang-portal/frontend/src/utils/
mv src/router/index.ts lang-portal/frontend/src/router/
mv src/views/*.vue lang-portal/frontend/src/views/

# Move config files to frontend root
mv tsconfig.json lang-portal/frontend/
mv vite.config.js lang-portal/frontend/
mv package.json lang-portal/frontend/
mv .env lang-portal/frontend/ 
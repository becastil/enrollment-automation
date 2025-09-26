#!/bin/bash

echo "===================================="
echo "Prime Enrollment Web Setup"
echo "===================================="
echo

echo "Installing root dependencies..."
npm install

echo
echo "Installing server dependencies..."
cd server
npm install
cd ..

echo
echo "Installing client dependencies..."
cd client
npm install
cd ..

echo
echo "===================================="
echo "Setup complete!"
echo "===================================="
echo
echo "To start the application, run:"
echo "  npm run dev"
echo
echo "The application will be available at:"
echo "  Frontend: http://localhost:5173"
echo "  Backend:  http://localhost:5000"
echo
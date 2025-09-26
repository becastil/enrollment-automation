# Prime Enrollment Validation Web Application

A modern web-based system for validating and managing Prime enrollment data across facilities, replacing the Excel/Python workflow with an intuitive visual interface.

## Features

### Core Functionality
- **📤 Excel File Upload**: Drag-and-drop interface for uploading source data files
- **✅ Real-time Validation**: Instant validation with visual feedback
- **📊 Tab Grid Visualization**: Color-coded grid showing expected vs actual values
- **🔍 Discrepancy Detection**: Smart alerts for mismatches and issues
- **⚙️ Configuration Management**: Visual plan code mapper and block aggregation editor
- **📥 Export & Reporting**: Generate corrected Excel files and validation reports

### Key Advantages
- **No Excel Corruption**: Work with data, not fragile macros
- **Visual Feedback**: Color-coded cells make issues immediately obvious
- **Multi-user Support**: Team collaboration capabilities
- **Audit Trail**: Track all changes and validations
- **Cloud-based**: Access from anywhere via Render deployment

## Tech Stack

### Frontend
- React 18 with TypeScript
- Redux Toolkit for state management
- Tailwind CSS for styling
- Recharts for data visualization
- React Dropzone for file uploads

- Centralized design tokens defined in `client/src/theme/designTokens.ts` covering color, spacing, typography, radii, shadows, and z-index. Additional guidance lives in `docs/design-system.md`.
- Runtime theme engine via `client/src/theme/ThemeProvider.tsx` applies tokens as CSS variables on the document `data-theme` attribute (`light` or `dark`).
- Tailwind is configured to consume semantic tokens only; component styles use classes such as `bg-surface`, `text-text-muted`, and `px-md` instead of hard-coded hex or numbers.
- Use the `useTheme()` hook to toggle themes or query the active theme inside components.

### Backend
- Node.js with Express
- TypeScript
- XLSX for Excel processing
- PostgreSQL (optional, for persistence)

## Installation

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/prime-efr-web.git
cd prime-efr-web
```

2. Install frontend dependencies:
```bash
cd client
npm install
```

3. Install backend dependencies:
```bash
cd ../server
npm install
```

4. Create environment variables:
```bash
# In server directory, create .env file
cp .env.example .env
```

## Development

### Run Frontend
```bash
cd client
npm run dev
# Opens at http://localhost:5173
```

### Run Backend
```bash
cd server
npm run dev
# Runs at http://localhost:5000
```

## Usage

### 1. Upload Data
- Navigate to "Upload Data" tab
- Drag and drop your Excel source file
- Preview the data to ensure correct parsing

### 2. View Validation
- Switch to "Validation Dashboard" tab
- Review control totals and tier distribution
- Check validation summary for errors/warnings

### 3. Inspect Tab Grid
- Expand individual tabs to see detailed validation
- Green cells = matching values
- Red cells = discrepancies
- Review block-level aggregations

### 4. Resolve Discrepancies
- Click on issues in the Discrepancy Panel
- Review suggested fixes
- Apply fixes with one click

### 5. Configure Mappings
- Go to "Configuration" tab
- Add/edit plan code mappings
- Export/import configuration sets

### 6. Export Results
- Generate corrected Excel files
- Export validation reports
- Download audit logs

## API Endpoints

### Upload
- `POST /api/upload/parse` - Parse Excel file
- `POST /api/upload/validate-structure` - Validate file structure

### Enrollment
- `POST /api/enrollment/process` - Process enrollment data
- `GET /api/enrollment/summary` - Get enrollment summary
- `POST /api/enrollment/export` - Export processed data

### Validation
- `POST /api/validation/validate` - Run validation
- `GET /api/validation/rules` - Get validation rules
- `POST /api/validation/apply-fix` - Apply suggested fix

### Configuration
- `GET /api/config` - Get all configuration
- `POST /api/config/plan-mappings` - Update plan mappings
- `GET /api/config/export` - Export configuration
- `POST /api/config/import` - Import configuration

## Deployment

### Deploy to Render

1. Push code to GitHub

2. Create new Web Service on Render:
   - Connect GitHub repository
   - Build Command: `cd server && npm install && npm run build`
   - Start Command: `cd server && npm start`

3. Create Static Site for frontend:
   - Build Command: `cd client && npm install && npm run build`
   - Publish Directory: `client/dist`

4. Set environment variables:
   - `NODE_ENV=production`
   - `PORT=5000`
   - Add database URL if using PostgreSQL

## Project Structure

```
prime-efr-web/
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── store/         # Redux store
│   │   ├── utils/         # Helper functions
│   │   └── App.tsx        # Main app component
│   └── package.json
├── server/                 # Express backend
│   ├── src/
│   │   ├── routes/        # API endpoints
│   │   ├── services/      # Business logic
│   │   ├── validators/    # Data validation
│   │   └── index.ts       # Server entry point
│   └── package.json
└── README.md
```

## Data Flow

1. **Upload**: Excel file → Parse → Validate structure
2. **Process**: Source data → Normalize → Apply mappings → Aggregate
3. **Validate**: Check totals → Detect mismatches → Generate issues
4. **Display**: Tab grid → Color coding → Discrepancy alerts
5. **Export**: Corrected data → Excel/CSV → Download

## Troubleshooting

### Common Issues

**File upload fails**
- Ensure file is .xlsx, .xls, or .csv format
- Check file size (max 10MB)
- Verify Sheet1 exists with correct headers

**Validation shows many errors**
- Review plan code mappings in Configuration
- Check excluded client IDs
- Verify tier normalization rules

**Export not working**
- Ensure all validations pass
- Check browser console for errors
- Verify backend is running

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues or questions, please open a GitHub issue or contact the development team.

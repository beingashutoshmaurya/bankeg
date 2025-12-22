# GIROBANK - Modern Banking Application

A comprehensive, full-stack banking application built with Vue.js (Frontend) and Flask (Backend), featuring AI-powered banking assistance, multi-role support (Customer, Employee, Manager), and modern UI/UX.

## About

GIROBANK is a modern banking application that provides a complete banking experience with features including fund transfers, bill payments, KYC verification, dispute resolution, and AI-powered spending coaching. The application supports three distinct user roles: Customers, Employees, and Managers, each with tailored dashboards and functionalities.

## Features

### Customer Features
- **Dashboard**: Real-time balance, transaction history, spending analytics with dynamic pie charts
- **Fund Transfers**: Secure money transfers with OTP and transaction password verification
- **Beneficiary Management**: Add, verify, and manage beneficiaries with cooling period protection
- **Bill Payments**: Pay utility bills, mobile recharges, and FASTag top-ups
- **Transaction History**: View and export transactions in JSON, CSV, or PDF formats
- **Profile Management**: View account details, KYC status, and uploaded documents
- **AI Assistant**: Personal spending coach and general banking chatbot powered by LLM
- **Dispute Resolution**: Raise and track customer disputes with status updates
- **Dark Mode**: Global dark mode toggle for better user experience

### Employee Features
- **KYC Verification**: Review and approve/reject customer KYC documents
- **AI-Powered KYC Analysis**: Automated document validation using AI
- **Customer Issue Resolution**: Handle customer disputes with AI-suggested responses
- **Task Management**: View and complete assigned tasks with priority tracking
- **Dashboard**: Overview of pending KYC, customer issues, and task statistics

### Manager Features
- **Management Dashboard**: Comprehensive overview with charts and statistics
- **Task Creation**: Create and assign tasks to employees
- **Active Task Monitoring**: Track task progress and completion status
- **KYC Approval**: Final approval authority for customer KYC documents
- **Performance Analytics**: Visual charts for team performance and task metrics

### AI Features
- **KYC Document Analyzer**: Automated validation of Aadhaar, PAN, Photo, and Signature documents
- **Dispute Drafter**: AI-generated response suggestions for customer issues
- **Spending Coach**: Personalized spending analysis and recommendations
- **General Chatbot**: Intelligent banking assistant for customer queries

## Tech Stack

### Frontend
- **Vue.js 3**: Progressive JavaScript framework
- **Vue Router**: Client-side routing
- **Vuex**: State management
- **Axios**: HTTP client for API calls
- **Bootstrap 5**: UI framework and styling
- **Vuetify**: Material Design component framework
- **Chart.js**: Data visualization
- **Lucide Vue Next**: Modern icon library

### Backend
- **Flask**: Python web framework
- **Flask-SQLAlchemy**: ORM for database operations
- **Flask-RESTful**: RESTful API framework
- **Flask-CORS**: Cross-origin resource sharing
- **SQLite**: Database
- **Llama.cpp (llama-cpp-python)**: Local LLM inference for AI features
- **FPDF**: PDF generation
- **Pillow**: Image processing
- **Pytesseract**: OCR for document processing

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**: For the backend server
- **Node.js (LTS) & npm**: For the frontend application
- **Git**: For cloning the repository

> **Note for Windows Users**: We strongly recommend using **WSL (Windows Subsystem for Linux)** with Ubuntu for better compatibility.

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd "Banking Application-3"
```

### 2. Backend Setup (Flask)

Navigate to the backend directory:

```bash
cd backend
```

**Create a virtual environment:**

```bash
# macOS / Linux / WSL
python3 -m venv venv
```

**Activate the virtual environment:**

```bash
# macOS / Linux / WSL
source venv/bin/activate

# Windows (PowerShell)
.\venv\Scripts\activate
```

**Install dependencies:**

```bash
pip install -r requirements.txt
```

**Note**: The `llama-cpp-python` package may take some time to install. For Apple Silicon (M1/M2), it will automatically use Metal acceleration.

### 3. Environment Variables

Create a `.env` file in the `backend` directory with the following variables:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### 4. Database Setup

The database will be automatically created when you first run the application. The SQLite database file will be located at `backend/instance/banking.db`.

### 5. AI Model Setup

The AI features require a quantized LLM model. Place your model file (e.g., `mistral-7b-instruct-v0.2.Q4_K_M.gguf`) in the `backend/models/` directory. The application is configured to use this model for AI-powered features.

### 6. Frontend Setup (Vue.js)

Open a **new** terminal tab/window and navigate to the frontend directory:

```bash
cd frontend
```

**Install Node dependencies:**

```bash
npm install
```

If you encounter peer dependency issues, use:

```bash
npm install --legacy-peer-deps
```

## Running the Application

You will need two running terminal processes: one for the backend and one for the frontend.

### 1. Start the Backend Server

In your **backend** terminal (with `venv` activated):

```bash
# Ensure you are in the /backend directory
python3 app.py
```

The backend server will start on `http://127.0.0.1:5000`.

### 2. Start the Frontend Application

In your **frontend** terminal:

```bash
# Ensure you are in the /frontend directory
npm run serve
```

The frontend development server will start, usually accessible at `http://localhost:8080`.

### 3. Access the Application

Open your browser and navigate to:
- **Frontend**: http://localhost:8080
- **Backend API**: http://127.0.0.1:5000

## 📁 Project Structure

```
Banking Application-3/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── models.py              # Database models
│   ├── resources.py           # Flask-RESTful API resources
│   ├── ai_service.py          # AI service for LLM integration
│   ├── requirements.txt       # Python dependencies
│   ├── instance/
│   │   └── banking.db         # SQLite database
│   ├── models/
│   │   └── *.gguf             # AI model files
│   └── uploads/
│       └── kyc/               # KYC document uploads
│
├── frontend/
│   ├── src/
│   │   ├── components/        # Vue components
│   │   │   ├── Dashboard.vue
│   │   │   ├── Payments.vue
│   │   │   ├── Profile.vue
│   │   │   ├── AIAssistant.vue
│   │   │   ├── CustomerDisputes.vue
│   │   │   ├── EmployeeDashboard.vue
│   │   │   └── ManagerDashboardLayout.vue
│   │   ├── router/
│   │   │   └── index.js       # Vue Router configuration
│   │   ├── composables/
│   │   │   └── useDarkMode.js # Dark mode composable
│   │   ├── services/
│   │   │   └── api.js         # Axios API configuration
│   │   └── views/
│   │       └── Home.vue       # Landing page
│   ├── public/
│   │   └── Fastag-logo.png    # Assets
│   └── package.json           # Node dependencies
│
└── README.md                  # This file
```

## API Endpoints Overview

### Authentication
- `POST /register` - Customer registration
- `POST /login` - Customer login
- `POST /verify_otp` - OTP verification
- `POST /forgot_password` - Password reset request
- `POST /reset_password` - Password reset

### Customer Operations
- `GET /customer/balance/<customer_id>` - Get account balance
- `GET /customer/transactions/<customer_id>` - Get transaction history
- `GET /customer/beneficiaries/<customer_id>` - List beneficiaries
- `POST /customer/add-beneficiary` - Add beneficiary
- `POST /customer/initiate-transfer` - Initiate fund transfer
- `POST /customer/confirm-transfer` - Confirm transfer with OTP
- `GET /customer/spending-categories/<customer_id>` - Get spending categories
- `GET /customer/profile/<customer_id>` - Get customer profile

### Payments
- `POST /customer/initiate-pay-bill` - Initiate bill payment
- `POST /customer/initiate-recharge` - Initiate mobile recharge
- `POST /customer/initiate-fastag` - Initiate FASTag top-up
- `POST /customer/confirm-pay-bill` - Confirm bill payment
- `POST /customer/confirm-recharge` - Confirm recharge
- `POST /customer/confirm-fastag` - Confirm FASTag top-up

### KYC
- `POST /kyc/upload/<customer_id>` - Upload KYC documents
- `POST /kyc/send_otp/<customer_id>` - Send KYC OTP
- `POST /kyc/verify_otp/<customer_id>` - Verify KYC OTP
- `GET /profile/kyc_docs/<filepath>` - Serve KYC documents

### AI Features
- `POST /api/chat` - General chatbot
- `GET /api/customer/coach/<customer_id>` - Spending coach
- `POST /api/kyc/analyze/<kyc_id>` - Analyze KYC documents
- `GET /api/employee/draft-dispute/<issue_id>` - Draft dispute response

### Employee/Manager
- `GET /api/task/get` - Get tasks
- `POST /api/task/create` - Create task
- `PUT /api/task/update/<task_id>` - Update task
- `GET /api/issue/get` - Get issues
- `POST /api/issue/create` - Create issue
- `PUT /api/issue/update/<issue_id>` - Update issue

## User Roles

### Customer
- Register with email, phone, and passwords
- Upload KYC documents (Aadhaar, PAN, Photo, Signature)
- Perform banking operations after account activation
- Access AI assistant and spending coach

### Employee
- Login with employee credentials
- Review and approve/reject KYC documents
- Handle customer disputes
- Complete assigned tasks

### Manager
- Login with manager credentials
- Create and assign tasks to employees
- Approve customer KYC documents
- Monitor team performance

## UI/UX Features

- **Modern Design**: Clean, professional interface with Bootstrap 5
- **Dark Mode**: Global dark mode toggle with persistent state
- **Responsive Layout**: Mobile-friendly design
- **Color-Coded Status**: Visual indicators for pending/completed items
- **Real-time Updates**: Dynamic data fetching and updates
- **Interactive Charts**: Visual representation of spending and analytics
- **Smooth Animations**: Enhanced user experience with transitions

## Security Features

- **Password Hashing**: Secure password storage using Werkzeug
- **OTP Verification**: Two-factor authentication for sensitive operations
- **Transaction Password**: Additional security layer for transactions
- **Cooling Period**: Protection against immediate beneficiary transfers
- **CORS Protection**: Configured CORS headers for secure API access
- **File Upload Security**: Secure filename handling for document uploads

## Troubleshooting

### Common Issues

**1. `ModuleNotFoundError` in Backend**
- **Cause**: Virtual environment not activated or packages not installed
- **Fix**: Ensure you see `(venv)` in your terminal prompt. Run `source venv/bin/activate` and then `pip install -r requirements.txt` again

**2. Port Already in Use**
- **Backend**: If port 5000 is taken, find and kill the process or edit `app.py` to use a different port
- **Frontend**: If port 8080 is taken, `npm run serve` will usually ask if you want to use a different port (e.g., 8081)

**3. Frontend Dependency Errors**
- **Fix**: Ensure you are using a stable Node version (v16 or v18 recommended). Try deleting `node_modules` and `package-lock.json` and running `npm install --legacy-peer-deps` again

**4. CORS Errors**
- **Fix**: The application includes comprehensive CORS configuration. Ensure the backend is running and the `@app.after_request` handler is active

**5. AI Model Not Loading**
- **Fix**: Ensure the model file is in `backend/models/` directory and the path in `ai_service.py` is correct

**6. Database Errors**
- **Fix**: Delete `backend/instance/banking.db` and restart the application to recreate the database

**7. Email Not Sending**
- **Fix**: Check your `.env` file has correct SMTP credentials. For Gmail, use an App Password instead of your regular password

## Development Notes

### Database Migrations
If you need to add new columns to existing tables, create migration scripts similar to:
- `backend/add_kyc_ai_columns.py`
- `backend/add_issue_resolution_column.py`

### Adding New Features
1. Backend: Add routes in `app.py` or resources in `resources.py`
2. Frontend: Create Vue components in `frontend/src/components/`
3. Routing: Add routes in `frontend/src/router/index.js`
4. API Integration: Use Axios in components to call backend endpoints

### AI Model Configuration
The AI service is configured in `backend/ai_service.py`. To change the model:
1. Update `MODEL_PATH` in `ai_service.py`
2. Adjust `n_ctx`, `n_gpu_layers`, and other parameters based on your hardware

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is part of a Software Engineering course project (SEP-41).

## Team

Developed by Team 41 for Software Engineering Project.

## Support

For issues, questions, or contributions, please open an issue on the repository.

---

**Note**: This is a development project. For production use, additional security measures, testing, and deployment configurations would be required.


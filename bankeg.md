# BANKEG Banking Application - Technical Documentation

## Executive Summary

BANKEG is a comprehensive full-stack banking application built with Vue.js 3 (frontend) and Flask (backend). The application provides a complete banking experience with features including fund transfers, bill payments, KYC verification, dispute resolution, and AI-powered banking assistance. The system supports three distinct user roles: Customers, Employees, and Managers, each with tailored dashboards and functionalities.

## Application Architecture

### Technology Stack

**Frontend:**
- Vue.js 3.2.13 (Progressive JavaScript framework)
- Vue Router 4.0.3 (Client-side routing)
- Vuex 4.0.0 (State management)
- Axios 1.12.2 (HTTP client for API calls)
- Bootstrap 5 (UI framework and styling)
- Vuetify 3.0.0-beta (Material Design component framework)
- Chart.js 4.5.1 (Data visualization)
- Lucide Vue Next 0.556.0 (Modern icon library)
- Webfontloader 1.0.0 (Font loading)

**Backend:**
- Flask 3.1.2 (Python web framework)
- Flask-SQLAlchemy 3.1.1 (ORM for database operations)
- Flask-RESTful 0.3.10 (RESTful API framework)
- Flask-CORS 6.0.1 (Cross-origin resource sharing)
- SQLite (Database)
- llama-cpp-python (Local LLM inference for AI features)
- FPDF 1.7.2 (PDF generation)
- Pillow (Image processing)
- Pytesseract (OCR for document processing)
- scikit-learn (Machine learning utilities)

### Project Structure

```
Banking Application-3/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── models.py              # Database models
│   ├── resources.py           # Flask-RESTful API resources
│   ├── ai_service.py          # AI service for LLM integration
│   ├── requirements.txt       # Python dependencies
│   ├── models/
│   │   └── mistral-7b-instruct-v0.2.Q4_K_M.gguf  # AI model
│   ├── instance/
│   │   └── banking.db         # SQLite database
│   └── uploads/
│       └── kyc/               # KYC document uploads
│
├── frontend/
│   ├── src/
│   │   ├── components/        # Vue components
│   │   ├── router/            # Vue Router configuration
│   │   ├── composables/       # Vue composables (useDarkMode)
│   │   ├── services/          # API and notification services
│   │   ├── store/             # Vuex store
│   │   ├── plugins/           # Vuetify and font loader plugins
│   │   ├── views/             # View components
│   │   └── assets/            # Static assets (images, logos)
│   ├── public/                # Public assets
│   └── package.json           # Node dependencies
│
└── README.md                  # Project documentation
```

## Backend Implementation

### Database Models

The application uses SQLAlchemy ORM with the following primary models:

**Customer Model:**
- Stores customer information (full_name, email, phone, passwords)
- Tracks account activation status
- Maintains relationships with accounts, beneficiaries, transactions, and KYC records

**Account Model:**
- Stores account details (account_number, balance, account_type)
- Linked to customer via foreign key
- Maintains transaction history

**Transaction Model:**
- Records all financial transactions
- Includes transaction_type, amount, timestamp, description
- Uses UUID for unique transaction identification

**KYC Model:**
- Manages KYC document uploads (Aadhaar, PAN, Photo, Signature)
- Tracks verification status (pending/approved/rejected)
- Stores AI validation results and remarks
- Includes OTP verification for document submission

**Beneficiary Model:**
- Stores beneficiary information for fund transfers
- Implements cooling period protection
- Tracks verification status

**Issue Model:**
- Customer dispute/issue tracking
- Stores issue description, status, and resolution
- Links to customer and assigned employee

**Task Model:**
- Task management for employees
- Includes priority, due_date, status tracking
- Links to customer and assigned employee

**Bank_employee Model:**
- Employee and manager account management
- Role-based access control (employee/manager)

### API Endpoints

**Authentication:**
- POST /register - Customer registration
- POST /login - User login (customer/employee/manager)
- POST /verify_otp - OTP verification
- POST /forgot_password - Password reset request
- POST /reset_password - Password reset

**Customer Operations:**
- GET /customer/balance/<customer_id> - Get account balance
- GET /customer/transactions/<customer_id> - Get transaction history
- GET /customer/beneficiaries/<customer_id> - List beneficiaries
- POST /customer/add-beneficiary - Add beneficiary
- POST /customer/initiate-transfer - Initiate fund transfer
- POST /customer/confirm-transfer - Confirm transfer with OTP
- GET /customer/spending-categories/<customer_id> - Get spending categories
- GET /customer/profile/<customer_id> - Get customer profile

**Payments:**
- POST /customer/initiate-pay-bill - Initiate bill payment
- POST /customer/initiate-recharge - Initiate mobile recharge
- POST /customer/initiate-fastag - Initiate FASTag top-up
- POST /customer/confirm-pay-bill - Confirm bill payment
- POST /customer/confirm-recharge - Confirm recharge
- POST /customer/confirm-fastag - Confirm FASTag top-up

**KYC:**
- POST /kyc/upload/<customer_id> - Upload KYC documents
- POST /kyc/send_otp/<customer_id> - Send KYC OTP
- POST /kyc/verify_otp/<customer_id> - Verify KYC OTP
- GET /profile/kyc_docs/<filepath> - Serve KYC documents

**AI Features:**
- POST /api/chat - General chatbot
- GET /api/customer/coach/<customer_id> - Spending coach
- POST /api/kyc/analyze/<kyc_id> - Analyze KYC documents
- GET /api/employee/draft-dispute/<issue_id> - Draft dispute response
- POST /api/employee/send-dispute-email/<issue_id> - Send dispute email

**Employee/Manager:**
- GET /api/task/get - Get tasks
- POST /api/task/create - Create task
- PUT /api/task/update/<task_id> - Update task
- GET /api/issue/get - Get issues
- POST /api/issue/create - Create issue
- PUT /api/issue/update/<issue_id> - Update issue

### AI Service Implementation

The AI service (ai_service.py) uses llama-cpp-python to run a local Mistral-7B model for:

**KYC Document Analysis:**
- OCR extraction from Aadhaar and PAN documents using Pytesseract
- PDF to image conversion for PDF documents
- AI-powered validation against KYC rules
- Generates validation reports with remarks

**Dispute Response Drafting:**
- Analyzes customer issue descriptions
- Reviews recent transactions for patterns
- Checks for duplicate transactions
- Generates professional response drafts
- Includes balance verification logic

**Spending Coach:**
- Analyzes transaction history
- Provides spending insights and recommendations
- Categorizes spending patterns

**General Chatbot:**
- Handles banking-related queries
- Provides account information
- Answers general banking questions

## Frontend Implementation

### Application Structure

**Main Entry Point (main.js):**
- Initializes Vue 3 application
- Configures router, Vuex store, and Vuetify
- Loads fonts using Webfontloader
- Initializes dark mode composable

**App Component (App.vue):**
- Root component with Vuetify v-app wrapper
- Contains router-view for dynamic component rendering

### Routing Architecture

The application uses Vue Router 4 with a hybrid routing structure:

**Customer Routes (Flat Structure):**
- / - Home page
- /login - Login page
- /register - Registration page
- /verify - OTP verification
- /forgot - Forgot password
- /reset - Reset password
- /dashboard - Customer dashboard
- /transfer - Fund transfer (uses Dashboard component)
- /beneficiary - Beneficiary management
- /history - Transaction history (uses Dashboard component)
- /kyc-upload/:customer_id - KYC document upload
- /kyc-otp/:customer_id - KYC OTP verification
- /chatbot - AI Assistant
- /payments - Bill payments
- /profile - Customer profile
- /disputes - Customer disputes
- /transaction-confirm - Transaction confirmation
- /transaction-confirm-bill - Bill payment confirmation

**Manager Routes (Nested Structure):**
- /manager-dashboard - Main layout component
  - /manager-dashboard - Dashboard home
  - /manager-dashboard/active-tasks - Active tasks view
  - /manager-dashboard/create-task - Task creation

**Employee Routes (Nested Structure):**
- /employee-dashboard - Main layout component
  - /employee-dashboard - Dashboard home
  - /employee-dashboard/pending-kyc - Pending KYC review
  - /employee-dashboard/customer-issues - Customer issues management

### Frontend Components

#### Customer Components

**Dashboard.vue:**
- Main customer dashboard with multiple views (dashboard, transfer, history)
- Displays account balance with masked account number (hover to reveal)
- Quick action buttons for common operations
- Recent transactions list with filtering
- Spending summary with pie chart visualization
- Notification system with dropdown
- Dark mode support with conditional styling
- Fixed sidebar navigation (280px width, position: fixed)
- Account number masking: Shows asterisks, reveals on hover for 3 seconds
- Uses Chart.js for spending visualization
- Responsive design with Bootstrap 5 grid system

**Profile.vue:**
- Customer profile information display
- Account information with masked account number
- KYC status and document display
- Reviewer comments for KYC
- Dark mode styling
- Account number masking similar to Dashboard

**Payments.vue:**
- Bill payment interface
- Mobile recharge functionality
- FASTag top-up
- Service provider logos and selection
- Form validation and submission
- Dark mode support for all payment cards
- Modal dialogs for payment confirmation

**Beneficiary.vue:**
- Add new beneficiary form
- Beneficiary list display
- Verification status indicators
- Cooling period tracking
- Dark mode styling
- Form validation

**AIAssistent.vue:**
- AI chatbot interface
- Message history display
- User and bot message bubbles
- Loading states during AI response
- Bot avatar image (Haaland.png)
- Dark mode support
- Fixed sidebar navigation
- Input field with send button
- Scrollable message area

**CustomerDisputes.vue:**
- Dispute list display
- Expandable dispute cards
- Click to view full resolution summary
- Status indicators (Pending, In Progress, Resolved)
- Dark mode styling
- Fixed sidebar navigation

**TransactionConfirm.vue:**
- Transaction confirmation dialog
- OTP input for transfer confirmation
- Transaction details display

**TransactionConfirmBill.vue:**
- Bill payment confirmation
- OTP input for payment confirmation
- Payment details display

**KYCUpload.vue:**
- KYC document upload interface
- File upload for Aadhaar, PAN, Photo, Signature
- File preview functionality
- Upload progress indicators

**KYCOTP.vue:**
- KYC OTP verification
- OTP input field
- Resend OTP functionality

#### Employee Components

**EmployeeDashboard.vue:**
- Main employee dashboard layout
- Fixed sidebar navigation (280px width)
- Dark mode toggle with Moon/Sun icons
- User profile section with avatar
- Navigation menu for employee features
- Child route rendering for nested views

**EmployeeDashboardHome.vue:**
- Employee dashboard home page
- Statistics cards (pending KYC, customer issues, tasks)
- Quick access to main features
- Dark mode support

**PendingKYC.vue:**
- Pending KYC document review interface
- Document display and preview
- AI analysis trigger button
- Approve/Reject functionality
- AI analysis results display
- Confirmation popups for actions
- Dark mode styling

**CustomerIssues.vue:**
- Customer issue/dispute management
- Issue list with status indicators
- AI draft generation button
- Draft display area
- Send email functionality
- Button state management (disabled during processing)
- Email confirmation popup
- Page refresh after email send
- Dark mode support

#### Manager Components

**ManagerDashboardLayout.vue:**
- Main manager dashboard layout
- Fixed sidebar navigation (280px width)
- Dark mode toggle
- User profile section with avatar
- Navigation menu for manager features
- Child route rendering

**ManagerDashboardHome.vue:**
- Manager dashboard home page
- Statistics and charts
- Team performance metrics
- Dark mode support

**ManagerActiveTasks.vue:**
- Active tasks list
- Task status tracking
- Task details display

**ManagerCreateTask.vue:**
- Task creation form
- Employee assignment
- Priority and due date selection
- Form validation

**ManagerDashboard.vue:**
- Manager dashboard content
- Charts and analytics
- Dark mode support

#### Authentication Components

**Login.vue:**
- User login form
- Role-based routing (customer/employee/manager)
- Form validation
- Error handling

**Register.vue:**
- Customer registration form
- Email and phone validation
- Password strength requirements
- OTP verification flow

**VerifyOTP.vue:**
- OTP verification interface
- Resend OTP functionality
- Timer for OTP expiration

**ForgotPassword.vue:**
- Password reset request form
- Email input and validation

**ResetPassword.vue:**
- Password reset form
- New password confirmation
- Token validation

#### Shared Components

**Home.vue:**
- Landing page
- Application introduction
- Call-to-action buttons
- Navigation to login/register

### Frontend Features

#### Dark Mode Implementation

**Composable (useDarkMode.js):**
- Reactive dark mode state management
- localStorage persistence
- Document theme attribute management
- Toggle function for switching modes
- Immediate application on component load

**Usage in Components:**
- Components import useDarkMode composable
- Conditional class binding based on isDarkMode
- Inline style binding for dynamic colors
- Consistent color scheme:
  - Dark background: #0f172a, #1e293b
  - Light text: white, text-white-50
  - Borders: rgba(255,255,255,0.1)

#### Sidebar Navigation

**Consistent Structure:**
- Fixed positioning (position: fixed, height: 100vh)
- Width: 280px
- Overflow-y: auto for scrolling
- Background: #1e293b (dark slate)
- Main content margin-left: 280px

**Common Elements:**
- Logo/Header section with BANKEG branding
- User profile section with avatar and name
- Navigation menu with icons (Lucide Vue Next)
- Dark mode toggle button
- Logout button

**Icons Used:**
- LayoutDashboard - Dashboard
- Users - Beneficiaries
- Send - Transfers
- FileText - Transactions/History
- MessageSquare - AI Assistant
- LogOut - Logout
- Moon/Sun - Dark mode toggle
- Bot - AI features
- Wallet - Payments
- CreditCard - Account details

#### Account Number Masking

**Implementation:**
- Computed property: maskedAccountNumber
- Data properties: showAccountNumber, accountNumberTimer
- Methods: revealAccountNumber(), hideAccountNumber()
- Hover event handlers: @mouseenter, @mouseleave
- Timer: 3000ms (3 seconds) auto-hide
- Format: Space every 5 digits
- Asterisk count matches actual account number length

**Usage:**
- Applied in Dashboard.vue and Profile.vue
- Font: monospace for consistent spacing
- Cursor: pointer to indicate interactivity
- Title attribute: "Hover to reveal account number"

#### Form Handling

**Common Patterns:**
- Bootstrap 5 form components
- v-model for two-way data binding
- Form validation with v-if error messages
- Loading states during API calls
- Success/error notifications
- Disabled states during processing

#### API Integration

**Service Layer (api.js):**
- Axios instance with baseURL: http://127.0.0.1:5000
- Centralized API configuration
- Error handling at component level

**Component Usage:**
- Import api from services/api.js
- Use async/await for API calls
- Error handling with try/catch
- Loading state management
- Response data handling

#### State Management

**Vuex Store (store/index.js):**
- Centralized state management
- User authentication state
- Session management

**Composables:**
- useDarkMode - Dark mode state
- Reusable across components
- Reactive state management

#### Styling Approach

**Bootstrap 5:**
- Utility classes for layout (d-flex, gap-3, etc.)
- Card components for content sections
- Button variants and states
- Responsive grid system
- Shadow and border utilities

**Custom CSS:**
- Inter font family (via webfontloader)
- Custom color schemes for dark mode
- Transition animations
- Hover effects

**Vuetify:**
- Material Design components
- Theme configuration
- Component library

#### Asset Management

**Images:**
- Service logos (Airtel, BSNL, Dish TV, etc.)
- Bank logo (bank.png)
- AI Assistant avatar (Haaland.png)
- Payment service icons

**Location:**
- frontend/src/assets/ - Component assets
- frontend/public/ - Public assets

### User Experience Features

**Responsive Design:**
- Mobile-friendly layouts
- Bootstrap responsive grid
- Flexible component sizing

**Loading States:**
- Spinner components during API calls
- Skeleton screens for data loading
- Disabled buttons during processing

**Notifications:**
- Toast notifications for actions
- Notification dropdown in header
- Unread count badges
- Mark as read functionality

**Error Handling:**
- User-friendly error messages
- Form validation feedback
- API error display
- Fallback UI states

**Accessibility:**
- Semantic HTML
- ARIA labels where appropriate
- Keyboard navigation support
- Focus management

## Security Features

**Password Security:**
- Werkzeug password hashing
- Separate login and transaction passwords
- Password strength requirements

**OTP Verification:**
- Time-limited OTP codes
- Expiration tracking
- One-time use enforcement

**Transaction Security:**
- OTP verification for transfers
- Transaction password requirement
- Beneficiary cooling period (24 hours)

**File Upload Security:**
- Secure filename handling
- File type validation
- Upload size limits

**CORS Protection:**
- Configured CORS headers
- Origin restrictions
- Method and header controls

## Data Flow

**Customer Registration Flow:**
1. User submits registration form
2. Backend creates customer record
3. OTP sent to email/phone
4. User verifies OTP
5. Account activated

**Fund Transfer Flow:**
1. Customer initiates transfer
2. Beneficiary validation
3. Cooling period check
4. OTP generation and sending
5. Customer confirms with OTP
6. Transaction password verification
7. Transaction processed
8. Balance updated
9. Transaction record created

**KYC Verification Flow:**
1. Customer uploads documents
2. OTP verification for submission
3. Documents stored
4. Employee reviews documents
5. AI analysis (optional)
6. Employee approves/rejects
7. Manager final approval (if required)
8. Status updated

**Dispute Resolution Flow:**
1. Customer raises dispute
2. Issue created in system
3. Employee views issue
4. AI generates draft response
5. Employee reviews and sends email
6. Customer receives resolution
7. Issue marked as resolved

## AI Integration

**Model Configuration:**
- Model: mistral-7b-instruct-v0.2.Q4_K_M.gguf
- Location: backend/models/
- Library: llama-cpp-python
- Context window: 2048 tokens

**KYC Analysis:**
- OCR extraction from documents
- Text cleaning and processing
- Rule-based validation
- AI-powered compliance checking
- Report generation

**Dispute Drafting:**
- Transaction analysis
- Pattern detection (duplicates, anomalies)
- Balance verification
- Professional response generation
- Context-aware suggestions

**Spending Coach:**
- Transaction categorization
- Spending pattern analysis
- Budget recommendations
- Personalized insights

**Chatbot:**
- General banking queries
- Account information
- Transaction history questions
- Policy and procedure answers

## Deployment Considerations

**Backend:**
- Flask development server (not for production)
- SQLite database (consider PostgreSQL for production)
- Environment variables for sensitive data (.env file)
- CORS configuration for production domains
- AI model file size considerations

**Frontend:**
- Vue CLI build process
- Static asset optimization
- Environment variable configuration
- API endpoint configuration
- Production build optimization

**Security:**
- HTTPS in production
- Secure session management
- API rate limiting
- Input sanitization
- SQL injection prevention (SQLAlchemy ORM)

## Conclusion

The BANKEG application demonstrates a comprehensive banking system with modern web technologies, AI integration, and a user-friendly interface. The architecture supports multiple user roles, secure transactions, and intelligent features powered by local LLM inference. The frontend provides a consistent, responsive experience with dark mode support and intuitive navigation, while the backend handles complex business logic, AI processing, and secure data management.


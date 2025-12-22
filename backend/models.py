from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    login_password = db.Column(db.String(128), nullable=False)
    transaction_password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=False)

    accounts = db.relationship('Account', backref='customer', lazy=True)
    otps = db.relationship('OTPVerification', backref='customer', lazy=True)
    beneficiaries = db.relationship('Beneficiary', backref='customer', lazy=True)
    spending_categories = db.relationship('SpendingCategory', backref='customer', lazy=True)
    virtual_cards = db.relationship('VirtualCard', backref='customer', lazy=True)
    issues = db.relationship('Issue', backref='customer', lazy=True)
    tasks = db.relationship('Task', backref = 'customer', lazy = True)

class KYC(db.Model):
    __tablename__ = 'kyc'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    aadhaar_file = db.Column(db.String(200))
    pan_file = db.Column(db.String(200))
    photo_file = db.Column(db.String(200))
    signature_file = db.Column(db.String(200))

    status = db.Column(db.String(20), default="pending")  # pending/approved/rejected
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    reviewer_comment = db.Column(db.String(300))

    kyc_otp = db.Column(db.String(6), nullable=True)
    otp_verified = db.Column(db.Boolean, default=False)
    otp_expires_at = db.Column(db.DateTime, nullable=True)

    customer = db.relationship("Customer", backref="kyc_record")
    
    ai_validation_status = db.Column(db.String(50)) #newly added for ai fetures
    ai_remarks = db.Column(db.String(500)) #newly added for ai fetures


class OTPVerification(db.Model):
    __tablename__ = 'otp_verification'
    id = db.Column(db.Integer, primary_key=True)
    otp_code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    balance = db.Column(db.Float, default=10000.0)
    account_type = db.Column(db.String(50), default='savings')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    transactions = db.relationship('Transaction', backref='account', lazy=True)
    bill_payments = db.relationship('BillPayment', backref='account', lazy=True)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)

    transaction_uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))

    transaction_type = db.Column(db.String(50))
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(200))
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)


class Beneficiary(db.Model):
    __tablename__ = 'beneficiaries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bank_name = db.Column(db.String(100))
    account_number = db.Column(db.String(20))
    ifsc_code = db.Column(db.String(20))
    transfer_mode = db.Column(db.String(20), default='IMPS') 
    verified = db.Column(db.Boolean, default=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    cooling_period_end = db.Column(db.DateTime, nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)


class BillPayment(db.Model):
    __tablename__ = 'bill_payments'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    amount = db.Column(db.Float, nullable=False)
    paid_on = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='completed')
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)

class VirtualCard(db.Model):
    __tablename__ = 'virtual_cards'
    id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.String(16), unique=True, nullable=False)
    expiry_date = db.Column(db.String(7))
    cvv = db.Column(db.String(3))
    balance_limit = db.Column(db.Float)
    active = db.Column(db.Boolean, default=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

class SpendingCategory(db.Model):
    __tablename__ = 'spending_categories'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50))
    budget_limit = db.Column(db.Float)
    spent_amount = db.Column(db.Float, default=0.0)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("Customer", backref="notifications")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "message": self.message,
            "is_read": self.is_read,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    

class Bank_employee(db.Model):
    __tablename__ = 'bank_employee' # If we do not define this, the model auto assigns name as lower case of class name
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,unique=True, nullable = False)
    name = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    role = db.Column(db.Integer, default =2)
    date_of_regn = db.Column(db.DateTime, default = datetime.now)
    contact_number = db.Column(db.String, nullable = False)
    status = db.Column(db.String, default = 'Active') # Active - 1, Flagged - 2, Blocked - 3
    manager_id = db.Column(db.Integer,db.ForeignKey('bank_manager.id'), nullable = False)
    tasks = db.relationship('Task', backref = 'bank_employee', lazy = True)
    


class Bank_manager(db.Model):
    __tablename__ = 'bank_manager' # If we do not define this, the model auto assigns name as lower case of class name
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,unique=True, nullable = False)
    name = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    role = db.Column(db.Integer, default =2)
    date_of_regn = db.Column(db.DateTime, default = datetime.now)
    contact_number = db.Column(db.String, nullable = False)
    status = db.Column(db.String, default = 'Active') # Active - 1, Flagged - 2, Blocked - 3
    # manager_id = db.Column(db.Integer,primary_key=True)
    employees = db.relationship('Bank_employee', backref = 'bank_manager', lazy = True)



class Task(db.Model):
    __tablename__ = 'task'
    id=db.Column(db.Integer,primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('bank_employee.id'), nullable = False)
    customer_id = db.Column(db.Integer,db.ForeignKey('customers.id'), nullable = False)
    title = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    # flag_sp = db.Column(db.Integer, default = 0) # Flagged - 1, not flagged - 0
    assigned_date = db.Column(db.DateTime, default = datetime.now) # NEED TO CONFIRM on type
    priority = db.Column(db.String, nullable = False)
    remarks = db.Column(db.String)
    due_date = db.Column(db.DateTime, nullable = False)
    status = db.Column(db.String, default = 'Pending') # Pending, Complete


class Issue(db.Model):
    __tablename__ = 'issue'
    id=db.Column(db.Integer,primary_key=True)
    customer_id = db.Column(db.Integer,db.ForeignKey('customers.id'), nullable = False)
    title = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    assigned_date = db.Column(db.DateTime, default = datetime.now) # NEED TO CONFIRM on type
    status = db.Column(db.String, default = 'Pending') # Pending, Complete
    
    resolution_summary = db.Column(db.String(500))#newly added


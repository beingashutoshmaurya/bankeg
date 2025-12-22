import pytest
import json
from io import BytesIO
from datetime import datetime, timedelta
import random
import string
from app import app, db
from models import (
    Customer, Account, KYC, OTPVerification, Transaction, Beneficiary,
    BillPayment, VirtualCard, SpendingCategory, Notification
)
from werkzeug.security import generate_password_hash

@pytest.fixture(scope="session")
def app_context():
    """
    Creates a global application context for all tests.
    This FIXES all 'Working outside application context' errors.
    """
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope="module")
def test_app():
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
        "UPLOAD_FOLDER": "/tmp",
    })

    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture()
def client(test_app):
    with test_app.test_client() as client:
        with test_app.app_context():
            yield client


@pytest.fixture
def create_customer(test_app):
    def _create_customer(
        full_name="Test User",
        email=None,
        phone=None,
        login_password="Login@123",
        transaction_password="Txn@123",
        is_active=True
    ):
        if email is None:
            email = generate_unique_email()
        if phone is None:
            phone = generate_unique_phone()

        customer = Customer(
            full_name=full_name,
            email=email,
            phone=phone,
            login_password=generate_password_hash(login_password),
            transaction_password=generate_password_hash(transaction_password),
            is_active=is_active
        )

        db.session.add(customer)
        db.session.commit()
        return customer

    return _create_customer

@pytest.fixture
def new_customer(create_customer):
    return create_customer()


@pytest.fixture()
def create_active_account(client, create_customer):
    def _create_active_account(password="Login@123"):
        customer = create_customer(is_active=True, login_password=password)
        account = Account(
            account_number=f"ACC{customer.id}{random.randint(100,999)}",
            balance=1000.0,
            customer_id=customer.id
        )
        db.session.add(account)
        db.session.commit()
        return account
    return _create_active_account


@pytest.fixture()
def create_inactive_account(client, create_customer):
    def _create_inactive_account(password="Login@123"):
        customer = create_customer(is_active=False, login_password=password)
        account = Account(
            account_number=f"ACC{customer.id}{random.randint(100,999)}",
            balance=1000.0,
            customer_id=customer.id
        )
        db.session.add(account)
        db.session.commit()
        return account
    return _create_inactive_account


@pytest.fixture()
def create_kyc_record(client, create_customer):
    def _create_kyc_record():
        customer = create_customer()
        kyc = KYC(customer_id=customer.id)
        db.session.add(kyc)
        db.session.commit()
        return kyc
    return _create_kyc_record


@pytest.fixture()
def create_kyc_with_otp(client, create_kyc_record):
    def _create_kyc_with_otp(otp="123456"):
        kyc = create_kyc_record()
        kyc.kyc_otp = otp
        kyc.otp_verified = False
        kyc.otp_expires_at = datetime.utcnow() + timedelta(minutes=10)
        db.session.commit()
        return kyc
    return _create_kyc_with_otp


@pytest.fixture()
def create_account_with_balance(client, create_customer):
    def _create_account_with_balance(balance=1000.0):
        customer = create_customer()
        account = Account(
            account_number=f"ACC{customer.id}B",
            balance=balance,
            customer_id=customer.id
        )
        db.session.add(account)
        db.session.commit()
        return account, customer
    return _create_account_with_balance

@pytest.fixture()
def setup_account_with_balance(create_customer):
    def _setup(balance=5000):
        customer = create_customer()

        account = Account(
            account_number="ACC" + str(random.randint(10000, 99999)),
            customer_id=customer.id,
            balance=balance
        )

        db.session.add(account)
        db.session.commit()

        return account, customer
    return _setup

@pytest.fixture()
def create_transactions(setup_account_with_balance):
    def _create(count=5):
        account, customer = setup_account_with_balance()
        for i in range(count):
            t = Transaction(
                account_id=account.id,
                amount=100 + i,
                transaction_type="debit",
                description=f"Test txn {i+1}"
            )
            db.session.add(t)
        db.session.commit()
        return account
    return _create


@pytest.fixture()
def create_beneficiary(client, create_customer):
    def _create_beneficiary():
        customer = create_customer()
        beneficiary = Beneficiary(
            name="ABC",
            account_number=f"BEN{customer.id}",
            ifsc_code="IFSC0001",
            bank_name="HDFC",
            verified=True,
            customer_id=customer.id
        )
        db.session.add(beneficiary)
        db.session.commit()
        return beneficiary
    return _create_beneficiary


@pytest.fixture()
def create_beneficiaries(client, create_customer):
    def _create_beneficiaries(count=3):
        customer = create_customer()
        beneficiaries = []
        for i in range(count):
            ben = Beneficiary(
                name=f"Ben{i+1}",
                account_number=f"BEN{customer.id}{i+1}",
                ifsc_code=f"IFSC{customer.id}{i+1}",
                bank_name="HDFC",
                verified=True,
                customer_id=customer.id
            )
            db.session.add(ben)
            beneficiaries.append(ben)
        db.session.commit()
        return customer, beneficiaries
    return _create_beneficiaries


@pytest.fixture()
def create_beneficiary_with_otp(client, create_beneficiary):
    def _create_beneficiary_with_otp(otp="123456"):
        ben = create_beneficiary()
        setattr(ben, "otp_code", otp)
        db.session.commit()
        return ben
    return _create_beneficiary_with_otp


@pytest.fixture()
def setup_transfer_accounts(client, create_customer):
    def _setup_transfer_accounts(balance=1000.0, verified=True):
        sender = create_customer()
        sender_account = Account(account_number=f"SENDER{sender.id}", balance=balance, customer_id=sender.id)
        db.session.add(sender_account)

        receiver = create_customer(email=f"receiver{sender.id}@example.com", phone=f"111222{sender.id:04d}")
        receiver_account = Account(account_number=f"RECEIVER{receiver.id}", balance=balance, customer_id=receiver.id)
        db.session.add(receiver_account)

        beneficiary = Beneficiary(
            name="Receiver",
            account_number=receiver_account.account_number,
            ifsc_code="IFSC0002",
            bank_name="HDFC",
            verified=verified,
            customer_id=sender.id
        )
        db.session.add(beneficiary)
        db.session.commit()
        return sender_account, beneficiary, receiver_account
    return _setup_transfer_accounts


@pytest.fixture()
def create_sender_account(client, create_customer):
    def _create_sender_account(balance=1000.0):
        sender = create_customer()
        account = Account(account_number=f"SENDER{sender.id}", balance=balance, customer_id=sender.id)
        db.session.add(account)
        db.session.commit()
        return account
    return _create_sender_account


@pytest.fixture()
def setup_cooling_period(client, create_customer):
    def _setup_cooling_period():
        sender = create_customer()
        sender_account = Account(account_number=f"SENDERCP{sender.id}", balance=1000.0, customer_id=sender.id)
        db.session.add(sender_account)
        beneficiary = Beneficiary(
            name="ReceiverCP",
            account_number=f"RECEIVERCP{sender.id}",
            ifsc_code="IFSCCP01",
            bank_name="HDFC",
            verified=True,
            cooling_period_end=datetime.utcnow() + timedelta(days=1),
            customer_id=sender.id
        )
        db.session.add(beneficiary)
        db.session.commit()
        return sender_account, beneficiary
    return _setup_cooling_period


@pytest.fixture()
def setup_same_account_transfer(client, create_customer):
    def _setup_same_account_transfer():
        customer = create_customer()
        account = Account(account_number=f"SAMEACC{customer.id}", balance=1000.0, customer_id=customer.id)
        db.session.add(account)
        db.session.commit()
        beneficiary = Beneficiary(
            name="Self",
            account_number=account.account_number,
            ifsc_code="IFSCSELF",
            bank_name="HDFC",
            verified=True,
            customer_id=customer.id
        )
        db.session.add(beneficiary)
        db.session.commit()
        return account, beneficiary
    return _setup_same_account_transfer


@pytest.fixture()
def create_user_only(client, create_customer):
    def _create_user_only():
        return create_customer()
    return _create_user_only

@pytest.fixture()
def create_notifications(create_customer):
    def _create(count=3):
        user = create_customer()
        notifications = []
        for i in range(count):
            n = Notification(
                user_id=user.id,
                title=f"Message {i}",
                message="Test",
                is_read=False
            )
            db.session.add(n)
            notifications.append(n)
        db.session.commit()
        return user, notifications
    return _create

@pytest.fixture()
def create_login_otp(client, create_active_account):
    def _create_login_otp(otp="123456"):
        account = create_active_account()
        otp_record = OTPVerification(
            otp_code=otp,
            expires_at=datetime.utcnow() + timedelta(minutes=10),
            customer_id=account.customer_id
        )
        db.session.add(otp_record)
        db.session.commit()
        return account, otp_record
    return _create_login_otp


@pytest.fixture()
def create_transaction_otp(client, create_active_account):
    def _create_transaction_otp(otp="123456"):
        account = create_active_account()
        otp_record = OTPVerification(
            otp_code=otp,
            expires_at=datetime.utcnow() + timedelta(minutes=10),
            customer_id=account.customer_id
        )
        db.session.add(otp_record)
        db.session.commit()
        return account, otp_record
    return _create_transaction_otp

def generate_unique_phone():
    return "9" + "".join(random.choice("0123456789") for _ in range(9))

def generate_unique_email():
    suffix = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    return f"user_{suffix}@example.com"


def test_home_route(client):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer testtoken123"
    }
    response = client.get("/", headers=headers)
    assert response.status_code == 200
    assert response.get_data(as_text=True) == "Banking Application Started."

def test_register_success(client):
    headers = {"Content-Type": "application/json", "Authorization": "Bearer testtoken123"}
    data = {
        "full_name": "Rohan Kumar",
        "email": "rohan@dummy.com",
        "phone": "9990001111",
        "login_password": "Login@123",
        "transaction_password": "Txn@123"
    }
    response = client.post(
            "/register", 
            data=json.dumps(data), 
            content_type="application/json", 
            headers=headers
        )
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["message"] == "Customer registered. Proceed to document upload."
    assert "customer_id" in json_data

def test_register_missing_passwords(client):
    headers = {
            "Content-Type": "application/json", 
            "Authorization": "Bearer testtoken123"
        }
    data = {
        "full_name": "Amit Singh",
        "email": "amit@dummy.com",
        "phone": "8884442222",
        "login_password": "",
        "transaction_password": ""
    }
    response = client.post(
            "/register", 
            data=json.dumps(data), 
            content_type="application/json", 
            headers=headers
        )
    assert response.status_code == 400
    assert response.get_json()["message"] == "Passwords are required"

def test_register_duplicate_email_phone(client, new_customer):
    response = client.post('/register', json={
        "full_name": "Another User",
        "email": new_customer.email,
        "phone": new_customer.phone,
        "login_password": "pwd",
        "transaction_password": "pwd"
    })
    assert response.status_code == 400
    assert response.get_json()["message"] == "Email or phone already registered"

def test_kyc_upload_success(client, create_customer):
    customer = create_customer()
    headers = {"Authorization": "Bearer testtoken123"}
    data = {
        "aadhaar": (BytesIO(b"dummy"), "aadhaar.png"),
        "pan": (BytesIO(b"dummy"), "pan.png"),
        "photo": (BytesIO(b"dummy"), "photo.png"),
        "signature": (BytesIO(b"dummy"), "sign.png")
    }
    response = client.post(
            f"/kyc/upload/{customer.id}", 
            data=data, 
            content_type="multipart/form-data", 
            headers=headers
        )
    assert response.status_code == 200
    assert response.get_json()["message"] == "KYC uploaded. Now verify with OTP."

def test_send_kyc_otp_success(client, create_kyc_record):
    kyc = create_kyc_record()
    headers = {
            "Content-Type": "application/json", 
            "Authorization": "Bearer testtoken123"
        }
    response = client.post(
            f"/kyc/send_otp/{kyc.customer_id}", 
            headers=headers
        )
    assert response.status_code == 200
    assert response.get_json()["message"] == "KYC OTP sent"

def test_verify_kyc_otp_success(client, create_kyc_with_otp):
    kyc = create_kyc_with_otp(otp="123456")
    headers = {
            "Content-Type": "application/json", 
            "Authorization": "Bearer testtoken123"
        }
    data = {"otp": "123456"}
    response = client.post(
            f"/kyc/verify_otp/{kyc.customer_id}", 
            data=json.dumps(data), 
            content_type="application/json", 
            headers=headers
        )
    assert response.status_code == 200
    assert "OTP Verified" in response.get_json()["message"]

def test_verify_kyc_otp_wrong(client, create_kyc_with_otp):
    kyc = create_kyc_with_otp(otp="999999")
    headers = {
        "Content-Type": "application/json", 
        "Authorization": "Bearer testtoken123"
    }
    data = {"otp": "000000"}
    response = client.post(
            f"/kyc/verify_otp/{kyc.customer_id}", 
            data=json.dumps(data), 
            content_type="application/json", 
            headers=headers
        )
    assert response.status_code == 400
    assert "Invalid" in response.get_json()["message"]

def test_verify_kyc_otp_customer_not_found(client):
    headers = {
            "Content-Type": "application/json", 
            "Authorization": "Bearer testtoken123"
        }
    data = {"otp": "123456"}
    response = client.post(
            "/kyc/verify_otp/999", 
            data=json.dumps(data), 
            content_type="application/json", 
            headers=headers
        )
    assert response.status_code == 404
    assert response.get_json()["message"] == "KYC not found"

def test_login_success(client, create_active_account):
    account = create_active_account(password="asdfgh")
    data = {
            "account_number": account.account_number, 
            "password": "asdfgh"
        }
    response = client.post(
            "/login", 
            data=json.dumps(data), 
            content_type="application/json"
        )
    assert response.status_code == 200
    assert response.get_json()["message"] == "OTP sent"


def test_login_invalid_account(client):
    headers = {
            "Content-Type": "application/json", 
            "Authorization": "Bearer testtoken123"
        }
    data = {
            "account_number": "INVALID123", 
            "login_password": "anything"
        }
    response = client.post(
            "/login", 
            data=json.dumps(data), 
            content_type="application/json", 
            headers=headers
        )
    assert response.status_code == 404
    assert response.get_json()["message"] == "Invalid account number"

def test_login_inactive_account(client, create_inactive_account):
    account = create_inactive_account(password="asdfgh")
    headers = {
            "Content-Type": "application/json", 
            "Authorization": "Bearer testtoken123"
        }
    data = {
            "account_number": account.account_number, 
            "login_password": "asdfgh"
        }
    response = client.post(
            "/login", 
            data=json.dumps(data), 
            content_type="application/json", 
            headers=headers
        )
    assert response.status_code == 403
    assert response.get_json()["message"] == "Account not activated by manager"

def test_forgot_login_password_success(client, create_active_account):
    account = create_active_account()
    customer = account.customer
    data = {"email": customer.email}
    response = client.post(
            "/forgot_password", 
            data=json.dumps(data), 
            content_type="application/json"
        )
    assert response.status_code == 200
    assert "OTP sent" in response.get_json()["message"] or "OTP sent for password reset" in response.get_json().get("message","")

def test_reset_login_password_success(client, create_login_otp):
    account, otp = create_login_otp(otp="123456")
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer testtoken123"
    }
    customer = account.customer
    data = {
            "email": customer.email, 
            "otp": "123456", 
            "new_password": "NewPass@123"
        }
    response = client.post(
            "/reset_password", 
            data=json.dumps(data), 
            content_type="application/json", 
            headers=headers
        )
    assert response.status_code == 200
    assert "Password reset successful" in response.get_json()["message"] or "Password reset successful" in response.get_data(as_text=True)

def test_reset_login_password_invalid_otp(client, create_login_otp):
    account, otp = create_login_otp(otp="999999")
    customer = account.customer
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer testtoken123"
    }
    data = {
            "email": customer.email, 
            "otp": "000000", 
            "new_password": "NewPass@123"
        }
    response = client.post(
            "/reset_password", 
            data=json.dumps(data), 
            content_type="application/json", 
            headers=headers
        )
    assert response.status_code == 400
    assert "Invalid or expired OTP" in response.get_json()["message"]

def test_check_balance_success(client, create_account_with_balance):
    account, _customer = create_account_with_balance(balance=12000.50)
    headers = {
            "Content-Type": "application/json", 
            "Authorization": "Bearer testtoken123"
        }
    response = client.get(
            f"/customer/balance/{_customer.id}", 
            headers=headers
        )
    assert response.status_code == 200
    data = response.get_json()
    assert data["balance"] == 12000.50

def test_check_balance_not_found(client):
    headers = {
            "Content-Type": "application/json", 
            "Authorization": "Bearer testtoken123"
        }
    response = client.get(
            "/customer/balance/99999", 
            headers=headers
        )
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Account not found"

def test_mini_statement_success(client, create_transactions, setup_account_with_balance):
    account, customer = setup_account_with_balance()
    for i in range(5):
        t = Transaction(
                account_id=account.id, 
                amount=100+i, 
                transaction_type="debit", 
                description=f"t{i}"
            )
        db.session.add(t)
    db.session.commit()

    response = client.get(f"/customer/mini-statement/{customer.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 5

def test_mini_statement_not_found(client):
    headers = {
            "Content-Type": "application/json", 
            "Authorization": "Bearer testtoken123"
        }
    response = client.get("/customer/mini-statement/99999", headers=headers)
    assert response.status_code == 404
    assert response.get_json()["error"] == "Account not found"

def test_transaction_history_success(client, setup_account_with_balance):
    account, customer = setup_account_with_balance()
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer testtoken123"
    }
    for i in range(10):
        t = Transaction(
                account_id=account.id, 
                amount=100+i, 
                transaction_type="debit", 
                description=f"t{i}"
            )
        db.session.add(t)
    db.session.commit()

    response = client.get(f"/customer/transactions/{customer.id}", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_transaction_history_not_found(client):
    headers = {
            "Content-Type": "application/json", 
            "Authorization": "Bearer testtoken123"
        }
    response = client.get("/customer/transactions/99999", headers=headers)
    assert response.status_code == 404
    assert response.get_json()["error"] == "Account not found"

def test_add_beneficiary_success(client, create_customer):
    customer = create_customer()
    data = {
        "customer_id": customer.id,
        "name": "ABC",
        "bank_name": "HDFC Bank",
        "account_number": "HDFC12345",
        "ifsc_code": "HDFC0001234"
    }
    response = client.post(
            "/customer/add-beneficiary", 
            data=json.dumps(data), 
            content_type="application/json"
        )
    assert response.status_code in (200, 201)

def test_verify_beneficiary_success(client, create_customer):
    customer = create_customer()
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer testtoken123"
    }
    payload = {
        "customer_id": customer.id,
        "name": "Ben1",
        "bank_name": "HDFC",
        "account_number": "BENX1",
        "ifsc_code": "IFSCTEST"
    }
    r = client.post(
            "/customer/add-beneficiary", 
            data=json.dumps(payload), 
            content_type="application/json", 
            headers=headers
        )
    otp = r.get_json().get("otp")
    verify_payload = {
        "customer_id": customer.id, 
        "otp": otp, 
        "account_number": "BENX1"
    }
    r2 = client.post(
            "/customer/verify-beneficiary-otp", 
            data=json.dumps(verify_payload), 
            content_type="application/json"
        )
    assert r2.status_code == 200


def test_verify_beneficiary_wrong_otp(client, create_beneficiary_with_otp):
    beneficiary = create_beneficiary_with_otp(otp="999999")
    headers = {"Content-Type": "application/json", "Authorization": "Bearer testtoken123"}
    data = {
        "customer_id": beneficiary.customer_id,
        "account_number": beneficiary.account_number,
        "otp": "000000"
    }
    response = client.post(
            "/customer/verify-beneficiary-otp", 
            data=json.dumps(data), 
            headers=headers
        )
    assert response.status_code == 400
    assert "Invalid" in response.get_json()["message"]

def test_list_beneficiaries_success(client, create_beneficiaries):
    customer, beneficiaries = create_beneficiaries(count=3)
    headers = {
            "Content-Type": "application/json", 
            "Authorization": "Bearer testtoken123"
        }
    response = client.get(
            f"/customer/beneficiaries/{customer.id}", 
            headers=headers
        )
    assert response.status_code == 200
    assert len(response.get_json()) == 3

def test_view_beneficiary_success(client, create_beneficiary):
    beneficiary = create_beneficiary()
    headers = {
            "Content-Type": "application/json", 
            "Authorization": "Bearer testtoken123"
        }
    response = client.get(
        f"/customer/view-beneficiary?customer_id={beneficiary.customer_id}&account_number={beneficiary.account_number}",
        headers=headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["account_number"] == beneficiary.account_number

def test_delete_beneficiary_success(client, create_beneficiary):
    beneficiary = create_beneficiary()
    headers = {
            "Content-Type": "application/json", 
            "Authorization": "Bearer testtoken123"
        }
    data = {
        "customer_id": beneficiary.customer_id,
        "account_number": beneficiary.account_number
    }
    response = client.post(
            "/customer/delete-beneficiary", 
            data=json.dumps(data), 
            headers=headers
        )
    assert response.status_code == 200
    assert f'Beneficiary {beneficiary.name} deleted successfully' in response.get_json()["message"]

def test_transfer_success(client, setup_transfer_accounts):
    sender_account, beneficiary, receiver_account = setup_transfer_accounts(balance=2000, verified=True)
    request_data = {
            "customer_id": sender_account.customer_id, 
            "beneficiary_account": beneficiary.account_number, 
            "amount": 500, 
            "remarks": "Rent"
        }
    headers = {
            "Content-Type": "application/json", 
            "Authorization": "Bearer testtoken123"
        }
    response = client.post(
            "/customer/transfer", 
            data=json.dumps(request_data), 
            headers=headers
        )
    assert response.status_code == 200
    res = response.get_json()
    assert "transferred successfully" in res["message"]
    assert "debit_transaction_id" in res
    assert "credit_transaction_id" in res

def test_transfer_beneficiary_not_found(client, create_sender_account):
    sender = create_sender_account()
    data = {
            "customer_id": sender.customer_id, 
            "beneficiary_account": "UNKNOWNBEN", 
            "amount": 500
        }
    response = client.post(
            "/customer/transfer", 
            data=json.dumps(data), 
            headers={"Content-Type": "application/json", "Authorization": "Bearer testtoken123"}
        )
    assert response.status_code == 404
    assert response.get_json()["message"] == "Beneficiary not found"

def test_transfer_cooling_period_active(client, setup_cooling_period):
    sender_account, beneficiary = setup_cooling_period()
    data = {
            "customer_id": sender_account.customer_id, 
            "beneficiary_account": beneficiary.account_number, 
            "amount": 300
        }
    response = client.post(
            "/customer/transfer", 
            data=json.dumps(data), 
            headers={"Content-Type": "application/json", "Authorization": "Bearer testtoken123"}
        )
    assert response.status_code == 400
    assert response.get_json()["message"] == "Cooling period active. Try later."

def test_transfer_insufficient_balance(client, setup_transfer_accounts):
    sender_account, beneficiary, receiver_account = setup_transfer_accounts(balance=200)
    data = {
            "customer_id": sender_account.customer_id, 
            "beneficiary_account": beneficiary.account_number, 
            "amount": 5000
        }
    response = client.post(
            "/customer/transfer", 
            data=json.dumps(data), 
            headers={"Content-Type": "application/json", "Authorization": "Bearer testtoken123"}
        )
    assert response.status_code == 400
    assert response.get_json()["message"] == "Insufficient balance"

def test_transfer_same_account(client, setup_same_account_transfer):
    account, beneficiary = setup_same_account_transfer()
    data = {
            "customer_id": account.customer_id, 
            "beneficiary_account": account.account_number, 
            "amount": 500
        }
    response = client.post(
            "/customer/transfer", 
            data=json.dumps(data), 
            headers={"Content-Type": "application/json", "Authorization": "Bearer testtoken123"}
        )
    assert response.status_code == 400
    assert response.get_json()["message"] == "Cannot transfer to same account"

def test_pay_bill_success(client, setup_account_with_balance):
    account, customer = setup_account_with_balance(balance=10000)
    data = {
            "customer_id": customer.id, 
            "bill_type": "Electricity", 
            "biller": "StateGrid", 
            "amount": 1500, 
            "bill_account": "ELEC-12345"
        }
    headers = {
            "Content-Type": "application/json", 
            "Authorization": "Bearer testtoken123"
        }
    response = client.post(
            "/customer/pay-bill", 
            data=json.dumps(data), 
            headers=headers
        )
    assert response.status_code == 200
    res = response.get_json()
    assert res["message"] == "Transaction successful"
    assert "transaction_id" in res
    assert res["new_balance"] == 8500.0

def test_pay_bill_missing_fields(client):
    data = {
            "customer_id": 1, 
            "amount": 500
        }
    response = client.post(
            "/customer/pay-bill", 
            data=json.dumps(data), 
            headers={"Content-Type": "application/json", "Authorization": "Bearer testtoken123"}
        )
    assert response.status_code == 400
    assert response.get_json()["message"] == "Missing or invalid fields"

def test_pay_bill_account_not_found(client):
    data = {
            "customer_id": 999, 
            "bill_type": "Internet", 
            "biller": "NetPlus", 
            "amount": 700
        }
    response = client.post(
            "/customer/pay-bill", 
            data=json.dumps(data), 
            headers={"Content-Type": "application/json", "Authorization": "Bearer testtoken123"}
        )
    assert response.status_code == 404
    assert response.get_json()["message"] == "Account not found"

def test_pay_bill_insufficient_balance(client, setup_account_with_balance):
    account, customer = setup_account_with_balance(balance=2000)
    data = {
            "customer_id": customer.id, 
            "bill_type": "Gas", 
            "biller": "GovGas", 
            "amount": 5000
        }
    response = client.post(
            "/customer/pay-bill", 
            data=json.dumps(data), 
            headers={"Content-Type": "application/json", "Authorization": "Bearer testtoken123"}
        )
    assert response.status_code == 400
    assert response.get_json()["message"] == "Insufficient balance."

def test_recharge_success(client, setup_account_with_balance):
    account, customer = setup_account_with_balance(balance=10000)
    data = {
            "customer_id": customer.id, 
            "recharge_type": "Mobile", 
            "operator": "Airtel", 
            "number": "9876543210", 
            "amount": 249
        }
    headers = {
            "Content-Type": "application/json", 
            "Authorization": "Bearer testtoken123"
        }
    response = client.post(
            "/customer/recharge", 
            data=json.dumps(data), 
            headers=headers
        )
    assert response.status_code == 200
    res = response.get_json()
    assert res["message"] == "Transaction successful"
    assert "transaction_id" in res
    assert res["new_balance"] == 10000 - 249

def test_recharge_missing_fields(client):
    data = {
            "customer_id": 1, 
            "operator": "Jio", 
            "amount": 199
        }
    response = client.post(
            "/customer/recharge", 
            data=json.dumps(data), 
            headers={"Content-Type": "application/json", "Authorization": "Bearer testtoken123"}
        )
    assert response.status_code == 400
    assert response.get_json()["message"] == "Missing or invalid fields"

def test_recharge_account_not_found(client):
    data = {
        "customer_id": 99999,
        "recharge_type": "DTH",
        "operator": "TataSky",
        "number": "ACC123",
        "amount": 300
    }
    headers = {
            "Content-Type": "application/json", 
            "Authorization": "Bearer testtoken123"
        }
    response = client.post(
            "/customer/recharge", 
            data=json.dumps(data), 
            headers=headers
        )
    assert response.status_code == 404
    assert response.get_json()["message"] == "Account not found"

def test_recharge_insufficient_balance(client, setup_account_with_balance):
    account, customer = setup_account_with_balance(balance=500)
    data = {
            "customer_id": customer.id, 
            "recharge_type": "Mobile", 
            "operator": "Vodafone", 
            "number": "9876543210", 
            "amount": 10000
        }
    response = client.post(
            "/customer/recharge", 
            data=json.dumps(data), 
            headers={"Content-Type": "application/json", "Authorization": "Bearer testtoken123"}
        )
    assert response.status_code == 400
    assert response.get_json()["message"] == "Insufficient balance."

def test_fastag_topup_success(client, setup_account_with_balance):
    account, customer = setup_account_with_balance(balance=10000)
    data = {
            "customer_id": customer.id, 
            "vehicle_number": "DL01AB1234", 
            "tag_id": "TAG7788", 
            "amount": 600
        }
    headers = {
            "Content-Type": "application/json", 
            "Authorization": "Bearer testtoken123"
        }
    response = client.post(
            "/customer/fastag-topup", 
            data=json.dumps(data), 
            headers=headers
        )
    assert response.status_code == 200
    res = response.get_json()
    assert res["message"] == "Transaction successful"
    assert res["new_balance"] == 9400.0

def test_fastag_missing_fields(client):
    data = {
        "customer_id": 1,
        "amount": 500
    }

    response = client.post("/customer/fastag-topup", data=json.dumps(data), headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer testtoken123"
    })

    assert response.status_code == 400
    assert response.get_json()["message"] == "Missing or invalid fields"


def test_fastag_account_not_found(client):
    data = {
        "customer_id": 99,
        "vehicle_number": "UP14CC2222",
        "amount": 400
    }

    response = client.post("/customer/fastag-topup", data=json.dumps(data), headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer testtoken123"
    })

    assert response.status_code == 404
    assert response.get_json()["message"] == "Account not found"


def test_get_notifications_success(client, create_notifications):
    user, notifications = create_notifications(count=1)
    response = client.get(f"/api/notifications/{user.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["user_id"] == user.id

def test_create_notification_success(client, create_customer):
    user = create_customer()
    data = {
            "user_id": user.id, 
            "title": "Transaction Alert", 
            "message": "₹500 credited to your account"
        }
    response = client.post(
            "/api/notifications", 
            data=json.dumps(data), 
            content_type="application/json"
        )
    assert response.status_code == 201
    res = response.get_json()
    assert res["user_id"] == user.id
    assert res["title"] == "Transaction Alert"
    assert res["is_read"] is False

def test_mark_notification_as_read(client, create_notifications):
    user, notifications = create_notifications(count=1)
    notif = notifications[0]
    response = client.put(
            f"/api/notifications/{notif.id}/read", 
            headers={"Content-Type": "application/json", "Authorization": "Bearer testtoken123"}
        )
    assert response.status_code == 200
    assert response.get_json()["message"] == "Notification marked as read"

def test_delete_notification_success(client, create_notifications):
    user, notifications = create_notifications(count=1)
    notif = notifications[0]
    response = client.delete(
            f"/api/notifications/{notif.id}", 
            headers={"Content-Type": "application/json", "Authorization": "Bearer testtoken123"}
        )
    assert response.status_code == 200
    assert response.get_json()["message"] == "Notification deleted"

def test_kyc_document_success(client, tmp_path, monkeypatch):
    upload_folder = tmp_path / "kyc_docs"
    upload_folder.mkdir()
    file_path = upload_folder / "sample_aadhaar.pdf"
    file_path.write_bytes(b"%PDF-1.4 Dummy PDF Data")
    monkeypatch.setattr("app.UPLOAD_FOLDER", str(upload_folder))
    response = client.get(
            "/kyc_docs/sample_aadhaar.pdf", 
            headers={"Content-Type": "application/json", "Authorization": "Bearer testtoken123"}
        )
    assert response.status_code == 200
    assert response.mimetype == "application/pdf"
    assert b"%PDF" in response.data

def test_kyc_document_not_found(client, monkeypatch, tmp_path):
    upload_folder = tmp_path / "kyc_docs"
    upload_folder.mkdir()
    monkeypatch.setattr("app.UPLOAD_FOLDER", str(upload_folder))
    response = client.get(
            "/kyc_docs/not_existing_file.png", 
            headers={"Content-Type": "application/json", "Authorization": "Bearer testtoken123"}
        )
    assert response.status_code == 404

def test_kyc_document_invalid_path(client):
    response = client.get(
            "/kyc_docs/../../etc/passwd", 
            headers={"Content-Type": "application/json", "Authorization": "Bearer testtoken123"}
        )
    assert response.status_code == 404

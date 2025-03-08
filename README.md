# 🌐 NetBill Manager - Backend

![NetBill Manager](https://via.placeholder.com/1000x300?text=NetBill+Manager+Backend)

### 🚀 **A Powerful ISP Billing & Management System**

NetBill Manager is a **Django-based** backend system designed for **ISPs (Internet Service Providers)** to manage **user accounts, billing, complaints, and announcements** efficiently. This backend handles user authentication, bill payments, service notifications, and more!

---

## 📂 **Project Structure**
```
NetBill_Manager/
️️│── accounts/           # User authentication & profiles
️️│── announcement/       # Announcements & reactions
️️│── bills/              # Billing & payments
️️│── complains/          # User complaints & replies
️️│── contact_us/         # Contact form messages
️️│── media/              # Uploaded files & user data
️️│── notifications/      # System notifications
️️│── packages/           # Store bill slips
️️│── staticfiles/        # Static assets
️️│── venv/               # Virtual environment
️️│── db.sqlite3          # Database (SQLite)
️️│── manage.py           # Django project manager
️️│── README.md           # Documentation
️️│── requirements.txt    # Dependencies
️️│── vercel.json         # Vercel deployment config
```

---

## ⚙️ **Installation & Setup**

### 🛠 **1. Clone the Repository**
```sh
git clone https://github.com/DurjoyKumar177/NetBill_Manager.git
cd NetBill_Manager
```

### 🛆 **2. Create & Activate Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### 📝 **3. Install Dependencies**
```sh
pip install -r requirements.txt
```

### 🛠 **4. Apply Migrations & Run Server**
```sh
python manage.py migrate
python manage.py runserver
```

---

## 🔐 **Authentication API**
| API | Method | Description |
|------|--------|-------------|
| `/api/accounts/register/` | `POST` | Register a new user |
| `/api/accounts/auth/login/` | `POST` | User login (returns token) |
| `/api/accounts/auth/logout/` | `POST` | Logout user |
| `/api/accounts/profile/update/` | `PUT/PATCH` | Update user profile |

---

## 📢 **Announcements API**
| API | Method | Description |
|------|--------|-------------|
| `/api/announcements/` | `GET/POST` | List or create announcements |
| `/api/announcements/<id>/` | `GET/PUT/DELETE` | Retrieve, update, or delete an announcement |
| `/api/announcements/comments/` | `GET/POST` | List or create comments |
| `/api/announcements/comments/<id>/` | `GET/PUT/DELETE` | Manage a comment |
| `/api/announcements/<id>/reactions/` | `POST` | Add or update a reaction |
| `/api/announcements/<id>/reactions/list/` | `GET` | List reactions for an announcement |

---

## 💰 **Billing & Payments API**
| API | Method | Description |
|------|--------|-------------|
| `/api/bills/` | `GET` | List all bills |
| `/api/bills/payments/` | `POST` | Create a new payment |
| `/api/bills/collections/` | `POST` | Create a collection |
| `/api/bills/payment-history/` | `GET` | List payment history |
| `/api/bills/collection-history/` | `GET` | List collection history |

---

## 🛠 **Complaints API**
| API | Method | Description |
|------|--------|-------------|
| `/api/complains/` | `GET/POST` | List or create complaints |
| `/api/complains/<id>/` | `GET/PUT/DELETE` | Retrieve, update, or delete a complaint |
| `/api/complains/<id>/reply/` | `POST` | Add a reply to a complaint |
| `/api/complains/categories/` | `GET/POST` | List or create complaint categories |

---

## 🚀 **Deployment**
This project is configured for **Vercel Deployment**. To deploy:

```sh
vercel deploy
```
Make sure to add required **environment variables** in your Vercel settings.

---

## 📧 **Contact & Support**
For issues, please open a [GitHub Issue](https://github.com/your-username/NetBill_Manager/issues) or contact:

📧 Email: **durjoykumar177@gmail.com**  
🌐 Website: **[NetBill Manager](https://net-bill-manager.vercel.app)**  

🔹 **Developed by [Durjoy Kumar]**


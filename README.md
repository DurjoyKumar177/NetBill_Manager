# 🌐 NetBill Manager - Backend

🌟 About NetBill_Manager

NetBill_Manager is a powerful and intuitive platform designed for Internet Service Providers (ISPs) to efficiently manage their customer accounts, billing, and service-related operations. With a focus on automation, transparency, and seamless user experience, our system ensures smooth interactions between ISPs and their users.

🎯 Our Motive

At NetBill_Manager, we aim to revolutionize the ISP management experience by offering a seamless, user-friendly, and automated platform. Our goal is to reduce manual efforts, enhance communication, and improve service efficiency, ensuring that both ISPs and customers benefit from a well-structured digital ecosystem.

🚀 Why We Built This?

✅ To streamline ISP operations with automated account management.
✅ To enhance transparency in billing, complaints, and announcements.
✅ To improve customer satisfaction by reducing downtime and response time.
✅ To empower ISPs with better control and insights into their services.

🎯 Our Goals

✅ Efficiency & Automation – Reduce manual workload with automated processes.✅ Customer-Centric Approach – Ensure user-friendly navigation and effective communication.✅ Security & Reliability – Provide a secure and stable system for account and transaction management.✅ Scalability & Performance – Design a robust system that grows with ISP needs.✅ Innovative Features – Continuously enhance with new functionalities and integrations.

🔑 Key Features

📢 Announcements Section – Publish ISP updates, network maintenance notices, and new features.📨 Complaint Management – Users can report issues, track complaints, and receive staff responses.🔄 Account Activation & Management – Secure verification process before activating user accounts.💰 Billing & Transactions – Users can view payment history and track outstanding bills.🔐 Secure Authentication – Token-based authentication with profile management options.📊 Admin Dashboard – Manage users, transactions, complaints, and announcements effectively.

🛠️ Technologies Used

NetBill_Manager is built with modern technologies to ensure a fast, scalable, and efficient ISP management experience:

Backend: Django (Python), PostgreSQL

Frontend: React, Tailwind CSS, Daisy UI

Authentication: Token-based authentication (JWT)

🚀 Join us in redefining ISP management with NetBill_Manager! 💡

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


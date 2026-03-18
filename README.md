# 🚀 Nexuzy ERP — Full ERP Ecosystem by Nexuzy Lab

> All-in-One Manufacturing + Business + Workforce System  
> Inspired by SAP / Odoo — Optimized for Shared Hosting

![Python](https://img.shields.io/badge/Python-PySide6-blue)
![PHP](https://img.shields.io/badge/Backend-Core%20PHP-purple)
![MySQL](https://img.shields.io/badge/DB-MySQL-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🧠 What is Nexuzy ERP?

Nexuzy ERP is a full enterprise resource planning system built for manufacturing and business management. It combines a beautiful Python desktop client with a lightweight PHP backend that runs on any shared hosting.

---

## 🏗️ Architecture

```
[ Python Desktop ERP (PySide6) ]
        ↓ REST API (JSON)
[ PHP Backend (cPanel Shared Hosting) ]
        ↓
[ MySQL Database ]
```

---

## 📦 Modules

| Module | Status |
|---|---|
| 🔐 Authentication & Roles | ✅ |
| 👨‍💼 Employee Management | ✅ |
| ⏱️ Attendance (Check-in/out) | ✅ |
| 📦 BOM (Bill of Materials) | ✅ |
| 🏭 Production Management | ✅ |
| 📦 Inventory Management | ✅ |
| 🛒 Purchase Management | ✅ |
| 💰 Sales Management | ✅ |
| 📊 Accounting | ✅ |
| 📈 Reports & Analytics | ✅ |
| 🔔 Notifications | ✅ |
| 🌍 Multi-language (EN/HI/BN) | ✅ |
| ☁️ Cloud Sync | ✅ |
| 🤖 AI Insights (Sarvaam AI) | ✅ |

---

## 🎨 UI/UX

- **Framework:** PySide6 (Qt6)
- **Theme:** Dark + Gradient (Blue → Purple)
- **Style:** Glass UI Cards, Smooth Animations
- **Responsive** sidebar navigation

---

## 🔐 Roles

| Role | Access |
|---|---|
| Admin | Full System |
| Manager | Production + Reports |
| Supervisor | Worker Control |
| Worker | Attendance + Tasks |
| Accountant | Finance |

---

## 🚀 Quick Start

### Python Desktop
```bash
git clone https://github.com/david0154/nexuzy-erp
cd nexuzy-erp
pip install -r requirements.txt
python main.py
```

### PHP Backend
1. Upload `/php_backend/` to your cPanel `public_html/api/`
2. Import `database/nexuzy_erp.sql`
3. Update `php_backend/config/db.php` with your credentials
4. Update `nexuzy_erp/config/settings.py` with your API URL

---

## 🌐 API Endpoints

```
POST /api/login.php
GET  /api/users.php
GET  /api/employees.php
POST /api/attendance.php
GET  /api/products.php
GET  /api/bom.php
GET  /api/inventory.php
POST /api/purchase.php
POST /api/production.php
POST /api/sales.php
GET  /api/reports.php
POST /api/sync.php
```

---

## 🤖 AI Integration

Nexuzy ERP integrates **Sarvaam AI API** for:
- Smart inventory predictions
- Sales trend insights
- Production optimization suggestions

Configure your API key in `nexuzy_erp/config/settings.py`.

---

## 🗃️ Database Tables

`users` • `roles` • `employees` • `attendance` • `departments` • `products` • `bom` • `inventory` • `warehouses` • `suppliers` • `purchases` • `sales` • `production_orders` • `logs`

---

## 📁 Project Structure

```
nexuzy-erp/
├── main.py
├── requirements.txt
├── nexuzy_erp/
│   ├── config/
│   ├── ui/
│   ├── modules/
│   ├── api/
│   └── database/
├── php_backend/
│   ├── config/
│   └── api/
└── database/
    └── nexuzy_erp.sql
```

---

## 🌍 Languages

English | हिंदी | বাংলা

---

## 📱 Future

- Flutter Mobile App
- Face Recognition Attendance
- Barcode Scanning
- Multi-company Support
- Advanced AI Analytics

---

## 🏢 Made by Nexuzy Lab

> © 2026 Nexuzy Lab — All Rights Reserved

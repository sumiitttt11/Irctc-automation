# 🚆 IRCTC Tatkal Booking Automation System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Nodriver](https://img.shields.io/badge/Nodriver-CDP%20Automation-2E8B57?style=for-the-badge)
![Gemini](https://img.shields.io/badge/Google-Gemini%20API-4285F4?style=for-the-badge&logo=google)
![Telegram](https://img.shields.io/badge/Telegram-Bot%20API-26A5E4?style=for-the-badge&logo=telegram)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**⚡ High-performance browser automation system for IRCTC Tatkal ticket booking using Python, Nodriver & Google Gemini API.**

</div>

---

# 📖 Overview

IRCTC Tatkal booking is an extremely time-sensitive process where tickets often sell out within seconds due to high demand.

This project automates the complete booking workflow using **Nodriver**, a Chromium DevTools Protocol (CDP) based browser automation framework. The objective is to minimize manual interaction, reduce booking time, and improve booking success during Tatkal reservation windows.

The system automatically:

- Logs into IRCTC
- Searches trains
- Selects the preferred train
- Loads passenger information from a master list
- Auto-fills booking details
- Solves CAPTCHA using Google Gemini API
- Completes the booking workflow
- Sends real-time Telegram notifications

---

# ✨ Features

## 🚄 End-to-End Booking Automation

Automates the complete booking workflow from login to final confirmation.

### Supported Workflow

- Login to IRCTC
- Search Trains
- Select Journey
- Select Coach Class
- Choose Quota
- Auto Fill Passenger Details
- AI CAPTCHA Recognition
- Review Booking
- Payment Navigation
- Telegram Status Updates

---

## 👥 Master Passenger List

Passenger information is stored inside a centralized configuration file.

The automation automatically fills:

- Passenger Name
- Age
- Gender
- Berth Preference
- Passenger Type
- Mobile Number

This removes repetitive manual data entry during Tatkal booking.

---

## 🤖 AI CAPTCHA Recognition

The project integrates **Google Gemini API** to recognize IRCTC CAPTCHA images.

Workflow:

```
Capture CAPTCHA

↓

Send Image to Gemini API

↓

Receive Prediction

↓

Fill CAPTCHA

↓

Continue Booking
```

This significantly reduces one of the largest manual bottlenecks during booking.

---

## ⚡ Nodriver Browser Automation

Instead of Selenium, the project uses **Nodriver**, which communicates directly with Chromium using the Chrome DevTools Protocol (CDP).

Advantages include:

- Faster execution
- Modern asynchronous architecture
- Reduced browser overhead
- Better handling of dynamic websites
- Reliable browser control
- No WebDriver dependency

---

## 🚉 Optimized for Tatkal Booking

The automation has been optimized specifically for high-demand booking windows.

Optimizations include:

- Preloaded passenger data
- Cached route information
- Smart element synchronization
- Automatic retry mechanism
- Efficient page navigation
- Dynamic wait strategies
- Reduced unnecessary interactions

---

## 📱 Telegram Notifications

Receive real-time updates including:

- Booking Started
- Train Found
- Booking Successful
- Booking Failed
- Unexpected Errors
- Runtime Logs

---

## 🛡 Robust Error Handling

The framework gracefully handles:

- Timeout Exceptions
- Dynamic DOM updates
- Missing Elements
- Browser Interruptions
- Network Delays
- Unexpected Navigation
- Retryable Failures

---

# 🏗 System Architecture

```
                 User Configuration
                         │
                         ▼
                  Config Loader
                         │
                         ▼
               Browser Initialization
                  (Nodriver/CDP)
                         │
                         ▼
                  Health Check
                         │
                         ▼
                    Login Module
                         │
                         ▼
                  Train Search
                         │
                         ▼
                 Train Selection
                         │
                         ▼
              Passenger Auto Fill
               (Master Passenger List)
                         │
                         ▼
              Gemini CAPTCHA Solver
                         │
                         ▼
                  Review Booking
                         │
                         ▼
                  Payment Workflow
                         │
                         ▼
             Telegram Notifications
                         │
                         ▼
                     Booking Complete
```

---

# 🛠 Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Core Development |
| Nodriver | Browser Automation |
| Chromium CDP | Browser Communication |
| Google Gemini API | CAPTCHA Recognition |
| Telegram Bot API | Notifications |
| JSON | Configuration Management |
| Git | Version Control |
| GitHub | Repository Hosting |

---

# 📂 Project Structure

```
IRCTC-Tatkal-Automation
│
├── config/
│   ├── passengers.json
│   ├── routes.json
│   └── selectors.py
│
├── core/
│   ├── __init__.py
│   ├── browser.py
│   ├── config_loader.py
│   ├── logger.py
│   ├── http.py
│   ├── poller.py
│   ├── profiler.py
│   ├── retry.py
│   ├── telegram.py
│   └── telegram_bot.py
│
├── modules/
│   ├── __init__.py
│   ├── health_check.py
│   ├── login.py
│   ├── passenger_filler.py
│   ├── payment.py
│   ├── review_page.py
│   ├── train_search.py
│   ├── train_selector.py
│   └── update.txt
│
├── .env.example
├── requirements.txt
├── render.yaml
├── main.py
└── README.md
```

---

# ⚙ Configuration

The application uses JSON configuration files to simplify customization.

### passengers.json

Stores reusable passenger profiles.

```json
{
  "name": "John Doe",
  "age": 28,
  "gender": "Male",
  "berth": "Lower"
}
```

---

### routes.json

Stores frequently used travel routes.

```json
{
  "from": "Mumbai Central",
  "to": "New Delhi",
  "quota": "Tatkal",
  "class": "3A"
}
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/IRCTC-Tatkal-Automation.git
```

Navigate to the project

```bash
cd IRCTC-Tatkal-Automation
```

Install dependencies

```bash
pip install -r requirements.txt
```

Configure environment variables

```bash
cp .env.example .env
```

Update

- Gemini API Key
- Telegram Bot Token
- Telegram Chat ID

Run

```bash
python main.py
```

---

# 📊 Workflow

```
Start

↓

Load Configuration

↓

Initialize Browser

↓

Perform Health Check

↓

Login to IRCTC

↓

Search Available Trains

↓

Select Preferred Train

↓

Load Passenger Data

↓

Fill Passenger Information

↓

Capture CAPTCHA

↓

Gemini API Recognition

↓

Fill CAPTCHA

↓

Review Booking

↓

Proceed to Payment

↓

Send Telegram Notification

↓

Finish
```

---

# 💡 Engineering Highlights

- Modular Architecture
- Separation of Concerns
- CDP Browser Automation
- AI-Assisted CAPTCHA Recognition
- Master Passenger Management
- Automatic Retry System
- Dynamic Polling Utilities
- Structured Logging
- Performance Profiling
- Configuration-Driven Workflow
- Real-Time Telegram Notifications
- Fault-Tolerant Execution

---

# 🔮 Roadmap

- Multi-Passenger Booking Queue
- OCR + Gemini Hybrid CAPTCHA Recognition
- Web Dashboard
- Docker Support
- Cloud Deployment
- Parallel Booking Sessions
- HTML Execution Reports
- Booking Analytics Dashboard
- Automatic Route Scheduler
- CI/CD Integration

---

# ⚠ Disclaimer

This project was developed for educational purposes and browser automation research.

It demonstrates browser automation techniques, modular software design, AI-assisted image recognition, and automation engineering concepts.

Users are solely responsible for complying with the IRCTC Terms of Service and all applicable laws and regulations when using or modifying this software.

---

# 👨‍💻 Author

## Sumit Kumawat

**Software Developer • AI • Browser Automation • Full Stack**

🌐 Portfolio  
https://sumitkumawat.dev

🐙 GitHub  
https://github.com/sumiitttt11

💼 LinkedIn  
https://linkedin.com/in/sumiitttt11

---

<div align="center">

⭐ If you found this project interesting, consider giving it a star!

</div>

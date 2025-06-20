🌾 Crop Recommendation System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![Django](https://img.shields.io/badge/Django-3.0-green.svg)](https://www.djangoproject.com)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![ML](https://img.shields.io/badge/Machine-Learning-red.svg)](https://scikit-learn.org)

📖 Introduction

The Crop Recommendation System is an intelligent agricultural solution that helps farmers make informed decisions about crop selection based on soil conditions and environmental factors. Using machine learning algorithms, the system analyzes soil nutrients (N-P-K values), environmental conditions (temperature, humidity, rainfall), and pH levels to recommend the most suitable crops for cultivation.

⭐ Features

🎯 Core Functionality
- 🤖 Crop Recommendation Engine: ML-based crop suggestions
- 🧪 Soil Analysis: N-P-K (Nitrogen, Phosphorus, Potassium) value interpretation
- 🌡️ Environmental Factor Analysis: Temperature, Humidity, pH, and Rainfall consideration
- 📊 Historical Data Tracking: Past recommendations and results
- 📈 Dataset Management: Dynamic dataset updates for improved accuracy

💻 User Interface
- 📱 Responsive Design: Mobile-friendly interface
- 📝 Interactive Forms: Easy data input
- ✅ Real-time Validation: Input verification
- 📊 Visual Feedback: Clear result presentation
- 📈 User Dashboard: Personal recommendation history
 👥 User Roles and Functions

👑 Admin Functions
1. Dataset Management
   - ➕ Add new crop data
   - 📝 Edit existing entries
   - 🗑️ Delete outdated records
   - 👀 View complete dataset

2. User Management
   - 👥 Manage user accounts
   - 📊 Monitor user activity
   - 🔐 Control access permissions

3. Feedback Management
   - 📬 View all user feedback
   - 🗑️ Delete inappropriate feedback
   - ⭐ Monitor system ratings

4. System Oversight
   - 📊 Access complete recommendation logs

👤 Authenticated User Functions
1. Crop Recommendation
   - 📝 Submit soil and environmental data
   - 🌱 Receive crop recommendations
   - 📋 View recommendation history
   - ⬇️ Download recommendation reports

2. Profile Management
   - 👤 Update personal information
   - 🔑 Change password
   - 📋 View activity history

3. Feedback System
   - 💬 Submit feedback
   - ⭐ Rate system performance
   - 📝 Edit own feedback
   - 🗑️ Delete own feedback

4. History Management
   - 📋 View past recommendations
   - 📊 Track soil parameter history
   - 🗑️ Delete personal records

 🚀 Project Setup

📋 Prerequisites
- 🐍 Python 3.8 or higher
- 📦 pip (Python package manager)
- 🔧 Virtual environment (recommended)
- 🔄 Git (for version control)

⚙️ Installation Steps

1. Clone the Repository
   ```bash
   git clone https://github.com/kkraddi111/Crop-recommendation-system
   cd Agri
   ```

2. Set Up Virtual Environment
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Database Setup
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create Admin User
   ```bash
   python manage.py createsuperuser
   # Follow prompts to create admin account
   ```

6. Start Development Server
   ```bash
   python manage.py runserver
   ```

7. Access the Application
   - 🌐 Main application: http://127.0.0.1:8000/
   - ⚙️ Admin interface: http://127.0.0.1:8000/admin/

# 📝 Additional Setup Notes
- ⚙️ Ensure all required environment variables are set
- 🗄️ Configure database settings if using custom database
- 📁 Set up static files and media storage
- 📧 Configure email settings if required

 💻 System Requirements
- 🖥️ OS: Windows/Linux/Mac OS
- 💾 RAM: Minimum 4GB (8GB recommended)
- 💽 Storage: 1GB free space
- ⚡ Processor: Dual-core processor or better
- 🌐 Internet: Required for initial setup and updates

 🛠️ Technology Stack
- 🔙 Backend: Django 3.0
- 🗄️ Database: SQLite (default)
- 🤖 ML Libraries: scikit-learn, pandas, numpy
- 🎨 Frontend: HTML5, CSS3, JavaScript
- 🖼️ Additional: Pillow for image processing

 📞 Support and Documentation
For additional support or documentation:
- 📚 Check the project wiki
- 🐛 Submit issues on GitHub
- 📧 Contact system administrators
- 📖 Review the code documentation

 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

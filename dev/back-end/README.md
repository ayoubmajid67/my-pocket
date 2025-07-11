# Project Setup Guide  

## 1. Create a Virtual Environment  

The **`venv`** folder is used to create a virtual environment in Python, which is an isolated environment that allows you to manage dependencies for your project without affecting the global Python installation. This ensures that each project can have its own set of dependencies.  

After cloning the repository, the virtual environment must be created to install the backend dependencies.  

### 1.1 Create a Virtual Environment  

```bash
cd BACK-END
python -m venv venv
```

### 1.2 Activate the Virtual Environment (In `cmd`, Not PowerShell)  

```bash
venv\Scripts\activate
```

### 1.3 Install the Dependencies  

```bash
pip install -r requirements.txt
```

---

## 2. Install MySQL Workbench  

Download and install MySQL Workbench from the official MySQL website:  

🔗 [Download MySQL Workbench](https://dev.mysql.com/downloads/workbench/)  

---

## 3. Create a New Database in MySQL  

Open MySQL Workbench and execute the following SQL commands to create a new database named **`MyPocketDb`**:  

```sql
run the code in /conception/MLD/MYPOCKET_DB_SQL.sql
```

---

## 4. Set Up Flask Project  

### 4.1 Install Dependencies  

Ensure you have Python installed, then navigate to your project folder and run:  

```bash
pip install -r requirements.txt
```

### 4.2 Create and Configure the `.env` File  

Inside your project directory, create a `.env` file and add the following:  

```
FLASK_APP=run.py
SECRET_KEY=b'#\x01e\xad?\x1djl`*\n~\x8f%\xdt\xcl'
AYOUB_DB_CNX=mysql+pymysql://root:majid077179_mysql@localhost:3306/MyPocketDb
```

### 4.3 Update Flask Configuration  

Modify the `config.py` file to load the environment variables:  

```python
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    UPLOAD_FOLDER = 'data/profiles'
    ALLOWED_IMG_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    ALLOWED_VIDEO_EXTENSIONS = {'mp4'}
    API_VERSION = 'v1'
    
    SQLALCHEMY_DATABASE_URI = os.getenv('AYOUB_DB_CNX')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

---

## 5. Run the Project  

Once everything is set up, you can start the project using the following command:  

```bash
py run.py

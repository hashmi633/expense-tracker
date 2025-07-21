# Database Configuration Guide

## Local PostgreSQL Setup

### 1. Installation

#### Windows
Download from: [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)

#### macOS (Homebrew)
```bash
brew install postgresql@15
brew services start postgresql@15
```

#### Linux (Ubuntu)
```bash
sudo apt install postgresql postgresql-contrib
sudo service postgresql start
```

---

### 2. Database Initialization Process

## Environment Setup

### Add PostgreSQL to PATH (Windows)

1. Open **System Properties** → **Environment Variables**
2. Under **System Variables**, edit **Path**
3. Add a new entry:
   ```
   C:\Program Files\PostgreSQL\<version>\bin
   ```

---

### Step-by-Step Navigation

#### 1. Open Command Prompt as Administrator

#### 2. Navigate to PostgreSQL bin directory
```cmd
cd "C:\Program Files\PostgreSQL\<version>\bin"
```

#### 3. Check the PostgreSQL version
```cmd
psql --version
```

#### 4. Initialize Database: Connect as admin
```cmd
psql -U postgres
```

#### 5. Create application user
```psql
CREATE USER app_user WITH PASSWORD 'secure_password123!';
```

#### 6. Create application database
```psql
CREATE DATABASE expense_tracker;
```

#### 7. Grant privileges
```psql
GRANT ALL PRIVILEGES ON DATABASE expense_tracker TO app_user;
```

#### 7.1 Confirm connection with new user
```bash
psql -U app_user -d expense_tracker -h localhost
```

#### 8. Verify users and databases
```psql
\du   -- View users
\l    -- View databases
```

---

### pgAdmin Setup

#### Installation

- Included with Windows PostgreSQL installer  
- Or download separately from [https://www.pgadmin.org/download/](https://www.pgadmin.org/download/)

#### First-Time Setup

1. Launch **pgAdmin**
2. Set a **master password** when prompted
3. Right-click **Servers** → **Register** → **Server**

#### Connection Details

- **Name**: Local PostgreSQL  
- **Host**: localhost  
- **Port**: 5432  
- **Username**: app_user  
- **Password**: secure_password123!

---
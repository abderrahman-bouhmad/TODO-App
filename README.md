## Database Schema

**users and tasks**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique ID for each user
    username TEXT NOT NULL UNIQUE,         -- Username (must be unique)
    hash TEXT NOT NULL                     -- Hashed password
);

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,         -- Unique ID for each task
    user_id INTEGER NOT NULL,                     -- References the user who owns the task
    description TEXT NOT NULL,                    -- The task's text/description
    completed INTEGER NOT NULL DEFAULT 0,         -- Task completion status (0 = not done, 1 = done)
    FOREIGN KEY(user_id) REFERENCES users(id)
);

```

## 🚀 How to Run This Flask App Locally

### 1. Clone the repository
```bash
git clone https://github.com/abderrahman-bouhmad/TODO-App.git
cd TODO-App
```
### 2. Set up virtual environment (optional but recommended)
```bash
python3 -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Run the app
```bash
flask run
Then visit the link provided
```
## 📸 Screenshots

| ![Screenshot 1](https://github.com/user-attachments/assets/10b9111f-6073-4178-8491-157e2e680551) | ![Screenshot 2](https://github.com/user-attachments/assets/8c3487ed-1882-4345-808a-13fff9fc1db9) |
| ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| ![Screenshot 3](https://github.com/user-attachments/assets/0054ee7e-ff42-4142-907a-888cd231291e) | ![Screenshot 4](https://github.com/user-attachments/assets/8593c68b-1e80-414f-a8b2-3c4c09d3abd2) |

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

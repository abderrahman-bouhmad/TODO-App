## Database Schema

### users
| Column   | Type    | Constraints            |
|----------|---------|------------------------|
| id       | INTEGER | Primary key, auto-increment |
| username | TEXT    | Not null, unique       |
| hash     | TEXT    | Not null (password hash) |

### tasks
| Column    | Type    | Constraints                   |
|-----------|---------|-------------------------------|
| id        | INTEGER | Primary key, auto-increment   |
| user_id   | INTEGER | Not null, foreign key → users.id |
| task      | TEXT    | Not null                      |
| completed | INTEGER | Default 0 (false)             |

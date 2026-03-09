_Railway Reservation System_

A complete **Railway Reservation System** developed using **Python** and **MySQL**, providing a simple CLI-based interface for managing train bookings. It allows users to **search for trains, book tickets, cancel bookings**, and view details through a terminal interface connected to a MySQL database.

---

_Features_

- Add new trains to the system
- View all available trains
- Search for specific trains
- Book tickets
- Cancel tickets
- View passenger details
- Admin and user interfaces
- Fully integrated with MySQL (no CSV file dependency)

---

_Technologies Used_

- **Python** – Core programming language
- **MySQL** – Relational database to store train and booking data
- **mysql-connector-python** – For connecting Python with MySQL
- **datetime** – Used for managing booking and journey dates
- **os** – Used for terminal screen clearing and formatting

---

_Project Structure_

```bash
railway-reservation-system/
│
├── railway.py                 # Main executable script
├── db_config.sql              # SQL schema and table creation queries
├── README.md                  # Project documentation (this file)
└── requirements.txt           # Python dependencies
```

---

_Setup & Installation_

### 1. Clone the repository
```bash
git clone (https://github.com/khu-lood/Railway-Reservation-System)
cd Railway-Reservation-System
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up MySQL Database
- Create a MySQL database (e.g., `railway`)
- Import the schema using the provided SQL file:
```bash
mysql -u root -p railway < db_config.sql
```
- Ensure your MySQL user, password, host, and database match the values in `railway.py`.

### 4. Run the Project
```bash
python railway.py
```

---

_Author_

- **Khulood** – [GitHub Profile](https://github.com/khu-lood)

---

_License_

This project is open-source and available under the [MIT License](LICENSE).

---

_TODO / Future Improvements_

- Add user login/registration system
- Add email notifications for booking confirmations

## Examination Printing Management System (EPMS)

### Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Configuration](#configuration)
6. [Contributing](#contributing)
7. [License](#license)
8. [Contact](#contact)

---

### Introduction

The **Examination Printing Management System (EPMS)** is a web-based application designed to streamline and optimize the management of printing tasks within an organization. It allows users to upload documents for printing, track the status of print jobs, manage print queues, and provide detailed reporting on print usage and costs.

### Features

- **User Management**: Supports multiple roles, including admin, printing agents, examiners, and users.
- **Document Upload and Tracking**: Allows users to upload documents and track their printing status.
- **Real-Time Dashboard**: Provides a comprehensive view of printing statistics, including the number of approved and pending print jobs, total courses, and total users.
- **Schedule Management**: Admin can manage and assign printing schedules, with a calendar view for better visualization.
- **Security**: Includes user authentication, password reset functionality, and secure file handling.
- **Analytics and Reporting**: Offers advanced reporting features to analyze printing costs and usage patterns.

### Installation

To get started with the Printing Management System, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/pms.git
    cd pms
    ```

2. **Set up a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    - Create a `.env` file in the project root and add your environment-specific variables such as `SECRET_KEY`, `MAIL_USERNAME`, `MAIL_PASSWORD`, etc.

5. **Run database migrations**:
    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

6. **Start the application**:
    ```bash
    flask run
    ```

### Usage

1. **Access the application**:
   Open a web browser and go to `http://localhost:5000`.

2. **Log in or create an account**:
   Depending on your role (admin, printing agent, examiner), you will have different access levels and functionalities.

3. **Upload documents for printing**:
   Navigate to the "Upload Documents" section to upload files and manage your print jobs.

4. **Manage schedules**:
   Admin users can add or edit printing schedules, view them in a table or calendar format, and assign resources as needed.

5. **Generate reports**:
   Use the reporting tools to analyze printing activity and optimize resource allocation.

### Configuration

The Printing Management System uses environment variables to manage sensitive information and settings. Here is a list of important environment variables:

- `SECRET_KEY`: A secret key for your Flask application.
- `MAIL_SERVER`: The SMTP server for sending emails.
- `MAIL_PORT`: The SMTP port.
- `MAIL_USERNAME`: The email address to send emails from.
- `MAIL_PASSWORD`: The password for the email account.
- `DATABASE_URL`: The database connection string.

Ensure these are set correctly in your `.env` file.

### Contributing

We welcome contributions to the Printing Management System project! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Open a Pull Request.

Please make sure your code follows our coding standards and includes relevant tests.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

### Contact

If you have any questions, suggestions, or need support, feel free to contact us:

- **Project Maintainer**: Abraham Forkuo
- **Email**: abrahamforkuo8@gmail.com

---

Feel free to customize this README according to your project's specific needs and details!

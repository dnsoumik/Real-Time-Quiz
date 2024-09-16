# Tornado Quiz App

This project is a basic Tornado application that provides a Sign-In API with JWT-based authentication and APIs for submitting quiz details and retrieving all quizzes. All data is stored in MongoDB.

## Features

- **Sign-In API** with JWT-based authentication
- **Submit Quiz API** to submit quiz details (requires authentication)
- **Get All Quizzes API** to fetch all quiz details (requires authentication)
- **MongoDB** for data storage

## Requirements

- Python 3.11
- MongoDB
- Tornado Web Framework
- Motor (Async MongoDB Driver)
- PyJWT for JWT generation and validation

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/dnsoumik/Real-Time-Quiz.git
    cd Real-Time-Quiz/backend-server
    ```

2. **Install dependencies:**

    You can install all required dependencies using `pip`:

    Alternatively, install the required packages manually:

    ```bash
    pip install tornado motor pymongo PyJwt
    ```

## Running the Application

**Start the Tornado Server:**

    Run the following command to start the Tornado server on port 8888:

    ```bash
    start.sh
    ```

    To check the Logs

    ```
    ./web_log.sh
    ```

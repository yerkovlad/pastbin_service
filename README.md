# Pastbin Service

Welcome to the **Pastbin Service**! This FastAPI-based web application allows users to securely register, log in, and post messages. With robust email verification and JWT-based authentication, this project offers a streamlined and secure experience for users.

![Pastbin Service Architecture](img/pastbin_service.png)

## Features

- **User Registration and Login**: Secure authentication with email verification.
- **Message Posting**: Users can post messages that are associated with a unique hash identifier.
- **Email Verification**: Automated confirmation emails sent upon registration.
- **JWT Authentication**: Token-based authentication for secure user access.

## Installation

**Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/pastbin-service.git
   cd pastbin_service
   ```

## Usage

**To run the application, start the FastAPI server:**
   ```bash
   uvicorn main:app --reload
   ```

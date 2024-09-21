# Ishikoridome - Identity Verification Microservice

Ishikoridome is a microservice designed for identity verification, allowing users to sign up by providing personal information and photos. The service verifies user identities and manages signup requests efficiently. It utilizes RabbitMQ for messaging, S3 for storage, PostgreSQL for database management, and Mailgun for email handling.

## Features

- **User Signup**: Users can sign up by submitting personal information and two photos for verification.
- **Identity Verification**: The service verifies submitted identities and approves or rejects signup requests.
- **Microservice Architecture**: Built to function effectively within a microservices ecosystem.
- **Asynchronous Messaging**: Utilizes RabbitMQ for communication between services.
- **Data Storage**: Stores user data and photos in S3.
- **Database Management**: Uses PostgreSQL for reliable data storage and management.
- **Email Notifications**: Sends verification emails using Mailgun.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) (for containerization)
- [RabbitMQ](https://www.rabbitmq.com/) (for messaging)
- [PostgreSQL](https://www.postgresql.org/) (for database)
- [AWS S3](https://aws.amazon.com/s3/) (for storage)
- [Mailgun](https://www.mailgun.com/) (for email notifications)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Manni-MinM/ishikoridome.git
   cd ishikoridome
   ```

2. Build the Docker image:

   ```bash
   docker build -t ishikoridome .
   ```

3. Start the services (RabbitMQ, PostgreSQL) as needed, either locally or through Docker Compose.

### Configuration

Edit the configuration files in the `config` directory to set up your database, RabbitMQ, and Mailgun settings.

### Usage

Once everything is set up, users can sign up through the API. The service will handle identity verification and notify users via email.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

# File Sharing Application

A secure and efficient temporary file sharing solution with QR code support and automatic file cleanup.

## Features

- Temporary file sharing with customizable expiration times
- QR code generation for easy file access
- Automatic cleanup of expired files
- User authentication and access control
- Secure file storage and sharing

## Prerequisites

1. Python 3.8 or higher
2. pip (Python package installer)
3. Git
4. Virtual environment (recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd file-sharing-app
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Set up environment variables:
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   export SECRET_KEY=your-secret-key
   ```

2. Configure application settings:
   - Update `base_url` in the application configuration
   - Set appropriate `UPLOAD_FOLDER` path
   - Adjust default file expiration time if needed

## Usage

1. Start the application:
   ```bash
   flask run
   ```

2. Access the application at `http://localhost:5000`

3. Register a new account or login

4. Upload files and share them using the generated URLs or QR codes

## Production Deployment

### Security Considerations

1. **Environment Configuration**:
   - Use strong, unique `SECRET_KEY`
   - Enable HTTPS/SSL
   - Set appropriate file size limits
   - Configure secure headers

2. **File Storage**:
   - Use cloud storage (e.g., AWS S3) for scalability
   - Implement proper access controls
   - Regular backup strategy

3. **Authentication**:
   - Implement rate limiting
   - Set secure password policies
   - Enable session timeout

### Deployment Steps

1. **Prepare the Application**:
   - Update dependencies
   - Set production configurations
   - Configure logging

2. **Server Setup**:
   - Use a production-grade WSGI server (e.g., Gunicorn)
   - Set up reverse proxy (e.g., Nginx)
   - Configure SSL certificates

3. **Database**:
   - Use a production database (e.g., PostgreSQL)
   - Set up database backups
   - Configure connection pooling

4. **Monitoring**:
   - Set up application monitoring
   - Configure error tracking
   - Implement health checks

## Troubleshooting

1. **File Upload Issues**:
   - Check file size limits
   - Verify upload directory permissions
   - Ensure proper directory structure

2. **URL Access Problems**:
   - Confirm base URL configuration
   - Check SSL/TLS settings
   - Verify network connectivity

3. **Performance Issues**:
   - Enable Flask debugging only in development
   - Use a production-grade WSGI server
   - Monitor system resources

## Support

For issues and feature requests, please create an issue in the repository.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
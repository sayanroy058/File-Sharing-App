# File Sharing Application

A secure file sharing application built with Flask that allows users to upload files and share them temporarily with others through unique URLs and QR codes.

## Configuration

### Base URL Configuration

Before deploying the application, you need to update the base URL in `app.py`. Locate the following code:

```python
temp_share = TempFileShare(
    base_url='http://127.0.0.1:5000',
    upload_folder=app.config['UPLOAD_FOLDER']
)
```

Replace `http://127.0.0.1:5000` with your production domain:
- For Heroku: `https://your-app-name.herokuapp.com`
- For AWS Elastic Beanstalk: `https://your-environment.region.elasticbeanstalk.com`
- For custom domain: `https://your-domain.com`

### Environment Variables

Create a `.env` file in the root directory with the following variables:
```
FLASK_SECRET_KEY=your-secure-secret-key
FLASK_ENV=production
```

## Deployment Guide

### Prerequisites

1. Python 3.8 or higher
2. pip (Python package installer)
3. Git
4. Account on your chosen cloud platform

### Local Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```

### Deploying to Heroku

1. Install Heroku CLI
2. Login to Heroku:
   ```bash
   heroku login
   ```
3. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```
4. Add Procfile (create a file named `Procfile`):
   ```
   web: gunicorn app:app
   ```
5. Update requirements.txt:
   ```bash
   pip install gunicorn
   pip freeze > requirements.txt
   ```
6. Deploy:
   ```bash
   git push heroku main
   ```

### Deploying to AWS Elastic Beanstalk

1. Install AWS EB CLI
2. Initialize EB application:
   ```bash
   eb init -p python-3.8 your-app-name
   ```
3. Create environment:
   ```bash
   eb create your-environment-name
   ```
4. Deploy:
   ```bash
   eb deploy
   ```

## Production Considerations

1. **Database**: Replace the in-memory user storage with a proper database system (e.g., PostgreSQL)
2. **File Storage**: Use cloud storage (e.g., AWS S3) instead of local file system
3. **Security**:
   - Update `SECRET_KEY` in production
   - Enable HTTPS
   - Set appropriate CORS policies
   - Implement rate limiting
4. **Monitoring**: Set up logging and monitoring

## Environment Variables

Configure these environment variables in your production environment:

- `FLASK_ENV`: Set to 'production'
- `FLASK_SECRET_KEY`: A secure random key
- `BASE_URL`: Your application's base URL
- `MAX_CONTENT_LENGTH`: Maximum file size (in bytes)

## Troubleshooting

1. **File Upload Issues**:
   - Check file size limits
   - Verify upload directory permissions

2. **URL Access Problems**:
   - Confirm base URL configuration
   - Check SSL/TLS settings

3. **Performance Issues**:
   - Enable Flask debugging only in development
   - Use a production-grade WSGI server (e.g., Gunicorn)

## Support

For issues and feature requests, please create an issue in the repository.

## License

MIT License
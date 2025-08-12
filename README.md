# Edson da Silva - Personal Website

A modern, responsive personal portfolio website built with HTML, CSS, and JavaScript, featuring a complete Python-based development stack and deployed on AWS using Terraform for Infrastructure as Code.

## 🚀 Features

- **Modern Design**: Clean, professional UI with smooth animations
- **Responsive**: Works perfectly on desktop, tablet, and mobile devices
- **Fast Loading**: Optimized for performance with CloudFront CDN
- **Secure**: HTTPS enabled with SSL certificates
- **SEO Friendly**: Optimized for search engines
- **Contact Form**: Interactive contact form for visitors
- **Python Development Stack**: Complete toolchain for development, testing, and deployment
- **Live Reload**: Hot reload development server
- **Comprehensive Testing**: HTML, CSS, JS, accessibility, and performance testing
- **Build Optimization**: Automated minification and asset optimization

## 🏗️ Architecture

### Infrastructure Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                AWS Cloud Infrastructure                          │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌──────────────┐    ┌─────────────────┐    ┌──────────────────────────────┐   │
│  │   Route 53   │    │   ACM (SSL)     │    │        CloudFront            │   │
│  │              │    │                 │    │                              │   │
│  │ DNS Management│◄──►│ SSL Certificate │◄──►│    Global CDN Network        │   │
│  │ (Optional)   │    │ Management      │    │                              │   │
│  └──────────────┘    └─────────────────┘    │ ┌──────────────────────────┐ │   │
│                                             │ │    Edge Locations        │ │   │
│                                             │ │  - Americas              │ │   │
│                                             │ │  - Europe                │ │   │
│                                             │ │  - Asia Pacific          │ │   │
│                                             │ └──────────────────────────┘ │   │
│                                             └──────────────┬───────────────┘   │
│                                                            │                   │
│  ┌─────────────────────────────────────────────────────────▼─────────────────┐ │
│  │                            S3 Bucket                                      │ │
│  │                                                                           │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │ │
│  │  │ index.html  │  │    CSS      │  │ JavaScript  │  │     Assets      │ │ │
│  │  │             │  │ style.css   │  │  main.js    │  │ images, fonts   │ │ │
│  │  │             │  │             │  │             │  │                 │ │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────────┘ │ │
│  │                                                                           │ │
│  │  Features:                                                                │ │
│  │  • Static Website Hosting                                                 │ │
│  │  • Versioning Enabled                                                     │ │
│  │  • Server-side Encryption                                                 │ │
│  └───────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                            Development Environment                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌──────────────┐    ┌─────────────────┐    ┌──────────────────────────────┐   │
│  │   Python     │    │   Terraform     │    │      Local Development       │   │
│  │              │    │                 │    │                              │   │
│  │ manage.py    │◄──►│ Infrastructure  │◄──►│   Flask Dev Server           │   │
│  │ deploy.py    │    │ as Code (IaC)   │    │   Live Reload                │   │
│  │ build.py     │    │                 │    │   Hot CSS/JS Reload          │   │
│  │ setup.py     │    │ • main.tf       │    │                              │   │
│  │              │    │ • variables.tf  │    │   Testing Suite              │   │
│  │              │    │ • outputs.tf    │    │   • HTML5 Validation         │   │
│  │              │    │                 │    │   • CSS Syntax Check         │   │
│  │              │    │                 │    │   • Accessibility Tests      │   │
│  │              │    │                 │    │   • Performance Tests        │   │
│  └──────────────┘    └─────────────────┘    └──────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

Data Flow:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐
│   Visitor   │───►│  Route 53   │───►│ CloudFront  │───►│   S3 Bucket     │
│             │    │   (DNS)     │    │   (CDN)     │    │ (Static Files)  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────────┘
      ▲                                       │
      │                                       │
      └───────────────────────────────────────┘
                    HTTPS Response
```

### Component Details

#### Frontend
- **HTML5, CSS3, JavaScript**: Modern web standards
- **Responsive Design**: Mobile-first approach
- **Progressive Enhancement**: Works without JavaScript

#### AWS Infrastructure
- **S3 Bucket**: Static website hosting with versioning and encryption
- **CloudFront**: Global CDN for fast content delivery and caching
- **Route 53**: DNS management for custom domains (optional)
- **ACM**: Automatic SSL certificate provisioning and renewal
- **Origin Access Control**: Secure access from CloudFront to S3

#### Development Stack
- **Python**: Development tools and automation
- **Terraform**: Infrastructure as Code for reproducible deployments
- **Flask**: Local development server with live reload
- **Pytest**: Comprehensive testing framework
- **Boto3**: AWS SDK for deployment automation

## 📋 Prerequisites

Before starting, ensure you have:

1. **Python 3.8+** installed
   ```bash
   python --version
   ```

2. **AWS CLI** installed and configured
   ```bash
   aws configure
   ```

3. **Terraform** installed (version >= 1.0)
   - Download from: https://www.terraform.io/downloads.html

4. **AWS Account** with appropriate permissions for:
   - S3 bucket creation and management
   - CloudFront distribution management
   - Route 53 (if using custom domain)
   - ACM certificate management

## 🚀 Quick Start

### 1. Project Setup
```bash
# Initialize the project environment
python manage.py setup
```
This will:
- Create a Python virtual environment
- Install all dependencies
- Set up project directories
- Create configuration files

### 2. Development
```bash
# Start the development server with live reload
python manage.py dev
```
- Automatically opens browser at http://localhost:8000
- Live reload on file changes
- Hot CSS/JS reloading

### 3. Testing
```bash
# Run comprehensive test suite
python manage.py test --coverage --html
```
Tests include:
- HTML5 validation
- CSS syntax checking
- JavaScript linting
- Accessibility testing
- Responsive design testing
- Performance checks

### 4. Build for Production
```bash
# Build optimized version
python manage.py build
```
- Minifies HTML, CSS, and JavaScript
- Optimizes assets
- Creates production-ready files

### 5. Deploy to AWS
```bash
# Deploy infrastructure and website
python manage.py deploy --action apply --bucket-name "your-unique-bucket-name"
```

## 📋 Available Commands

The project includes a unified management CLI with the following commands:

```bash
python manage.py info      # Show project information and help
python manage.py status    # Check project health and configuration
python manage.py setup     # Initialize project environment
python manage.py dev       # Start development server with live reload
python manage.py test      # Run comprehensive test suite
python manage.py build     # Build optimized version for production
python manage.py deploy    # Deploy to AWS infrastructure
python manage.py clean     # Clean build artifacts and temporary files
```

For detailed help on any command:
```bash
python manage.py COMMAND --help
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file (automatically created by setup):

```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_PROFILE=default

# Development Server
DEV_HOST=localhost
DEV_PORT=8000

# Build Configuration
BUILD_DIR=dist

# Deployment Configuration
BUCKET_NAME=edson-personal-website
DOMAIN_NAME=
ENVIRONMENT=production
```

### Deployment Configuration

Create `deploy_config.json` (automatically created on first deploy):

```json
{
  "aws_region": "us-east-1",
  "bucket_name": "edson-personal-website-unique-name",
  "domain_name": "",
  "environment": "production",
  "exclude_patterns": [
    "terraform/*",
    "tests/*",
    "*.py",
    "*.md",
    "requirements.txt",
    ".git/*",
    "__pycache__/*",
    "*.pyc",
    ".env",
    "deploy_config.json"
  ]
}
```

### Custom Domain Setup

If using a custom domain:

1. Set `domain_name` in `deploy_config.json`
2. After deployment, update your domain's nameservers to the Route 53 nameservers (shown in deployment outputs)
3. Wait for DNS propagation (can take up to 48 hours)

## 🎨 Customization

### Content Updates

1. **Personal Information**: Edit `index.html`
   - Update name, title, and bio in the hero and about sections
   - Add your skills, projects, and experience

2. **Styling**: Modify `css/style.css`
   - Change colors in the `:root` CSS variables
   - Adjust fonts, spacing, and animations

3. **Functionality**: Update `js/main.js`
   - Add new interactive features
   - Modify animations and behaviors

### Adding New Sections

1. Add HTML structure in `index.html`
2. Add corresponding styles in `css/style.css`
3. Add any interactive functionality in `js/main.js`
4. Run tests to ensure everything works: `python manage.py test`

## 🔧 Development Workflow

### Development Server

The built-in development server provides:
- **Live reload** on file changes
- **Hot CSS/JS reloading** without page refresh
- **Automatic browser opening**
- **Cross-platform compatibility**

```bash
# Start development server
python manage.py dev

# Custom host and port
python manage.py dev --host 0.0.0.0 --port 3000

# Disable live reload
python manage.py dev --no-reload

# Don't open browser automatically
python manage.py dev --no-browser
```

### Testing Workflow

```bash
# Run all tests
python manage.py test

# Run with coverage report
python manage.py test --coverage

# Generate HTML test report
python manage.py test --html

# Run specific test categories
pytest tests/ -m "not slow"  # Skip slow tests
pytest tests/ -m "accessibility"  # Only accessibility tests
```

### Build Process

```bash
# Build for production
python manage.py build

# Build to custom directory
python manage.py build --build dist-custom

# Clean and build
python manage.py clean && python manage.py build
```

### File Structure

```
personal-website/
├── index.html                    # Main HTML file
├── css/
│   └── style.css                # Styles and animations
├── js/
│   └── main.js                  # Interactive functionality
├── terraform/                   # Infrastructure as Code
│   ├── main.tf                  # Main Terraform configuration
│   ├── variables.tf             # Variable definitions
│   ├── outputs.tf               # Output values
│   └── terraform.tfvars.example # Configuration template
├── tests/                       # Test suite
│   ├── test_website.py          # Website tests
│   └── reports/                 # Test reports
├── dist/                        # Production build output
├── venv/                        # Python virtual environment
├── manage.py                    # Project management CLI
├── setup.py                     # Project setup script
├── deploy.py                    # AWS deployment script
├── dev_server.py                # Development server
├── build.py                     # Build and optimization
├── requirements.txt             # Python dependencies
├── pytest.ini                  # Test configuration
├── .env                         # Environment variables
└── README.md                    # This file
```

## 📊 Monitoring and Maintenance

### AWS CloudWatch

Monitor your website performance:
- CloudFront metrics
- S3 access logs
- Error rates and response times

### Updates

To update your website:

1. **Content Changes**: 
   ```powershell
   aws s3 sync . s3://your-bucket-name --exclude "terraform/*"
   ```

2. **Infrastructure Changes**:
   ```powershell
   cd terraform
   terraform plan
   terraform apply
   ```

3. **Cache Invalidation** (if needed):
   ```powershell
   aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"
   ```

## 💰 Cost Estimation

Typical monthly costs (US East):
- **S3**: ~$1-5 (depending on traffic)
- **CloudFront**: ~$1-10 (first 1TB free)
- **Route 53**: ~$0.50 per hosted zone
- **ACM**: Free for AWS resources

## 🔒 Security

- HTTPS enforced via CloudFront
- S3 bucket configured with proper access policies
- No sensitive data exposed in frontend code

## 🆘 Troubleshooting

### Common Issues

1. **Bucket name already exists**: Choose a more unique bucket name
2. **Domain validation fails**: Check DNS settings and wait for propagation
3. **403 Forbidden**: Verify S3 bucket policy and public access settings

### Useful Commands

```powershell
# Check Terraform state
terraform show

# View outputs
terraform output

# Validate configuration
terraform validate

# Format code
terraform fmt
```

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Feel free to fork this project and customize it for your own use!

---

**Built with ❤️ by Edson da Silva**

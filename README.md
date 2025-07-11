# PenzFlow - ERP & SFA System

PenzFlow is a comprehensive Enterprise Resource Planning (ERP) and Sales Force Automation (SFA) system built with Python and Streamlit. It provides a modern, web-based interface for managing customers, products, inventory, sales, and generating insightful reports for your business.

## Features

### 🏢 Core ERP Modules
- **Dashboard**: Real-time business metrics and analytics
- **Customer Management**: Complete customer relationship management
- **Product Management**: Inventory and product catalog management
- **Sales Management**: Order processing and sales tracking
- **Inventory Control**: Stock management with automatic alerts
- **Reports & Analytics**: Comprehensive business intelligence
- **User Management**: Role-based access control

### 📊 Key Capabilities
- Interactive dashboards with real-time charts
- Customer relationship tracking
- Product catalog and inventory management
- Sales order processing
- Inventory alerts and stock management
- Financial reporting and analytics
- Multi-user support with role-based permissions
- Data export capabilities (CSV, Excel)

## Project Structure

```
PenzFlow/
├── src/
│   ├── main.py                 # Main Streamlit application
│   ├── database/
│   │   └── init_db.py         # Database initialization and schema
│   └── utils/
│       ├── auth.py            # Authentication utilities
│       └── helpers.py         # Helper functions and utilities
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── data/                      # Database and data files (auto-created)
├── requirements.txt           # Python dependencies
├── config.py                  # Application configuration
└── README.md                  # Project documentation
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/PenzFlow.git
   cd PenzFlow
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   streamlit run src/main.py
   ```

5. **Access the application:**
   Open your web browser and navigate to `http://localhost:8501`

## Default Login Credentials

- **Admin User**: username: `admin`, password: `admin123`
- **Demo User**: username: `demo`, password: `demo`

## Usage Guide

### Getting Started
1. Start the application using the setup instructions above
2. Login using the default credentials or create a new account
3. Explore the different modules from the sidebar navigation

### Key Modules

#### 📈 Dashboard
- View key business metrics at a glance
- Monitor sales trends and performance
- Track inventory levels and alerts
- Visualize customer data and analytics

#### 👥 Customer Management
- Add, edit, and manage customer information
- Track customer purchase history
- Manage customer communications
- Export customer data for analysis

#### 📦 Product Management
- Maintain product catalog
- Set pricing and cost information
- Track product categories and suppliers
- Monitor stock levels and reorder points

#### 💰 Sales Management
- Create and process sales orders
- Track order status and fulfillment
- Manage payment methods and terms
- Generate sales reports

#### 📊 Inventory Control
- Monitor stock levels in real-time
- Set automatic reorder alerts
- Track inventory movements
- Manage suppliers and purchase orders

#### 📋 Reports & Analytics
- Generate comprehensive business reports
- Analyze sales performance trends
- Monitor inventory turnover
- Export data in multiple formats

## Configuration

### Database
- The application uses SQLite database by default
- Database file is automatically created in the `data/` directory
- Sample data is populated on first run

### Customization
- Modify `config.py` for application settings
- Update `.streamlit/config.toml` for UI customization
- Add custom business logic in respective modules

## Technical Details

### Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python 3.8+
- **Database**: SQLite (easily upgradeable to PostgreSQL/MySQL)
- **Charts**: Plotly and Altair for interactive visualizations
- **Data Processing**: Pandas for data manipulation

### Architecture
- **Modular Design**: Separated concerns with dedicated modules
- **MVC Pattern**: Clean separation of data, logic, and presentation
- **Session Management**: Secure user sessions with role-based access
- **Database ORM**: Direct SQL with connection pooling

### Security Features
- User authentication and authorization
- Role-based access control
- Session timeout management
- Input validation and sanitization

## Development

### Adding New Features
1. Create new functions in the appropriate module
2. Add database schema changes in `database/init_db.py`
3. Update the main navigation in `main.py`
4. Test thoroughly before deployment

### Database Schema
The application uses the following main tables:
- `users`: User accounts and authentication
- `customers`: Customer information and contacts
- `products`: Product catalog and inventory
- `sales_orders`: Sales transactions and orders
- `order_items`: Line items for each order
- `inventory_transactions`: Inventory movement tracking

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes and commit (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## Deployment

### Production Deployment
1. Set environment variables for production
2. Update database configuration for production database
3. Configure SSL certificates
4. Set up reverse proxy (nginx/Apache)
5. Use process manager (PM2/supervisor)

### Docker Deployment
```bash
# Build Docker image
docker build -t penzflow .

# Run container
docker run -p 8501:8501 penzflow
```

## Support

### Troubleshooting
- Check Python version compatibility
- Verify all dependencies are installed
- Ensure database permissions are correct
- Check firewall settings for port 8501

### Getting Help
- Create an issue on GitHub for bugs
- Check documentation for common questions
- Review logs in the application for errors

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Built with Streamlit framework
- Uses Plotly for interactive visualizations
- Inspired by modern ERP and CRM systems
- Thanks to the open-source community for tools and libraries
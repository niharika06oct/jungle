# Jungle - Sustainable E-commerce Platform

Jungle is an eco-friendly e-commerce platform that connects conscious consumers with sustainable products. From biodegradable essentials to bamboo alternatives, we make sustainable living accessible and convenient.

## Features

### Web Platform
- Sustainable product marketplace
- Category-based browsing (Home & Living, Personal Care, Kitchen & Dining)
- Shopping cart functionality
- Product recommendations
- New arrivals section
- Responsive design with modern UI

### Android App
- Native Android application with embedded Flask server
- Beautiful bamboo-themed interface
- Seamless shopping experience on mobile
- Category-based product browsing
- Responsive and intuitive UI

## Design

- **Color Palette**:
  - Deep forest green (#2F4538)
  - Sage green (#5C7C64)
  - Soft moss green (#A4BE7B)
  - Off-white with green tint (#F5F7F2)
  - Light sage highlights (#DAE5D0)
  - Muted green text (#6B8E7B)

- **UI Elements**:
  - Custom leaf icon
  - Gradient backgrounds
  - Sophisticated shadows and depth effects
  - Enhanced card designs with subtle borders
  - Modern typography with Poppins font family

## Tech Stack

### Web Platform
- Backend: Python/Flask
- Database: SQLAlchemy
- Frontend: HTML5, CSS3, JavaScript
- Styling: Custom CSS with responsive design

### Android App
- Android Native (Java)
- Chaquopy for Python integration
- WebView for UI rendering
- Embedded Flask server
- Custom Android resources and layouts

## Setup Instructions

### Web Platform

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the application:
```bash
flask run
```

### Android App

1. Open the project in Android Studio
2. Install required Android SDK components
3. Build the project:
```bash
cd JungleAndroid
./gradlew assembleDebug
```

## Project Structure

```
jungle/
├── app/                    # Web application
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── static/
│   └── templates/
├── JungleAndroid/         # Android application
│   ├── app/
│   │   ├── src/
│   │   │   ├── main/
│   │   │   │   ├── java/
│   │   │   │   ├── python/
│   │   │   │   └── res/
│   │   └── build.gradle
│   ├── gradle/
│   └── build.gradle
├── config.py
├── requirements.txt
└── run.py
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

# Django URL Shortener

A modern, responsive URL shortening web application built with Django.

## Features

- Shorten long URLs to easy-to-share short links
- User registration and login
- Dashboard to manage your URLs
- View statistics for each short URL (clicks, expiration, etc.)
- Responsive, modern UI (Bootstrap-based)
- Custom branding and styles

## Project Structure

```
URL Shortner/
│
├── requirements.txt
├── urlshortener_project/
│   ├── README.md
│   ├── media/
│   ├── db.sqlite3
│   ├── manage.py
│   ├── shortener/
│   │   ├── migrations/
│   │   ├── templates/
│   │   ├── static/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   └── ...
│   └── urlshortener_project/
│       ├── settings.py
│       ├── urls.py
│       └── ...
└── ...
```

## Setup Instructions

1. Clone the repository
   git clone https://github.com/ManirajKatuwal/urlshortner.git
   cd URL Shortner

2. Install dependencies
   pip install -r requirements.txt

3. Apply migrations
   python urlshortener_project/manage.py migrate
   
4. Run the development server
   python urlshortener_project/manage.py runserver
   

5. Access the app
   Open your browser and go to `http://127.0.0.1:8000/`

## Customization

- UI styles are in `static/style.css`
- Templates are in `shortener/templates/shortener/`
- Update branding, colors, and layout as needed

## License

This project is licensed under the MIT License.

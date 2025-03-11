# KhaoChan: Thailand News In Short

KhaoChan is a Django-based web application that provides quick, bite-sized summaries of Thai news. Each summary is a concise (around 30-word) digest of the original article, making it easy for busy expats, locals, and travelers to stay updated on Thailand's current events without reading lengthy articles.

## Features

- **Concise News Summaries:** Quick overviews that distill each article into approximately 30 words.
- **Responsive Design:** A clean, mobile-friendly UI for easy reading on any device.
- **Admin Panel Integration:** Use Django's built-in admin to easily manage and update news items.
- **Direct Source Linking:** Each summary includes a link to the full article on the original publication.

## Tech Stack

- **Backend:** Python and Django
- **Database:** SQLite for development (upgrade to PostgreSQL in production)
- **Frontend:** Django Templates with a CSS framework (Bootstrap or Tailwind CSS recommended)
- **Hosting:** Deployable on low-cost VPS services (e.g., DigitalOcean, Linode, Hetzner)

## Getting Started

Follow these instructions to set up a local development environment.

### Prerequisites

- Python 3.x
- Git (optional, but recommended for version control)
- Virtual Environment tool (e.g., `venv`)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/khaochan.git
   cd khaochan
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
    # Activate on macOS/Linux:
    source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install django
   ```
4. **Apply migrations:**
   ```bash
   python manage.py makemigrations
    python manage.py migrate
   ``` 
5. **Create a superuser for the admin panel:**
   ```bash
   python manage.py createsuperuser
   ```
6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
   
### Usage

- Admin Interface: Log in at http://127.0.0.1:8000/admin/ to add, edit, or remove news items.
- Home Page: Displays the latest news summaries in a simple card layout with direct links to the original articles.

### Future Enhancements

- Automated News Aggregation: Integrate web scraping and AI-based summarization for automated content updates.
- Multi-language Support: Enable toggling between Thai and English summaries.
- Notifications: Add push notifications or email newsletters for daily updates.

### Contributing

Contributions are welcome! If you’d like to help improve KhaoChan, please fork the repository and submit a pull request. For major changes, open an issue first to discuss your ideas.

### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Acknowledgements

- Inspired by the concept of quick news updates similar to InShorts.
- Thanks to the Django community for providing a robust framework.
- Special thanks to all contributors and supporters.

This project is a work in progress. Feedback and suggestions are greatly appreciated!

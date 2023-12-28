# Sweet Lemons Bakery

Sweet Lemons Bakery is a Flask-based web application for managing a bakery's product catalog, custom cake orders, and class registrations. Users can explore and order products, customize cake orders, and sign up for baking classes.

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/sweetlemons-backend.git
   
2. install dependencies 

         pip install -r requirements.txt
3. Set up the database:

         flask db init
         flask db migrate
         flask db upgrade

4. Run the application:
         
         python main.py

5. Open your browser and go to http://localhost:5000 to access the application
6. Project Structure
   1. main.py: The main Flask application file.
   2. static/: Static files, including images and stylesheets.
   3. templates/: HTML templates for rendering pages.
   4. forms.py: Form classes for user input validation.
   5. README.md: Project documentation.
   6. requirements.txt: List of Python dependencies.

7. Features
   1. Product Management: Add, view, and manage bakery products.
   2. Custom Cake Orders: Allow users to customize cake orders with specific details.
   3. Baking Class Registration: Users can sign up for baking classes.

8. File Uploads
   1. Uploaded files are stored in the static/uploads directory.
   2. Images are stored in the database as base64-encoded binary data.

9. Database
   SQLite is used as the database backend.
   

10. Configuration: Set environment variables for email and password in app.py to enable email functionality.

my_Email = "your-email@gmail.com"
my_Password = "your-email-password"


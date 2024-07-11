## Create a Versatile Photo Collection App with Django

### Setup Instructions 

#### Prerequisites

* Python 3.8+
* Django 3.1+
* Cloudinary account

#### Installation

1.  Fork and clone the repository:

```python
git clone https://github.com/yourusername/lookbook.git
cd lookbook
```

2. Create and activate a virtual environment:

```python
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:

```python
pip install -r requirements.txt
```

4. Configure Cloudinary:
   1. Sign up at [Cloudinary](http://cloudinary.com/ip/sy) 
   2. Create a `.env` file in the project root and add the following. 
   3. Update the `.env` file with your Cloudinary credentials:
      1. Copy the API environment variable format from the [API Keys](https://console.cloudinary.com/settings/api-keys) page and paste it into your `.env` file. 
      2. Replace <your_api_key> and <your_api_secret> with your actual values, while your cloud name is already correctly included in the format. 
      3. Add the following code in your `settings.py` file:
   
        ```python
        from dotenv import load_dotenv
        load_dotenv()
        ```
        

5. Apply migrations and start the server:
   
   ```python
   python manage.py migrate
   python manage.py runserver
   ```

6. Access the application at `http://127.0.0.1:8000`.

## Contributing

1. Fork the repository.
2. Create your feature branch (git checkout -b feature/your-feature).
3. Commit your changes (git commit -m 'Add some feature').
4. Push to the branch (git push origin feature/your-feature).
5. Open a pull request.

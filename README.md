# Chatbot for WordPress Websites
This project provides a chatbot that interacts with WordPress websites. The chatbot uses a Flask backend to handle API requests and a Streamlit frontend for user interactions.

## Project Structure
The project is divided into two main parts:

### Backend (Flask): The Flask app (app.py) serves as the backend for handling API requests and interacting with the WordPress site.
### Frontend (Streamlit): The Streamlit app (frontend.py) provides the user interface where users can ask questions to the chatbot.
Folder Structure:
my-chatbot-project/
│
├── app.py            # Flask backend for API
├── frontend.py       # Streamlit frontend for chatbot interface
├── requirements.txt  # Python dependencies
└── README.md         # Project documentation


## Prerequisites
Before running the project, make sure you have the following installed on your system:

Python 3.7 or higher
pip (Python package manager)
## Setup Instructions
### 1. Clone the Repository
First, clone the project repository to your local machine:

```bash
git clone https://github.com/your-username/my-chatbot-project.git
cd my-chatbot-project
```

### 2. Set up a Virtual Environment
It is recommended to create a virtual environment to manage dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
Install the required Python libraries using pip:

```bash
pip install -r requirements.txt
The requirements.txt file should contain all necessary dependencies. Here’s an example requirements.txt:
```

```makefile
Flask==2.1.1
streamlit==1.12.0
requests==2.26.0
pandas==1.3.3

```
### 4. Configure API Endpoints (Optional)
If your chatbot interacts with a WordPress site, you might need to configure the API endpoint for WordPress in your Flask app.

In app.py, update the relevant sections to point to your WordPress API endpoint. For example, if you have a WordPress site hosted at https://your-wordpress-site.com, make sure the API endpoint is correctly set.

### 5. Run the Flask Backend (app.py)
To run the Flask backend, use the following command:

```bash
python app.py
This will start the Flask server, which will handle API requests.

The Flask app will be available at http://localhost:5000 by default.
```
### 6. Run the Streamlit Frontend (frontend.py)
In a new terminal window, run the Streamlit frontend with the following command:

```bash
streamlit run frontend.py
This will start a local server for the Streamlit app.
By default, Streamlit will open your default web browser and load the chatbot interface at http://localhost:8501.
```
### 7. Interact with the Chatbot
Once both the Flask backend and the Streamlit frontend are running, you can interact with the chatbot through the Streamlit app:

Open your web browser and go to http://localhost:8501.
Type your question in the input box and the bot will respond with relevant information.
Project Configuration
Flask (app.py)
The Flask app exposes an API that the Streamlit frontend communicates with. The app processes incoming queries, retrieves relevant data from WordPress or other sources, and sends back a response.

Streamlit (frontend.py)
The Streamlit app is a simple frontend for user interaction. It allows users to input questions and receive responses from the backend API.

Example Usage
Start Flask Backend:
```bash
python app.py
Start Streamlit Frontend:
```
```bash
streamlit run frontend.py
Open http://localhost:8501 in your web browser to interact with the chatbot.
```
Example Query:
#### User: "Who is Dave Raggio?"
#### Bot: "Dave Raggio is a TikTok personality known for his comedic sketches and lip-syncing videos."
#### Additional Features
The chatbot can be customized to fetch information from different WordPress websites by adding additional endpoints.
The Flask app can be extended to handle more complex queries or fetch additional data from other sources.
Troubleshooting
If you face issues with dependencies, try updating pip and reinstalling the requirements:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```
If you encounter issues with the Streamlit app not loading properly, make sure that the backend server (app.py) is running before starting Streamlit.


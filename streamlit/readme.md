# Real Estate Data Engineer Streamlit App

This is a Streamlit application used to visualize data from the `real_estate_db` PostgreSQL database.

## Database Setup

Before running the Streamlit app, make sure to start the necessary services (PostgreSQL, etc.) using Docker:

1. Navigate to the `Docker` directory:

   ```bash
   cd ../Docker
   ```

2. Start the services:

   ```bash
   docker compose up
   ```

   (Or `docker-compose up` if using the older version)

3. Return to the `streamlit` directory to run the app.

## Installation

1. Navigate to the `streamlit` directory:

   ```bash
   cd streamlit
   ```

2. (Optional but recommended) Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

To run the Streamlit application, execute the following command:

```bash
streamlit run app.py
```

The application will open in your default browser (usually at `http://localhost:8501`).

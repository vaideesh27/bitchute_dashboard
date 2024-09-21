# BitChute Analytics Dashboard

## Summary

The BitChute Analytics Dashboard is a web application designed to provide insights into video and channel performance on BitChute. It utilizes data scraping to gather metrics such as views, likes, dislikes, comments, and trends over time. The app leverages a SQLite database for data storage, making it easy to track changes and visualize analytics in real time.

## Features

- **Video Analytics**: Detailed insights into individual video performance, including views, likes, dislikes, and comments.
- **Channel Overview**: Aggregate metrics for channels, displaying total views, likes, dislikes, and comments.
- **Trends Visualization**: Interactive charts for viewing trends over selected date ranges.
- **Information Integrity**: Simulated integrity score to assess information integrity of videos.

## Installation Instructions

### Prerequisites

- Python 3.7 or higher
- SQLite (included with Python)
- Chrome browser (for Selenium WebDriver)

### Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/bitchute-analytics-dashboard.git
   cd bitchute-analytics-dashboard
   ```

2. **Create a Virtual Environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Required Packages**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Backend Application**:
   Start the Bitchute - Web Scraping app using:

   ```bash
   python3 main.py
   ```

5. **Run the Frontend Application**:
   Start the Streamlit app using:

   ```bash
   streamlit run app.py
   ```

6. **Access the Dashboard**:
   Open your web browser and navigate to `http://localhost:8501`.

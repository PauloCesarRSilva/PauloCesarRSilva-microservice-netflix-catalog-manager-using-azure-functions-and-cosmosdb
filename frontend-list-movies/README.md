# Streamlit Video App

This project is a Streamlit application that displays video cards populated from an API. Users can click on the cards to play the videos in a new window or modal.

## Project Structure

```
streamlit-video-app
├── src
│   ├── app.py               # Main entry point of the Streamlit application
│   ├── components
│   │   └── card.py          # Component for rendering video cards
│   └── utils
│       └── api.py           # Utility functions for API calls
├── requirements.txt          # Project dependencies
└── README.md                 # Documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd streamlit-video-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the Streamlit application, execute the following command in your terminal:
```
streamlit run src/app.py
```

Open your web browser and navigate to `http://localhost:8501` to view the application.

## Features

- Displays video cards with titles and thumbnails.
- Fetches video data from an external API.
- Allows users to play videos by clicking on the cards.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.
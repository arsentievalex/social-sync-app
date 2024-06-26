# SocialSync: YouTube to Social Media Content Generator

Welcome to SocialSync! This Streamlit app uses a novel Snowflake Arctic LLM to generate social media posts for LinkedIn, Twitter (X), and Instagram based on YouTube video content.

## Features

- **LinkedIn Post Generation:** Creates professional LinkedIn posts with key takeaways from the video.
- **Twitter (X) Thread Generation:** Generates engaging Twitter threads with multiple tweets.
- **Instagram Post Generation:** Produces short, casual Instagram posts.
- **Regeneration Option:** Allows users to regenerate posts if needed.

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/arsentievalex/social-sync-app.git
    cd socialsync
    ```

2. **Install Dependencies:**

    Ensure you have Python 3.8+ installed. Then, install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. **Add Configuration:**

    Create a `config.yaml` file in the root directory and add your configuration settings.


## Usage

1. **Run the Streamlit App:**

    ```bash
    streamlit run app.py
    ```

2. **Open the App in Your Browser:**

    The app will automatically open in your default web browser. If not, navigate to `http://localhost:8501`.

3. **Generate Social Media Content:**

    - Enter your Replicate API Token in the sidebar.
    - Input the YouTube video URL.
    - Click the "Generate content" button.
    - The app will display the generated LinkedIn post, Twitter thread, and Instagram post in respective columns.
    - Use the "Re-generate 🔄" button to regenerate content if needed.


## Contributing

All contributions are welcome. Please fork the repository and create a pull request with your changes.

## Contact

If you have any questions or feedback, please feel free to reach out to me at [arsentiev9393@gmail.com](mailto:arsentiev9393@gmail.com).

---


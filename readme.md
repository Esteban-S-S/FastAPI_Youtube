# YouTube Data API FastAPI Application

This FastAPI application interacts with the YouTube Data API to retrieve information about YouTube channels and videos. It exposes three endpoints to get data:

1. **Get Channel Data (`/get_channel_data`):**
   - **Input:** YouTube channel URL.
   - **Output:** Information about the specified YouTube channel, including title, custom URL, channel ID URL, description, subscriber count, video count, and general view count.

2. **Get Video Data (`/get_video_data`):**
   - **Input:** YouTube video URL.
   - **Output:** Information about the specified YouTube video, including URL, title, published date, description, view count, comment count, like count, category, and the date of consultation.

3. **Get Channel Videos (`/get_channel_videos`):**
   - **Input:** YouTube channel URL.
   - **Output:** Information about all videos on the specified YouTube channel. This includes URL, title, published date, description, view count, comment count, like count, category, and the date of consultation for each video.

## How to Run

1. Install the required dependencies:

   ```bash
   pip install fastapi uvicorn google-api-python-client
   ```

2. Replace the placeholder `API_KEY` in the code with your actual YouTube Data API key.

3. Run the FastAPI application using the following command:

   ```bash
   uvicorn your_file_name:app --reload
   ```

   Replace `your_file_name` with the name of the Python file containing the code.

4. Open your browser and go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to access the Swagger documentation. You can use the interactive documentation to test the different endpoints.

## Important Note

- Ensure that you have a valid YouTube Data API key (`API_KEY`) and that the necessary API services are enabled in your Google Cloud Console.

- The YouTube Data API has usage limits. Be mindful of these limits. 

- This application assumes that the provided URLs are valid YouTube channel and video URLs.

Feel free to customize and extend the application as needed for your use case.
from embedchain import App
import os
import streamlit as st
import time


@st.cache_resource(show_spinner=False)
def load_data(url):
    bot = App.from_config(config_path="config.yaml")
    bot.add(url, data_type='youtube_video')
    return bot


def write_linkedin(app, source_url):

    linkedin_guidance = f"""
    LinkedIn Post Guidance:
    Start with a catchy sentence that grabs the reader's attention.
    Keep professional tone and avoid slang or cliches.
    Keep it concise: Aim for 1-3 paragraphs.
    Use "\n" to separate paragraphs.
    Use short paragraphs and bullet points to make the post easy to read.
    You can use emojis, but don’t overdo it.
    Include a Call to Action: Encourage readers to engage with your post.
    In the end, mention the video URL: {source_url}
    Choose relevant hashtags, but don’t overdo it: maximum 3 hashtags.
    
    The post should be significantly different from all the previous posts. Here are the previous posts:
    {st.session_state['linkedin_post']}
    """

    response = app.query(f"Write a LinkedIn post with key takeaways from this video. Use the following guidance: {linkedin_guidance}")

    for chunk in response:
        yield chunk


def write_x(app, source_url):

    x_guidance = f"""
    Twitter Thread Guidance:
    In the first tweet, make it clear what the thread is about, and that there are multiple tweets on this topic.
    Keep casual tone and use emojis.
    Keep it concise: Aim for 3-5 tweets.
    Each tweet should be a standalone point and provide value.
    Be personal and use phrases like "I think", "I believe" or "I learned".
    In the last tweet, suggest following me for more content.
    Start each tweet with "Tweet #1", "Tweet #2", etc.
    In the last tweet of the thread, mention the video URL: {source_url}
    Reset the numbering for each new thread.
    Use "\n" to separate tweets.
    
    The tweets should be significantly different from all the previous tweets. Here are the previous tweets:
    {st.session_state['twitter_thread']}
    """

    response = app.query(f"Write a Twitter thread with key takeaways from this video. Use the following guidance: {x_guidance}")

    for chunk in response:
        yield chunk


def write_instagram(app, source_url):

    instagram_guidance = f"""
    Instagram Post Guidance:
    Be very brief: Aim for 3-4 short sentences.
    Use a casual tone and emojis.
    Be personal and share your thoughts or feelings about the video.
    Include a call to action to engage your followers.
    In the end, mention the video URL: {source_url}
    Use "\n" to separate ideas.
    Use a few relevant hashtags, but don’t overdo it.
    
    The instagram post should be significantly different from all the previous posts. Here are the previous posts:
    {st.session_state['instagram_post']}
    
    """

    response = app.query(f"Write an Instagram post content with key takeaways from this video. Use the following guidance: {instagram_guidance}")

    for chunk in response:
        yield chunk


@st.experimental_fragment
def linkedin_fragment(app, placeholder, source_url):
    l_full_response = st.write_stream(write_linkedin(app, source_url))
    st.session_state['instagram_post'].append(l_full_response)

    with placeholder:
        # check if button already exists
        if 'regenerate_l_button' not in st.session_state:
            st.button("Re-generate 🔄", key="regenerate_l_button")


@st.experimental_fragment
def twitter_fragment(app, placeholder, source_url):
    x_full_response = st.write_stream(write_x(app, source_url))
    st.session_state['instagram_post'].append(x_full_response)

    with placeholder:
        # check if button already exists
        if 'regenerate_x_button' not in st.session_state:
            st.button("Re-generate 🔄", key="regenerate_x_button")


@st.experimental_fragment
def instagram_fragment(app, placeholder, source_url):
    ig_full_response = st.write_stream(write_instagram(app, source_url))
    st.session_state['instagram_post'].append(ig_full_response)

    with placeholder:
        # check if button already exists
        if 'regenerate_ig_button' not in st.session_state:
            st.button("Re-generate 🔄", key="regenerate_ig_button")


def main():

    st.set_page_config(layout="wide")

    if 'linkedin_post' not in st.session_state:
        st.session_state['linkedin_post'] = []
    if 'twitter_thread' not in st.session_state:
        st.session_state['twitter_thread'] = []
    if 'instagram_post' not in st.session_state:
        st.session_state['instagram_post'] = []

    col5, col6 = st.columns(2, gap='large')

    with col5:
        st.title("SocialSync: YouTube to Social Media")
        st.header("Generate social media content from YouTube videos with AI")

    with col6:
        st.image("image.png", width=270)

    st.write('')
    st.write('')
    st.write('')

    col1, col2, col3 = st.columns(3, gap='medium')

    with col1:
        st.subheader("LinkedIn Post")
        button_placeholder1 = st.container()

    with col2:
        st.subheader("Twitter (X) Thread")
        button_placeholder2 = st.container()

    with col3:
        st.subheader("Instagram Post")
        button_placeholder3 = st.container()

    with st.sidebar:
        replicate_token = st.text_input("Your Replicate API Token", type="password", value=st.secrets["replicate_credentials"]["TOKEN"])
        yt_url = st.text_input("Enter YouTube URL")
        run_button = st.button('Generate content')

        if yt_url:
            st.video(yt_url)

        html_code = """
        <p style='color:#249EDC; font-weight: bold;'>Powered by Snowflake Arctic ❄</p>
        """
        st.markdown(html_code, unsafe_allow_html=True)

    if run_button:
        if not replicate_token:
            st.warning("Please enter your Replicate API Token!")
        
        elif not yt_url:
            st.warning("Please insert YouTube URL!")
            os.environ['REPLICATE_API_TOKEN'] = replicate_token
            
        else:
            app = load_data(yt_url)
    
            with col1:
                linkedin_fragment(app, button_placeholder1, source_url=yt_url)
    
            with col2:
                twitter_fragment(app, button_placeholder2, source_url=yt_url)
    
            with col3:
                instagram_fragment(app, button_placeholder3, source_url=yt_url)


if __name__ == "__main__":
    main()



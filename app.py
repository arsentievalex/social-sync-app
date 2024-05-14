from embedchain import App
import os
import streamlit as st
import time


# Function to modify the output by adding spaces between each word with a delay
def modify_output(input):
    # Iterate over each line in the input string to preserve line breaks
    for line in input.split('\n'):
        # Split the line by spaces to get words, and process each word
        for word in line.split():
            # Yield the word with an added space
            yield word + " "
            # Introduce a small delay between each word
            time.sleep(0.05)
        # After finishing a line, yield a line break
        yield '\n'


@st.cache_resource(show_spinner=False)
def load_data(url):
    bot = App.from_config(config_path="config.yaml")
    bot.add(url, data_type='youtube_video')
    return bot


def write_linkedin(app):

    linkedin_guidance = f"""
    LinkedIn Post Guidance:
    Start with a catchy sentence that grabs the reader's attention.
    Keep professional tone and avoid slang or cliches.
    Keep it concise: Aim for 1-3 paragraphs.
    Use "\n" to separate paragraphs.
    Structure the post: Use short paragraphs and bullet points to make the post easy to read.
    You can use emojis, but don’t overdo it.
    Include a Call to Action: Encourage readers to engage with your post.
    Choose relevant hashtags, but don’t overdo it: maximum 3 hashtags.
    
    The post should be significantly different from all the previous posts. Here are the previous posts:
    {st.session_state['linkedin_post']}
    """

    response = app.chat(f"Write a LinkedIn post with key takeaways from this video. Use the following guidance: {linkedin_guidance}")

    # update session state
    st.session_state['linkedin_post'].append(response)

    return modify_output(response)


def write_x(app):

    x_guidance = f"""
    Twitter Thread Guidance:
    Start with a catchy headline that grabs the reader's attention.
    In the first tweet, make it clear what the thread is about, and that there are multiple tweets on this topic.
    Keep casual tone and use emojis.
    Keep it concise: Aim for 3-5 tweets.
    Each tweet should be a standalone point and provide value.
    Be personal and use phrases like "I think", "I believe" or "I learned".
    In the last tweet, suggest following me for more content.
    Start each tweet with "Tweet #1", "Tweet #2", etc.
    Reset the numbering for each new thread.
    Use "\n" to separate tweets.
    
    The tweets should be significantly different from all the previous tweets. Here are the previous tweets:
    {st.session_state['twitter_thread']}
    """

    response = app.chat(f"Write a Twitter thread with key takeaways from this video. Use the following guidance: {x_guidance}")

    # update session state
    st.session_state['twitter_thread'].append(response)

    return modify_output(response)


def write_instagram(app):

    instagram_guidance = """
    Instagram Post Guidance:
    Be very brief: Aim for 3-4 short sentences.
    Use a casual tone and emojis.
    Be personal and share your thoughts or feelings about the video.
    Include a call to action to engage your followers.
    Use a few relevant hashtags, but don’t overdo it.
    """

    response = app.chat(f"Write a Twitter thread with key takeaways from this video. Use the following guidance: {instagram_guidance}")

    # update session state
    st.session_state['instagram_post'].append(response)

    return modify_output(response)


@st.experimental_fragment
def linkedind_fragment(app, placeholder):
    st.write_stream(write_linkedin(app))

    with placeholder:
        # check if button already exists
        if 'regenerate_l_button' not in st.session_state:
            st.button("Re-generate 🔄", key="regenerate_l_button")


@st.experimental_fragment
def twitter_fragment(app, placeholder):
    st.write_stream(write_x(app))

    with placeholder:
        # check if button already exists
        if 'regenerate_x_button' not in st.session_state:
            st.button("Re-generate 🔄", key="regenerate_x_button")


@st.experimental_fragment
def instagram_fragment(app, placeholder):
    st.write_stream(write_instagram(app))

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
        st.image("Untitled design (6).png", width=270)

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
        replicate_token = st.text_input("Your Replicate API Token", type="password")
        yt_url = st.text_input("Enter YouTube URL", value='https://www.youtube.com/watch?v=-ZagrEDUnHQ')
        run_button = st.button('Generate content')

        if yt_url:
            st.video(yt_url)

    if run_button:
        app = load_data(yt_url)

        with col1:
            linkedind_fragment(app, button_placeholder1)

        with col2:
            twitter_fragment(app, button_placeholder2)

        with col3:
            instagram_fragment(app, button_placeholder3)


if __name__ == "__main__":
    main()












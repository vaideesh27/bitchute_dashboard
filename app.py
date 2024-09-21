import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

def page_layout():
    st.set_page_config(page_title="Bitchute Analytics Dashboard", layout="wide")
    st.sidebar.write("Home")
    st.sidebar.page_link("app.py", label="Home", icon=":material/home:", use_container_width=True)
    st.sidebar.write("Dashboard")
    st.sidebar.page_link("pages/dashboard.py", label="Dashboard", icon=":material/dashboard:", use_container_width=True)
    st.title("Bitchute Analytics Dashboard")
    st.header("Introduction")
    st.write("As online platforms grow in influence, understanding how misinformation spreads and how users engage with such content is crucial. This system analyzes user engagement patterns on BitChute, focusing on how information integrity influences user interaction (views, likes, dislikes, and comments) and using various graphs and metrics, it shows the  trends in misinformation dynamics.")
    st.header("Application Use Case")
    st.write("Content Analysis: The graphs generated help identifying patterns around how engagement (views, likes, comments, dislikes) correlates with information  integrity.")
    st.write("Misinformation Detection: The graphs generated help users to detect whether low information integrity content is attracting more engagement, which may be important in flagging or managing misinformation.")
    st.header("Additional Information")
    st.write("The integrity of information in a video can be assessed by analyzing its audio, comments, and converting them to text. This text can then be further analyzed using parameters such as relevant articles and credible sources to determine the video's integrity score. To manage the large volume of videos on the platform, focus can be placed on critical topics that are more likely to have significant real-world impact. This ensures that important topics are prioritized, guiding users to content with high information integrity.")
    st.write("For example, when a user visits the platform and searches for a video, they will be shown pre-analyzed videos with information integrity scores. They can also view how the content aligns with information integrity through graphs. Additionally, they can track the trends of views, likes, dislikes, and comments over time for both videos and channels to understand how information spreads on the platform. Furthermore, users can see the reasoning behind the scores assigned to videos, ensuring transparency. This system helps users save time and access accurate information.")

page_layout()
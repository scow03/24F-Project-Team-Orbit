import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import numpy as np
import random
import time
from modules.nav import SideBarLinks

SideBarLinks()


st.title(f"Here are some potential mentees, {st.session_state['first_name']}.")

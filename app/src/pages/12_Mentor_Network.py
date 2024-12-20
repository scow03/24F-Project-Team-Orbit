import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
from PIL import Image, ImageDraw
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
from datetime import datetime

directory = 'assets/'
default = "assets/default.jpg"

st.set_page_config(layout='wide')

mentorId = 28

SideBarLinks()

def fetch_mentees(mentor_id):
    response = requests.get(f"http://web-api:4000/u/MentorMentees/{mentor_id}", params={"mentor_id": mentor_id})
    
    if response.status_code == 200:
        return response.json() 
    else:
        st.error(f"Error fetching mentees: Please Build Profile First{response.json().get('error')}")
        return []

def fetch_metrics(mentee_id):
    response = requests.get(f"http://web-api:4000/o/Metrics/{menteeId}")
    
    if response.status_code == 200:
       return response.json() 
    else:
        st.error(f"Error fetching metrics")
        return []
    
def fetch_application_data(mentee_id):
    response = requests.get(f"http://web-api:4000/c/ApplicationTotal/{menteeId}")
    
    if response.status_code == 200:
       return response.json() 
    else:
        st.error(f"Error fetching metrics")
        return []
    
def fetch_detailed_application_data(mentee_id):
    response = requests.get(f"http://web-api:4000/c/Applications/{menteeId}")
    
    if response.status_code == 200:
       return response.json() 
    else:
        st.error(f"Error fetching metrics")
        return []
    

# instead of hardcoding, use the max mentorID implementation
mentees = fetch_mentees(mentorId)

# x = np.linspace(0, 31)
# y = np.linspace(0, 30)

# fig, ax = plt.subplots()

# ax.plot(x, y) 
# st.pyplot(fig)

st.title(f"Your Network, {st.session_state['first_name']}.")
                
if mentees:
    for idx, mentee in enumerate(mentees):
        with st.container(border=True):
            if mentee["profilepic"] and "assets/" not in mentee["profilepic"]:
                    img_path = os.path.join(directory, mentee["profilepic"])
                    img = Image.open(img_path)
                    width, height = img.size
                    min_side = min(width, height)
                    left = (width - min_side) / 2
                    top = (height - min_side) / 2
                    right = (width + min_side) / 2
                    bottom = (height + min_side) / 2
                    img = img.crop((left, top, right, bottom))
                    
                    mask = Image.new("L", (min_side, min_side), 0)
                    draw = ImageDraw.Draw(mask)
                    draw.ellipse((0, 0, min_side, min_side), fill=255)
                    
                    img = img.resize((140, 140)) 
                    circular_img = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
                    circular_img.paste(img, (0, 0), mask.resize((140, 140)))
                    
                    st.image(circular_img)

                        # else:
                        #     st.write("No profile picture available.")
            elif "assets/" in mentee["profilepic"]:
                    img_path = mentee["profilepic"]
                    img = Image.open(img_path)
                    width, height = img.size
                    min_side = min(width, height)
                    left = (width - min_side) / 2
                    top = (height - min_side) / 2
                    right = (width + min_side) / 2
                    bottom = (height + min_side) / 2
                    img = img.crop((left, top, right, bottom))
                    
                    mask = Image.new("L", (min_side, min_side), 0)
                    draw = ImageDraw.Draw(mask)
                    draw.ellipse((0, 0, min_side, min_side), fill=255)
                    
                    img = img.resize((140, 140)) 
                    circular_img = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
                    circular_img.paste(img, (0, 0), mask.resize((140, 140)))
                    
                    st.image(circular_img)

                        # else:
                        #     st.write("No profile picture available.")
            else:
                    img = Image.open(default) 
                    width, height = img.size
                    min_side = min(width, height)
                    left = (width - min_side) / 2
                    top = (height - min_side) / 2
                    right = (width + min_side) / 2
                    bottom = (height + min_side) / 2
                    img = img.crop((left, top, right, bottom))
            
                    mask = Image.new("L", (min_side, min_side), 0)
                    draw = ImageDraw.Draw(mask)
                    draw.ellipse((0, 0, min_side, min_side), fill=255)


                    img = img.resize((140, 140)) 
                    circular_img = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
                    circular_img.paste(img, (0, 0), mask.resize((140, 140)))
            
                    st.image(circular_img)

            st.write(f"**Name**: {mentee['name']}")
            st.write(f"**Major**: {mentee['major']}")
            st.write(f"**Bio**: {mentee['bio']}")

            if mentee['resume'] and mentee['resume'].lower() != "none":
                resume_path = os.path.join(directory, mentee['resume'])
                if os.path.exists(resume_path):
                    st.download_button(
                    label="Download Resume",
                    data=open(resume_path, "rb").read(),
                    file_name=f"{mentee['name']}_Resume.pdf",
                    mime="application/pdf",
                    key=f"resume_{idx}" 
                )
            else:
                st.write("Resume not available.")
            
            st.markdown("---")
            menteeId = mentee['menteeId']   
            st.write("***Metrics***:")

            metrics = fetch_metrics(menteeId)
            applications = fetch_application_data(menteeId)

            with st.expander("Metric History"):
                    if metrics :
                        for metric in metrics:
                            st.write(f"**Progress**: {metric['progressNotes']}")
                            st.write(f"**Adjustment**: {metric['adjustmentNotes']}")

                    else :
                        st.text("No Metrics Available at This Time")

                    
                    if applications :
                        st.text(f"Applications Submitted: {applications[0]['total']}")
                        detailed_application = fetch_detailed_application_data(menteeId)
                        timestamps = []
                        applicationInc = []

                        for index, application in enumerate(detailed_application):
                            timestamp = datetime.strptime(application['timeApplied'], '%a, %d %b %Y %H:%M:%S GMT')
                            timestamps.append(timestamp)
                            applicationInc.append(index)
                            
                        # st.write(timestamp)
                        # st.write(applicationInc)    
                        plt.figure(figsize=(10, 6))
                        plt.plot(timestamps, applicationInc, marker='o', linestyle='-', color='b')

                        plt.title('Applications Over Time')
                        plt.xlabel('Date')
                        plt.ylabel('Number of Applications')

                        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
                        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
                        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
                        plt.gcf().autofmt_xdate()
                        st.pyplot(plt)  

                        plt.grid(True)

                    else :
                        st.text("No Application Data Available at This Time")
            
            with st.expander("Add Metrics", expanded=False):
                with st.form(key=f"MetricsForm_{idx}"):
                    progressNotes = st.text_input("Progress Notes")
                    adjustmentNotes = st.text_input("Adjustment Notes")

                    submit_button = st.form_submit_button(label="Save")

                    if submit_button:
                        metric_data = {
                            "progressNotes": progressNotes,
                            "adjustmentNotes": adjustmentNotes,
                            "mentorId": mentorId, 
                            "menteeId": menteeId
                        }

                        # st.write("Data to be submitted:", metric_data)

                        try:
                            create_metric = requests.post('http://web-api:4000/o/createMetric', json=metric_data)

                            if create_metric.status_code == 200:
                                st.info("Metrics Added")
                                st.session_state['profile_built'] = True
                            else:
                                st.error(f"Error creating metrics. Status code: {create_metric.status_code}")
                        except requests.exceptions.RequestException as e:
                            st.error(f"Error connecting to server: {str(e)}")

else:
    st.write("No mentees found.")


st.write('')
st.write('')

if st.button('Find More Mentees', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/15_Mentor_Find_Mentees.py')

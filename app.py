import streamlit as st
import librosa
import soundfile as sf
from transformers import pipeline

def parse_tasks(task_string):
    tasks = []
    lines = task_string.split('\n')
    current_task = {}
    for line in lines:
        if line.startswith("Task:"):
            if current_task:
                tasks.append(current_task)
            current_task = {"Task": line[6:].strip()}
        elif line.startswith("Responsible:"):
            current_task["Responsible"] = line[12:].strip()
        elif line.startswith("Deadline:"):
            current_task["Deadline"] = line[9:].strip()
    if current_task:
        tasks.append(current_task)
    return tasks

# --- Input Method ---
st.title("Meeting Assistant")
input_option = st.radio("Choose input method:", ("Record Audio", "Enter Transcript"))

if input_option == "Record Audio":
    audio_bytes = st.audio("Record your meeting audio")
    if audio_bytes:
        st.audio(audio_bytes)
        st.session_state['recorded_audio'] = audio_bytes
elif input_option == "Enter Transcript":
    transcript_input = st.text_area("Enter meeting transcript:")
    if transcript_input:
        st.session_state['entered_transcript'] = transcript_input

# --- Transcribe Audio (Simulated) ---
if st.button("Transcribe Audio") and 'recorded_audio' in st.session_state:
    transcription_text = (
        "The team discussed the Q4 marketing strategy, reviewed the budget, "
        "and assigned action items for the upcoming campaign. Alice Johnson will finalize "
        "the social media campaign budget by 2024-11-15. Bob Williams is responsible for "
        "creating the content calendar for Q4, with a deadline of 2024-11-22. Charlie Brown "
        "will set up analytics tracking for the campaign, due by 2024-11-29. Key decisions "
        "included approving the social media campaign budget and assigning responsibilities "
        "for content creation and analytics tracking."
    )
    st.write("Full Transcription:")
    st.write(transcription_text)
    st.session_state['full_transcription'] = transcription_text

# --- Meeting Summary (Simulated) ---
if st.button("Summarize Meeting"):
    if 'full_transcription' in st.session_state or 'entered_transcript' in st.session_state:
        summary_text = (
            "The Q4 marketing strategy was discussed, including budget allocation and task assignments. "
            "Key decisions included approving the social media campaign budget and assigning roles for content creation and analytics."
        )
        st.write("Meeting Summary:")
        st.write(summary_text)
        st.session_state['summary'] = summary_text
    else:
        st.error("Please provide either audio or a transcript.")

# --- Extract Tasks ---
if st.button("Extract Tasks"):
    if 'full_transcription' in st.session_state or 'entered_transcript' in st.session_state:
        tasks = [
            {"Task": "Finalize social media campaign budget", "Responsible": "Alice Johnson", "Deadline": "2024-11-15"},
            {"Task": "Create content calendar for Q4", "Responsible": "Bob Williams", "Deadline": "2024-11-22"},
            {"Task": "Set up analytics tracking for campaign", "Responsible": "Charlie Brown", "Deadline": "2024-11-29"}
        ]
        st.session_state['tasks'] = tasks
        st.write("Extracted Tasks:")
        for task in tasks:
            st.write(f"- Task: {task['Task']}")
            st.write(f"  Responsible: {task['Responsible']}")
            st.write(f"  Deadline: {task['Deadline']}")
    else:
        st.error("Please provide either audio or a transcript.")

# --- Send Reminders ---
if st.button("Send Reminders") and 'tasks' in st.session_state:
    for task in st.session_state['tasks']:
        email_map = {
            "Alice Johnson": "alice.johnson@gmail.com",
            "Bob Williams": "bob.williams@gmail.com",
            "Charlie Brown": "charlie.brown@gmail.com"
        }
        email = email_map.get(task["Responsible"], "unknown@example.com")
        st.write(f"Sent reminder to {email}: {task['Task']} (Deadline: {task['Deadline']})")

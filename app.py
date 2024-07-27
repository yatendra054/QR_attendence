import streamlit as st
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import datetime
import time

whitelist_txt = 'D:/QR-Attendence/whitelist.txt'
log_path = 'D:/QR-Attendence/log.txt'

def load_authorized_users(whitelist_txt):
    with open(whitelist_txt, 'r') as f:
        authorized_users = [l.strip() for l in f.readlines() if len(l) > 0]
    return set(authorized_users)

def save_new_user(whitelist_txt, user):
    with open(whitelist_txt, 'a') as f:
        f.write(user + '\n')

def log_access_event(log_path, user):
    current_time = datetime.datetime.now()
    with open(log_path, 'a') as f:
        f.write(f"{user},{current_time}\n")

if 'stop' not in st.session_state:
    st.session_state.stop = False

if 'start' not in st.session_state:
    st.session_state.start = False

st.title("QR Code Attendance System")

if st.button("Start"):
    st.session_state.start = True
    st.session_state.stop = False

if st.button("Quit"):
    st.session_state.stop = True
    st.session_state.start = False

FRAME_WINDOW = st.image([])

authorized_users = load_authorized_users(whitelist_txt)
seen_users = set(authorized_users)
most_recent_access = {}
time_between_logs_th = 5

if st.session_state.start:
    cap = cv2.VideoCapture(0)
    while cap.isOpened() and not st.session_state.stop:
        ret, frame = cap.read()
        if not ret:
            break

        qr_info = decode(frame)
        access_message = ""

        if qr_info:
            qr = qr_info[0]
            data = qr.data.decode('utf-8')
            rect = qr.rect
            polygon = qr.polygon

            if data in authorized_users:
                access_message = "ACCESS GRANTED"
                cv2.putText(frame, access_message, (rect.left, rect.top - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                if data not in most_recent_access or time.time() - most_recent_access[data] > time_between_logs_th:
                    most_recent_access[data] = time.time()
                    log_access_event(log_path, data)
            else:
                access_message = "ACCESS DENIED"
                cv2.putText(frame, access_message, (rect.left, rect.top - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                if data not in seen_users:
                    save_new_user(whitelist_txt, data)
                    authorized_users.add(data)
                    seen_users.add(data)

            frame = cv2.rectangle(frame, (rect.left, rect.top), (rect.left + rect.width, rect.top + rect.height),
                                  (0, 255, 0), 5)
            frame = cv2.polylines(frame, [np.array(polygon)], True, (255, 0, 0), 5)

        FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    cap.release()

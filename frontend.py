
import streamlit as st
from modelmain import RedisModel
from langchain_core.messages import HumanMessage
import uuid
from db import push_to_store, get_from_store,get_user_sessions
import random

# --- Authentication Check ---
if not getattr(st.user, 'is_logged_in', False):
    st.title("Welcome to Chatbot App")
    st.write("Please log in to continue.")
    if st.button("Log in with OIDC"):
        st.login()
    st.stop()

st.sidebar.write(f"Logged in as: **{st.user.name}**")
st.sidebar.write(f"Logged in as: **{st.user.email}**")

if st.sidebar.button("Log out"):
    st.logout()

if 'message_hist' not in st.session_state:
    st.session_state['message_hist'] = []

if 'sessions' not in st.session_state:
    st.session_state['sessions'] = []

if 'session_id' not in st.session_state:
    st.session_state['session_id'] = str(uuid.uuid4())
    st.session_state['sessions'].append(st.session_state['session_id'])
    st.session_state['chat_id'] = [random.randint(0, 100)]


# ----------------------------------------funcs---------------------------------------#
def create_session():
    st.session_state['session_id'] = str(uuid.uuid4())
    st.session_state['message_hist'] = []
    st.session_state['sessions'].append(st.session_state['session_id'])
    st.session_state['chat_id'] = [random.randint(0, 100)]



current_user_email = st.user.email

def update():
    push_to_store(
        session_id=st.session_state['session_id'],
        chat_id=st.session_state['chat_id'][-1],
        chat=st.session_state['message_hist'][-2:],
        user_email=str(current_user_email)
    )
    st.session_state['chat_id'].append(st.session_state['chat_id'][-1] + 1)
chatbot = RedisModel(st.session_state['session_id'])


# ----------------------SideBar----------------------------#
st.sidebar.title('MY CONV')
if st.sidebar.button('NEW CONV'):
    if st.session_state['message_hist']:
        create_session()

st.sidebar.header('Message History')
user_sessions = get_user_sessions(str(current_user_email))
st.session_state['sessions'].extend(user_sessions)

for session in set(st.session_state['sessions']):
    if st.sidebar.button(session, key=session):
        l = get_from_store(session, str(current_user_email))
        st.session_state['message_hist'] = l
        st.session_state['session_id'] = session

# -------------------------main------------------------------#

for message in st.session_state['message_hist']:
    if message['avatar'] == 'user':
        with st.chat_message('user'):
            st.text(message['message'])
    else:
        with st.chat_message('assistant'):
            st.text(message['message'])

inp = st.chat_input('Type Here')
if inp:
    with st.chat_message('user'):
        st.session_state['message_hist'].append({'avatar':'user','message':inp})
        st.text(inp)
    with st.chat_message('assistant'):
        mes=[]
        mes.append((st.write_stream(chatbot.invoke(inp))))
    res="".join(mes)
    st.session_state['message_hist'].append({'avatar':'assistant','message':res})
    update()
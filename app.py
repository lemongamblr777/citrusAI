import streamlit as st
import requests
import json
import os
import time

# 1. Your secret password
SECRET_PASSWORD = "lemon_scented"

# 2. Check if the user is logged in
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# 3. Initialize anti-spam timer tracker
if "last_submit_time" not in st.session_state:
    st.session_state["last_submit_time"] = 0

# Show the $1 lock screen if they aren't logged in
if not st.session_state["authenticated"]:
    st.title("hello!")
    st.write("enter the password you got")
    
    user_input = st.text_input("Enter Password:", type="password")
    if st.button("Unlock"):
        if user_input == SECRET_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Inaccurate")
            
    # --- PROPRIETARY TERMS & CONDITIONS ---
    st.markdown("---")
    st.caption("### 📄 Terms & Conditions")
    st.caption("By using this AI service, you agree to the following terms:")
    st.caption("1. **No Copying:** All rights reserved. You may not copy, modify, or steal this software's source code.")
    st.caption("2. **Single User:** DO NOT share passwords Sharing passwords will result inacces to these services being bloked so dont")
    st.caption("3. **Fair Use:** You are at fault for misuse follow the school rules")

# 4. If they enter the right password, show the actual AI Chatbot
else:
    # --- TROUBLESHOOTING SIDEBAR WITH ANTI-SPAM ---
    with st.sidebar:
        st.header("Help & Feedback")
        
        st.subheader("Troubleshooting")
        with st.expander("CitrusAI taking a while?"):
            st.write("network traffic can make it take longer Wait about 10 seconds or try refreshing.")
            
        with st.expander("problem?"):
            st.write("there is a report section for bugs")
            
        st.markdown("---")
        
        st.subheader("Tell us! (Submit Bug/Feedback)")
        feedback_name = st.text_input("Your Name (Optional):", placeholder="Classmate or Anonymous")
        feedback_type = st.selectbox("What is the issue?", ["AI Problems", "Website Problems"])
        feedback_text = st.text_area("What's wrong or what feature do you want next?", placeholder="Type your message here...")
        
        if st.button("Submit Report"):
            current_time = time.time()
            time_passed = current_time - st.session_state["last_submit_time"]
            SPAM_LIMIT = 300  # 5 minutes in seconds
            
            # Check if 5 minutes have passed since their last post
            if time_passed < SPAM_LIMIT:
                seconds_left = int(SPAM_LIMIT - time_passed)
                minutes_left = seconds_left // 60
                rem_seconds = seconds_left % 60
                st.error(f"⏳ Anti-Spam timer! Please wait {minutes_left}m {rem_seconds}s before submitting another report.")
            elif feedback_text.strip() == "":
                st.error("Please type a message first.")
            else:
                # Format feedback cleanly to display publicly
                formatted_entry = f"**[{feedback_type}]** {feedback_name if feedback_name else 'Anonymous'}: {feedback_text}\n\n---\n\n"
                
                with open("feedback.txt", "a") as f:
                    f.write(formatted_entry)
                
                # Save the new submission timestamp
                st.session_state["last_submit_time"] = current_time
                st.success("upload successful!")
                st.rerun()  # Refresh so the public board updates instantly

    # --- YOUR CUSTOM CITRUSAI MAIN INTERFACE ---
    st.title("CITRUSAI")
    st.write("heyo type questions in the box below")
    
    user_prompt = st.text_input("Ask em anything:")
    
    if user_prompt:
        st.write("Thinking...")
        
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "phi4-mini",
            "prompt": user_prompt,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload)
            result = response.json()
            st.write("### AI Response:")
            st.write(result.get("response", "No response text found."))
        except Exception as e:
            st.error("Could not connect to the AI engine. servers may be down at the moment for troubleshooting tell jay!")

    # --- PUBLIC FEEDBACK BOARD ---
    st.markdown("### Public Feedback & Bug report")
    st.write("See problems or feature requests other people have submitted:")
    
    # Read the file and display it to everyone
    if os.path.exists("feedback.txt"):
        with open("feedback.txt", "r") as f:
            public_logs = f.read()
        if public_logs.strip() != "":
            st.markdown(public_logs)
        else:
            st.info("No feedback submitted yet.")
    else:
        st.info("No feedback submitted yet.")

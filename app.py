import streamlit as st
import pandas as pd
import webbrowser
import pyautogui
import pyperclip
import time
import random

pyautogui.FAILSAFE = True  # Move mouse to top-left corner to abort if needed

st.set_page_config(page_title="Bulk WhatsApp Sender", page_icon="💬", layout="centered")
st.title("💬 Bulk WhatsApp Message Sender (No API Required)")
st.markdown("### Send WhatsApp messages directly from your CSV file using WhatsApp Web.")

st.info("""
**Instructions:**
1. Prepare a CSV file with columns: `Number` and `Message`.  
2. Make sure you’re logged in to WhatsApp Web in the browser that opens.  
3. Don’t move your mouse or keyboard while the process is running (except if you need to abort by moving mouse to top-left corner).  
4. Avoid spamming to prevent number blocking.
""")

uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])

def human_sleep(base=1.0, jitter=0.7):
    """Sleep a little to mimic human behaviour."""
    time.sleep(base + random.random()*jitter)

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.dataframe(data)

    if st.button("🚀 Send WhatsApp Messages (Use single tab)"):
        st.warning("⚠️ Don’t touch your mouse/keyboard during the process! Move mouse to top-left to abort.")

        total = len(data)
        progress = st.progress(0)
        status_text = st.empty()

        # Open WhatsApp Web once (if not already open)
        st.write("Opening WhatsApp Web — please scan QR if not logged in.")
        webbrowser.open("https://web.whatsapp.com", new=0)  # try to open in same browser window if possible
        time.sleep(12)  # initial wait for WhatsApp Web to load (adjust if needed)
        human_sleep(1, 1)

        for index, row in data.iterrows():
            try:
                number = str(row['Number']).strip()
                message = str(row['Message']).strip()

                # Build chat URL (we will navigate to it in the same tab using address bar)
                url = f"https://web.whatsapp.com/send?phone={number}"

                # Focus address bar and navigate to url (this will reuse the same tab)
                pyautogui.hotkey("ctrl", "l")   # focus address bar
                human_sleep(0.2, 0.2)
                pyperclip.copy(url)
                pyautogui.hotkey("ctrl", "v")
                human_sleep(0.2, 0.2)
                pyautogui.press("enter")

                # Wait for chat to load — give slightly longer for unknown contacts
                wait_time = 8 + random.uniform(1.0, 4.0)
                time.sleep(wait_time)

                # Copy message then paste into message box
                pyperclip.copy(message)
                human_sleep(0.3, 0.5)

                # Try to click message input area to ensure focus (screen-dependent)
                # You can adjust these coordinates or remove the click if unnecessary.
                # If you don't want fixed coordinates, comment out the next two lines.
                # pyautogui.click(x=600, y=920)  # example coordinates for message box (change per your screen)
                # human_sleep(0.2, 0.3)

                pyautogui.hotkey("ctrl", "v")
                human_sleep(0.4, 0.6)

                # Small random mouse movement (human-like)
                curx, cury = pyautogui.position()
                pyautogui.moveTo(curx + random.randint(-5, 5), cury + random.randint(-5, 5), duration=0.1)

                pyautogui.press("enter")

                # Wait after sending
                human_sleep(2.0, 1.5)

                progress.progress((index + 1) / total)
                status_text.text(f"✅ Sent to {number} ({index + 1}/{total})")
            except Exception as e:
                status_text.text(f"❌ Error for {number}: {e}")
                # short pause before continuing
                time.sleep(2)
                continue

        st.success("🎉 All messages processed (check statuses above).")

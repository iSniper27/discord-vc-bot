from flask import Flask, render_template, redirect
from threading import Thread
import asyncio
from bot import MyClient
import os
from dotenv import load_dotenv

app = Flask(__name__)
connected = False
client = None
loop = asyncio.new_event_loop()

def run_bot():
    global client
    asyncio.set_event_loop(loop)
    client = MyClient()
    loop.run_until_complete(client.start(os.getenv("TOKEN"), reconnect=True))

@app.route("/")
def index():
    return render_template("index.html", connected=connected)

@app.route("/connect")
def connect():
    global connected
    if not connected:
        thread = Thread(target=run_bot)
        thread.start()
        connected = True
    return redirect("/")

@app.route("/disconnect")
def disconnect():
    global connected, client
    if connected and client:
        loop.call_soon_threadsafe(lambda: asyncio.create_task(client.close()))
        connected = False
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)

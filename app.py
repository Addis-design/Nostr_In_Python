from flask import Flask, render_template, request, session, redirect, url_for
from pynostr.key import PrivateKey
import json
import ssl
import time
import uuid
from pynostr.event import Event
from pynostr.relay_manager import RelayManager
from pynostr.filters import FiltersList, Filters
from pynostr.event import EventKind
from pynostr.message_type import ClientMessageType
from pynostr.key import PrivateKey

app = Flask(__name__)

private_key = PrivateKey()
public_key = private_key.public_key
app.config['SECRET_KEY'] = "N4qzB^mxJPjV0(s~.ge,e\"''"
relay_manager = RelayManager(timeout=2)
relay_manager.add_relay("wss://nostr-pub.wellorder.net")
relay_manager.add_relay("wss://relay.damus.io")
filters = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE], limit=100)])
subscription_id = uuid.uuid1().hex
relay_manager.add_subscription_on_all_relays(subscription_id, filters)

relay_manager.run_sync()
event_msg_content = []
notice_msg_content = []

while relay_manager.message_pool.has_events():
    event_msg = relay_manager.message_pool.get_event()
    event_msg_content.append(event_msg.event.content)
    # print(event_msg_content)
@app.route('/',methods=['POST',"GET"])
def index():
    if 'public_key' in session:
      
        relay_manager = RelayManager(timeout=6)
        relay_manager.add_relay("wss://nostr-pub.wellorder.net")
        relay_manager.add_relay("wss://relay.damus.io")
        private_key = PrivateKey()

        filters2 = FiltersList([Filters(authors=[private_key.public_key.hex()], limit=100)])
        subscription_id = uuid.uuid1().hex
        relay_manager.add_subscription_on_all_relays(subscription_id, filters2)
      

        if request.method == 'POST':
           
            message = request.form.get('message')

            event=Event(message) 

            event.sign(private_key.hex())

        
            relay_manager.close_all_relay_connections()
        
        return render_template('index.html', public_key=session['public_key'], event_msg_content=event_msg_content, notice_msg_content=notice_msg_content)
    else:   
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        selected_public_key = request.form.get("public_key")
        if public_key.bech32() == selected_public_key:
            session['public_key'] = selected_public_key
            return redirect(url_for('index'))
        else:
            print("not equal")
            return render_template('login.html', public_key=public_key.bech32())
    else:
        return render_template('login.html', public_key=public_key.bech32())
@app.route('/logout', methods=['POST'])
def logout():
    # Clear the session data
    session.pop('public_key', None)
    # Redirect to the login page or any other page you want
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)

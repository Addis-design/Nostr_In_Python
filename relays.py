from pynostr.relay_manager import RelayManager
from pynostr.filters import FiltersList, Filters
from pynostr.event import EventKind
import time
import uuid

relay_manager = RelayManager(timeout=2)
relay_manager.add_relay("wss://nostr-pub.wellorder.net")
relay_manager.add_relay("wss://relay.damus.io")
filters = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE], limit=100)])
subscription_id = uuid.uuid1().hex
relay_manager.add_subscription_on_all_relays(subscription_id, filters)
relay_manager.run_sync()
while relay_manager.message_pool.has_notices():
    notice_msg = relay_manager.message_pool.get_notice()
    print(notice_msg.content)
# while relay_manager.message_pool.has_events():
#     event_msg = relay_manager.message_pool.get_event()
#     print(event_msg.event.content)
relay_manager.close_all_relay_connections()
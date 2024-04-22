from pynostr.relay import Relay
from pynostr.filters import FiltersList, Filters
from pynostr.event import EventKind
from pynostr.base_relay import RelayPolicy
from pynostr.message_pool import MessagePool
import tornado.ioloop
from tornado import gen
import time
import uuid

message_pool = MessagePool(first_response_only=False)
policy = RelayPolicy()
io_loop = tornado.ioloop.IOLoop.current()
r = Relay(
    "wss://relay.damus.io",
    message_pool,
    io_loop,
    policy,
    timeout=2
)
filters = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE], limit=100)])
subscription_id = uuid.uuid1().hex

r.add_subscription(subscription_id, filters)

try:
    io_loop.run_sync(r.connect)
except gen.Return:
    pass
io_loop.stop()

while message_pool.has_notices():
    notice_msg = message_pool.get_notice()
    print(notice_msg.content)
# while message_pool.has_events():
#     event_msg = message_pool.get_event()
#     print(event_msg.event.content)
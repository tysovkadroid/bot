from datetime import datetime, timedelta
from queue import Queue
from threading import Thread

from telegram.bot import Bot
from telegram.ext import Dispatcher, Defaults, JobQueue
from telegram.ext.messagequeue import MessageQueue, queuedmessage
from telegram.utils.request import Request

from bot.config import TOKEN, TIMEZONE
from bot.handlers import register_handlers
from bot.handlers.scheduler import scheduler


class MQBot(Bot):
    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or MessageQueue()

    @queuedmessage
    def send_message(self, *args, **kwargs):
        return super(MQBot, self).send_message(*args, **kwargs)


request = Request(con_pool_size=8)
queue = MessageQueue(all_burst_limit=29, all_time_limit_ms=1035, group_burst_limit=19,
                     group_time_limit_ms=60990)
defaults = Defaults(parse_mode='MarkdownV2', disable_web_page_preview=True, tzinfo=TIMEZONE)

bot = MQBot(TOKEN, request=request, mqueue=queue, defaults=defaults)
update_queue = Queue()
job_queue = JobQueue()

dispatcher = Dispatcher(bot=bot, update_queue=update_queue, job_queue=job_queue)

register_handlers(dispatcher)

thread = Thread(target=dispatcher.start, name='dispatcher')
thread.start()

now = datetime.now(TIMEZONE)
time_first = (now + timedelta(seconds=60)).replace(second=0, microsecond=0)

job_queue.set_dispatcher(dispatcher)
job_queue.run_repeating(callback=scheduler, interval=60, first=time_first, name='scheduler')
job_queue.start()

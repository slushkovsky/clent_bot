import time
import datetime
from collections import namedtuple

import feedparser
import schedule
from telegram import Bot, ParseMode

import db
import config


News = namedtuple('News', ['title', 'summary', 'link'])

def parse_rss(link): 
    feed = feedparser.parse(link)

    upd_time = datetime.datetime.strptime(feed['feed']['updated'], '%Y-%m-%dT%H:%M:%SZ')

    return ([News(entry['title'], entry['summary'], entry['link']) for entry in feed['entries']], upd_time) 

def upd():
    __session = db.Session() 
    rss_list = __session.query(db.RSS).all() 

    for rss in rss_list: 
        news_list, upd_time = parse_rss(rss.link)

        if rss.last_upd_time is None or upd_time > rss.last_upd_time: 
            rss.last_upd_time = upd_time
            __session.commit()

            for news in news_list:  
                Bot(config.BOT_TOKEN).send_message(
                    chat_id=rss.user.chat_id, 
                    text=f'{news.link}\n[{rss.id}] {news.title}\n----------------------------------------------\n{news.summary}', 
                    parse_mode=ParseMode.HTML
                )
 

if __name__ == '__main__': 
    schedule.every(config.RSS_UPDATE_TIMEOUT_MINUTES).minutes.do(upd)

    while True:
        schedule.run_pending()
        time.sleep(10) 

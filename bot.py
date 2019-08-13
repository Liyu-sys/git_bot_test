import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent
from pprint import pprint

from function import record

import pymysql

bot = telepot.Bot('Your token')
telepot.api.set_proxy('http://127.0.0.1:1087')

user = {}

def on_inline_query(msg):
    def compute():
        context = ''
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        print ('Inline Query:', query_id, from_id, query_string)
        conn = pymysql.connect()
        cursor = conn.cursor()
        sql = "select * from events_information where date = '{}'".format(query_string)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            context += row[2]
            context += '\n'
        conn.close()
        articles = [InlineQueryResultArticle(
                        id = query_string,
                        title = 'New events',
                        input_message_content=InputTextMessageContent(
                            message_text = context
                        )
             )]
        return articles
    answerer.answer(msg,compute)

def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print ('Chosen Inline Result:', result_id, from_id, query_string)
    response = bot.getUpdates()
    pprint(response)
    record(from_id,user)
    print(user)
    conn = pymysql.connect()
    cursor = conn.cursor()
    sql = "select * from user_info where user_id"
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)
    indicator = True
    for row in results:
        if  row[0] == from_id:
            indicator = False
    conn.close()
    if indicator:
        conn = pymysql.connect()
        cursor = conn.cursor()
        sql = """insert into user_info
        values({},1,{},'{}')""".format(from_id,response[0]['message']['chat']['id'],result_id)
        cursor.execute(sql)
        conn.commit()
        conn.close()
    else:
        conn = pymysql.connect()
        cursor = conn.cursor()
        sql = """update user_info set forward_times = forward_times + 1,
        last_group_id = {},last_info_id = '{}' where user_id = {} """.format(response[0]
            ['message']['chat']['id'],result_id,from_id)
        cursor.execute(sql)
        conn.commit()
        conn.close()



answerer = telepot.helper.Answerer(bot)
MessageLoop(bot, {
                'inline_query': on_inline_query,
                  'chosen_inline_result': on_chosen_inline_result,
                  }).run_as_thread()

while True:
    time.sleep(10)

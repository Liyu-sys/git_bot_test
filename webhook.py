from __future__ import print_function
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config, view_defaults
from pyramid.response import Response

from github import Github

import telepot

import pymysql

import datetime

bot = telepot.Bot('Your token')
telepot.api.set_proxy('http://127.0.0.1:1087')
ENDPOINT = "webhook"

@view_defaults(
    route_name=ENDPOINT, renderer="json", request_method="POST"
)
class PayloadView(object):
    def __init__(self, request):
        self.request = request
        self.payload = self.request.json

    @view_config(header="X-Github-Event:push")
    def payload_push(self):
        print('New commit to ' +self.payload['compare']+'\n'+
          self.payload['after'][0:7]+': '+self.payload['commits'][0]['message']+
          ' by '+self.payload['commits'][0]['author']['username']+'\n')
        bot.sendMessage(,'New commit to ' +self.payload['compare']+'\n'+
          self.payload['after'][0:7]+': '+self.payload['commits'][0]['message']+
          ' by '+self.payload['commits'][0]['author']['username']+'\n')
        conn = pymysql.connect()
        cursor = conn.cursor()
        sql = """insert into events_information
            values('commit','{}','{}','{}','{}')""".format(self.payload['compare'],
                self.payload['commits'][0]['message'],self.payload['commits'][0]['author']['username'],
                str(datetime.datetime.strptime(self.payload['commits'][0]['timestamp'],
                    '%Y-%m-%dT%H:%M:%S+08:00'))[0:10])
        try:
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()
        conn.close()
        return Response("success")

    @view_config(header = "X-Github-Event:commit_comment")
    def payload_commit_comment(self):
        print('New comment on '+self.payload['comment']['html_url']+
        ' by '+self.payload['comment']['user']['login']+'\n'+
        self.payload['comment']['body']+'\n')
        bot.sendMessage(,'New comment on '+self.payload['comment']['html_url']+
        ' by '+self.payload['comment']['user']['login']+'\n'+
        self.payload['comment']['body']+'\n')
        conn = pymysql.connect()
        cursor = conn.cursor()
        sql = """insert into events_information
            values('commit_comment','{}','{}','{}','{}')""".format(self.payload['comment']['html_url'],
                self.payload['comment']['body'],self.payload['comment']['user']['login'],
                str(datetime.datetime.strptime(self.payload['comment']['updated_at'],'%Y-%m-%dT%H:%M:%SZ')
                +datetime.timedelta(hours = 8))[0:10])
        try:
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()
        conn.close()
        return Response("success")

    @view_config(header="X-Github-Event:pull_request_review_comment")
    def payload_pull_request_review_comment(self):
        print('New comment on '+self.payload['comment']['html_url']+
        ' by '+self.payload['comment']['user']['login']+'\n'+
        self.payload['comment']['body']+'\n')
        bot.sendMessage(,'New comment on '+self.payload['comment']['html_url']+
        ' by '+self.payload['comment']['user']['login']+'\n'+
        self.payload['comment']['body']+'\n')
        conn = pymysql.connect()
        cursor = conn.cursor()
        sql = """insert into events_information
            values('commit_comment','{}','{}','{}','{}')""".format(sself.payload['comment']['html_url'],
                self.payload['comment']['body'],self.payload['comment']['user']['login'],
                str(datetime.datetime.strptime(self.payload['comment']['updated_at'],'%Y-%m-%dT%H:%M:%SZ')
                +datetime.timedelta(hours = 8))[0:10])
        try:
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()
        conn.close()
        return Response("success")

    @view_config(header="X-Github-Event:pull_request_review")
    def payload_pull_request_review(self):
        print('New review on '+self.payload['review']['html_url']
          +' by '+self.payload['review']['user']['login']+'\n'+
          self.payload['review']['body']+'\n')
        bot.sendMessage(,'New review on '+self.payload['review']['html_url']
          +' by '+self.payload['review']['user']['login']+'\n'+
          self.payload['review']['body']+'\n')
        conn = pymysql.connect()
        cursor = conn.cursor()
        sql = """insert into events_information
            values('pull_request_review','{}','{}','{}','{}')""".format(self.payload['review']['html_url'],
                self.payload['review']['body'],self.payload['review']['user']['login'],
                str(datetime.datetime.strptime(self.payload['review']['submitted_at'],'%Y-%m-%dT%H:%M:%SZ')
                +datetime.timedelta(hours = 8))[0:10])
        try:
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()
        conn.close()
        return Response("success")

    @view_config(header="X-Github-Event:pull_request")
    def payload_pull_request(self):
        print('New pull request '+self.payload['pull_request']['html_url']+'\n'
          +'by: '+self.payload['pull_request']['user']['login']+'\n'+
          self.payload['pull_request']['body']+'\n')
        bot.sendMessage(,'New pull request '+self.payload['pull_request']['html_url']+'\n'
          +'by: '+self.payload['pull_request']['user']['login']+'\n'+
          self.payload['pull_request']['body']+'\n')
        conn = pymysql.connect()
        cursor = conn.cursor()
        sql = """insert into events_information
            values('pull_request','{}','{}','{}','{}')""".format(self.payload['pull_request']['html_url'],
                self.payload['pull_request']['body'],self.payload['pull_request']['user']['login'],
                str(datetime.datetime.strptime(self.payload['pull_request']['updated_at'],'%Y-%m-%dT%H:%M:%SZ')
                +datetime.timedelta(hours = 8))[0:10])
        try:
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()
        conn.close()
        return Response("success")

    @view_config(header= "X-Github-Event:issue_comment")
    def payload_issue_comments(self):
        print('New comment on '+self.payload['comment']['html_url']+
        ' by '+self.payload['comment']['user']['login']+'\n'+
        self.payload['comment']['body']+'\n')
        bot.sendMessage(,'New comment on '+self.payload['comment']['html_url']+
        ' by '+self.payload['comment']['user']['login']+'\n'+
        self.payload['comment']['body']+'\n')
        conn = pymysql.connect()
        cursor = conn.cursor()
        sql = """insert into events_information
            values('issue_comment','{}','{}','{}','{}')""".format(self.payload['comment']['html_url'],
                self.payload['comment']['body'],self.payload['comment']['user']['login'],
                str(datetime.datetime.strptime(self.payload['comment']['updated_at'],'%Y-%m-%dT%H:%M:%SZ')
                +datetime.timedelta(hours = 8))[0:10])
        try:
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()
        conn.close()
        return Response("success")

    @view_config(header="X-Github-Event:issues")
    def payload_issues(self):
        print('New issue '+self.payload['issue']['html_url']+
            ' by '+str(self.payload['issue']['user']['login'])+'\n'
            +self.payload['issue']['body']+'\n')
        bot.sendMessage(,'New issue '+self.payload['issue']['html_url']+
            ' by '+str(self.payload['issue']['user']['login'])+'\n'
            +self.payload['issue']['body']+'\n')
        conn = pymysql.connect()
        cursor = conn.cursor()
        sql = """insert into events_information
            values('issues','{}','{}','{}','{}')""".format(self.payload['issue']['html_url'],
                self.payload['issue']['body'],self.payload['issue']['user']['login'],
                str(datetime.datetime.strptime(self.payload['issue']['updated_at'],'%Y-%m-%dT%H:%M:%SZ')
                +datetime.timedelta(hours = 8))[0:10])
        try:
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()
        conn.close()
        return Response("success")
    

    @view_config(header="X-Github-Event:ping")
    def payload_else(self):
        print("Pinged! Webhook created with id {}!".format(self.payload["hook"]["id"]))
        return {"status": 200}


def create_webhook():
    USERNAME = ""
    PASSWORD = ""
    OWNER = ""
    REPO_NAME = ""
    EVENTS = ["push", "pull_request","issues","issue_comment","commit_comment",
              "pull_request_review_comment","pull_request_review"]
    HOST = ""
    config = {
        "url": "http://{host}/{endpoint}".format(host=HOST, endpoint=ENDPOINT),
        "content_type": "json"
    }

    g = Github(USERNAME, PASSWORD)
    repo = g.get_repo("{owner}/{repo_name}".format(owner=OWNER, repo_name=REPO_NAME))
    repo.create_hook("web", config, EVENTS, active=True)


if __name__ == "__main__":
    config = Configurator()
    create_webhook()
    config.add_route(ENDPOINT, "/{}".format(ENDPOINT))
    config.scan()
    app = config.make_wsgi_app()
    server = make_server("0.0.0.0", 80, app)
    server.serve_forever()

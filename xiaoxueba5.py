#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib
import urllib2
import cookielib
import json
import re
import random

#解决中文编码问题
reload(sys)
sys.setdefaultencoding( "utf-8" )

class SimSimi:
    pattern_space = re.compile(u"[\[\]\s]", re.IGNORECASE)
    pattern_simsimi = re.compile(u"(simsimi|simsim|simisimi|sim)", re.IGNORECASE)
    pattern_mobile = re.compile(u"[\d\-\.\*一二三四五六七八九零〇壹贰叁肆伍陆柒捌玖拾]{7,}")
    replace_in_list = [u'小学霸', u'小霸霸', u'霸儿', u'学霸', u'霸霸', u'小霸', u'xueba']
    replace_out_list = [
        [[u'你大爷', u'大爷', u'sb', u'SB', u'傻逼', u'煞笔', u'傻屄', u'孬'],
         [u'小笨蛋', u'小笨笨', u'笨笨']],
        [[u'操', u'艹'],
         [u'爱爱', u'爱']],
        [[u'主人', u'主任', u'主淫', u'主银'],
         [u'童鞋']],
        [[u'小黄鸡', u'小贱鸡', u'小萌鸡', u'小妖鸡', u'小黄基', u'小鸡鸡', u'黄基', u'鸡鸡', u'小鸡', u'鸡'],
         [u'小霸']],
        [[u'小黃雞', u'小賤雞', u'小萌雞', u'小妖雞', u'小黃基', u'小雞雞', u'黃基', u'雞雞', u'小雞', u'雞'],
         [u'小霸']],
    ]
    banned_list = [u'weixiaob8', u'微信', u'QQ', u'qq', u'扣扣', u'企鹅', u'天宇姐姐', u'官方旗舰店', u'淘宝', u'手机', u'号码', u'微博']
    banned_reply = [u'嗯~', u'哦~', u'啊~', u'呃', u'哈哈~', u'嘿嘿', u'好的~', u'然后呢?', u'知道了~', u'讨厌，小霸不知道你在说神马。>_<!']
    welcome_reply = u"""童鞋你好！我在佛前苦苦求了几千年终于把你盼来了！欢迎关注「我要当学霸」～

「我要当学霸」被称为改变人一生的手机应用，一度风靡全球。此微信官方帐号负责聊天、卖萌、不务正业，偶尔也会分享一些有趣的东西。

非常欢迎和小霸勾搭闲聊，比如你可以让小霸给你唱个歌、讲个故事、卖个萌或向你道晚安。总之，从今往后最关心你的不是10086也不是10010，就是小霸了！

(●'◡'●)ﾉ♥"""
    customized_dialogue = [
        [[u'Hello2BizUser'],
         [welcome_reply]],
        [[u'/:'],
         [u'发表情没诚意！']],
        [[u'自动回复'],
         [u'你才是自动回复，你全家都是自动回复！', u'讨厌，人家哪是自动回复呢！', u'你哪里看出我是自动回复了？', u'你才是自动回复呢~~~']],
        [[u'杨元', u'小元', u'小元元', u'小元小元小元'],
         [u'他是我的父亲！', u'嗯，你认识他？', u'他是我的作者，很帅哦！']]
    ]
    
    #初始化&登陆
    def __init__(self):
        self.cookiejar = cookielib.LWPCookieJar()
        self.url_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar))
        self.headers = {
            'Referer':'http://www.simsimi.com/talk.htm' 
        }
        self.url = 'http://www.simsimi.com/func/req?lc=ch&msg=%s'
        request = urllib2.Request(url = self.url, headers = self.headers)
        try:
            retval = self.url_opener.open(request, timeout = 10)
        except:
            exit

    #聊天hack api
    def chat(self, message = ''):
        request = urllib2.Request(url = self.url % message, headers = self.headers)
        try:
            retval = self.url_opener.open(request, timeout = 10)
            message = json.loads(retval.read())
        except:
            answer = u'讨厌(￣ー￣)人家回答不上来了嘛~~~'
        else:
            if message != {}:
                answer = message['response']
            else:
                answer = ''
        finally:
            return answer

    #用户提问语言优化
    def filter_in(self, message = ''):
        #去除空格
        question = self.pattern_space.sub("", message)
        #将对学霸的称呼转为对SimSimi
        for item in self.replace_in_list:
            question = question.replace(item, u'小鸡鸡')
        return question

    #SimSimi回答内容优化
    def filter_out(self, message = ''):
        #将SimSimi类字样替换为小学霸
        answer = self.pattern_simsimi.sub(u'小学霸', message)
        #去除空格
        answer = self.pattern_space.sub("", answer)
        #替换空回复
        if answer == '':
            answer = random.choice(self.banned_reply)
        else:
            #屏蔽微信、广告
            for banned_word in self.banned_list:
                if banned_word in answer:
                    answer = random.choice(self.banned_reply)
                    break
            else:
                #屏蔽手机号、QQ号等
                if self.pattern_mobile.findall(answer):
                    answer = random.choice(self.banned_reply)
                else:
                    #替换不良词语及小黄鸡类称呼
                    for dirty_list, clean_list in self.replace_out_list:
                        clean_word = random.choice(clean_list)
                        for dirty_word in dirty_list:
                            answer = answer.replace(dirty_word, clean_word)
        return answer

    #自行回复
    def customized_chat(self, message = ''):
        for question_list, answer_list in self.customized_dialogue:
            answer_word = random.choice(answer_list)
            for question_word in question_list:
                if question_word in message:
                    return answer_word
        else:
            return ""

    #“小学霸”调用接口
    def affected_chat(self, message = ''):
        question = self.filter_in(message)
        answer = self.customized_chat(question)
        if answer == "":
            answer = self.filter_out(self.chat(question))
        return answer


def main(argv = None):
    if argv is None:
        argv = sys.argv
    
    if len(argv) > 1:
        simi = SimSimi()
        print simi.affected_chat(argv[1])
    else:
        print 'Hi! (^.^)'


if __name__ == '__main__':
    main()


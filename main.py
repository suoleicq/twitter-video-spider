# coding: UTF-8
#!/usr/bin/python3

import os
import tweepy
from time import sleep
import urllib.error
import urllib.request
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import configparser
import ssl
from multiprocessing.dummy import Pool as ThreadPool
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')
CONSUMER_KEY = config_ini['CONSUMER']['KEY']
CONSUMER_SECRET = config_ini['CONSUMER']['SECRET']
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth)

def download_movies(author):
    author = author.replace("\n","") 
    search_results = tweepy.Cursor(api.user_timeline, screen_name = author).items(99999)
    if not os.path.exists(author):
        os.mkdir(author)
        i = 0
        for result in search_results:
            try:
                #動画
                movie_url = [variant['url'] for variant in result.extended_entities["media"][0]["video_info"]['variants'] if variant['content_type'] == 'video/mp4'][0]
                print(movie_url)
                dst_path = author+'/{}.mp4'.format(i)
                try:
                    with urllib.request.urlopen(movie_url) as web_file:
                        data = web_file.read()
                        with open(dst_path, mode='wb') as local_file:
                            local_file.write(data)
                except urllib.error.URLError as e:
                    print(e)
                i += 1
                sleep(1)
            except:
                pass
        print(author+'已下载完毕')
    else:
        print(author+'已存在，将跳过')
def main():
    with open('author.txt', encoding='utf-8') as f:
        authors = f.readlines()
    pool = ThreadPool(10) #双核电脑
    pool.map(download_movies, authors)#多线程工作
    pool.close()
    pool.join()

if __name__ == "__main__":
    main()

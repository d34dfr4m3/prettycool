#!/usr/bin/python3
# https://buckets.grayhatwarfare.com/apiDoc
import requests
import sys
import json
from helpers import httpClient
key = ""  # Get from enviroment


def queryStringGrayHatWarfareKeywords(keywords):
    return "https://buckets.grayhatwarfare.com/api/v1/buckets/0/1000?access_token=" + \
        key+'&keywords='+keywords


def queryStringGrayHatWarfareFiles(bucketId):
    return f"https://buckets.grayhatwarfare.com/api/v1/bucket/{bucketId}/files/0/100?access_token={key}"


class AwsSearch:
    def __init__(self):
        self.buckets = []
        self.wordlist = []

    def search(self, domainName, keywords, key):
        print("[-] Searching for string: {}".format(keywords))
        URL = queryStringGrayHatWarfareKeywords(keywords)
        data = httpClient.Get(URL, isJson=True)["data"]
        bucketsLen = int(data['buckets_count'])
        if bucketsLen == 0:
            print("[*] No buckets found")
        else:
            for ids in range(bucketsLen):
                buckets = data["buckets"][ids]
                bucket_id = buckets['id']
                bucket_name = buckets['bucket']
                print(f'Bucket: {bucket_name} ID: {bucket_id}')
                data_bucket = httpClient.get(
                    queryStringGrayHatWarfareFiles(bucket_id), isJson=True)
                self.buckets.append(bucket_name)
                if data_bucket.data['results'] == 0:
                    print(f'\t [-] Content of bucket id {bucket_id} not found')

    def generateBucketWordList(self, prefixKeyWord):
        badWords = ['com', 'br', 'net', 'ru', 'job']
        chars = ['-', '_', '+', '', '.']
        self.wordlist.append(prefixKeyWord)
        if '.' in prefixKeyWord:
            words = prefixKeyWord.split('.')
            for bad in badWords:
                if bad in words:
                    words.remove(bad)
                for i in range(len(words)):
                    for char in chars:
                        prework = char.join(words)
                        if prework not in self.wordlist:
                            self.wordlist.append(prework)
                words.reverse()
                for i in range(len(words)):
                    for char in chars:
                        prework = char.join(words)
                        if prework not in self.wordlist:
                            self.wordlist.append(prework)
                for word in words:
                    if word not in self.wordlist:
                        self.wordlist.append(word)
            for bad in badWords:
                if bad in self.wordlist:
                    self.wordlist.remove(bad)

    def awsSearchFor(self, domainName, key):
        print("[+] Bucket S3 Routing is starting")
        self.generateBucketWordList(domainName)
        for keyword in self.wordlist:
            self.search(domainName, keyword, key)

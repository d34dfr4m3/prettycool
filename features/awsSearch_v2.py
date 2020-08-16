from grayhatwarfare import API
import argparse

class BGHW:

    def __init__(self, api_key):
        self.buckets = []
        self.files = []
        self.api_key = api_key
        self.start = 0
        self.limit = 1000
    
    def search_buckets(self, keyword):
        print("[*] Searching for buckets with keyword: {}".format(keyword))
        buckets = API.search_buckets(self.api_key, keyword, start=self.start, limit=self.limit)
        if buckets:
            for bucket in buckets.list:
                self.buckets.append(bucket)
    
    def search_files(self, bucket_id, keyword=None):
        print("[+] Searching in bucket {} for files with keyword: {}".format(bucket_id, keyword))
        files = API.search_files(self.api_key, bucket_id, keyword=keyword, start=self.start, limit=self.limit)
        if files:
            for file in files.list:
                self.files.append(file)

    def search_buckets_with_keywords(keywords):
        for key in keywords:
            self.search_buckets(key)
        
    def search_files_with_keywords(bucket_id, keywords):
        for key in keywords:
            pass
            
    


parser = argparse.ArgumentParser()
bucket_group = parser.add_mutually_exclusive_group()
file_group = parser.add_mutually_exclusive_group()
parser.add_argument("api_key", help="The API Key of GrayHatWarfare")

bucket_group.add_argument("-k", "--bucket_keyword", help="The keyword to search in buckets")
bucket_group.add_argument("-b", "--bucket-id", type=int, help="The bucket ID")

parser.add_argument("-s", "--start", type=int, help="Set the start offset")
parser.add_argument("-l", "--limit", type=int, help="Set the limit offset")

file_group.add_argument("-f", "--file-keyword", help="The keyword to search in files")
file_group.add_argument("--show-files", action="store_true", help="Show the files of buckets")

args = parser.parse_args()

api_key = args.api_key
bucket_keyword = args.bucket_keyword
bucket_id = args.bucket_id
file_keyword = args.file_keyword
start = args.start
limit = args.limit
show_files = args.show_files

b = BGHW(api_key)
    
if start:
    b.start = start
    
if limit:
    b.limit = limit
    
if bucket_id:
    b.search_files(bucket_id, file_keyword)
else:
    if bucket_keyword:
        b.search_buckets(keyword=bucket_keyword)

        if file_keyword or show_files:
            for bucket in b.buckets:
                b.search_files(bucket.id, file_keyword)


if b.buckets:
    print("------ Buckets -------")
    for bucket in b.buckets:
        print(bucket.bucket)

if b.files:
    print("------ Files ------")
    for file in b.files:
        print(file.url)

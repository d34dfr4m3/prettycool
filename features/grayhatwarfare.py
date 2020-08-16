import requests, json

class ForbbidenAccess(Exception):
    pass

class File:
    def __init__(self):
        self.id = None
        self.bucket = None
        self.filename = None
        self.full_path = None
        self.url = None
        self.size = None


class Files:
    def __init__(self):
        self.count = None
        self.list = []

    def append(self, file):
        self.list.append(file)

class Bucket:
    def __init__(self):
        self.id = None
        self.bucket = None
        self.fileCount = None
    
class Buckets:

    def __init__(self):
        self.count = None
        self.list = []
    
    def append(self, bucket):
        self.list.append(bucket)

class util:

    def buckets_from_json(buckets_json):
        buckets = Buckets()
        buckets.count = buckets_json['buckets_count']
        for bucket in buckets_json['buckets']:
            b = util.bucket_from_json(bucket)
            buckets.append(b)
        return buckets

    def bucket_from_json(bucket_json):
        bucket = Bucket()
        bucket.id = bucket_json['id']
        bucket.bucket = bucket_json['bucket']
        bucket.fileCount = bucket_json['fileCount']
        return bucket
    
    def file_from_json(file_json):
        file = File()
        file.id = file_json['id']
        file.bucket = file_json['bucket']
        file.filename = file_json['filename']
        file.full_path = file_json['fullPath']
        file.url = file_json['url']
        file.size = file_json['size']
        return file
    
    def files_from_json(files_json):
        files = Files()
        files.count = files_json['results']
        for file in files_json['files']:
            f = util.file_from_json(file)
            files.append(f)
        return files

class API:

    ROOT_API = "https://buckets.grayhatwarfare.com/api/v1"

    def __build_url(api_key, bucket_id=None, keyword=None, start=None, limit=None):
        url = API.ROOT_API
        if bucket_id:
            url = url + "/bucket/{}/files".format(bucket_id)
        else:
            url = url + "/buckets"
        
        if start:
            url = url + "/{}".format(start)

        if limit:
            if start:
                url = url + "/{}".format(limit)
            else:
                url = url + "/0/{}".format(limit)

        url = url + "?access_token={}".format(api_key)

        if keyword:
            url = url + "&keywords={}".format(keyword)

        return url
    
    def __make_request(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise ForbbidenAccess

    def __search(api_key, bucket_id=None, keyword=None, start=None, limit=None):
        url = API.__build_url(api_key, bucket_id, start=start, limit=limit, keyword=keyword)
        return API.__make_request(url)
    
    def search_files(api_key, bucket_id, keyword=None, start=None, limit=None):
        files_json = API.__search(api_key=api_key, bucket_id=bucket_id, keyword=keyword, start=start, limit=limit)
        return util.files_from_json(files_json)
    
    def search_buckets(api_key, keyword=None, start=None, limit=None):
        buckets_json = API.__search(api_key=api_key, keyword=keyword, start=start, limit=limit)
        return util.buckets_from_json(buckets_json)

from minio import Minio
import json
client = Minio(
        '192.168.2.12:9000',
        access_key='minio',
        secret_key='minio123',
        secure= False)

def test():
    try:
        # Get the notifications configuration for a bucket.
        #notification = client.get_bucket_notification('pestdetection')
        print('going to listen noti')
        buckets = client.list_buckets()
        if client.bucket_exists('pestdetection'):
            print('bucket exists')
        else:
            print('bucket does not exists, creating')
            client.make_bucket('pestdetection')
        print('received done')
        return
        # If no notification is present on the bucket:
        # notification == {}
    except Exception as err:
        print(err)

def main():
    test()
    print('done')

if __name__ == "__main__":
    main()

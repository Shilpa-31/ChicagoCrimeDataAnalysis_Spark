import requests
import boto3
import time
from tqdm import tqdm

def fetch_crime_data_in_batches(api_url, limit, bucket_name, s3_key):
    # Initialize AWS S3 client
    s3 = boto3.client('s3')

    offset = 0
    batch_number = 1
    while True:
        # Build the URL with limit and offset for pagination
        paginated_url = f"{api_url}?$limit={limit}&$offset={offset}"
        print(f"Fetching batch {batch_number} from {paginated_url}...")
        
        # Make the API request
        response = requests.get(paginated_url)
        if response.status_code != 200:
            print(f"Failed to fetch data at offset {offset}. Retrying...")
            time.sleep(2)
            continue
        
        # Get the content in CSV format
        csv_data = response.content
        
        # Generate the S3 key for this batch, appending batch number
        batch_s3_key = f"{s3_key.split('.csv')[0]}_part{batch_number}.csv"  # Adding the part number
        
        # Upload the data to S3
        s3.put_object(Bucket=bucket_name, Key=batch_s3_key, Body=csv_data)
        print(f"Batch {batch_number} uploaded to {bucket_name}/{batch_s3_key}")
        
        # Increment the offset and batch number for the next request
        offset += limit
        batch_number += 1
        
        # If the response contains fewer rows than the limit, it means we've reached the last batch
        if len(csv_data) < limit:
            print(f"Last batch fetched. All data uploaded to S3.")
            break
        
        # Sleep to avoid hitting rate limits
        time.sleep(0.5)

# Inject data into AWS s3 bucket
def upload_csv_to_s3(api_url, s3_bucket, s3_key):
    response = requests.get(api_url)
    csv_data = response.content
    s3 = boto3.client('s3')
    s3.put_object(Bucket=s3_bucket, Key=s3_key, Body=csv_data)
    print(f"File uploaded to {s3_bucket}/{s3_key}")
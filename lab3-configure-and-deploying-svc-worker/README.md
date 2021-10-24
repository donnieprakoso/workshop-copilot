# Lab 3: Configure and Deploy `svc-worker`  
  
In this lab, we are going to deploy a Worker Service, called `svc-worker` to complete our application. As a worker service, the `svc-worker` doesn’t run on HTTP protocols and therefore doesn’t expose any ports. The `svc-worker` runs on Amazon ECS and AWS Fargate. It’s always running as it needs to retrieve and process the messages from queue.  
  
## Task 1: Initialize svc-worker  
  
Priority: 1  
  
In this task, you’re going to deploy `svc-worker` as a Worker Service.   
  
- Open terminal  
- Navigate to `source/` folder  
- Run `copilot svc init` command — this will trigger Copilot to start service creation  
  
Follow instructions below to complete the task  
  
- Choose **Worker Service***   
  
```  
Which service type best represents your service's architecture?  [Use arrows to move, type to filter, ? for more help]  
    Request-Driven Web Service  (App Runner)  
    Load Balanced Web Service   (Internet to ECS on Fargate)  
    Backend Service             (ECS on Fargate)  
  > Worker Service              (Events to SQS to ECS on Fargate)  
```  
  
- Name the Worker Service as `svc-worker`  
  
```  
Service type: Worker Service  
  
  What do you want to name this Worker Service? [? for help] svc-worker  
```  
  
- Select the Dockerfile in `svc-worker-pdf/` folder  
  
```  
Service type: Worker Service  
  
  Which Dockerfile would you like to use for svc-worker?  [Use arrows to move, type to filter, ? for more help]  
    svc-api/Dockerfile  
  > svc-worker-pdf/Dockerfile  
    Enter custom path for your Dockerfile  
    Use an existing image instead  
```  
  
- Wait until the process is finished. At the end of the process, Copilot will create a `manifest.yml` file in `copilot/svc-worker/` folder. This is the manifest file that we will configure in the next tasks.  
  
```  
Dockerfile: svc-worker-pdf/Dockerfile  
parse EXPOSE: no EXPOSE statements in Dockerfile svc-worker-pdf/Dockerfile  
No environments are currently deployed. Skipping subscription selection.  
✔ Wrote the manifest for service svc-worker at copilot/svc-worker/manifest.yml  
Your manifest contains configurations like your container size and port.  
  
✔ Created ECR repositories for service svc-worker..  
  
Recommended follow-up actions:  
  - Update your manifest copilot/svc-worker/manifest.yml to change the defaults.  
  - Run `copilot svc deploy --name svc-worker --env test` to deploy your service to a test environment.  
```  
  
## Task 2: Add environment variable AWS_REGION  
  
In this task, you’ll learn how to add an environment variable into your service. We’re going to add a variable called `AWS_REGION` into `svc-worker`. In the first task, we’ve created the application along with the `svc-api` service. For every service initialized with Copilot, it will create a manifest file in this location `copilot/<SERVICE_NAME>/manifest.yaml`.  
  
- Open `copilot/svc-worker/manifest.yml`  
- Navigate to the end of the file and add following lines:  
  
```  
environments:  
  staging:  
    variables:  
      AWS_REGION: ap-southeast-1  
```  
  
## Task 3: Add SQS to svc-worker  
  
As `svc-worker` is responsible to process the message published by `svc-api`. In the previous lab, we have configured the Amazon SNS Topic for `svc-api`. In this task, we are going to create an Amazon SQS Queue and subscribe to the Amazon SNS Topic.   
  
- Open `copilot/svc-worker/manifest.yml`  
- Navigate to the end of the file and add following lines:  
  
```  
subscribe:  
  topics:  
    - name: requests   
      service: svc-api  
```  
  
Above lines will create a Amazon SQS queue and create a subscription between the queue and the Amazon SNS Topic created by the `svc-api` service. Copilot will also create an environment variable called “COPILOT_QUEUE_URI” and automatically inject it into the `svc-worker`.  
  
## Task 4: Modify svc-worker to add COPILOT_QUEUE_URI  
  
In this task, you will need to evaluate the code on how that you can get the environment variable called `COPILOT_SQS_URI` to retrieve the Amazon SQS Queue URI.   
  
This task requires NO action from your end. You only need to evaluate on how to use the environment variable so `svc-worker` can do polling to the queue and process the request.  
  
1. Open `svc-worker/app.py`  
2. In the beginning of the code, after imports, you will see following line:  
  
```python  
SQS_URI = os.getenv("COPILOT_QUEUE_URI")  
```  
  
To retrieve the environment variable, we use the `os.getenv()` function.  
  
4. Go to ` receive_queue_message()` function  
5. Evaluate following lines:  
  
```python  
response = sqs_client.receive_message(  
            QueueUrl=SQS_URI, WaitTimeSeconds=5, MaxNumberOfMessages=1)  
```  
  
Above code allows us to retrieve the message published by the `svc-api`. For every message we received, SQS provides us with an attribute called `ReceiptHandle`. The `ReceiptHandle` is the identifier you must provide when deleting the message.  
  
6. Go to `main` function  
7. Evaluate following lines:  
  
```python  
create_directory("/tmp/images/requests/")  
fileoutput_path = "/tmp/images/requests/{}.pdf".format(data['request_ID'])  
pdfkit.from_url(data['request_url'], fileoutput_path)  
```  
  
Above lines are the routines to process the requested URL into a PDF. The application uses `pdfkit` library, a wrapper to `wkhtmltopdf`. You can refer to the Dockerfile in `svc-worker` to know more on including `wkhtmltopdf` into the container image.   
  
6. Go to ` delete_queue_message() `  
7. Evaluate following lines:  
  
```python  
response = sqs_client.delete_message(QueueUrl=SQS_URI,  
                                             ReceiptHandle=receipt_handle)  
```  
Once that we have retrieved the message and process the request (converting to PDF and upload them into Amazon S3), then we can safely remove the message from the queue.  
  
## Task 5: Add Amazon S3 Bucket to svc-worker  
  
Once the application processed the URL and convert the web page to PDF format, the next thing that we need to do is to upload the file into Amazon S3.   
  
In this task, you’ll add Amazon S3 using Copilot.   
  
- Open terminal  
- Navigate to `source` folder  
- Run `copilot storage init` command  
- Choose `svc-worker` to associate the S3 bucket  
  
```  
Which workload would you like to associate with this storage resource?  [Use arrows to move, type to filter]  
    svc-api  
  > svc-worker  
```  
  
- Choose Amazon S3 as type of the storage we’d like to associate with the `svc-worker`  
  
```  
Name: svc-worker  
  
What type of storage would you like to associate with svc-worker?  [Use arrows to move, type to filter, ? for more help]  
    DynamoDB            (NoSQL)  
  > S3                  (Objects)  
    Aurora Serverless   (SQL)  
```  
  
- Name the S3 bucket to “s3-pdf-requests”  
  
```  
Name: svc-worker  
Storage type: S3  
  
What would you like to name this S3 Bucket? [? for help] s3-pdf-requests  
```  
  
Upon deployment, Copilot will create an S3 bucket. In this context, it will be called as `S3PDFREQUESTS_NAME`.  
  
## Task 6: Modify svc-worker to add Amazon S3 Bucket  
  
In this task, you will need to evaluate the code on how that you can get the environment variable called `S3PDFREQUESTS_NAME` to retrieve the Amazon SQS Queue URI.   
  
This task requires NO action from your end. You only need to evaluate on how to use the environment variable so `svc-worker` can do polling to the queue and process the request.  
  
1. Open `svc-worker/app.py`  
2. In the beginning of the code, after imports, you will see following line:  
  
```python  
S3_BUCKET = os.getenv("S3PDFREQUESTS_NAME")  
```  
  
To retrieve the environment variable, we use the `os.getenv()` function.  
  
4. Go to ` upload_to_s3()` function  
5. Evaluate following lines:  
  
```python  
filename = os.path.basename(filepath)  
bucket = S3_BUCKET  
key = os.path.join(S3_KEY_OUTPUT_PROCESSED, filename)  
args = {'ServerSideEncryption': 'AES256'}  
s3_client = boto3.client("s3", region_name=AWS_REGION)  
s3_resp = s3_client.upload_file(filepath, bucket, key, ExtraArgs=args)  
url = s3_client.generate_presigned_url('get_object', ExpiresIn=3600, Params={'Bucket': bucket, 'Key': key})  
  
```  
This is the function to upload the PDF (located in `/tmp`) folder. We also provide a secure way to upload the file by setting the `ServerSideEncryption`.   
Once the file is successfully uploaded, we generate the URL so we can access it. In this case, the presigned URL is set to 3600 seconds. You are welcome to adjust this based on your needs.  
  
## Task 7: Add service discovery from svc-worker to svc-api  
  
When `svc-worker` finished processing the request, it also requires to update the status of the request back to `svc-api`. To do this, we need to have the endpoint of `svc-api` so `svc-worker` able to call the API with HTTP protocol.   
  
The `svc-worker` can call the `svc-api` from the public address. However, that’s not recommended as the connection needs to go through the internet. To be able calling the `svc-api` (or any other services) locally, we need to implement Service Discovery.   
  
Service Discovery is a way of letting services discover and connect with each other. Copilot leverages Amazon ECS Service Discovery feature and automatically created the variable called ` COPILOT_SERVICE_DISCOVERY_ENDPOINT` for each service. We can use this variable to call `svc-api` from `svc-worker`.   
  
In this task, you’ll learn how to retrieve and call `svc-api` using the endpoint we retrieve from `COPILOT_SERVICE_DISCOVERY_ENDPOINT`.   
  
1. Open `source/svc-worker-pdf/app.py`  
2. In the beginning of the code, after imports, you will see following line:  
  
```python  
SVC_API_ENDPOINT = os.getenv("SVC_API_ENDPOINT")  
```  
  
3. Go to ` update_request_status` function   
4. Evaluate the code below:  
  
```python  
req = requests.post("{}/status".format(SVC_API_ENDPOINT), json=data)  
```  
  
As you see, once that we have the API endpoint for `svc-api`, we’re able to invoke the API endpoint as what we usually trigger any other APIs.  
  
## Task 8: Deploy svc-worker to staging environment  
  
In this task, you’ll deploy the `svc-worker` into the `staging` environment. To deploy the `svc-worker`, you   
  
- Open terminal  
- Navigate to the `source/` folder  
- Run `copilot svc deploy --name svc-worker`  
  
If you don’t specify the service name using `--name` flag, Copilot will ask you the service name that you’d like to deploy.   
  
As we only have an environment, Copilot will automatically deploy to the `staging` environment. If you have multiple environments, Copilot will ask you into which environment you’d like to deploy or you can specify the environment name by passing `--env` flag.   
  
This process requires roughly 6-8 mins to complete. It’s time to have a break ☕️.  
  
## Task 9: Check the svc-worker environment  
  
In this task, you’ll learn how to get the details of the `svc-worker`. Once that you have the service deployed, you can see the details of the service by running `copilot svc show` command.   
  
- Open terminal  
- Navigate to `source/` folder  
- Run `copilot svc show --name svc-worker`  
  
Copilot will return similar output:  
  
```  
About  
  
  Application       test-webtopdf  
  Name              svc-worker  
  Type              Worker Service  
  
Configurations  
  
  Environment       Tasks               CPU (vCPU)          Memory (MiB)        Port  
  -----------       -----               ----------          ------------        ----  
  staging           1                   0.25                512                 -  
  
Variables  
  
  Name                                Container           Environment         Value  
  ----                                ---------           -----------         -----  
  COPILOT_APPLICATION_NAME            svc-worker          staging             test-webtopdf  
  COPILOT_ENVIRONMENT_NAME              "                   "                 staging  
  COPILOT_QUEUE_URI                     "                   "                 https://sqs.ap-southeast-1.amazonaws.com/XXXXXXXXXX/test-webtopdf-staging-svc-worker-EventsQueue-XXXXXXXXX  
  COPILOT_SERVICE_DISCOVERY_ENDPOINT    "                   "                 staging.test-webtopdf.local  
  COPILOT_SERVICE_NAME                  "                   "                 svc-worker  
```  
  
## Next Lab  
  
Click here to go to the next lab: [Lab 4: Testing Application`][1]  
  
  
[1]: https://github.com/donnieprakoso/workshop-copilot/tree/main/lab4-testing-app  

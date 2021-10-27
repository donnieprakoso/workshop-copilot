# Lab 1: Getting Started  
  
In this lab, we’ll prepare everything needed to deploy and operate the application.   
  
As this workshop objective is to help you understand how to build and operate your containers using AWS Copilot, throughout the labs you are expected to use AWS Copilot CLI as well as making some required changes in the infrastructure-as-code (`manifest.yml`) and source code files.  
  
## Task 1: Clone Github Repo  
  
To get all the source code we’ll be using in this workshop, you need to clone this Github repo.   

- Open your terminal  
- If you’re using SSH, do a Git clone by running this command:  

```bash  
    git clone git@github.com:donnieprakoso/workshop-copilot.git 
```  

- If you’re using HTTPS, Git clone by running following command:  

```bash  
    git clone https://github.com/donnieprakoso/workshop-copilot.git
```  
  
The source code for the application is located in `source/` folder. You’ll be using the source code provided.  
  
## Task 2: Application Code Review  
  
Inside `source/` folder, there are 2 subfolders: 1) svc-api and 2) svc-worker. As the name suggests, `svc-api` is the source code for the API service and `svc-worker` is the source code for the worker service.   
  
```  
├── svc-api  
│   ├── Dockerfile  
│   ├── app.py  
│   └── requirements.txt  
├── svc-worker-pdf  
│   ├── Dockerfile  
│   ├── app.py  
│   └── requirements.txt  
```  
  
This page describes the overall flow within each service, as well as how these 2 services connect to get the task done.  
  
### Review: svc-api  
  
`svc-api` is the public facing and any clients need to interact with the API provided in this app. There are 4 endpoints defined:  
  
1. `/ping`: for healthcheck  
2. `/status` with GET method: to get the latest status of a request  
3. `/status` with POST method: to update the status of a request  
4. `/process` with POST method: to trigger the main process to convert a website based on the input provided  
  
The flow starts whenever a client trigger `/process` with POST method along with the payload in JSON format. Below is the sample of the input payload:  
  
```json  
{  
    "request_url": "https://aws.github.io/copilot-cli/"  
}  
```  
  
The `request_url` is the website URL that we’d like to be converted into PDF, and in this case it refers to AWS Fargate product page.   
  
When the API received the request, it will save the data into Amazon DynamoDB and return a `request_ID` to the client. Moreover, `svc-api` will publish a message to a Amazon SNS topic with message attribute “ request_pdf_received”. Amazon SNS will then pass the message to Amazon SQS queue(s) who subscribed to this particular attribute. The request at this point, will be processed by `svc-worker`.   
  
As the PDF converting process runs asynchronously, the client will need to check the status of a respective request. To know the status of the request, the client needs to make another HTTP call to endpoint `/status/<request_ID>`  with GET method, where the <request_ID> is the ID client received previously.   
  
If the request is successfully completed, it return a response with following structure:  
  
```json  
{  
  "ID": “<request_ID>”,  
  "URL": "https://<signed_s3_url>”,  
  "request_completed": true,  
  "request_status": "Completed"  
}  
```  
  
### Review: svc-worker  
  
The main task for `svc-worker` is to standing by to any request published in the respective queue (handled by Amazon SQS) and process the request to convert the respective URL into a PDF and upload them into Amazon S3.   
  
When `svc-api` published the message into the topic on Amazon SNS, the message will be forwarded to a queue running on Amazon SQS. The `svc-worker` is doing a long-polling into the Amazon SQS queue, retrieve the message, process and finally delete the message.   
  
The main logic in the `svc-worker` is to convert the requested webpage from from the payload properties called `request_url`. Then, it will use `pdfkit` library to convert the web page into a PDF. The `pdfkit` itself is a wrapper library for `wkhtmltopdf`, to convert HTML to PDF using webkit. This dependency is explicitly declared on the Dockerfile.   
  
Once the service successfully converted the webpage into PDF, it will upload the file into Amazon S3. Then, it will generate a presigned URL to get the an access to the file within a specific time period (currently set to 3600 seconds).   
  
Upon completion, the service will update the request information to `svc-api` by calling the `status` endpoint with POST method. The JSON payload follows below structure:  
  
```json  
{  
  “request_ID": “<request_ID>”,  
  “request_output”: "https://<signed_s3_url>”,  
  "request_completed": true,  
  "request_status": "Completed"  
}  
```  
  
## Next Lab  
  
Click here to go to the next lab: [Lab 2: Configure and Deploy `svc-api`][1]  
  
  
[1]: https://github.com/donnieprakoso/workshop-copilot/tree/main/lab2-configure-and-deploying-svc-api  

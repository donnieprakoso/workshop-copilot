# Lab 2: Configure and Deploy `svc-api`  
  
In this lab, we are going to configure and deploy `svc-api` as the public facing API to interact with our application.  
  
## Task 1: Initialise Application  
  
To get started to deploy the applications, we need to initialize a new Copilot application. This would be the first task.  
  
- Open terminal  
- Navigate to `source/` folder  
- Run `copilot app init`  
  
This command creates a new application within the directory that will contain your services. When you run this command, Copilot will take you to a step-by-step guide by asking you questions.   
  
Follow the instructions below to complete this task:  
  
- Create a new application  
```  
Would you like to use one of your existing applications? (Y/n) n  
```  
  
- Naming the application  
```  
Use existing application: No  
  
Ok, let's create a new application then.  
What would you like to name your application? [? for help] test-webtopdf  
```  
  
- Choosing Load Balanced Web Service  
```  
Use existing application: No  
Application name: test-webtopdf  
  
  Which workload type best represents your architecture?  [Use arrows to move, type to filter, ? for more help]  
  
  > Load Balanced Web Service   (Internet to ECS on Fargate)  
  
```  
  
- Naming the service  
```  
Use existing application: No  
Application name: test-webtopdf  
Workload type: Load Balanced Web Service  
  
What do you want to name this Load Balanced Web Service? [? for help] svc-api  
```  
  
- Selecting the Dockerfile  
```  
Use existing application: No  
Application name: test-webtopdf  
Workload type: Load Balanced Web Service  
Service name: svc-api  
  
  Which Dockerfile would you like to use for svc-api?  [Use arrows to move, type to filter, ? for more help]  
  > svc-api/Dockerfile  
```  
  
- Don’t create an environment. AWS Copilot will create the application along for the first service: `svc-api` . At the end of the process, when Copilot asks if you’d like to deploy a test environment, choose “N (no)”. We are going to manually create the environment in the next task.  
  
```  
Use existing application: No  
Application name: test-webtopdf  
Workload type: Load Balanced Web Service  
Dockerfile: svc-api/Dockerfile  
Ok great, we'll set up a Load Balanced Web Service named svc-api in application test-webtopdf listening on port 8081.  
  
✔ Created the infrastructure to manage services and jobs under application test-webtopdf..  
  
✔ The directory copilot will hold service manifests for application test-webtopdf.  
  
✔ Wrote the manifest for service svc-api at copilot/svc-api/manifest.yml  
Your manifest contains configurations like your container size and port (:8081).  
  
✔ Created ECR repositories for service svc-api..  
  
  
  
All right, you're all set for local development.  
  
Would you like to deploy a test environment? [? for help] (y/N) N  
```  
  
- Congrats! You’ve successfully created a new Copilot application and a service. You'll notice that AWS Copilot created a manifest file for your service with path `copilot/svc-api/manifest.yml`.  
- Please proceed to the next task.  
  
## Task 2: Create environment — staging  
  
Link: [aws.amazon.com/blogs/containers/amazon-ecs-availability-best-practices/][1]  
  
In this task, we are going to create an environment. You can create an environment upon `copilot app init` execution. However, we are going to separate that particular task so we know how to manually create an environment as well as understanding few important flags.   
  
- Open terminal  
- Navigate to `source/` folder  
- Run `copilot env init`  
  
Follow the instructions below to complete this task:  
  
- Naming the environment  
  
```  
What is your environment's name? [? for help] staging  
```  
  
- Use default profile  
  
```   
Which credentials would you like to use to create staging?  [Use arrows to move, type to filter, ? for more help]  
    Enter temporary credentials  
  > [profile default]  
```  
  
- Use default configuration with new VPC  
  
```  
Credential source: [profile default]  
  
  Would you like to use the default configuration for a new environment?  
    - A new VPC with 2 AZs, 2 public subnets and 2 private subnets  
    - A new ECS Cluster  
    - New IAM Roles to manage services and jobs in your environment  
  [Use arrows to move, type to filter]  
  > Yes, use default.  
    Yes, but I'd like configure the default resources (CIDR ranges).  
    No, I'd like to import existing resources (VPC, subnets).  
```  
  
Creating the environment with a new VPC in 2 AZs, 2 public subnets and 2 private subnets is one of the best practice. For more information, you can read the blog titled [“Amazon ECS availability best practices”]( https://aws.amazon.com/blogs/containers/amazon-ecs-availability-best-practices/).   
  
However, you also have the option to import existing resource.   
If you’d like to import existing resource, you will need the VPC ID. To get the VPC ID using `aws cli`, use following command:  
  
```bash  
aws ec2 describe-vpcs --filters Name=isDefault,Values=true --query 'Vpcs[0].VpcId'  
```  
  
- Copilot will create all required resources for the environment. At the end of the process, you will see following outputs.   
  
```  
Credential source: [profile default]  
Default environment configuration? Yes, use default.  
✔ Linked account XXXXXXXXX and region ap-southeast-1 to application test-webtopdf..  
  
✔ Proposing infrastructure changes for the test-webtopdf-staging environment.  
- Creating the infrastructure for the test-webtopdf-staging environment.  [create complete]  [87.1s]  
  - An IAM Role for AWS CloudFormation to manage resources                [create complete]  [26.6s]  
  - An ECS cluster to group your services                                 [create complete]  [8.6s]  
  - Enable long ARN formats for the authenticated AWS principal           [create complete]  [1.0s]  
  - An IAM Role to describe resources in your environment                 [create complete]  [26.4s]  
  - A security group to allow your containers to talk to each other       [create complete]  [5.4s]  
  - An Internet Gateway to connect to the public internet                 [create complete]  [15.2s]  
  - Private subnet 1 for resources with no internet access                [create complete]  [18.6s]  
  - Private subnet 2 for resources with no internet access                [create complete]  [18.6s]  
  - Public subnet 1 for resources that can access the internet            [create complete]  [15.5s]  
  - Public subnet 2 for resources that can access the internet            [create complete]  [15.5s]  
  - A Virtual Private Cloud to control networking of your AWS resources   [create complete]  [15.2s]  
✔ Created environment staging in region ap-southeast-1 under application test-webtopdf.  
```  
  
- Congrats! You’ve successfully created an environment. Please proceed to the next task.  
  
## Task 3: Add environment variable AWS_REGION  
  
In this task, you’ll learn how to add an environment variable into your service. We’re going to add a variable called `AWS_REGION` into `svc-api`. In the first task, we’ve created the application along with the `svc-api` service. For every service initialized with Copilot, it will create a manifest file in this location `copilot/<SERVICE_NAME>/manifest.yaml`.  
  
- Open `copilot/svc-api/manifest.yml`  
- Navigate to the end of the file and add following lines:  
  
```  
environments:  
  staging:  
    variables:  
      AWS_REGION: ap-southeast-1  
```  
  
## Task 4: Add SNS Topic to svc-api  
  
In this task, we will begin the first stage on implementing Pub/Sub architecture for our application with AWS Copilot. The implementation of Pub/Sub consists of Amazon SNS Topic and Amazon SQS Queue creation. We will start to add Amazon SNS Topic in this task and on the next lab, when we configure the `svc-worker` we will add integration for SQS.   
  
- Open `copilot/svc-api/manifest.yml`  
- Navigate to the end of the file and add following lines:  
  
```  
publish:  
  topics:  
    - name: requests  
```  
  
With above lines, we define an Amazon SNS Topic called `requests`. When we deploy this service, AWS Copilot will create an environment variable called `COPILOT_SNS_TOPIC_ARNS`. From there, we need to configure our application to retrieve the Amazon SNS Topic ARN by loading the environment variable.  
  
## Task 5: Modify svc-api to add COPILOT_SNS_TOPIC_ARNS  
  
In this task, you will need to evaluate the code on how that you can get the environment variable called `COPILOT_SNS_TOPIC_ARNS` to retrieve the Amazon SNS Topic ARNs.   
  
This task requires NO action from your end. You only need to evaluate on how to use the environment variable so `svc-api` can publish the message to the respective topic.  
  
1. Open `svc-api/app.py`  
2. In the beginning of the code, after imports, you will see following line:  
  
```python  
SNS_ARN = json.loads(os.getenv('COPILOT_SNS_TOPIC_ARNS'))  
```  
  
To retrieve the environment variable, we use the `os.getenv()` function. Furthermore, to properly load the variable, we are using `json.loads()` function as Copilot will inject the SNS Topic ARNs with following format:  
  
```json  
{  
    “<TOPIC_NAME>”:”<TOPIC_ARN>”  
}  
```  
  
4. Go to `process` function  
5. Evaluate following lines:  
  
```python  
resp_sns = sns_client.publish(  
            TopicArn=SNS_ARN["requests"],  
            Message=json.dumps(  
                {"payload": {"request_ID": request_id, "request_url": req["request_url"]}}))  
```  
  
To publish the message into Amazon SNS Topic, we use `publish()` function from `sns_client` object.   
  
<del>For this application, we are using Message Filtering. The `MessageAttributes` field includes attributes `event` with a string value `request_pdf_received`. With this filter policy, we can let our `svc-worker` to receive a subset of the messages.  
  
To learn more about Message Filtering on Amazon SNS, please visit this [documentation link]( [docs.aws.amazon.com/sns/latest/dg/sns-message-filtering.html][1] ). </del>  
  
## Task 6: Add DynamoDB to svc-api  
  
With AWS Copilot, you can also add database and Amazon S3 bucket for your service. The `copilot storage` command will create a Cloudformation template into `addons` folder for respective service.   
  
In this task, you’ll learn how to add Amazon DynamoDB for `svc-api`.   
  
- Open terminal  
- Navigate to `source/` folder  
- Run `copilot storage init` command. This will trigger guided experience and please follow the instructions below:  
  
- Selecting service `svc-api`  
  
```  
Which workload would you like to associate with this storage resource?  [Use arrows to move, type to filter]  
  > svc-api  
    svc-worker  
```  
  
- Choose DynamoDB  
  
```  
Name: svc-api  
  
What type of storage would you like to associate with svc-api?  [Use arrows to move, type to filter, ? for more help]  
  > DynamoDB            (NoSQL)  
    S3                  (Objects)  
    Aurora Serverless   (SQL)  
```  
  
- Naming DynamoDB table to `pdf-requests`  
  
```  
Storage type: DynamoDB  
  
What would you like to name this DynamoDB Table? [? for help] pdf-requests  
```  
  
- Name partition key to `REQUEST_ID`  
  
```  
Storage type: DynamoDB  
Storage resource name: pdf-requests  
  
What would you like to name the partition key of this DynamoDB? [? for help] REQUEST_ID  
```  
  
- Select `String` as the datatype for the partition key  
  
```  
Storage type: DynamoDB  
Storage resource name: pdf-requests  
Partition key: REQUEST_ID  
  
What datatype is this key?  [Use arrows to move, type to filter, ? for more help]  
  > String  
    Number  
    Binary  
```  
  
- Choose NO for adding sort key  
  
```  
Storage type: DynamoDB  
Storage resource name: pdf-requests  
Partition key: REQUEST_ID  
Partition key datatype: String  
  
Would you like to add a sort key to this table? [? for help] (y/N) N  
```  
  
Copilot will create the Cloudformation template as an addon with following path: `copilot/svc-api/addons/pdf-requests.yml`.   
  
You’ll see a similar output from Copilot at the end of this process.  
  
```  
Storage type: DynamoDB  
Storage resource name: pdf-requests  
Partition key: REQUEST_ID  
Partition key datatype: String  
Sort key? No  
✔ Wrote CloudFormation template for DynamoDB Table pdf-requests at copilot/svc-api/addons/pdf-requests.yml  
  
Recommended follow-up actions:  
  - Update svc-api's code to leverage the injected environment variable PDFREQUESTS_NAME.  
For example, in JavaScript you can write `const storageName = process.env.PDFREQUESTS_NAME`.  
  - Run `copilot deploy --name svc-api` to deploy your storage resources.  
```  
  
- Note the environment variable name: `PDFREQUESTS_NAME`  
  
## Task 7: Modify svc-api to add DynamoDB Table  
  
As we just configured a DynamoDB table for `svc-api` service, in this task you will need to evaluate how to use the environment variable so we can interact with DynamoDB Table.  
  
This task requires NO action from your end. You only need to evaluate on how to use the environment variable so `svc-api` able to interact with DynamoDB table.  
  
- Open `svc-api/app.py`  
- In the beginning of the code, after imports, you will see following line:  
  
```python  
DYNAMODB_TABLE = os.getenv("PDFREQUESTS_NAME")  
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)  
```  
  
The environment variable name is based on the output when we completed the `copilot storage init` in the previous task. In the next line, we instantiated a DynamoDB object along with the region we are connecting to.  
  
- Go to `save_request_received()` function.   
  
```python  
def save_request_received(data):  
    dynamodb_table = dynamodb.Table(DYNAMODB_TABLE)  
```  
  
In this function, we are using the environment variable to specify the table name we need to interact with.  
  
## Task 8: Deploy svc-api to staging environment  
  
In this task, you’ll deploy the `svc-api` into the `staging` environment. To deploy the `svc-api`, you   
  
- Open terminal  
- Navigate to the `source/` folder  
- Run `copilot svc deploy --name svc-api`  
  
If you don’t specify the service name using `--name` flag, Copilot will ask you the service name that you’d like to deploy.   
  
As we only have an environment, Copilot will automatically deploy to the `staging` environment. If you have multiple environments, Copilot will ask you into which environment you’d like to deploy or you can specify the environment name by passing `--env` flag.   
  
This process requires roughly 6-8 mins to complete. It’s time to have a break ☕️.  
  
## Task 9: Check the svc-api environment  
  
In this task, you’ll learn how to get the details of the `svc-api`. Once that you have the service deployed, you can see the details of the service by running `copilot svc show` command.   
  
- Open terminal  
- Navigate to `source/` folder  
- Run `copilot svc show --name svc-api`  
  
Copilot will return similar output:  
  
```  
About  
  
  Application       test-webtopdf  
  Name              svc-api  
  Type              Load Balanced Web Service  
  
Configurations  
  
  Environment       Tasks               CPU (vCPU)          Memory (MiB)        Port  
  -----------       -----               ----------          ------------        ----  
  staging           1                   0.25                512                 8081  
  
Routes  
  
  Environment       URL  
  -----------       ---  
  staging           http://XXXXXXXXXX.ap-southeast-1.elb.amazonaws.com  
  
Service Discovery  
  
  Environment       Namespace  
  -----------       ---------  
  staging           svc-api.staging.test-webtopdf.local:8081  
  
Variables  
  
  Name                                Container           Environment         Value  
  ----                                ---------           -----------         -----  
  COPILOT_APPLICATION_NAME            svc-api             staging             test-webtopdf  
  COPILOT_ENVIRONMENT_NAME              "                   "                 staging  
  COPILOT_LB_DNS                        "                   "                 XXXXXXXXXX.ap-southeast-1.elb.amazonaws.com  
  COPILOT_SERVICE_DISCOVERY_ENDPOINT    "                   "                 staging.test-webtopdf.local  
  COPILOT_SERVICE_NAME                  "                   "                 svc-api  
  COPILOT_SNS_TOPIC_ARNS                "                   "                 {"requests":"arn:aws:sns:ap-southeast-1:XXXXXXXXXX:test-webtopdf-staging-svc-api-requests"}  
```  
  
## Next Lab  
  
Click here to go to the next lab: [Lab 3: Configure and Deploy `svc-worker`][2]  
  
  
[1]: https://aws.amazon.com/blogs/containers/amazon-ecs-availability-best-practices/  
[2]: https://github.com/donnieprakoso/workshop-copilot/tree/main/lab3-configure-and-deploying-svc-worker  

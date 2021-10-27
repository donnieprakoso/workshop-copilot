## 🚀 Welcome to AWS Copilot Workshop  
  
In this workshop, you'll learn how to build, release and operate your containerised applications to [Amazon ECS][1] and [AWS Fargate][2] using [AWS Copilot][3].  
  
### Tl;dr Get Started!  
  
Click here to [Get Started with Labs][4]  
  
## 💻 What we are going to build  
  
In this workshop, we are going to deploy an API to convert a website page into a PDF. We are using containers to build the application and deploy them into Amazon ECS using AWS Fargate as the computing option.  
  
### Show me how it looks like!  
  
Here’s a quick look on what you’re going to build.   
  
![Quick Look][5]  
  
### Diagram architecture  
  
This is the full diagram architecture that we will build in this workshop.   
  
![Diagram Architecture][6]  
  
There are 2 main components in this applications, 1) internet facing API, and 2) private worker to process request. The API is responsible to handle to validate and process the initial request. The API then will publish a topic with message "request_received" to Amazon SNS.  
  
### How does it work?  
  
The flow works when we trigger HTTP POST method with JSON payload to the API endpoint `/process`. As the system is running on asynchronous communication between services, we won't get the PDF immediately. The return response from `/process` would be a request ID. In order to get the PDF file, we need to pass the request ID to the `/status/<request_ID>` endpoint. Using that endpoint, we can also check the status of the request.  
  
To build the application, defining the release pipeline and operate the application, we will be using AWS Copilot. AWS Copilot is an open-source CLI tool that makes it easy for us to run containers on AWS. If you'd like to know more about AWS Copilot, please refer to the   
[documentation page][7].   
  
To understand how we can build and operate our containerized applications, the workshop is break down into 5 labs. The labs provided in this workshop are structured to build understanding how to use AWS Copilot from ground up.  
  
## 📖 About This Workshop  
  
This is L100-300 workshop and specifically structured for developers from any levels.  
  
## ✅ Requirements  
  
This workshop requires following applications and tools properly configured. Please follow the instruction provided on the links for each applications/tools.  
  
### 1. AWS CLI  
  
The AWS Command Line Interface (CLI) is a unified tool to manage your AWS services. With just one tool to download and configure, you can control multiple AWS services from the command line and automate them through scripts.  
  
There are 2 versions of the AWS CLI, and we strongly recommend for you to use AWS CLI version 2.  
  
[https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)  
  
### 2. AWS credentials  
  
Once that you have your AWS CLI installed, you also need to configure the settings. The configurations that you need to configure includes your security credentials, the default output format, and the default AWS Region.   
  
[https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)  
  
### 3. Docker Desktop  
  
Docker is required in this workshop as we are going to package the application using Docker and Amazon ECS will run the application using Docker engine.  
  
[https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)  
  
### 4. Copilot CLI  
  
The AWS Copilot CLI is a tool for developers to build, release and operate production ready containerized applications. At the point of building this workshop, AWS Copilot supports deployment to AWS AppRunner, Amazon ECS and AWS Fargate.  
  
If you have homebrew installed on your platform, you can use following command to install AWS Copilot  
  
```  
brew install aws/tap/copilot-cli  
```  
  
Otherwise, you need to follow the instructions listed on this page [https://github.com/aws/copilot-cli](https://github.com/aws/copilot-cli) to install AWS Copilot for your platform.  
  
## ⚠️ Cleaning Up  
  
This workshop uses AWS services that are mostly covered by the Free Tier allowance - ONLY if your account is less than 12 months old. For accounts passed the free tier eligibility, it may incur some costs. To minimize the cost, make sure you **delete resources used in this workshop when you are finished**.  
  
Please refer to Lab 5: Cleaning Up for more information.
  
## 💻 Let's Get Started!  
  
If you have all the requirements needed to run this workshop, now it's time to deploy some apps!  
  
[Get Started!][8]  
  
  
[1]: https://aws.amazon.com/ecs/  
[2]: https://aws.amazon.com/fargate/  
[3]: https://aws.github.io/copilot-cli/  
[4]: https://github.com/donnieprakoso/workshop-copilot/tree/main/lab1-getting-started  
[5]: https://gitcdn.link/repo/donnieprakoso/workshop-copilot/main/assets/Event_20211123_MADWorkshop_AWS%20Copilot.gif  
[6]: https://gitcdn.link/repo/donnieprakoso/workshop-copilot/main/assets/Container-ECS-WebToPdf-App.png  
[7]: https://aws.github.io/copilot-cli/  
[8]: https://github.com/donnieprakoso/workshop-copilot/tree/main/lab1-getting-started  

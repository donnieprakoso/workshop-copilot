# Lab 5: Cleaning up ⚠️

This workshop uses AWS services that are mostly covered by the Free Tier allowance - ONLY if your account is less than 12 months old. For accounts passed the free tier eligibility, it may incur some costs. To minimize the cost, make sure you **delete resources used in this workshop when you are finished**.  
  
Please follow the steps outlined below to clean up all resources:  

## Task 1: Empty Amazon S3 Bucket

First thing first, you need to make sure to empty the Amazon S3 bucket associated with this workshop. To do this, you need to manually delete all the objects within the S3 Bucket. 

- Open [Amazon S3 Dashboard](https://s3.console.aws.amazon.com/)
- Find buckets with keyword: `s3-pdf-requests` or your application name (in this case `test-webtopdf`)
- Empty the bucket

Then, you'll need to select the bucket and click on the empty button. The image below illustrates how you can do this.
![Select and Empty the bucket](https://gitcdn.link/repo/donnieprakoso/workshop-copilot/main/assets/lab5-cleaning-selectbucket.png)

- Confirm the process

You'll be redirected to a page to confirm the deletion.

![Permanently Delete](https://gitcdn.link/repo/donnieprakoso/workshop-copilot/main/assets/lab5-cleaning-permanentdelete.png)

## Task 2: Delete the application

Once that you have your Amazon S3 bucket emptied, you can delete the application and all the resources using `copilot app delete` command.

- Go to your AWS Copilot application folder  
- Run `copilot app delete`

This command will delete all associated resources that you've created during the workshop.

- Follow the instructions

At the end of the process, you'll see a similar output.

```
 Are you sure you want to delete application test-webtopdf? Y [? for help] (Y/n)

✔ Deleted service svc-api from environment staging..
✔ Deleted resources of service svc-api from application test-webtopdf..
✔ Deleted service svc-api from application test-webtopdf.
✔ Deleted service svc-worker from environment staging..
✔ Deleted resources of service svc-worker from application test-webtopdf..
✔ Deleted service svc-worker from application test-webtopdf.
✔ Deleted environment staging from application test-webtopdf..
✔ Cleaned up deployment resources..
✔ Deleted application resources..
✔ Deleted application configuration.
✔ Deleted local .workspace file.

```   

In situation that AWS Copilot wasn't able to remove all resources, you need to check your [AWS CloudFormation dashboard](https://ap-southeast-1.console.aws.amazon.com/cloudformation) and manually delete the stack(s).  
  
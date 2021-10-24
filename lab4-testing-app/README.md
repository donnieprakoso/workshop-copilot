# Lab 4: Testing Application
  
Congrats! At this point, you have deployed all required services as well as configuring them to run properly. In this lab, you’ll learn how to test the application.  
  
## Task 1: Test svc-api health check endpoint  
  
In this task, you will check the status of the `svc-api` by invoking the `/ping` endpoint.   
  
- Open terminal  
- Navigate to `source/` folder  
- Get the ALB address for `svc-api` by running below command:  
  
```bash  
copilot svc show --name svc-api  
```  
  
In `Routes` section, you will see a similar output as below:  
  
```  
Routes  
  
  Environment       URL  
  -----------       ---  
  staging           http://xxxxxxxx.ap-southeast-1.elb.amazonaws.com  
  
```  
This is the public address of your `svc-api`. Copy the URL as we need it for the next step.  
  
- Use `curl` to call the `/ping` endpoint.   
  
```bash  
curl <SVC_API>/ping  
```  
  
You will have an output as below:  
  
```json  
{  
  "value": "ok"  
}  
```  
  
This means that your `svc-api` is working properly.  
  
## Task 2: Request URL to convert to PDF  
  
In this task, you will initiate a request to convert a web page URL into PDF.   
  
- Create a JSON file called `test.json` with following lines:  
  
```json  
{  
    "request_url": " https://aws.github.io/copilot-cli/“  
}  
```  
  
- Call `/process` with POST method and `test.json` as the input file  
  
```bash  
 curl -X POST http://SVC_API_ADDRESS/process -d @test.json --header "Content-Type: application/j  
son"  
```  
  
You’ll receive a `request_ID`.  
  
```json  
{  
  "request_ID": "4f35c25e-6795-4fcc-831c-bbce8eee35e9"  
}  
  
```  
  
- Copy the `request_ID`   
- Call `/status/<request_ID>` with GET method and replace it with the request_ID.   
  
```bash  
curl http://test-Publi-1DUCRLGDH3HTQ-766999690.ap-southeast-1.elb.amazonaws.com/status/4f35c25e-6795-4fcc-831c-bbce8eee35e9  
```  
  
The response will similar as below:  
  
```json  
{  
  "ID": "4f35c25e-6795-4fcc-831c-bbce8eee35e9",  
  "URL": “https://Amazon-S3-URL”,  
  "request_completed": true,  
  "request_status": "Completed"  
}  
```  
  
- Congrats! Your application works properly. Now if you copy the URL property and open it with your browser, you will have your PDF.  
  

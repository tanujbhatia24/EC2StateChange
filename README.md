# Monitor EC2 Instance State Changes Using AWS Lambda, Boto3, and SNS
## Overview
This project sets up an AWS Lambda function that listens for EC2 instance state changes (e.g., `running`, `stopped`) and sends an email notification using Amazon SNS.
---

## Components Used
- **AWS Lambda** – to run the function in response to EC2 events.
- **Amazon EventBridge** – to detect EC2 instance state changes.
- **Amazon SNS (Simple Notification Service)** – to send email notifications.
- **IAM** – to grant Lambda permission to access EC2 and SNS.
---

## Setup Instructions
### 1. Create SNS Topic and Subscription
1. Navigate to the **SNS Console** → **Topics** → `Create topic`.
2. Choose **Standard** and name it, e.g., `EC2StateChangeTopic_tanuj`.
3. Click `Create topic`.
4. On the topic page, click `Create subscription`:
   - **Protocol**: Email
   - **Endpoint**: Your email address
5. Confirm the subscription via the email sent to you.
---

### 2. Create IAM Role for Lambda
1. Go to **IAM** → **Roles** → `Create Role`.
2. Choose **Lambda** as the trusted service.
3. Attach the following policies:
   - `AmazonEC2ReadOnlyAccess`
   - `AmazonSNSFullAccess`
   - `AWSLambdaBasicExecutionRole` (for logging)
4. add the ec2:CreateTags permission to your Lambda's IAM role.
   - Go to the IAM Console → Roles.
   - Search and select your role: tanuj_LambdaEC2SNSRole.
   - Click Add permissions → Attach policies.
   - Choose Create policy (if needed) with the following content:
     ```bash
        {
           "Version": "2012-10-17",
           "Statement": [
             {
               "Effect": "Allow",
               "Action": [
                  "ec2:CreateTags"
               ],
               "Resource": "*"
             }
           ]
         }
     ```
5. Name the role `LambdaEC2SNSRole`.
---

### 3. Create the Lambda Function
1. Go to **Lambda Console** → `Create function`.
2. Choose:
   - Name: `EC2StateChangeNotifier`
   - Runtime: `Python 3.12`
   - Execution role: Use existing role → `tanuj_LambdaEC2SNSRole`
3. Lambda Code
   - You can use the below file for reference.<br>
     [EC2StateChange_tanuj.py](https://github.com/tanujbhatia24/EC2StateChange/blob/main/EC2StateChange_tanuj.py)
   - Add a new resource-based policy
4. Under Configuration → Environment variables:
   - Key: SNS_TOPIC_ARN
   - Value: Paste the ARN of your SNS topic.
---

### 4. Create EventBridge Rule
1. Go to EventBridge → Rules → Create rule.
2. Name: EC2StateChangeRule_tanuj
3. Define the event pattern:
  ```bash
     {
      "source": ["aws.ec2"],
      "detail-type": ["EC2 Instance State-change Notification"],
      "detail": {
      "state": ["running", "stopped"]
        }
      }
  ```
4. Add a target:
- Target type: Lambda
- Function: EC2StateChangeNotifier_tanuj
- Click Create.
---

## Testing
1. Go to EC2 Console.
2. Start or stop an instance.
3. You should receive an email notification with the instance ID and new state.
---

## Notes
- You can modify the Lambda function to include additional data such as region, timestamp, or instance tags.
- To monitor more states (like pending, terminated), simply update the EventBridge rule.
---

## Screenshots
- SNS Topic<br>
![image](https://github.com/user-attachments/assets/478bb9b3-d28d-46b8-b3a7-86352293f4fe)<br>
- IAM role with permissions<br>
![image](https://github.com/user-attachments/assets/c2ce25f1-a101-4615-98db-8759ae99eca3)<br>
- Lambda function, trigger and resource-based policy<br>
![image](https://github.com/user-attachments/assets/8cae2462-1dba-40a4-b4f0-9631ffdd1654)<br>
![image](https://github.com/user-attachments/assets/45f897e9-cce3-4be4-9071-695b3010201c)<br>
- EventBridge Rule Setup<br>
![image](https://github.com/user-attachments/assets/0f61a560-3a22-4791-bf12-2e98877e3660)<br>
- Start & Stop EC2 Instance<br>
![image](https://github.com/user-attachments/assets/2f8a89a0-c75a-4776-ba9b-4c2a91b24c93)<br>
- SNS Notification Received<br>
![image](https://github.com/user-attachments/assets/937c8918-75af-47b4-a177-eb426b0bc51e)<br>
---

## License
This project is intended for educational and demonstration purposes. You are welcome to use and adapt it as a reference; however, please ensure that your work represents your own understanding and is not reproduced verbatim.

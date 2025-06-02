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
2. Choose **Standard** and name it, e.g., `EC2StateChangeTopic`.
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
4. Name the role `LambdaEC2SNSRole`.
---

### 3. Create the Lambda Function
1. Go to **Lambda Console** → `Create function`.
2. Choose:
   - Name: `EC2StateChangeNotifier`
   - Runtime: `Python 3.12`
   - Execution role: Use existing role → `LambdaEC2SNSRole`
3. Lambda Code
   You can use the below file for reference.<br>
   [EC2StateChange_tanuj.py](https://github.com/tanujbhatia24/EC2StateChange/blob/main/EC2StateChange_tanuj.py)
4. Under Configuration → Environment variables:
   - Key: SNS_TOPIC_ARN
   - Value: Paste the ARN of your SNS topic.
---

### 4. Create EventBridge Rule
1. Go to EventBridge → Rules → Create rule.
2. Name: EC2StateChangeRule
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
- Email Confirmation<br>
- IAM role with permissions<br>
- Lambda function<br>
- Lambda test execution<br>
- EventBridge Rule Setup<br>
- Start & Stop EC2 Instance<br>
- SNS Notification Received<br>
- Example Email Notification<br>
---

## License
This project is intended for educational and demonstration purposes. You are welcome to use and adapt it as a reference; however, please ensure that your work represents your own understanding and is not reproduced verbatim.

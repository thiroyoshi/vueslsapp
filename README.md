# Vue + Serverless Framework App

## Description

This is the serverless application framework using Vue.js and Serverless Framework.

You can build the application that you can ...

- sign up
- log in
- register userinfo
- change password
- delete account
- reset password
- call REST API with authentication

## Requirements

- node.js
- Vue.js
- python 3.7
- AWS CLI
- Serverless Framework 1.6 >=

## Building

This is the step of building the app at your local.

### set up AWS account

- sign up AWS
- create AWS IAM user for building app and get access key and secret access key

### get your domain, create Hosted zone and create a certificate

- buy your own domain
  - you can buy it in Route53 
- create Hosted Zone in Route53
- get Alias Hosted Zone ID
  - Not Hosted Zone ID
- create a certificate in ACM
  - recommend to use DNS Confirmation

### create User Pool and Identity Pool

- create User Pool and Identity Pool for each env
- copy ClientId, UserPoolId and IdentityPoolId to 
  - for Vue : .env.xxx
  - for serverless : sls_configuration/config/xxx/cognito.yml

### create Serverless Dashboard account and app

- sign up serverless dashboard
  - https://serverless.com/dashboard/
- create app in Serverless Dashboard
  - app name must be same as `app` in serverless.yml
- get serverless access key

### create a tracking ID of Google Analytics (optional)

- create account and get tracking ID

### set environment vars

- set below vars to environment vars
  - AWS access key
  - AWS secret access key
  - AWS default region
  - Serverless Access key

### set configurations

- for client app
  - edit .env.XXX and set vars
    - NODE_ENV : for example, dev or prod
    - VUE_APP_API_ORIGIN : your custom domain name for REST API
    - VUE_APP_COGNITO_REGION : your region
    - VUE_APP_GOOGLE_ANALYTICS : optional, tracking Id

- for backend(REST API)
  - sls_configuration/config/common.yml
    - edit and set below vars
      - ACCOUNT_ID : AWS Account ID
      - DOMAIN : your own domain name you bought
      - ALIAS_HOSTED_ZONEID : you can get this in Route53
      - ALIAS_DNS_NAME : you can get this in Route53
  - serverless.yml
    - you must decide and edit `org`, `app`, `service`
    - `app` must be same as app name you crated in Serverless Dashboard

### install required softwares and libs

- install required softwares
  - serverless framework
    ```
    npm install -g serverless
    ```
  - pip-tools
    ```
    pip install pip-tools
    ```
  - aws cli
    - ref: `https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/install-cliv2-windows.html`
- install libs
  - node modules
    ```
    npm install
    ```
  - python libs
    ```
    pip-compile requirements.in
    ```
    ```
    pip install -r requirements.txt -t pylibs
    ```

### build app at local and deploy to AWS

- build vue app
  - for Dev env
    ```
    npm run build-dev
    ```
  - for Prod env
    ```
    npm run build-prod
    ```
- create custom domain for API Gateway
  ```
  sls create_domain
  ```
- deploy serverless app
  ```
  sls deploy
  ```

## Reference
- Vue.js : https://vuejs.org
- Serverless Framework : https://serverless.com/
- AWS : https://aws.amazon.com/
- AWS Custom Authorizer : https://dev.classmethod.jp/cloud/aws/verify_cognit_idtoken_by_apig_custom_auth/

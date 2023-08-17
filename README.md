# Account and Password Management

## Setup Steps
### 1.Pull docker image
docker hub link :  https://hub.docker.com/r/aderli26/account_management
```
docker pull aderli26/account_management
```
### 2. Run docker
```
docker run -p 5000:5000 --name account_api aderli26/account_management
```

## API URL & SPEC
###  1.Create Account

#### Request Method
| Method | URL  | 
|-------|:-----:|
| POST   |  http://127.0.0.1:5000/register |

#### Request Body
Content-Type : application/json
| Parameter | Type  | Description   |
|-------|:-----:|:-----:|
| username   | String| minimum length of 3 characters and a maximum length of 32 characters |
| password   | String| minimum length of 8 characters and a maximum length of 32 characters, containing at least 1 uppercase letter, 1 lowercase letter, and 1 number.| 

#### Response body example
Content-Type : application/json
```json
Success example :
StatusCode:200
{
    "reason": "Successfully registered",
    "success": true
}

Create fail example :
StatusCode:200
{
    "reason": "Username already exists",
    "success": false
}
```
---
###  2.Verify Account

#### Request Method
| Method | URL  | 
|-------|:-----:|
| POST   |  http://127.0.0.1:5000/login |

#### Request Body
Content-Type : application/json
| Parameter | Type  | Description   |
|-------|:-----:|:-----:|
| username   | String| minimum length of 3 characters and a maximum length of 32 characters |
| password   | String| minimum length of 8 characters and a maximum length of 32 characters, containing at least 1 uppercase letter, 1 lowercase letter, and 1 number.| 

#### Response body example
Content-Type : application/json
```json
Success example :
StatusCode:200
{
    "reason": "Successfully verified",
    "success": true
}

Verify fail example :
StatusCode:200
{
    "reason": "Wrong password",
    "success": false
}

Verify fail to five times example:
StatusCode:403
{
    "reason": "Please wait for one minute",
    "success": false
}
```


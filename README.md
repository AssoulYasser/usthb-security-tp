# Project Description
Todo()

## GET
`same ip address only - Web page` [/tp3/users/](#get-1billingretrieve-billing-datajson) <br/>

## POST
[/tp3/get-rsa-key/]() <br/>
[/tp3/login/]() <br/>
[/tp3/email-two-factor-authentication/]() <br/>
[/tp3/verify-email-two-factor-authentication/]() <br/>
[/tp3/face-recognition-factor/]() <br/>
[/tp3/android-id/]() <br/>
___

### POST tp3/get-rsa-key/
Check if the user is registered and returns RSA public key if so.

**Parameters**

|          Name | Required |  Type  | Description   |
|--------------:|:--------:|:------:|---------------|
|       `email` |   true   | string | User's email. |

**Response**

###### If user has found
```
status = 200 OK STATUS 
data = {
    "public_key": string
}
```
###### If user has not found
```
status = 404 NOT FOUND STATUS
```
___
###### If user has been blocked
```
status = 423 LOCKED STATUS
```
___

### POST /tp3/login/
To validate password for the first factor authentication.

**Parameters**

|       Name | Required |        Type        | Description      |
|-----------:|:--------:|:------------------:|------------------|
|    `email` |   true   |       string       | User's email.    |
| `password` |   true   | string `Encrypted` | User's password. |

**Response**
###### If user has not found
```
status = 404 NOT FOUND STATUS 
```
###### If encryption is not valid
```
status = 422 UNPROCESSABLE_CONTENT_STATUS
```
###### If password is correct
```
status = 200 OK STATUS
```
###### If password is incorrect
```
status = 401 UNAUTHORIZED
```
###### If password hasn't completed authentication proccess in time
```
status = 408 TIMEOUT
```
___

### POST /tp3/email-two-factor-authentication/
Request a validation code to user's email.

**Parameters**

|       Name | Required |        Type        | Description      |
|-----------:|:--------:|:------------------:|------------------|
|    `email` |   true   |       string       | User's email.    |

**Response**

###### If email has been sent successfully
```
status = 200 OK STATUS
```
###### If email has not been sent
```
status = 500 SERVER ERROR STATUS
```
___
###### If password hasn't completed authentication process in time
```
status = 408 TIMEOUT
```

### POST /tp3/verify-email-two-factor-authentication/
Check if the received code is the same as the code has been sent to the email.

**Parameters**

|    Name | Required |  Type  | Description                            |
|--------:|:--------:|:------:|----------------------------------------|
| `email` |   true   | string | User's email.                          |
|  `code` |   true   |  int   | code that has been sent through email. |

**Response**

###### If the code match the email
```
status = 200 OK STATUS
```
###### If the code didn't match the email
```
status = 401 UNAUTHORIZED
``` 
###### If password hasn't completed authentication proccess in time
```
status = 408 TIMEOUT
```

### POST /tp3/face-recognition-factor/
Check face id for the user.

**Parameters**

|    Name | Required |    Type    | Description   |
|--------:|:--------:|:----------:|---------------|
| `email` |   true   |   string   | User's email. |
| `image` |   true   | image file | User's face.  |

**Response**

###### If model failed to recognize a face
```
status = 422 UNPROCESSABLE_CONTENT_STATUS
```
###### If the face id has been validated
```
status = 200 OK STATUS
``` 
###### If the face id has not been validated
```
status = 401 UNAUTHORIZED
``` 
###### If password hasn't completed authentication proccess in time
```
status = 408 TIMEOUT
```
### POST /tp3/android-id/
Check face id for the user.

**Parameters**

|    Name | Required |  Type  | Description       |
|--------:|:--------:|:------:|-------------------|
| `email` |   true   | string | User's email.     |
| `android_id` |   true   | string | User's device id. |

**Response**

###### If model failed to recognize a face
```
status = 422 UNPROCESSABLE_CONTENT_STATUS
```
###### If the face id has been validated
```
status = 200 OK STATUS
``` 
###### If the face id has not been validated
```
status = 401 UNAUTHORIZED
``` 
###### If password hasn't completed authentication proccess in time
```
status = 408 TIMEOUT
```
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
status = 200
data = {
    "public_key": string
}
```
###### If user has not found
```
status = 404
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
status = 404
```
###### If encryption is not valid
```
status = 422
```
###### If password is correct
```
status = 200
```
###### If password is incorrect
```
status = 401
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
status = 200
```
###### If email has not been sent
```
status = 500
```
___

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
status = 200
```
###### If the code didn't match the email
```
status = 401
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
status = 422
```
###### If the face id has been validated
```
status = 200
``` 
###### If the face id has not been validated
```
status = 401
``` 
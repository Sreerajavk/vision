# API Documentation

Secure vision provide endponints for developers. This can be used to integrate Secure Vision into your project.

# Allowed HTTP method

POST    : Update resource \
GET     : Get a resource or list of resources

# API endpoints

## USER LOGIN

**URL** : `/api/app_login/`

**Method** : `POST`

**Auth required** : NO

**Permissions required** : None

**Data constraints**

Provide username and password.

```json
{
    "username" : "username",
    "password" : "password"
}
```


## Success Response

**Condition** : If everything is OK and an Account  exists for this User.

**Code** : `200 OK`

**Content Response Example**

```json
{
    "status": 200,
    "data"  : 
    {
        "username": "pippu",
        "name": " Philip Paul",
        "email": "sree@gmail.com",
        "image_url": "/media/pictures/IMG.jpg",
        "org_id": 1, 
        "phone": "9037502273",
        "api_key": "VKlAxsaWPAHDVC1"
    }
}
```

## Error Responses

**Condition** : If Account does't exist for User.

**Code** : `204 No content`




## GET CANDIDATES

**URL** : `/api/get_candidtes/`

**Method** : `POST`

**Auth required** : YES

**Permissions required** : None

**Data Request Format**

Provide corresponding api key.

```json
{
    "api_key" : "api_key",
}
```


## Success Response

**Condition** : If everything is OK and api key is valid.

**Code** : `200 OK`

**Content Response Example**

```json
[
    {
        "username": "test",
        "name": "Test" ,
        "image_url": "/media/pictures/rahul.jpg"
    }
]
```

## Error Responses

**Condition** : If api key is invalid or not found.

**Code** : `403 Access Denied`


## GET USER ANALYTICS

**URL** : `/api/get_user_analytics/`

**Method** : `POST`

**Auth required** : YES

**Permissions required** : None

**Data Request Format**

Provide the parameters given below.

```json
{
    "api_key"   : "api_key",
    "username"  : "username",
    "type"      : "type",
    "camera_id" : "camera_id"
}
```


## Success Response

**Condition** : If everything is OK and parameters are valid.

**Code** : `200 OK`

**Content Response Format**

```json
{
    "status": 200,
    "data" : 
    [
        ["01 Jun", "02 Jun", "03 Jun", "04 Jun", "05 Jun", "06 Jun", "07 Jun"],
        [0, 0, 0, 0, 12, 0, 0]
    ],
    "raw_data": 
    [
        {
             "time_stamp": "05 Jun 2020 09:48:29 PM",
             "camera_name": "camera1"
         },
    ]
}
```

## Error Responses

**Condition** : If api key is invalid or not found.

**Code** : `403 Access Denied`


## EDIT PROFILE

**URL** : `/api/edit_profile/`

**Method** : `POST`

**Auth required** : YES

**Permissions required** : None

**Data Request Format**

Provide the parameters given below.

```json
{
    "username"   : "username",
    "first_name" : "first_name",
    "last_name"  : "last_name",
    "phone"      : "phone" ,
    "api_key"    : "api_key"
}
```


## Success Response

**Condition** : If everything is OK and parameters are valid.

**Code** : `200 OK`

**Content Response Format**

```json
{
    "status" : "200"
}
```

## Error Responses

**Condition** : If api key is invalid or not found.

**Code** : `403 Access Denied`

## GET OVERALL ANALYTICS

**URL** : `/api/get_overall_analytics/`

**Method** : `POST`

**Auth required** : YES

**Permissions required** : None

**Data Request Format**

Provide the parameters given below.

```json
{
    "api_key"   : "api_key",
    "from_date" : "from_date",
    "to_date"   : "to_date" ,
    "type"      : "type",
    "camera_id" : "camera_id"
}
```


## Success Response

**Condition** : If everything is OK and parameters are valid.

**Code** : `200 OK`

**Content Response Format**

```json
{
    "count_list": [0, 0, 0, 0, 0, 1, 0, 0],
    "time_list": ["31 May", "01 Jun", "02 Jun", "03 Jun", "04 Jun", "05 Jun", "06 Jun", "07 Jun"],
    "data": 
    [
        {
            "no": 1,
            "email": "test",
            "name": "Test" ,
            "image_url": "/media/pictures/rahul.jpg",
            "type": "Candidate",
            "count": 12
        }
    ],
    "status": 200
}
```

## Error Responses

**Condition** : If api key is invalid or not found.

**Code** : `403 Access Denied`


## EDIT PROFILE PICTURE

**URL** : `/api/edit_profile_picture/`

**Method** : `POST`

**Auth required** : YES

**Permissions required** : None

**Data Request Format**

Provide the parameters given below.

```json
{
    "username"   : "username",
    "file"       : "BYTE_STREAM", 
    "api_key"    : "api_key"
}
```


## Success Response

**Condition** : If everything is OK and parameters are valid.

**Code** : `200 OK`

**Content Response Format**

```json
{
    "status" : "200",
    "image_url" : "/media/pic.jpg"
}
```

## Error Responses

**Condition** : If api key is invalid or not found.

**Code** : `403 Access Denied`


## ADD ANALYTICS

**URL** : `/api/add_analytics/`

**Method** : `POST`

**Auth required** : YES

**Permissions required** : None

**Data Request Format**

Provide the parameters given below.

```json
{
    "embedding"   : "EMBEDDING_LIST",
    "camera_id"   : "camera_id", 
    "api_key"     : "api_key",
    "time_stamp"  : "time_stamp"
}
```


## Success Response

**Condition** : If everything is OK and parameters are valid.

**Code** : `200 OK`

**Content Response Format**

```json
{
    "status" : "200",
}
```

## Error Responses

**Condition** : If api key is invalid or not found.

**Code** : `500 No Access`



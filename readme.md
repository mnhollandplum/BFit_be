# BFit Backend


## Routes, Request Body and Response<br/>
### Functioning<br/>

#### POST api/v1/users<br/>

| Object Field       | Type   | Required? | Description |
|--------------------|--------|-----------|-------------|
| `id`               | integer| yes       | The id is automatically created. Do not send in POST.
| `username`         | string | yes       | The username must be unique and under 20 chars.
| `email`            | string | yes       | The email must be unique and under 200 chars.
| `avatar`           | string | no        | The avatar image is stored as a url.
| `password`         | string | yes       | The password is hashed for secure storage.

#### Expected JSON request structure <br/>
```json
{
  "username":"username1",
  "email":"email@email.com",
  "avatar":"image.com",
  "password":"12345"
}
```

#### Expected JSON response structure upon successful POST request<br/>
```json
{
    "user": {
        "avatar": "image.com",
        "email": "email@email.com",
        "id": 1,
        "username": "username1"
    }
}
```
#### PUT api/v1/users/:id/edit

#### Expected JSON request structure upon successful GET request
```json
{"avatar":"new avatar"}
```

#### Expected JSON response structure upon successful GET request
```json
{"avatar":"new avatar"}
```

### GET api/v1/users

#### Expected JSON response structure upon successful GET request
```json
[
    {
        "users": {
            "avatar": "new image",
            "email": "test",
            "username": "test"
        }
    },
    {
        "users": {
            "avatar": "test2",
            "email": "test2",
            "username": "test2"
        }
    }
]
```

#### GET api/v1/users/:username 

#### Expected JSON response structure upon successful GET request
```json
{
    "user": {
        "avatar": "image.com",
        "email": "email@email.com",
        "id": 1,
        "username": "username1"
    }
}
```

#### GET api/v1/users/:id 

#### Expected JSON response structure upon successful GET request
```json
{
    "user": {
        "avatar": "image.com",
        "email": "email@email.com",
        "id": 1,
        "username": "username1"
    }
}
```

#### POST api/v1/posts for a meal post_type
<br/>
Post<br/>

| Object Field      | Type   | Required? | Description |
|-------------------|--------|-----------|-------------|
| `id`              | integer| yes       | The id is automatically created. Do not send in POST.
| `title   `        | string | yes       | The title must be unique and under 200 chars.
| `description`     | string | no        | The description must be under 200 chars.
| `image_url`       | string | no        | The image is stored as a url.
| `user_id `        | integer| yes       | The user_id associates the post with the user.
| `post_type `      | string | yes       | The post_type must be "meal".

Meal<br/>

| Object Field      | Type   | Required? | Description |
|-------------------|--------|-----------|-------------|
| `id`              | integer| yes       | The id is automatically created. Do not send in POST.
| `name`            | string | no        | The name must be under 20 chars.

Foods<br/>

| Object Field      | Type   | Required? | Description |
|-------------------|--------|-----------|-------------|
| `id`              | integer| yes       | The id is automatically created. Do not send in POST.
| `name`            | string | no        | The name must be unique and under 20 chars.
| `calories`        | integer| no        | The calories must be an integer.
| `post_id`         | integer| yes       | The post_id attributes the exercise to a post.

#### Expected JSON request structure upon successful POST request<br/>
```json
{
  "title": "test meal post title",
  "description": "test meal post description",
  "image_url": "testmealpost.image_url",
  "user_id": 1,
  "post_type": "meal",
  "meal": {
      "name": "breakfast",
          "foods": [{
              "name": "carrot",
              "calories": 12
          },
          {
            "name": "",
            "calories": 0
          } ]
    }
 }
 ```

#### Expected JSON response structure upon successful POST request<br/>
```json
{
   "post": {
       "date": "Tue, 19 Feb 2019 21:56:54 GMT",
       "description": "test meal post description",
       "id": 18,
       "image_url": "testmealpost.image_url",
       "meal": {
           "foods": [
               {
                   "calories": 12,
                   "id": 27,
                   "name": "carrot"
               },
               {
                   "calories": 0,
                   "id": 28,
                   "name": ""
               }
           ],
            "id": 1,
            "name": "breakfast",
            "post_id": 1
        },
        "post_type": "meal",
        "title": "test meal post title",
        "user_id": 1
    }
}
```

####POST api/v1/posts for a exercise post_type<br/>

Post<br/>

| Object Field      | Type   | Required? | Description |
|-------------------|--------|-----------|-------------|
| `id`              | integer| yes       | The id is automatically created. Do not send in POST.
| `title   `        | string | yes       | The title must be unique and under 200 chars.
| `description`     | string | no        | The description must be under 200 chars.
| `image_url`       | string | no        | The image is stored as a url.
| `user_id `        | integer| yes       | The user_id associates the post with the user.
| `post_type `      | string | yes       | The post_type must be "meal".

Exercise
| Object Field      | Type   | Required? | Description |
|-------------------|--------|-----------|-------------|
| `id`              | integer| yes       | The id is automatically created. Do not send in POST.
| `name`            | string | yes       | The name must be under 200 chars.
| `muscle_group`    | string | yes       | The muscle_group is set by user. Cardio changes other attributes.
| `reps`            | integer| no        | The reps attribute is for strength exercises
| `weight`          | integer| no        | The weight attribute is for strength exercises
| `time`            | integer| no        | The time attribute replaces weight when muscle_group == 'cardio'
| `distance`        | integer| no        | The distance attribute replaces reps when muscle_group == 'cardio'
| `post_id`         | integer| yes       | The post_id attributes the exercise to a post.


#### Expected JSON request structure upon successful POST request<br/>
```json
{
     "title": "Running is the worst!",
     "description": "But do it anyways!",
     "image_url": "pumpingiron.png",
     "user_id": "1",
     "post_type": "exercise",
     "muscle_group": "cardio",
     "name": "Treadmill for days",
     "weightORTime": "50",
     "repsORDistance": "5"
}
```

#### Expected JSON response structure upon successful POST request<br/>
```json
{
    "post": {
        "date": "Tue, 19 Feb 2019 23:16:56 GMT",
        "description": "But do it anyways!",
        "exercise": {
            "distance": 5,
            "id": 2,
            "muscle_group": "cardio",
            "name": "Treadmill for days",
            "reps": null,
            "time": 50,
            "weight": null
        },
        "id": 1,
        "image_url": "pumpingiron.png",
        "post_type": "exercise",
        "title": "Running is the worst!",
        "user_id": 1
    }
}
```


GET api/v1/users/<id>/posts<br/>
	
#### Expected JSON response structure upon successful GET request<br/>
	
```json
{
    "posts": [
    	{
        "post": {
       		"date": "Tue, 19 Feb 2019 21:56:54 GMT",
       		"description": "test meal post description",
       		"id": 18,
       		"image_url": "testmealpost.image_url",
      		 "meal": {
           		"foods": [
              		 {
			   "calories": 12,
                  	   "id": 27,
                   	   "name": "carrot"
               		},
               {
                   	   "calories": 0,
                  	   "id": 28,
                  	   "name": ""
              		}
           ],
            "id": 1,
            "name": "breakfast",
            "post_id": 1
        },
        "post_type": "meal",
        "title": "test meal post title",
        "user_id": 1
    },
        {
           
    "post": {
        "date": "Tue, 19 Feb 2019 23:16:56 GMT",
        "description": "But do it anyways!",
        "exercise": {
            "distance": 5,
            "id": 2,
            "muscle_group": "cardio",
            "name": "Treadmill for days",
            "reps": null,
            "time": 50,
            "weight": null
        },
        "id": 1,
        "image_url": "pumpingiron.png",
        "post_type": "exercise",
        "title": "Running is the worst!",
        "user_id": 1
    }
            ],
    "username": "56789"
}
```



###WIP<br/>
GET api/v1/users/<id>/followers<br/>
GET api/v1/users/<id>/following<br/>
GET api/v1/users/<id>/feed<br/>

##MVP Schema<br/>
![Schema](./Schema.png)<br/>

##Known Issues

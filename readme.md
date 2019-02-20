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
{<br/>
  "username":"username1",<br/>
  "email":"email@email.com",<br/>
  "avatar":"image.com",<br/>
  "password":"12345"<br/>
}<br/>

#### Expected JSON response structure upon successful POST request<br/>
{<br/>
    "user": {<br/>
        "avatar": "image.com",<br/>
        "email": "email@email.com",<br/>
        "id": 1,<br/>
        "username": "username1"<br/>
    }<br/>
}<br/>


#### GET api/v1/users/:id 
<br/>

#### Expected JSON response structure upon successful GET request
<br/>
{<br/>
    "user": {<br/>
        "avatar": "image.com",<br/>
        "email": "email@email.com",<br/>
        "id": 1,<br/>
        "username": "username1"<br/>
    }<br/>
}<br/>

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

#### Expected JSON response structure upon successful POST request<br/>
{<br/>
  "title": "test meal post title",<br/>
  "description": "test meal post description",<br/>
  "image_url": "testmealpost.image_url",<br/>
  "user_id": 1,<br/>
  "post_type": "meal",<br/>
  "meal": {<br/>
      "name": "breakfast",<br/>
          "foods": [{<br/>
              "name": "carrot",<br/>
              "calories": 12<br/>
          },<br/>
          {<br/>
            "name": "",<br/>
            "calories": 0<br/>
          } ]<br/>
    }
 }

#### Expected JSON response structure upon successful POST request<br/>
{<br/>
    "post": {<br/>
        "date": "Tue, 19 Feb 2019 21:56:54 GMT",<br/>
        "description": "test meal post description",<br/>
        "id": 18,<br/>
        "image_url": "testmealpost.image_url",<br/>
        "meal": {<br/>
            "foods": [<br/>
                {<br/>
                    "calories": 12,<br/>
                    "id": 27,<br/>
                    "name": "carrot"<br/>
                },<br/>
                {<br/>
                    "calories": 0,<br/>
                    "id": 28,<br/>
                    "name": ""<br/>
                }<br/>
            ],<br/>
            "id": 1,<br/>
            "name": "breakfast",<br/>
            "post_id": 1<br/>
        },<br/>
        "post_type": "meal",<br/>
        "title": "test meal post title",<br/>
        "user_id": 1<br/>
    }<br/>
}<br/>

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


####Expected JSON response structure upon successful POST request<br/>
{<br/>
	"title": "Running is the worst!",<br/>
	"description": "But do it anyways!",<br/>
	"image_url": "pumpingiron.png",<br/>
	"user_id": "1",<br/>
	"post_type": "exercise",<br/>
  "muscle_group": "cardio",<br/>
  "name": "Treadmill for days",<br/>
  "weightORTime": "50",<br/>
  "repsORDistance": "5"<br/>
}<br/>

####Expected JSON response structure upon successful POST request<br/>
{<br/>
    "post": {<br/>
        "date": "Tue, 19 Feb 2019 23:16:56 GMT",<br/>
        "description": "But do it anyways!",<br/>
        "exercise": {<br/>
            "distance": 5,<br/>
            "id": 2,<br/>
            "muscle_group": "cardio",<br/>
            "name": "Treadmill for days",<br/>
            "reps": null,<br/>
            "time": 50,<br/>
            "weight": null<br/>
        },<br/>
        "id": 1,<br/>
        "image_url": "pumpingiron.png",<br/>
        "post_type": "exercise",<br/>
        "title": "Running is the worst!",<br/>
        "user_id": 1<br/>
    }
}


GET api/v1/users/<id>/posts<br/>
####Expected JSON response structure upon successful GET request<br/>
{<br/>
    "posts": [<br/>
        {<br/>
            "description": "test meal post description",<br/>
            "id": 1,<br/>
            "image_url": "testmealpost.image_url",<br/>
            "post_type": "meal",<br/>
            "title": "test meal post title",<br/>
            "user_id": 1<br/>
        },<br/>
        {<br/>
            "description": "But do it anyways!",<br/>
            "id": 2,<br/>
            "image_url": "pumpingiron.png",<br/>
            "post_type": "exercise",<br/>
            "title": "Running is the worst!",<br/>
            "user_id": 1<br/>
        },<br/>
            ],<br/>
    "username": "56789"<br/>
}<br/>



###WIP<br/>
GET api/v1/users/<id>/followers<br/>
GET api/v1/users/<id>/following<br/>
GET api/v1/users/<id>/feed<br/>

##MVP Schema<br/>
![Schema](./Schema.png)<br/>

##Known Issues

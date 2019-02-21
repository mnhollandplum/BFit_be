# BFit API


## Functioning Routes, Request Body and Response

### POST api/v1/users
<hr>

| Object Field       | Type   | Required? | Description |
|--------------------|--------|-----------|-------------|
| `id`               | integer| yes       | The id is automatically created. Do not send in POST.
| `username`         | string | yes       | The username must be unique and under 20 chars.
| `email`            | string | yes       | The email must be unique and under 200 chars.
| `avatar`           | string | no        | The avatar image is stored as a url.
| `password`         | string | yes       | The password is hashed for secure storage.

#### Expected JSON request structure

```json
{
  "username":"username1",
  "email":"email@email.com",
  "avatar":"image.com",
  "password":"12345"
}
```

#### Expected JSON response structure upon successful POST request

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
### PUT api/v1/users/:id/edit
<hr>

#### Expected JSON request structure
```json
{"avatar":"new_avatar.png"}
```

#### Expected JSON response structure upon successful GET request
```json
{"avatar":"new_avatar.png"}
```

### GET api/v1/users
<hr>

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
##### Optional query param that will match username with similar usernames in database. Key: username Value: username query.
Ex: localhost:5000/api/v1/users?username=jane
#### Expected JSON response structure upon successful GET request with query.
```json
[
    {
        "users": {
            "avatar": "janeimage",
            "email": "janedoe@email.com",
            "username": "Jane Doe"
        }
    },
    {
        "users": {
            "avatar": "janenotdoeimage",
            "email": "janenotdoe@email.com",
            "username": "Jane Notdoe"
        }
    }
]
```

### GET api/v1/users/:id
<hr>

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

### GET api/v1/users/:id/following
<hr>

#### Expected JSON response structure upon successful GET request
```json
[
    {
        "users": {
	    "avatar": "image.com",
	    "email": "email@email.com",
	    "id": 1,
	    "username": "username1"
        }
    },
    {
        "users": {
            "avatar": "image2.com",
            "email": "email2@email.com",
            "id": 2,
            "username": "username2"
        }
    }
]
```


### POST api/v1/posts for a meal post_type
<hr>

#### Post

| Object Field      | Type   | Required? | Description |
|-------------------|--------|-----------|-------------|
| `id`              | integer| yes       | The id is automatically created. Do not send in POST.
| `title   `        | string | yes       | The title must be unique and under 200 chars.
| `description`     | string | no        | The description must be under 200 chars.
| `image_url`       | string | no        | The image is stored as a url.
| `user_id `        | integer| yes       | The user_id associates the post with the user.
| `post_type `      | string | yes       | The post_type must be "meal".

#### Meal

| Object Field      | Type   | Required? | Description |
|-------------------|--------|-----------|-------------|
| `id`              | integer| yes       | The id is automatically created. Do not send in POST.
| `name`            | string | no        | The name must be under 20 chars.

#### Foods

| Object Field      | Type   | Required? | Description |
|-------------------|--------|-----------|-------------|
| `id`              | integer| yes       | The id is automatically created. Do not send in POST.
| `name`            | string | no        | The name must be unique and under 20 chars.
| `calories`        | integer| no        | The calories must be an integer.
| `post_id`         | integer| yes       | The post_id attributes the exercise to a post.

#### Expected JSON request structure

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

#### Expected JSON response structure upon successful POST request

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

### POST api/v1/posts for a exercise post_type
<hr>

#### Post

| Object Field      | Type   | Required? | Description |
|-------------------|--------|-----------|-------------|
| `id`              | integer| yes       | The id is automatically created. Do not send in POST.
| `title   `        | string | yes       | The title must be unique and under 200 chars.
| `description`     | string | no        | The description must be under 200 chars.
| `image_url`       | string | no        | The image is stored as a url.
| `user_id `        | integer| yes       | The user_id associates the post with the user.
| `post_type `      | string | yes       | The post_type must be "meal".

#### Exercise
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


#### Expected JSON request structure

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


## GET api/v1/users/:id/posts
<hr>
	
#### Expected JSON response structure upon successful GET request
	
```json
[
    {
        "post": {
            "date": "Wed, 20 Feb 2019 18:39:38 GMT",
            "description": "She does it every day",
            "exercise": {
                "distance": null,
                "id": 2,
                "muscle_group": "arms",
                "name": "AfternoonLift",
                "reps": 10,
                "time": null,
                "weight": 85
            },
            "id": 2,
            "image_url": "janelifting.png",
            "post_type": "exercise",
            "title": "Jane likes to lift",
            "user_id": 2
        },
        "username": "Jane Doe"
    },
    {
        "post": {
            "date": "Wed, 20 Feb 2019 18:42:14 GMT",
            "description": "This is Jane's meal post",
            "id": 4,
            "image_url": "janesmeal.image_url",
            "meal": {
                "foods": [
                    {
                        "calories": 300,
                        "id": 3,
                        "name": "milkshake"
                    },
                    {
                        "calories": 12,
                        "id": 4,
                        "name": "apple"
                    }
                ],
                "id": 2,
                "name": "lunch"
            },
            "post_type": "meal",
            "title": "Jane's meal post",
            "user_id": 2
        },
        "username": "Jane Doe"
    },
    {
        "post": {
            "date": "Wed, 20 Feb 2019 18:47:12 GMT",
            "description": "",
            "exercise": {
                "distance": null,
                "id": 3,
                "muscle_group": "Triceps",
                "name": "Dips",
                "reps": 4,
                "time": null,
                "weight": 3
            },
            "id": 5,
            "image_url": "",
            "post_type": "exercise",
            "title": "Dips",
            "user_id": 2
        },
        "username": "Jane Doe"
    }
]
```
## GET api/v1/users/:id/feed
<hr>
	
#### Expected JSON response structure upon successful GET request
```json
[
    {
        "avatar": "56789",
        "post": {
            "date": "Wed, 20 Feb 2019 23:59:08 GMT",
            "description": "This is a meal post",
            "id": 19,
            "image_url": "meal.image_url",
            "meal": {
                "foods": [
                    {
                        "calories": 300,
                        "id": 26,
                        "name": "cake"
                    },
                    {
                        "calories": 12,
                        "id": 27,
                        "name": "bean"
                    }
                ],
                "id": 9,
                "name": "breakfast"
            },
            "post_type": "meal",
            "title": "follow meal post",
            "user_id": 3
        },
        "username": "12345"
    },
    {
        "avatar": "qzz7bnuue32ss6zidmbu.jpg",
        "post": {
            "date": "Wed, 20 Feb 2019 23:58:36 GMT",
            "description": "This is Jane's meal post",
            "id": 18,
            "image_url": "janesmeal.image_url",
            "meal": {
                "foods": [
                    {
                        "calories": 300,
                        "id": 24,
                        "name": "milkshake"
                    },
                    {
                        "calories": 12,
                        "id": 25,
                        "name": "apple"
                    }
                ],
                "id": 8,
                "name": "lunch"
            },
            "post_type": "meal",
            "title": "Jane's meal post",
            "user_id": 2
        },
        "username": "Jane Doe"
    },
    {
        "avatar": "fzuciwvrum47u3gghdvm.jpg",
        "post": {
            "date": "Wed, 20 Feb 2019 23:35:23 GMT",
            "description": "",
            "exercise": {
                "distance": null,
                "id": 10,
                "muscle_group": "Abs",
                "name": "Bicycles",
                "reps": 5,
                "time": null,
                "weight": 4
            },
            "id": 17,
            "image_url": "",
            "post_type": "exercise",
            "title": "Bicycles",
            "user_id": 7
        },
        "username": "Salmon"
    },
    {
        "avatar": "fzuciwvrum47u3gghdvm.jpg",
        "post": {
            "date": "Wed, 20 Feb 2019 22:11:11 GMT",
            "description": "",
            "id": 16,
            "image_url": "",
            "meal": {
                "foods": [
                    {
                        "calories": 4,
                        "id": 19,
                        "name": "Other things"
                    },
                    {
                        "calories": 5,
                        "id": 20,
                        "name": "More things (not salmon)"
                    },
                    {
                        "calories": 0,
                        "id": 21,
                        "name": ""
                    },
                    {
                        "calories": 0,
                        "id": 22,
                        "name": ""
                    },
                    {
                        "calories": 0,
                        "id": 23,
                        "name": ""
                    }
                ],
                "id": 7,
                "name": "Not salmon"
            },
            "post_type": "meal",
            "title": "Not salmon",
            "user_id": 7
        },
        "username": "Salmon"
    },
    {
        "avatar": "fzuciwvrum47u3gghdvm.jpg",
        "post": {
            "date": "Wed, 20 Feb 2019 22:10:42 GMT",
            "description": "",
            "exercise": {
                "distance": null,
                "id": 9,
                "muscle_group": "Abs",
                "name": "Front lever",
                "reps": 4,
                "time": null,
                "weight": 7
            },
            "id": 15,
            "image_url": "",
            "post_type": "exercise",
            "title": "Front lever",
            "user_id": 7
        },
        "username": "Salmon"
    }
```

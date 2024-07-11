# Yuki Kitayama API

REST = Representational State Transfer. Transfer data instead fo user interfaces.

- Uniform interface
  - Clearly defined API endpoints with clearly defined request + response data structure
- Stateless interactions
  - Server and client don't store any connection history, every request is handled separately.

- PUT
  - Put a resource onto the Server (i.e. create or overwrite a Resouce)
- PATCH
  - Update parts of an existing resource on the server.

- `200`
  - Success
- `201`
  - Successful to create a resource

**CORS** is Cross-Origin Resource Sharing. When client and server runs on different domains, it has CORS error. But we want to share data between client and server. 

Typically, CORS error is solved in server side, not in client side.

```
const express = require("express");
const app = express();
app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
  next();
});
```

## Tool

- Postman
- Node.js
- Express.js

## Node.js/Express

`npm init`

`npm install`
```
--save express
--save-dev nodemon
(--save body-parser)
```

`package.json`, `"scripts": {"start": "nodemon app.js"}`.

## Resource

- https://academind.com/tutorials/building-a-restful-api-with-nodejs
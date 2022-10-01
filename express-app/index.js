const express = require("express");
const app = express();

app.get("/users", (req, res) => {
   console.log(req.path);
   console.log(req.method);
   console.log(res.type('json'));
   res.send("Hello Users");
})

app.listen(3000, () => {
   console.log('Started')
})

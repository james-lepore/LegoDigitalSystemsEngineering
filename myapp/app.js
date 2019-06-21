var express = require('express');
var app = express();
var path = require('path');
var router = express.Router();

// viewed at http://localhost:3000
router.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
});

app.use('/', router)
app.listen(3000);
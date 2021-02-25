var express = require('express');
var app = express();
var bodyParser = require('body-parser');

// Create application/x-www-form-urlencoded parser
var urlencodedParser = bodyParser.urlencoded({ extended: false })

app.use(express.static('.'));

app.get('/',function(req,res) {
  res.sendFile('/home/denizkorkmaz/Desktop/CMPE483/Projects/2/CMPE483-FALL2020-Homework2-Korkmaz-Ozdemir-Sari/index.html');
});

var server = app.listen(8081, function () {

  var host = server.address().address
  var port = server.address().port

  console.log("Example app listening at http://%s:%s", host, port)

})

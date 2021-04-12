const express = require('express');
const app = express();
const dotenv = require('dotenv');
const mongo = require('mongodb');
const mongoUtil = require('./mongoUtil');
const postRoute = require('./routes/post');
const deptRoute = require('./routes/Department');
const studRoute = require('./routes/student');
const fourRoute = require('./routes/fouryear');
const courseRoute = require('./routes/Course');

// import routes
const authRoute = require('./routes/auth');

dotenv.config();

// connect to db
mongoUtil.connectToServer( function(err, client) {
    
    if(err) console.log(err);
});

// middleware
app.use(express.json());

// Route middleware
app.use('/api/user', authRoute);
app.use('/api/post', postRoute);
app.use('/api/Department', deptRoute);
app.use('/api/Student', studRoute);
app.use('/api/FourYear', fourRoute);
app.use('/api/Course', courseRoute);

app.listen(5000, () => console.log('Server running'));

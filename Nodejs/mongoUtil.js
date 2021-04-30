const mongo = require('mongodb').MongoClient;
const mongoose = require('mongoose');

var db, collection;

// connect to db
module.exports = {
    connectToServer: function(callback) {
        
        mongo.connect(process.env.DB_CONNECT,
        {useNewUrlParser: true},
        {useUnifiedTopology: true}, function(err, client) {
            db = client.db('COSC425AAT');
            return callback(err);
        });
        mongoose.connect(process.env.DB_CONNECT,
            {useNewUrlParser: true},
            {useUnifiedTopology: true}, function(err, client) {
            });
    },
    getDb: function(){
        return db;
    },

    getDept: function(){
        collection = db.collection("Department");
        return collection;
    },

    getStud: function(){
        collection = db.collection("Student");
        return collection;
    },

    getCourse: function(){
        collection = db.collection("Course");
        return collection;
    },

    getFourYear: function(){
        collection = db.collection("FourYear");
        return collection;
    }
};

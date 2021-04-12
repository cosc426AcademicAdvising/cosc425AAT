const router = require("express").Router();
const mongoUtil = require('../mongoUtil');
const verify = require('./verifyToken');

var collection;

// getStudentbyID
router.get("/:id", verify, (req, res) => {
    collection = mongoUtil.getStud();
    var sid = parseInt(req.params.id);
    collection.findOne({"s_id": sid},
    (error, result) => {
        if(error) {
            return res.status(500).send(error);
        }
        res.send(result);
    });
});

module.exports = router;
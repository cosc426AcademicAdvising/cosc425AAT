const router = require("express").Router();
const mongoUtil = require('../mongoUtil');
const verify = require('./verifyToken');

var collection;

// getFourYearPoliciesbyMajor
router.get("/Policy/:major", verify, (req, res) => {
    collection = mongoUtil.getFourYear();
    var maj = req.params.major;
    collection.find({"major": maj}).project({'policies': 1, _id: 0}).toArray((error, result) => {
        if(error) {
            return res.status(500).send(error);
        }
        res.send(result);
    });
});

// getFourYearbyMajor
router.get("/:major", verify, (req, res) => {
    collection = mongoUtil.getFourYear();
    var maj = req.params.major;
    collection.findOne({"major": maj},
    (error, result) => {
        if(error) {
            return res.status(500).send(error);
        }
        res.send(result);
    });
});

module.exports = router;
'use strict';
/**
 * Utilities
 */

const _ = require('lodash');

const zeroBuffer = new Buffer([0]);

function unsigned(bignum) {
	if (_.isNil(bignum) || !_.isBuffer(bignum) || _.isEmpty(bignum)) {
		return bignum;
	}

	if (bignum.readInt8(0) < 0) {
		return Buffer.concat([ zeroBuffer, bignum ], bignum.length + 1);
	}
	return bignum;
}

module.exports.unsigned = unsigned;

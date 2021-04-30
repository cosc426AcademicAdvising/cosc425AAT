'use strict';
/**
 * Algorithms
 */

const SUPPORTED_KTY = [
	'RSA',
	'EC',
	'oct'
];

class JWA {

	static get supportedKeyTypes() {
		return SUPPORTED_KTY;
	}

}

module.exports = JWA;

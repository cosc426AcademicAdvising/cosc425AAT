'use strict';
/**
 * Binary (symmetric) key
 */

const _ = require('lodash');
const base64url = require('base64url');

class BinKey {

	constructor(k) {
		this._k = k;
	}

	get hasPrivateKey() {
		return true;
	}

	get raw() {
		return this._k;
	}

	toPublicKeyPEM() {
		return null;
	}

	toPrivateKeyPEM() {
		return null;
	}

	static validate(key) {
		// @see RFC-7517 par. 6.3
		return _.has(key, 'k');
	}

	static fromKey(key) {
		const k = base64url.toBuffer(key.k);

		return new BinKey(k);
	}


}

module.exports = BinKey;

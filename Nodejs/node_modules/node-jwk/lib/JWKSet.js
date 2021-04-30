'use strict';
/**
 * JWK set
 */

const _ = require('lodash');
const JWA = require('./JWA');
const JWK = require('./JWK');

class JWKSet {

	/**
	 * @private
	 */
	constructor(data) {

		// Filter unsupported key types and invalid keys (@see RFC-7517 par. 5)
		const supportedKeys = _.filter(data.keys, key => _.includes(JWA.supportedKeyTypes, key.kty) && JWK.validate(key));
		this._keys = _.map(supportedKeys, key => JWK.fromObject(key));

	}

	get keys() {
		return this._keys;
	}

	findKeyById(kid) {
		return _.find(this.keys, [ 'kid', kid ]);
	}

	findKeysByUse(use) {
		return _.find(this.keys, [ 'use', use ]);
	}

	static validate(keySet) {
		let result = _.has(keySet, 'keys') && _.isArray(keySet.keys);
		return result;
	}

	static fromObject(keySet) {
		if (!JWKSet.validate(keySet)) {
			throw new Error('Invalid JWK set');
		}
		return new JWKSet(keySet);
	}

	/**
	 * Create a JWK instance from a stringified JSON.
	 * @throws When the JSON cannot be parsed or is missing mandatory properties.
	 */
	static fromJSON(json) {

		if (!_.isString(json)) {
			throw new Error('JSON input must be stringified');
		}

		const parsedJSON = JSON.parse(json);
		return JWKSet.fromObject(parsedJSON);
	}

}

module.exports = JWKSet;

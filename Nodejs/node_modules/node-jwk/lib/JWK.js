'use strict';
/**
 * JWK
 */

const _ = require('lodash');
const keytypes = require('./keytypes');

class JWK {

	/**
	 * @private
	 */
	constructor(data) {
		this._data = data;
		this._key = keytypes[data.kty].fromKey(data);
	}

	get kty() {
		return this._data.kty;
	}

	get use() {
		return this._data.use;
	}

	get key_ops() {
		return this._data.key_ops;
	}

	get alg() {
		return this._data.alg;
	}

	get kid() {
		return this._data.kid;
	}

	get x5u() {
		return this._data.x5u;
	}

	get x5c() {
		return this._data.x5c;
	}

	get x5t() {
		return this._data.x5t;
	}

	get 'x5t#S256'() {
		return this._data['x5t#S256'];
	}

	get key() {
		return this._key;
	}

	static validate(key) {
		let result = _.has(key, 'kty') && _.has(keytypes, key.kty) && keytypes[key.kty].validate(key);

		return result;
	}

	static fromObject(key) {
		if (!_.isObject(key) || !JWK.validate(key)) {
			throw new Error('Invalid JWK');
		}
		return new JWK(key);
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
		return JWK.fromObject(parsedJSON);
	}

}

module.exports = JWK;

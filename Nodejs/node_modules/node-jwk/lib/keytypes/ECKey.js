'use strict';
/**
 * EC key
 */

const _ = require('lodash');
const base64url = require('base64url');
const asn = require('asn1.js');

const COORD_PREFIX_UNCOMPRESSED = new Buffer([0x04]);

const SUPPORTED_CURVES = [
	'P-256',
	'P-384',
	'P-521'
];

// @see RFC-6637 par. 11
const CURVE_OIDS = {
	'1.2.840.10045.3.1.7': 'P-256',
	'1.3.132.0.34': 'P-384',
	'1.3.132.0.35': 'P-521'
};

const ECPublicKeyHeader = asn.define('ECPublicKeyHeader', function() {
	this.seq().obj(
		this.key('keyType').objid({
			'1.2.840.10045.2.1': 'EC'
		}),
		this.key('crv').objid(CURVE_OIDS)
	);
});

const ECPublicKey = asn.define('ECPublicKey', function() {
	this.seq().obj(
		this.key('header').use(ECPublicKeyHeader),
		this.key('content').bitstr()
	);
});

const ECPrivateKey = asn.define('ECPrivateKey', function() {
	this.seq().obj(
		this.key('id').int(),
		this.key('d').octstr(),
		this.key('crv').explicit(0).objid(CURVE_OIDS),
		this.key('coord').explicit(1).bitstr()
	);
});

class ECKey {

	constructor(crv, x, y, d) {
		this._crv = crv;
		this._x = x;
		this._y = y;
		this._d = d;
	}

	get hasPrivateKey() {
		return !_.isNil(this._d);
	}

	toPublicKeyPEM() {
		// Construct x/y coordinate
		const coordinate = Buffer.concat([COORD_PREFIX_UNCOMPRESSED, this._x, this._y]);

		const params = {
			header: {
				keyType: 'EC',
				crv: this._crv
			},
			content: {
				data: coordinate
			}
		};
		return ECPublicKey.encode(params, 'pem', { label: 'PUBLIC KEY' });
	}

	toPrivateKeyPEM() {
		if (!this.hasPrivateKey) {
			return null;
		}

		// Construct x/y coordinate
		const coordinate = Buffer.concat([COORD_PREFIX_UNCOMPRESSED, this._x, this._y]);

		const params = {
			id: 1,
			d: this._d,
			crv: this._crv,
			coord: { data: coordinate }
		};
		return ECPrivateKey.encode(params, 'pem', { label: 'EC PRIVATE KEY' });
	}

	static validate(key) {
		// y must only be defined for the three curves defined in RFC-7517 par. 6.2.1
		// FIXME: Currently y is treated as mandatory here.
		return _.has(key, 'crv') && _.has(key, 'x')  && _.has(key, 'y') && _.includes(SUPPORTED_CURVES, key.crv);
	}

	static fromKey(key) {
		const x = base64url.toBuffer(key.x);
		const y = base64url.toBuffer(key.y);
		const d = key.d ? base64url.toBuffer(key.d) : undefined;

		return new ECKey(key.crv, x, y, d);
	}

}

module.exports = ECKey;

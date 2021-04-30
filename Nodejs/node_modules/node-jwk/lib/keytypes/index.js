'use strict';
/**
 * Supported algorithms.
 */

const keytypes = {
	'EC': require('./ECKey'),
	'RSA': require('./RSAKey'),
	'oct': require('./BinKey')
};

module.exports = keytypes;

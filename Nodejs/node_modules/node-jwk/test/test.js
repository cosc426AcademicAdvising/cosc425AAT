/**
 * node-jwk test suite
 */

const fs = require('fs');
const path = require('path');
const _ = require('lodash');

const walkSync = (dir, pattern) => {
	const regex = new RegExp(pattern);
	return _.compact(_.flatMap(fs.readdirSync(dir),
		file => {
			const filePath = path.join(dir, file);
			if (fs.statSync(filePath).isDirectory()) {
				return walkSync(filePath, pattern);
			}

			return regex.test(file) ? filePath : null;
		}
	));
};

describe('node-jwk', () => {

	const tests = walkSync(__dirname, ['.*\.test\.js']);
	_.forEach(tests, test => require(test));

});

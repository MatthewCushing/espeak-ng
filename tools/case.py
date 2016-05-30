#!/usr/bin/python

# Copyright (C) 2012-2016 Reece H. Dunn
#
# This file is part of ucd-tools.
#
# ucd-tools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ucd-tools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ucd-tools.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import ucd

ucd_rootdir = sys.argv[1]
ucd_version = sys.argv[2]

unicode_chars = {}
null = ucd.CodePoint('0000')
for data in ucd.parse_ucd_data(ucd_rootdir, 'UnicodeData'):
	if data['LowerCase'] != null or data['UpperCase'] != null or data['TitleCase'] != null:
		unicode_chars[data['CodePoint']] = (data['LowerCase'], data['UpperCase'], data['TitleCase'])

if __name__ == '__main__':
	sys.stdout.write("""/* Unicode Case Conversion
 *
 * Copyright (C) 2012-2016 Reece H. Dunn
 *
 * This file is part of ucd-tools.
 *
 * ucd-tools is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * ucd-tools is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with ucd-tools.  If not, see <http://www.gnu.org/licenses/>.
 */

// NOTE: This file is automatically generated from the UnicodeData.txt file in
// the Unicode Character database by the ucd-tools/tools/categories.py script.

#include "ucd/ucd.h"

#include <stddef.h>

// Unicode Character Data %s

struct case_conversion_entry
{
	codepoint_t codepoint;
	codepoint_t uppercase;
	codepoint_t lowercase;
	codepoint_t titlecase;
};
""" % ucd_version)

	sys.stdout.write('\n')
	sys.stdout.write('static const struct case_conversion_entry case_conversion_data[] =\n')
	sys.stdout.write('{\n')
	for codepoint in sorted(unicode_chars.keys()):
		lower, upper, title = unicode_chars[codepoint]
		sys.stdout.write('\t{ 0x%s, 0x%s, 0x%s, 0x%s },\n' % (codepoint, upper, lower, title))
	sys.stdout.write('};\n')

	for case in ['upper', 'lower', 'title']:
		sys.stdout.write('\n')
		sys.stdout.write('codepoint_t ucd_to%s(codepoint_t c)\n' % case)
		sys.stdout.write('{\n')
		sys.stdout.write('\tint begin = 0;\n')
		sys.stdout.write('\tint end   = sizeof(case_conversion_data)/sizeof(case_conversion_data[0]);\n')
		sys.stdout.write('\twhile (begin <= end)\n')
		sys.stdout.write('\t{\n')
		sys.stdout.write('\t\tint pos = (begin + end) / 2;\n')
		sys.stdout.write('\t\tconst struct case_conversion_entry *item = (case_conversion_data + pos);\n')
		sys.stdout.write('\t\tif (c == item->codepoint)\n')
		sys.stdout.write('\t\t\treturn item->%scase == 0 ? c : item->%scase;\n' % (case, case))
		sys.stdout.write('\t\telse if (c > item->codepoint)\n')
		sys.stdout.write('\t\t\tbegin = pos + 1;\n')
		sys.stdout.write('\t\telse\n')
		sys.stdout.write('\t\t\tend = pos - 1;\n')
		sys.stdout.write('\t}\n')
		sys.stdout.write('\treturn c;\n')
		sys.stdout.write('}\n')

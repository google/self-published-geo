#!/usr/bin/python
#
# Copyright (c) 2012 IETF Trust and the persons identified as
# authors of the code.  All rights reserved.  Redistribution and use
# in source and binary forms, with or without modification, is
# permitted pursuant to, and subject to the license terms contained
# in, the Simplified BSD License set forth in Section 4.c of the
# IETF Trust's Legal Provisions Relating to IETF
# Documents (http://trustee.ietf.org/license-info).

import sys
from ipgeo_feed_validator import IPGeoFeedValidator

class IPGeoFeedValidatorTest(object):
  def __init__(self):
    self.validator = IPGeoFeedValidator()
    self.validator.SetOutputStream(None)
    self.successes = 0
    self.failures = 0

  def Run(self):
    self.TestFeedLine('# asdf', 0, 0)
    self.TestFeedLine('   ', 0, 0)
    self.TestFeedLine('', 0, 0)

    self.TestFeedLine('asdf', 1, 1)
    self.TestFeedLine('asdf,US,,,', 1, 0)
    self.TestFeedLine('aaaa::,US,,,', 0, 0)
    self.TestFeedLine('zzzz::,US', 1, 1)
    self.TestFeedLine(',US,,,', 1, 0)
    self.TestFeedLine('55.66.77', 1, 1)
    self.TestFeedLine('55.66.77.888', 1, 1)
    self.TestFeedLine('55.66.77.asdf', 1, 1)

    self.TestFeedLine('2001:db8:cafe::/48,PL,PL-MZ,,02-784', 0, 0)
    self.TestFeedLine('2001:db8:cafe::/48', 0, 1)

    self.TestFeedLine('55.66.77.88,PL', 0, 1)
    self.TestFeedLine('55.66.77.88,PL,,,', 0, 0)
    self.TestFeedLine('55.66.77.88,,,,', 0, 0)
    self.TestFeedLine('55.66.77.88,ZZ,,,', 0, 0)
    self.TestFeedLine('55.66.77.88,US,,,', 0, 0)
    self.TestFeedLine('55.66.77.88,USA,,,', 1, 0)
    self.TestFeedLine('55.66.77.88,99,,,', 1, 0)

    self.TestFeedLine('55.66.77.88,US,US-CA,,', 0, 0)
    self.TestFeedLine('55.66.77.88,US,USA-CA,,', 1, 0)
    self.TestFeedLine('55.66.77.88,USA,USA-CA,,', 2, 0)

    self.TestFeedLine('55.66.77.88,US,US-CA,Mountain View,', 0, 0)
    self.TestFeedLine('55.66.77.88,US,US-CA,Mountain View,94043',
                      0, 0)
    self.TestFeedLine('55.66.77.88,US,US-CA,Mountain View,94043,'
                      '1600 Ampthitheatre Parkway', 0, 1)

    self.TestFeedLine('55.66.77.0/24,US,,,', 0, 0)
    self.TestFeedLine('55.66.77.88/24,US,,,', 1, 0)
    self.TestFeedLine('55.66.77.88/32,US,,,', 0, 0)
    self.TestFeedLine('55.66.77/24,US,,,', 1, 0)
    self.TestFeedLine('55.66.77.0/35,US,,,', 1, 0)

    self.TestFeedLine('172.15.30.1,US,,,', 0, 0)
    self.TestFeedLine('172.28.30.1,US,,,', 1, 0)
    self.TestFeedLine('192.167.100.1,US,,,', 0, 0)
    self.TestFeedLine('192.168.100.1,US,,,', 1, 0)
    self.TestFeedLine('10.0.5.9,US,,,', 1, 0)
    self.TestFeedLine('10.0.5.0/24,US,,,', 1, 0)
    self.TestFeedLine('fc00::/48,PL,,,', 1, 0)
    self.TestFeedLine('fe00::/48,PL,,,', 0, 0)

    print ('%d tests passed, %d failed'
      % (self.successes, self.failures))

  def IsOutputLogCorrectAtSeverity(self, severity,
    expected_msg_count):
    msg_count = self.validator.CountErrors(severity)

    if msg_count != expected_msg_count:
      print ('TEST FAILED: %s\nexpected %d %s[s], observed %d\n%s\n'
         % (self.validator.line, expected_msg_count, severity,
           msg_count,
          str(self.validator.output_log[severity])))
      return False
    return True

  def IsOutputLogCorrect(self, new_errors, new_warnings):
    retval = True

    if not self.IsOutputLogCorrectAtSeverity('ERROR', new_errors):
      retval = False
    if not self.IsOutputLogCorrectAtSeverity('WARNING',
                                             new_warnings):
      retval = False

    return retval

  def TestFeedLine(self, line, warning_count, error_count):
    self.validator.output_log['WARNING'] = []
    self.validator.output_log['ERROR'] = []
    self.validator._ValidateLine(line)

    if not self.IsOutputLogCorrect(warning_count, error_count):
      self.failures += 1
      return False

    self.successes += 1
    return True


if __name__ == '__main__':
  IPGeoFeedValidatorTest().Run()

#!/usr/bin/env python 
"""Module docstring 
"""

import sys
import mortgage_tools

if __name__ == '__main__':
  args = mortgage_tools.parse_args()
  mortgage_tools.print_args( args )
  mortgage_tools.table( args )

#!/usr/bin/env python 

import sys
import mortgage

if __name__ == '__main__':
  args = mortgage.parse_args()
  mortgage.print_args( args )
  mortgage.table( args )

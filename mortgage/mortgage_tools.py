#/usr/bin/env python 

import argparse 
from datetime import datetime

def parse_args():
  desc = 'Print mortgage tables'
  parser = argparse.ArgumentParser( description=desc )
  parser.add_argument( '--apr', 
      type = float,
      default = 4.375,
      help = "APR in %% (E.g. 4.5)" )
  parser.add_argument( '--monthly', 
      type = float,
      default = 0,
      help = "Monthly payment (0 for minimum)" )
  parser.add_argument( '--annual', 
      type = float,
      default = 0,
      help = "Annual extra payment (0 for minimum)" )
  parser.add_argument( '--term', 
      type = int,
      default = 30,
      help = "Term in years" )
  parser.add_argument( '--taxrate', 
      type = float,
      default = 1.25,
      help = "County property tax" )
  parser.add_argument( '--value', 
      type = float,
      default = 1090000.0,
      help = "Principal amount" )
  parser.add_argument( '--principal', 
      type = float,
      default = 872000.0,
      help = "Principal amount" )
  parser.add_argument( '--start', 
      type = str,
      default = "2012/10/1",
      help = "Date of first payment" )
  parser.add_argument( '--payments', 
      type = str,
      default = "",
      help = "File containing payments made thus far (CSV or SSV)" )
  parser.add_argument( '--verbose', 
      type = int,
      default = 0,
      help = "Verbosity level" )
  args = parser.parse_args()
  args = compute_monthly_payment( args )
  args = load_payments( args )
  args = compute_date( args )

  return args

def print_args( args ):
  print( "Start date: %s" % args.start.date() )
  print( "Principal: $%d" % args.principal )
  print( "Interest: %.3f%%" % args.apr )
  print( "Term: %.1f years" % args.term )
  print( "Property tax rate: %.3f" % args.taxrate )
  print( "Monthly payment: $%.2f (minimum: $%.2f)" % ( args.monthly,
    args.min_monthly) )
  if len( args.paid ):
    print( "Imported payments for %d months" % len( args.paid ) )
  print( "Annual supplemental payment: $%.2f" % args.annual)


def load_payments( args ):
  """
  """
  paid = list()
  if args.payments != '':
    try:
      f = open( args.payments )
      for l in f.readlines():
        paid.extend( l.split() )
      f.close()
      print( 'Imported %d payments from %s' % ( len( paid ), args.payments ) )
    except:
      print( 'Cannot load %s to import payments made' )
  args.paid = list( float( p ) for p in paid )

  return args


def compute_date( args ):
  dd = [2012,10,1]
  for s in ['/', '-']:
    if len( args.start.split( s ) ) == 3:
      dd = list( int( x ) for x in args.start.split( s ) )
      break
  args.start = datetime( dd[0], dd[1], dd[2] )
  return args
    

def compute_monthly_payment( args ):
  """
  """
  p = args.principal
  r = 1. + args.apr / 12. / 100.
  t = 12 * args.term
  args.min_monthly = p * pow( r, t ) * ( 1 - r ) / ( 1 - pow( r, t ) )
  if args.monthly == 0:
    args.monthly = args.min_monthly

  return args


def table( args ):
  '''
  Compute the table 
  '''
  t = args.term * 12
  r = 1 + args.apr / 12. / 100.
  p = args.principal
  m = args.monthly
  a = args.annual
  paid = args.paid
  dd = args.start

  rp = p     # remaining principal
  tp = 0     # total principal
  ti = 0     # total interest

  if args.verbose > 0:
    print( '\n' )
    print( '%6s %6s %10s %10s %10s %12s' % 
        ( 'Year', 'Month', 'Int.', 'Avg. Int', 'Rem. Pr.', 'Date' ) )
    print( '%s' % ''.join( '-' for i in range( 60 ) ) )

  month = 0
  year = 0
  for i in range( int( t ) ):
    month = ( i ) % 12 + 1
    year = int( ( i ) / 12 )
    # current payment (monthly + annual)
    cp = m + a if month == 12 else m
    # override from imported 
    if len( paid ) > i:
      cp = paid[i]
      #print 'cp = %.2f' % cp
    
    # interest for month i
    ii = rp * ( r - 1 )    # interest for month i
    # remaining principal before monthly payment
    rp += ii               # remaining principal
    # total interest paid
    ti += ii
    # total principal paid
    tp += cp - ii if rp > cp else rp - ii
    # principal for this month
    pi = cp - ii if rp > cp else rp - ii 
    # remaining principal after monthly payment 
    rp -= cp if rp > cp else rp              
    # average interest paid so far (rest is equity)
    ai = ti / ( i + 1 )

    ppp = True if args.verbose > 0 and i <= len(paid) else False
    ppp = True if args.verbose > 1 and ( month == 12 or rp == 0 ) else ppp
    ppp = True if args.verbose > 2 else ppp
    if ppp:
      print( '%6d %6d %10.0f %10.0f %10.0f %12s' % 
          ( year, month, ii, ai, rp, dd.date() ) )
    if rp <= 0.00001:
      break
    dd = datetime( dd.year+1, 1, dd.day ) if dd.month == 12 else datetime(
        dd.year, dd.month+1, dd.day )

  print( "--" )
  print( "Last payment at %d years, %d months" % ( year, month ) )
  ti_min_pay = float( args.min_monthly ) * t - float( p )
  print( "Total interest based on min payment: $%.0f " % ( ti_min_pay ) )
  print( "Total interest paid: $%.0f (less: $%.0f)" % ( ti, ti_min_pay - ti ) )
  print( "Interest averaged monthly: $%.0f " % ( ai ) )
  ptax = args.value * args.taxrate / 100;
  print( "Property tax averaged monthly: $%.0f (annual: $%.0f)" % ( ptax / 12,
    ptax ) )


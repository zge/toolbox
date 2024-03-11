# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 20:33:57 2023

@author: gezhe
"""

def interest2apy(r, n=365):
  """calculate APY from annual interest rate"""
  # r: annual interest rate
  # n: compound freq (monthly:12, daily:365)
  # apy: annual percentage yeild
  apy = (1+r/n) ** n - 1
  return apy

def apy2interest(apy, n=365):
  """calculate annual interest rate from APY"""
  r = n * ((apy+1)**(1/n) - 1)
  return r

# example 1: calculate APY from interest rate
r = 0.0464
apy = interest2apy(r)
print("interest rate: {:.2f}% --> APY: {:.2f}%".format(r*100, apy*100))

# example 2: calculate interest rate from APY
apy = 0.0475
r = apy2interest(apy)
print("APY: {:.2f}% --> interest rate: {:.2f}%".format(apy*100, r*100))
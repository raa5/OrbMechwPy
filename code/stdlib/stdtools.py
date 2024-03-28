#--------------------------------------------------------------------------------
# Husseinat Etti-Balogun
# 28/03/2024
#---------------------------- IMPORTS ------------------------------------------------------
import math as m

#---------------------------- CONSTANTS ----------------------------------------------------

G = 6.67e-11 # universal constant of gravitation
a = 2160000 #semi major axis in meters
Kerbin_mass = 5.29e22 # mass of the body in kg
e = 0.832 # eccentricity
t = 900 # time elapsed in seconds
a = 2160000 #semi major axis in meters

#---------------------------- EQUATIONS ----------------------------------------------------

Kerbin_mass = 5.29e22 # mass of the body in kg
mu = G * Kerbin_mass # kerbin grav const 
T = 2 * m.pi * m.sqrt( (a**3) / mu ) # the orbital period of rocket around Kerbin in days
n = ( 2 * m.pi ) / T # mean motion of the rocket rad/sec
mu = G * Kerbin_mass # kerbin grav const 
M = n * t # mean anomaly

args = [ e, M ]
E0 = M - e

#---------------------------- FUNCTION DEFINITIONS ------------------------------------------

def Kepler(E, args):
    ''' Defines the function of Kepler's equation '''
    return ( E + (args[0] * m.sin(E) - args[1]))

def KeplerDeriv (E, args):
    ''' Defines the derivative function of Kepler's equation '''
    return ( 1 - args[0] * m.cos(E))

def NewtonsAlgotrithm (f, f_prime, current_guess, args, tolerance=0.01):
    ''' Returns current guess and step number using Newtons numerical method of root solving variable functions '''
    step = 1 # step counter

    delta_f = f(current_guess, args) / f_prime(current_guess, args) # calculate the ratio of function and derivative

    # start loop and break when absolute of delta_f is less than tolerance
    while abs( delta_f ) > tolerance:

        current_guess -= delta_f # calculate next current guess

        delta_f = f(current_guess, args) / f_prime(current_guess, args) # calculate new delta_f

        step += 1 # increment step

    return current_guess, step


def TrueAnomaly():
    ''' Returns true anomaly value (nu) '''
    eccAnom, steps = NewtonsAlgotrithm(Kepler, KeplerDeriv, E0, args )
    eccFrac = ( 1 - e ) / ( 1 + e )
    halfEccAnom = eccAnom / 2
    nu = 2 * m.atan( m.sqrt( eccFrac * m.tan(halfEccAnom )) )
    return nu 

def polarEqn():
    ''' Returns return radial value of position of rocket '''
    p = a * ( 1 - e**2)
    newDeriv = 1 + e * m.cos(TrueAnomaly())
    r = p / newDeriv
    return r

def visViva():
    ''' Returns return velocity at elapsed time using Vis Viva equation '''
    r = polarEqn()
    v = m.sqrt(mu * ( ( 2 / r ) - ( 1 / a )))
    return v
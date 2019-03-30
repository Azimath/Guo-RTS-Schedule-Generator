#GCD and LCM functions from https://gist.github.com/endolith/114336/eff2dc13535f139d0d6a2db68597fad2826b53c3

def gcd(a,b):
    """Compute the greatest common divisor of a and b"""
    while b > 0:
        a, b = b, a % b
    return a
    
def lcm(a, b):
    """Compute the lowest common multiple of a and b"""
    return a * b / gcd(a, b)
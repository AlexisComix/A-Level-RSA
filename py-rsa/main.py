from math import lcm
from egcd import egcd
from typing import Tuple
from sympy import randprime


class RSA:
    def __init__(self):
        self.__p = 73#self.rand_large_prime()
        self.__q = 103#self.rand_large_prime()
        self.__n = self.__p * self.__q
        self.__totient = self.prime_ctotient(self.__p, self.__q)
        self.__e = self.__compute_e()
        self.__private_key = self.__compute_key()

    def get_public_key(self) -> Tuple[int, int]:
        """
        Returns the public key, (n, e).
        """
        return (self.__n, self.__e)

    @staticmethod
    def encrypt(m: int, key: Tuple[int, int]) -> int:
        """
        Encrypts m with key (n, e) to a value c such that
        c === m^e mod n
        """
        n = key[0]
        e = key[1]
        return (m ** e) % n 

    def decrypt(self, c: int) -> int:
        """
        Decrypts c to find m such that
        m = c^d mod n
        """
        return (c**self.__private_key) % self.__n
  
    def __compute_e(self) -> int:
        e = self.__totient
        while self.__totient % e == 0: # while e not coprime to tot
            e = randprime(2, self.__totient)
        return e

    def __compute_key(self) -> int:
        """
        Computes the key (d) by using the extended euclidean
        algorithm to find a value x (_, x, _) and then returning
        x mod the totient.
        The EEU returns the GCD, and the two coefficients to Bezout's
        identity, revealing the modular multiplicative inverse as
        the first coefficient. 
        """
        _, x, _ = egcd(self.__e, self.__totient)
        return x % self.__totient
   
    @staticmethod
    def rand_large_prime() -> int:
        """
        Gnerate a random large prime number     
        """
        return randprime(64, 256)

    @staticmethod
    def prime_ctotient(p: int, q: int) -> int:
        """
        Calculates Carmichael's Totient function for a number
        n = pq where p and q are prime numbers.
        """
        return lcm(p - 1, q - 1)

    def debug(self):
        print(self.__n, self.__totient, self.__private_key, self.__e)


if __name__ == "__main__":
    print("Running...")
    
    A = RSA()
    B = RSA()
    
    A.debug()
    
    message = 65
    
    A_key = A.get_public_key()
    encrypted = RSA.encrypt(message, A_key)
    decrypted = A.decrypt(encrypted)
    
    print(message, encrypted, decrypted)
    assert message == decrypted
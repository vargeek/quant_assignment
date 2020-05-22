#%%
import numpy as np
from scipy.stats import norm

class EuropeanOption:
    def __init__(self, S, K, T, sigma, r, call_or_put='C'):
        """
        :param S: underlying assets price  
        :param K: strike price  
        :param T: Time to maturity(represented as a unit-less fraction of one year)  
        :param sigma: Volatility sigma  
        :param r: risk-free rate  
        :param call_or_put: 'C' for call, 'P' for put  
        """
        self.S = S
        self.K = K
        self.T = T
        self.sigma = sigma
        self.r = r
        self.call_or_put = call_or_put
    
    def get_option_price(self, sigma=None):
        """
        定价
        """
        sigma = self.sigma if sigma is None else sigma
        if self.call_or_put == 'C':
            self.price = self.calculate_call_price(sigma)
            self.delta = self.calculate_call_delta()
        else:
            self.price = self.calculate_put_price(sigma)
            self.delta = self.calculate_put_delta()

    def calculate_d1_d2(self, sigma=None):
        sigma = self.sigma if sigma is None else sigma
        tmp = sigma * np.sqrt(self.T)
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * sigma ** 2) * self.T) / tmp
        d2 = d1 - tmp

        return d1, d2
    def calculate_d1(self, sigma=None):
        sigma = self.sigma if sigma is None else sigma
        tmp = sigma * np.sqrt(self.T)
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * sigma ** 2) * self.T) / tmp

        return d1

    def calculate_call_price(self, sigma):
        d1, d2 = self.calculate_d1_d2(sigma)

        C = self.S * self.N(d1) - self.K * np.exp(-self.r * self.T) * self.N(d2)
        return C

    def calculate_put_price(self, sigma):
        d1, d2 = self.calculate_d1_d2(sigma)

        P = self.K * np.exp(-self.r * self.T) * self.N(-d2) - self.S * self.N(-d1)

        return P

    def calculate_call_delta(self):
        d1 = self.calculate_d1()

        delta = np.exp(-self.r * self.T) * self.N(d1) 
        return delta

    def calculate_put_delta(self):
        d1 = self.calculate_d1()

        delta = -norm.cdf(-d1, 0.0, 1.0)
        return delta

    def calculate_gamma_test(self, h):
        option1 = EuropeanOption(self.S+h, self.K, self.T, self.sigma, self.r, call_or_put=self.call_or_put)
        option2 = EuropeanOption(self.S-h, self.K, self.T, self.sigma, self.r, call_or_put=self.call_or_put)
        gamma = (option1.get_option_price() - 2 * self.price + option2.get_option_price()) / h**2
        return gamma

    def calculate_gamma(self):
        tmp = self.sigma * np.sqrt(self.T)
        d1 = (np.log(self.S / self.K) + (0.5 * self.sigma ** 2) * self.T) / tmp
        gamma = self.n(d1) * np.exp(-self.r * self.T) / (self.S * self.sigma * np.sqrt(self.T))
        return gamma

    def calculate_vega(self):
        d1 = self.calculate_d1()
        
        vega = self.S * norm.cdf(d1, 0.0, 1.0) * np.sqrt(self.T)

        return vega

    def calculate_call_theta(self):
        d1, d2 = self.calculate_d1_d2()
        prob_density = 1 / np.sqrt(2 * np.pi) * np.exp(-d1 ** 2 * 0.5)
        
        theta = (-self.sigma * self.S * prob_density) / (2 * np.sqrt(self.T)) - self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(d2, 0.0, 1.0)
        
        return theta

    def calculate_put_theta(self):
        d1, d2 = self.calculate_d1_d2()
        prob_density = 1 / np.sqrt(2 * np.pi) * np.exp(-d1 ** 2 * 0.5)
                
        prob_density = 1 / np.sqrt(2 * np.pi) * np.exp(-d1 ** 2 * 0.5)
        
        theta = (-self.sigma * self.S * prob_density) / (2 * np.sqrt(self.T)) + self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-d2, 0.0, 1.0)
        
        return theta

    def calculate_theta(self):
        if self.call_or_put == 'C':
            return self.calculate_call_theta()
        else:
            return self.calculate_put_theta()

    def calculate_iv(self, option_price):
        """
        calculate option implied vol using bisection method
        """
        def f(sigma):
            return self.get_option_price(sigma) - option_price

        a = 0
        b = 10
        N = 1024
        if f(a)*f(b) >= 0:
            print("Bisection method fails.")
            return None
        a_n = a
        b_n = b
        for _ in range(1,N+1):
            m_n = (a_n + b_n)/2
            f_m_n = f(m_n)
            if f(a_n)*f_m_n < 0:
                a_n = a_n
                b_n = m_n
            elif f(b_n)*f_m_n < 0:
                a_n = m_n
                b_n = b_n
            elif f_m_n == 0:
                print("Found exact solution.")
                return m_n
            else:
                print("Bisection method fails.")
                return None
        return (a_n + b_n)/2

    @staticmethod
    def N(x):
        return norm.cdf(x)

    @staticmethod
    def n(x):
        return np.exp(-x**2) / np.sqrt(2 * np.pi)

if __name__ == "__main__":
    pass


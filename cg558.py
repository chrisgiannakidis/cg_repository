from math import sqrt , pi ,log , e
from scipy.stats import norm

class Greeks :
    def __init__ (self , args ):
        self.Type = int (args [0])
        self.S = float (args [1])
        self.K = float (args [2])
        self.r = float (args [3])
        self.q = float (args [4])
        self.T = float (args [5]) / 365.0
        self.sigma = float (args [6])
        self.sigmaT = self.sigma * self.T ** 0.5
        self.d1 = (log(self.S / self.K) + \
        (self.r - self.q + 0.5 * (self.sigma ** 2)) \
        * self.T) / self.sigmaT
        self.d2 = self.d1 - self.sigmaT
        
        [ self.Value ] = self.value ()
        [ self.Delta ] = self.delta ()
        [ self.Vega ] = self.vega ()
        [ self.Theta ] = self.theta ()
        [ self.Rho ] = self.rho ()
        [ self.Gamma ] = self.gamma ()
        [ self.Vanna ] = self.vanna ()
        [ self.Charm ] = self.charm ()
        [ self.Vomma ] = self.vomma ()
        [ self.Veta ] = self.veta ()
        [ self.Speed ] = self.speed ()
        [ self.Zomma ] = self.zomma ()
        [ self.Color ] = self.color ()
        [ self.Ultima ] = self.ultima ()
        [ self.Dual_Delta ] = self.dual_delta ()
        [ self.Dual_Gamma ] = self.dual_gamma ()
        [ self.Phi ] = self.phi ()
        
    def value ( self ):
        dfq = e ** (- self.q * self.T)
        dfr = e ** (- self.r * self.T)
        if self.Type == 1:
            return [self.S * dfq * norm.cdf(self.d1) - dfr * self.K * 
                    norm.cdf(self.d2)]
        else :
            return [dfr * self.K * norm.cdf(-self.d2) - self.S * dfq * 
                    norm.cdf(- self.d1)]
        
    def delta ( self ):
        dfq = e ** (- self.q * self.T)
        
        if self.Type == 1:
            return [ dfq * norm.cdf (self.d1 )]
        else :
            return [- dfq * ( norm.cdf ( - self.d1 ))]
        
    def vega ( self ):
        return [0.01 * self.S * e ** (- self.q * self.T) * \
                norm.pdf ( self.d1) * self.T ** 0.5]
                
    def theta ( self ):
        dfr = e ** (- self.r * self.T)
        dfq = e ** (- self.q * self.T)
        
        if self.Type == 1:
            return [- 0.5 * dfq * self.S * norm.cdf(self.d1) * self.sigma / 
                    ((self.T) ** (0.5)) - self.r * self.K * dfr * 
                    norm.cdf(self.d2) + self.q * self.S * dfq *  
                    norm.cdf(self.d1)]
            
        else :
            return [- 0.5 * dfq * self.S * norm.cdf(self.d1) * self.sigma / 
                    ((self.T) ** (0.5)) + self.r * self.K * dfr * 
                    norm.cdf(- self.d2) - self.q * self.S * dfq *  
                    norm.cdf(- self.d1)]
    
    def rho ( self ):
      dfr = e ** (- self.r * self.T)
      
      if self.Type == 1:
          return [self.K * self.T * dfr *  norm.cdf(self.d2)]
      
      else :
          return [- self.K * self.T * dfr *  norm.cdf(- self.d2)]
    
    def gamma ( self ):
        return [e ** (- self.q * self.T) * norm.pdf (self.d1) / 
                ( self.S * self.sigmaT )]

    def vanna ( self ):
        return [e ** (- self.q * self.T) * norm.pdf (self.d1) * self.d2 /
                self.sigma]    
    
    def charm ( self ):
        dfq = e ** (- self.q * self.T)
        
        if self.Type ==1:
            return [self.q * dfq * norm.cdf(self.d1) - dfq * norm.pdf(self.d1)
                     * (2 * (self.r - self.q) * self.T - self.d2 * self.sigmaT)
                     /(2 * self.T * self.sigmaT)]
            
        else :
            return [- self.q * dfq * norm.cdf(- self.d1) - dfq * 
                    norm.pdf(self.d1) * (2 * (self.r - self.q) * self.T - \
                             self.d2 * self.sigmaT) / (2 * self.T * \
                                                  self.sigmaT)]
            
    def vomma ( self ):
        return [self.S * (e ** (- self.q * self.T)) * norm.pdf (self.d1) * 
                ((self.T) ** (0.5)) * self.d1 * self.d2 / self.sigma]
    
    def veta ( self ):
        a = (self.r * - self.q) * self.d1 / self.sigmaT
        b = (1 + self.d1 * self.d2) / (2 * self.T)
        dfq = e ** (- self.q * self.T)
        
        return [self.S * dfq * norm.pdf(self.d1) * ((self.T) ** (0.5)) *
                (self.q + a -b)]
    
    def speed ( self ):
        dfq = e ** (- self.q * self.T)
        
        return [- dfq * norm.pdf (self.d1) * (1 + self.d1 / self.sigmaT) / 
                (((self.S) ** 2) * self.sigmaT)]
    
    def zomma ( self ):
        dfq = e ** (- self.q * self.T)
        
        return [dfq * norm.pdf (self.d1) * (self.d1 * self.d2 - 1) /
                (self.S) * self.sigma * self.sigmaT]
    
    def color ( self ):
        a = self.d1 * (2 * (self.r - self.q) * self.T - self.d2 * self.sigmaT) \
        / self.sigmaT
        dfq = e ** (- self.q * self.T)
        
        return [-dfq * norm.pdf(self.d1) / (2 * self.S * self.T * self.sigmaT)
                * (2 * self.q * self.r + 1 + a)]
    
    def ultima ( self ):
        dfq = e ** (- self.q * self.T)
        V = self.S * dfq * norm.pdf (self.d1) * ((self.T) ** (0.5))
        
        b = self.d1 * self.d2 * (1 - self.d1 * self.d2) + self.d1 ** 2 + \
        self.d2 ** 2

        return [- V * b  / ((self.sigma) ** 2)]
    
    def dual_delta ( self ):
        dfr = e ** (- self.r * self.T)
        
        if self.Type == 1:
            return [- dfr * norm.cdf(self.d2)]
        else :
            return [ dfr * norm.cdf(- self.d2)]

    def dual_gamma ( self ):
        dfr = e ** (- self.r * self.T)
        
        return [- dfr * norm.pdf (self.d2) / (self.K * self.sigmaT)]
    
    def phi ( self ):
        return [0.01* -self.Type * self.T * self.S * \
        e ** (- self.q * self.T) * norm . cdf (self.Type * self .d1 )]
    
               
    
        
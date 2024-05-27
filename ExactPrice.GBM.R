#this code returns the exact price of European options under GBM framework (Black-Scholes formula)

#input:
#S.0: initial asset price
#MT: maturity time
#r: risk-free rate
#sigma: volatility
#K: strike price
#type: option type, either 'put' or 'call' 

#output:
#exact.price: exact price of European options under GBM framework (Black-Scholes formula)

ExactPrice.GBM <- function(S.0,MT,r,sigma,K,type){
  if (type == 'call'){
    #exact option prices using Black-Scholes formula
    exact.price=S.0*pnorm((log(S.0/K)+(r+sigma^2/2)*MT)/(sigma*sqrt(MT)))-K*exp(-r*MT)*pnorm((log(S.0/K)+(r-sigma^2/2)*MT)/(sigma*sqrt(MT)))}else{
      exact.price=K*exp(-r*MT)*pnorm((log(K/S.0)-(r-sigma^2/2)*MT)/(sigma*sqrt(MT)))-S.0*pnorm((log(K/S.0)-(r+sigma^2/2)*MT)/(sigma*sqrt(MT)))
    }
  
  return (exact.price)
}
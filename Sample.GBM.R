#this code generates n sample paths of a Geometric Brownian motion that is monitored d times 

#input:
#S.0: initial asset price
#MT: maturity time
#r: risk-free rate
#sigma: volatility
#d: monitoring frequency 
#n: simulation size

#output:
#S: n*d matrix with n sample paths of GBM,the initial asset price is not included

Sample.GBM <- function(S.0,MT,r,sigma,d,n){
  #generate nxd pseudo-random normal numbers (n sample paths with d time nodes for each path)
  x<-matrix(rnorm(n*d),nrow=n)
  
  #generate n sample paths of Brownian Motion
  delta <- MT/d
  #when d=1, BM is a n*1 vector that needs special handling
  if(d==1) BM<-sqrt(delta)*as.matrix(apply(x,1,cumsum)) else BM<- sqrt(delta)*t(apply(x,1,cumsum))
  
  
  #generate n sample paths of stock price
  grid<-seq(delta,MT,length.out=d) #time grid
  S<-S.0*exp(sweep(sigma*BM,MARGIN=2,(r-sigma^2/2)*grid,'+')) #calculate sample paths using Geometric Brownian motion
  
  return (S)
}
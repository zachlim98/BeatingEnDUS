library(riingo)
library(ggplot2)
library(tidyverse)

RIINGO_TOKEN <- "1bc7cb8276a48813f93a1ad4633420444e39e500"

#set token for riingo
riingo_set_token(RIINGO_TOKEN) 
#get prices for ROKU
aapl_price <- riingo_prices("AAPL", start_date = "2019-01-01") 
#calculate log daily returns
returns_tib <- tibble(returns = diff(log(aapl_price$adjClose), lag=1))

aapl_daily_returns <- roku_price %>%
  tq_transmute(select = adjClose,           # this specifies which column to select   
               mutate_fun = periodReturn,   # This specifies what to do with that column
               period = "daily",      # This argument calculates Daily returns
               col_rename = "aapl_returns")

#plot log daily returns
returns_tib %>% ggplot(aes(x=returns)) +
  geom_density(fill="#69b3a2", color="#e9ecef", alpha=0.8) +
  labs(y="Density", x="Returns", title="Distribution of AAPL returns (1 year)")

u = mean(returns_tib$returns)
var = var(returns_tib$returns)
drift = u - (0.5*var)
stdd = sqrt(var)

gbm_vec <- function(nsim = 100, t = 25, mu = 0, sigma = 0.1, S0 = 100, dt = 1./365) {
  # matrix of random draws - one for each day for each simulation
  epsilon <- matrix(rnorm(t*nsim), ncol = nsim, nrow = t)  
  # get GBM and convert to price paths
  gbm <- exp((mu - sigma * sigma / 2) * dt + sigma * epsilon * sqrt(dt))
  gbm <- apply(rbind(rep(S0, nsim), gbm), 2, cumprod)
  return(gbm)
}

nsim <- 1000
t <- 37
mu <- u
sigma <- stdd
S0 <- 135.39

gbm <- gbm_vec(nsim = 1000, t = 37, mu = 0.2368, sigma = 2.37, S0)

gbm_df <- as.data.frame(gbm) %>%
  mutate(ix = 1:nrow(gbm)) %>%
  pivot_longer(-ix, names_to = 'sim', values_to = 'price')

gbm_df %>%
  ggplot(aes(x=ix, y=price, color=sim)) +
  geom_line() +
  labs(x="Days", y="Price", title="1000 Simulations of AAPL price") +
  theme(legend.position = 'none')

BlackScholes <- function(S, K, r, T, sig, type){
  
  if(type=="C"){
    d1 <- (log(S/K) + (r + sig^2/2)*T) / (sig*sqrt(T))
    d2 <- d1 - sig*sqrt(T)
    
    value <- S*pnorm(d1) - K*exp(-r*T)*pnorm(d2)
    return(value)}
  
  if(type=="P"){
    d1 <- (log(S/K) + (r + sig^2/2)*T) / (sig*sqrt(T))
    d2 <- d1 - sig*sqrt(T)
    
    value <-  (K*exp(-r*T)*pnorm(-d2) - S*pnorm(-d1))
    return(value)}
}

putPrice <- matrix(0,38,1000)

for (s in 1:ncol(gbm)){
  for (t in 1:nrow(gbm)) {
    putPrice[t,s] <- BlackScholes(gbm[t,s], 122.5, 0.01, (nrow(gbm)+1-t)/365, 0.37, "P")
  }
}

plottest <- as.data.frame(putPrice) %>%
  mutate(ix = 1:nrow(gbm)) %>%
  pivot_longer(-ix, names_to = 'sim', values_to = 'price')

plottest %>%
  ggplot(aes(x=ix, y=price, color=sim)) +
  geom_line() +
  labs(x="Days", y="Price", title="1000 Simulations of AAPL 122.5 Put Price") +
  coord_cartesian(
    xlim = NULL,
    ylim = c(0,3),
    expand = TRUE,
    default = FALSE,
    clip = "on"
  ) +
  theme(legend.position = 'none')

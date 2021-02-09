library(tabulizer)
library(dplyr)

out <- extract_tables("P:/Adulting/Banking/Tsel/Account Statements/Oct20_TD.pdf")

table1 <- out[5][[1]]

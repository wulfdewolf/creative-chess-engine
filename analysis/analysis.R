library(ggplot2)

data <- read.csv("~/Documents/studies/2/CC/creative-chess-engine/analysis/creative_engine_learnt.csv", header=FALSE)

ggplot(data, aes(x = seq(1, 298))) +
  geom_line(aes(y = V1, colour = "Unkown move")) +
  geom_line(aes(y = V2, color = "Low winrate")) + 
  geom_line(aes(y = V3, color = "Suboptimal capture")) +
  geom_line(aes(y = V4, color = "Sacrifice")) + 
  geom_line(aes(y = V5, color = "Optimality"))

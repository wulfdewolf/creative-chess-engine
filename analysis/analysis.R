
library(ggplot2)

data <- read.csv("~/Documents/studies/2/CC/creative-chess-engine/analysis/selfplay/white_learnt.csv", header=FALSE)

# Evolution of the weights
ggplot(data, aes(x = seq(1, 997))) +
  geom_line(aes(y = V1, color = "Unkown move")) +
  geom_line(aes(y = V2, color = "Low winrate")) + 
  geom_line(aes(y = V3, color = "Suboptimal capture")) +
  geom_line(aes(y = V4, color = "Sacrifice")) + 
  geom_line(aes(y = V5, color = "Optimality")) + 
  xlab("Game") + 
  ylab("Weight") + 
  labs(colour = "Type")

# Histogram game results
barplot(table(data$V6), xlab="Game result", ylab="Games")

data <- read.csv('link_node_ratio_output/pegonet_ratios_second_first.csv')
avgratios <- vector()
tmplist <- split(data, data$X.nodesInPegonet)
for (i in 1:length(tmplist)) {
    tmpdf <- tmplist[[i]]
    avgratios <- c(avgratios, mean(tmpdf$ratioForPegonet))
}
rsdf <- data.frame(nbNodesInPegonet = as.numeric(names(tmplist)), avgRatios = avgratios)
write.csv(rsdf, file = "link_node_ratio_output/pegonet_avgratios_second_first.csv", row.names=FALSE)


data <- read.csv('link_node_ratio_output/pegonet_ratios_third_first.csv')
avgratios <- vector()
tmplist <- split(data, data$X.nodesInPegonet)
for (i in 1:length(tmplist)) {
    tmpdf <- tmplist[[i]]
    avgratios <- c(avgratios, mean(tmpdf$ratioForPegonet))
}
rsdf <- data.frame(nbNodesInPegonet = as.numeric(names(tmplist)), avgRatios = avgratios)
write.csv(rsdf, file = "link_node_ratio_output/pegonet_avgratios_third_first.csv", row.names=FALSE)


data <- read.csv('link_node_ratio_output/pegonet_ratios_third_second.csv')
avgratios <- vector()
tmplist <- split(data, data$X.nodesInPegonet)
for (i in 1:length(tmplist)) {
    tmpdf <- tmplist[[i]]
    avgratios <- c(avgratios, mean(tmpdf$ratioForPegonet))
}
rsdf <- data.frame(nbNodesInPegonet = as.numeric(names(tmplist)), avgRatios = avgratios)
write.csv(rsdf, file = "link_node_ratio_output/pegonet_avgratios_third_second.csv", row.names=FALSE)

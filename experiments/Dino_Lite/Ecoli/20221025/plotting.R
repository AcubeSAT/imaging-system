# Load libraries
library(dplyr)
library(tidyverse)
library(ggplot2)
library(RColorBrewer)
library(wesanderson)

# Set paths
data_path <- 
data_filename <- 

# Set wd
setwd(data_path)

# Load data
data <- read.csv(file.path(data_path, file.path(data_filename, "csv", fsep = ".")), header = TRUE, stringsAsFactors = FALSE)

gp1 <- wes_palettes$Darjeeling1
gp2 <- wes_palettes$Darjeeling2

data_plot <- filter(data, 
(Construct %in% c("BBa_J364000") | Construct %in% c("BBa_J364007")))

# Plotting
ggplot(data_plot, aes(x = as.numeric(Concentration), y = as.numeric(Mean)))+
    geom_point(color = "#87c487", size = 6) +
    geom_smooth(aes(color = Construct), se = FALSE, span = .25) +
    # geom_smooth() +
    theme_bw(base_size = 20) +
    scale_color_manual(values = wes_palette(n = 3, name = "Darjeeling1")) +
    # geom_errorbar(aes(ymin=Mean-sd, ymax=Mean+sd), width=.2,
    # position=position_dodge(.01)) +  
    labs(x = "Cell density factor", y = "Brightness (a.u.)") +
    theme(strip.text = element_text(face = "bold",
                                  hjust = 0, size = 20),
        strip.background = element_rect(fill = "#FFFFFF"))


ggsave("20221025_CK_000_07.pdf")
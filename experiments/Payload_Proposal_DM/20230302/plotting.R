# Load libraries
library(dplyr)
library(tidyverse)
library(ggplot2)
library(RColorBrewer)
library(wesanderson)

# Set paths
data_path <-
data_filename <- "20230302_IK"

# Set wd
setwd(data_path)

# Load data
data <- read.csv(file.path(data_path, file.path(data_filename, "csv", fsep = ".")), header = TRUE, stringsAsFactors = FALSE)

# Exclude wells with just media or water
data_plot <- subset(data, Type != "Blank")

# Select wells with just media or water
# data_plot <- subset(data, Type == "Blank")

# Rename values
data_plot[data_plot == "I"] <- "E. coli (J23100)"
data_plot[data_plot == "K"] <- "E. coli (J23104)"
data_plot[data_plot == "C"] <- "E. coli (J23101)"
data_plot[data_plot == "E"] <- "E. coli (J23106)"
data_plot[data_plot == "M"] <- "E. coli (J23116)"
data_plot[data_plot == "G"] <- "E. coli (J23117)"

data_plot[data_plot == "YHL033C"] <- "Yeast (YHL033C)"
data_plot[data_plot == "YIL066C"] <- "Yeast (YIL066C)"
data_plot[data_plot == "YML058W"] <- "Yeast (YML058W)"

# Order strains (E. coli plasmids by expression strength)
# data_plot$Strain <- factor(data_plot$Strain, levels = c("Fluorescein", "YHL033C", "YIL066C", "YML058W", "I", "K", "C", "E", "M", "G"))

data_plot$Strain <- factor(data_plot$Strain, levels = c("Fluorescein", "Yeast (YHL033C)", "Yeast (YIL066C)", "Yeast (YML058W)", "E. coli (J23100)", "E. coli (J23104)", "E. coli (J23101)", "E. coli (J23106)", "E. coli (J23116)", "E. coli (J23117)"))


# Choose color palettes
gp1 <- wes_palettes$Darjeeling1
gp2 <- wes_palettes$Darjeeling2

# Plotting
ggplot(data_plot, aes(x = as.factor(Concentration), y = as.numeric(Mean)))+
    geom_point(color = "#87c487", size = 6) +
    # geom_smooth() +
    theme_bw(base_size = 25) +
    # geom_errorbar(aes(ymin=Mean-sd, ymax=Mean+sd), width=.2,
    # position=position_dodge(.01)) +  
    labs(x = "Concentration factor", y = "Brightness (a.u.)") +
    theme(strip.text = element_text(face = "bold", hjust = 0, size = 20),
        strip.background = element_rect(fill = "#FFFFFF"),
        axis.text.x = element_text(angle=60, hjust=1)) +
    facet_wrap(~Strain)
    # facet_grid(cols = vars(Strain), rows = vars(Type))

ggsave("20230302_IK.pdf")

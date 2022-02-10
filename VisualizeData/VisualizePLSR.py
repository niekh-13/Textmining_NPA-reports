##############################################################
#                                                            #
#    Niek Huijsmans (2021)                                   #
#    Textmining medical notes for cognition                  #
#    Visualizing                                             #
#                                                            #
##############################################################

# Import the relevant packages
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from pathlib import Path


class VisualizeDataset:
    point_displays = ['+', 'x'] #'*', 'd', 'o', 's', '<', '>']
    line_displays = ['-'] #, '--', ':', '-.']
    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']

    # Set some initial attributes to define and create a save location for the images.
    def __init__(self, module_path:str='.py'):
        subdir = Path(module_path).name.split('.')[0]

        self.plot_number = 1
        self.figures_dir = Path('figures') / subdir
        self.figures_dir.mkdir(exist_ok=True, parents=True)

    def save(self, plot_obj, formats=('png',)):  # 'svg'

        fig_name = f'figure_{self.plot_number}'

        for format in formats:
            save_path = self.figures_dir / f'{fig_name}.{format}'
            plot_obj.savefig(save_path)
            print(f'Figure saved to {save_path}')

        self.plot_number += 1

    def boxplot(self, data):
        plot = sns.boxplot(y='value', x='variable',
                           data=data,
                           width=0.5,
                           palette="colorblind",
                           orient="v")
        return plot

    def swarmplot(self, data):
        plot = self.boxplot(data)
        plot = sns.swarmplot(y='value',
                             x='variable',
                             data=data,
                             color='black',
                             alpha=0.75, orient="v")
        plot.axes.set_title("Cognitive predictions with PLSR",
                             fontsize=16)

        plot.set_xlabel("Training set",
                         fontsize=14)

        plot.set_ylabel("Coefficient of determination (R^2)",
                         fontsize=14)

        plot.tick_params(labelsize=10)

        self.save(plt)
        plt.show()

    def boxplot_self(self, data):
        plot = sns.boxplot(y='value', x='variable',
                           data=data,
                           width=0.5,
                           palette="colorblind",
                           orient="v")
        # plot.axes.set_title("Cognitive predictions with PLSR",
        #                      fontsize=16)

        plot.set_xlabel("Training set",
                         fontsize=14)

        plot.set_ylabel("Coefficient of determination (R^2)",
                         fontsize=14)

        plot.tick_params(labelsize=10)

        self.save(plt)
        plt.show()
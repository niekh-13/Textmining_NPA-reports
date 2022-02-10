##############################################################
#                                                            #
#    Niek Huijsmans (2021)                                   #
#    Textmining medical notes for cognition                  #
#    Visualizing                                             #
#                                                            #
##############################################################

# Import the relevant packages
import missingno as msno
from wordcloud import WordCloud
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

    def missing_values(self, data_table):
        fig = msno.matrix(data_table, labels=True)
        fig_copy = fig.get_figure()
        self.save(fig_copy)

    def histogram(self, data_table, bin):
        for column in data_table.columns:
            if 'obs' in column:
                x = data_table[column].apply(lambda x: len(str(x).split()))
                fig, ax = plt.subplots()
                # Title = 'Histogram of NPA reports'
                plt.xlabel('Number of words', fontsize=14)
                plt.ylabel('Number of NPA reports',fontsize=14)
                # plt.title(Title)
                ax.hist(x, bins=bin, fill=False, edgecolor='black', linewidth=2)
                # Hide the right and top spines
                ax.spines['right'].set_visible(False)
                ax.spines['top'].set_visible(False)
                # Only show ticks on the left and bottom spines
                ax.yaxis.set_ticks_position('left')
                ax.xaxis.set_ticks_position('bottom')
                # thicker xaxis
                ax.spines['left'].set_linewidth(2)
                ax.spines['bottom'].set_linewidth(2)
                # bigger front size xaxis
                ax.tick_params(axis='x', labelsize=12)
                ax.tick_params(axis='y', labelsize=12)
                self.save(plt)
                plt.show()
                plt.close()
            else:
                continue
    def wordcloud(self, data_table):
        for column in data_table.columns:
            if "obs" in column:
                x =  data_table[column].values
                wordcloud2 = WordCloud(width=10000, height=500).generate(str(x))
                plt.imshow(wordcloud2)
                plt.axis("off")
                plt.show()
                self.save(plt)

    def wordcloud_list(self, data_table):
        slist = []
        for column in data_table.columns:
            if "obs" in column:
                for i, x in data_table.iterrows():
                    slist.append(' '.join(x[column]))
                string = ' '.join(slist)
                # print(string)
                wordcloud2 = WordCloud(width=10000, height=500).generate(string)
                plt.imshow(wordcloud2)
                plt.axis("off")
                plt.show()
                self.save(plt)

    def tSNE_m(self, data_table):
        pal = sns.color_palette("hls", len(data_table['sex'].value_counts()))
        #plot
        plt.figure(figsize=(6, 6))
        # sns scattplot
        sns.scatterplot(
            x="tsne1", y="tsne2",
            hue="sex",
            palette=pal,
            data=data_table,
            legend="full",
            alpha=1
        )
        #x and y label
        plt.xlabel('Dimension 1', fontsize=10)
        plt.ylabel('Dimension 2', fontsize=10)
        plt.title('t-SNE Results:', fontsize=18)
        self.save(plt)
        plt.show()
        plt.close()

    def tSNE_b(self, data_table):
        pal = sns.color_palette("hls", len(data_table['sex'].value_counts()))
        #plot
        plt.figure(figsize=(6, 6))
        # sns scattplot
        sns.scatterplot(
            x="tsne1", y="tsne2",
            hue="sex",
            palette=pal,
            data=data_table,
            legend="full",
            alpha=1
        )
        #x and y label
        plt.xlabel('Dimension 1', fontsize=10)
        plt.ylabel('Dimension 2', fontsize=10)
        #title
        plt.title('BERT vector space', fontsize=14)
        self.save(plt)
        plt.show()
        plt.close()

    def tSNE_plain(self, data_table, name):
        pal = sns.color_palette("hls")
        plt.figure(figsize=(16, 10))
        sns.scatterplot(
            x="tsne1", y="tsne2",
            palette=pal,
            data=data_table,
            legend="full",
            alpha=1
        )
        plt.xlabel("tSNE 1")
        plt.ylabel("tSNE 2")
        plt.title(name)
        self.save(plt)
        plt.show()

    def PCA(self, data_table, name, i, label):
        pal = sns.color_palette("hls", len(data_table[label].value_counts()))
        plt.figure(figsize=(16, 10))
        sns.scatterplot(
            x="PCA1", y="PCA2",
            hue = label,
            palette=pal,
            data=data_table,
            legend="full",
            alpha=1
        )
        plt.xlabel("PCA 1 ("+str(i[0])+"%)")
        plt.ylabel("PCA 2 ("+str(i[1])+"%)")
        plt.title(name)
        self.save(plt)
        plt.show()
        plt.close()


    def PCA_plain(self, data_table, name, i):
        pal = sns.color_palette("hls")
        plt.figure(figsize=(16, 10))
        sns.scatterplot(
            x="PCA1", y="PCA2",
            palette=pal,
            data=data_table,
            legend="full",
            alpha=1
        )
        plt.xlabel("PCA 1 ("+str(i[0])+"%)")
        plt.ylabel("PCA 2 ("+str(i[1])+"%)")
        plt.title(name)
        self.save(plt)
        plt.show()
        plt.close()


    def boxplot(self, scores, name):
        plt.boxplot(scores.values(), labels=scores.keys())
        plt.grid(axis='y', alpha=0.75)
        plt.ylabel('R2')
        plt.xlabel('Models')
        plt.title('Nested loop CV for: '+ name)
        self.save(plt)
        plt.show()
        plt.close()
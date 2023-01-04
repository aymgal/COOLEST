__author__ = 'XXX'


from coolest.io.analysis import Analysis
from coolest.api.util import read_json_param


class Plotting(object):
    """
    Handles computation of model-independent quantities and other analysis computations
    """

    def __init__(self, coolest_file_path):
        self.analysis = Analysis(coolest_file_path)
        self.coolest_data = self.analysis.coolest_data

    def plot_summary(self):
        pass

class Comparison_analytical(object):
    """
    Handles plot of analytical models in a comparative way
    """
    def __init__(self,coolest_file_list, nickname_file_list):
        self.file_names = nickname_file_list
        self.param_lens, self.param_source = read_json_param(coolest_file_list,self.file_names, lens_light=False)

    def plotting_routine(self,param_dict,idx_file=0):
        """
        plot the parameters

        INPUT
        -----
        param_dict: dict, organized dictonnary with all parameters results of the different files
        idx_file: int, chooses the file on which the choice of plotted parameters will be made
        (not very clear: basically in file 0 you may have a sersic fit and in file 1 sersic+shapelets. If you choose
         idx_file=0, you will plot the sersic results of both file. If you choose idx_file=1, you will plot all the
         sersic and shapelets parameters when available)
        """

        #find the numer of parameters to plot and define a nice looking figure
        number_param = len(param_dict[idx_file])
        unused_figs = []
        if number_param <= 4:
            print('so few parameters not implemented yet')
        else:
            if number_param % 4 == 0:
                num_lines = int(number_param / 4.)
            else:
                num_lines = int(number_param / 4.) + 1

                for idx in range(3):
                    if (number_param + idx) % 4 != 0:
                        unused_figs.append(-idx - 1)
                    else:
                        break

        f, ax = plt.subplots(num_lines, 4, figsize=(4 * 3.5, 2.5 * num_lines))
        markers = ['*', '.', 's', '^','<','>','v','p','P','X','D','1','2','3','4','+']
        #may find a better way to define markers but right now, it is sufficient

        for j, file_name in enumerate(self.file_names):
            i = 0
            result = param_dict[file_name]
            for key in result.keys():
                idx_line = int(i / 4.)
                idx_col = i % 4
                p = result[key]
                m = markers[j]
                if file_posterior[j]:
                    # UNCOMMENT IF NO ERROR BARS AVAILABLE ON SHEAR
                    #             if (j== 1) and (key=='SHEAR_0_gamma_ext' or key == 'SHEAR_0_phi_ext'):
                    #                 ax[idx_line,idx_col].plot(j,p['point_estimate'],marker=m,ls='',label=file_name)
                    #                 i+=1
                    #                 continue

                    #trick to plot correct error bars if close to the +180/-180 edge
                    if (key == 'SHEAR_0_phi_ext' or key == 'PEMD_0_phi'):
                        if p['percentile_16th'] > p['median']:
                            p['percentile_16th'] -= 180.
                        if p['percentile_84th'] < p['median']:
                            p['percentile_84th'] += 180.
                    ax[idx_line, idx_col].errorbar(j, p['median'], [[p['median'] - p['percentile_16th']],
                                                                    [p['percentile_84th'] - p['median']]],
                                                   marker=m, ls='', label=file_name)
                else:
                    ax[idx_line, idx_col].plot(j, p['point_estimate'], marker=m, ls='', label=file_name)

                if j == 0:
                    ax[idx_line, idx_col].get_xaxis().set_visible(False)
                    ax[idx_line, idx_col].set_ylabel(p['latex_str'], fontsize=12)
                    ax[idx_line, idx_col].tick_params(axis='y', labelsize=12)
                i += 1

        ax[0, 0].legend()
        for idx in unused_figs:
            ax[-1, idx].axis('off')
        plt.tight_layout()
        plt.show()
        return f,ax
    def plot_source(self,idx_file=0):
        f,ax = self.plotting_routine(self.param_source,idx_file)
        return f,ax
    def plot_lens(self,idx_file=0):
        f,ax = self.plotting_routine(self.param_lens,idx_file)
        retrn f,ax
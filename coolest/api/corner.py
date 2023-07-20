import csv
from getdist import plots,chains,MCSamples



def plot_corner(parameter_id_list,coolest_obj_list,labels=None):
    """
    Parameters
    ----------
    parameter_id_list : array
        A list of parameter unique ids obtained from lensing entities. Their order determines the order of the plot panels.
    coolest_obj_list : array
        A list of coolest objects.
    labels : dict,optional
        A dictionary matching the parameter_id_list entries to some human-readable labels.
    

    Returns
    -------
    An image

    TODO
    ----
    - Take a list of vectors of fixed parameter values as input.
    - Take flags as input that can plot the point estimates of "MAP", "mean", "median".
    - Take an input option to indicate whether confidence intervals should be included from the COOLEST.json file, calculated, or excluded.
    - Take GetDist options as input, especially the 'smooth_scale_2D' and the 'mult_bias_correction_order' ones.
    - Take triangle_plot arguments as input, e.g. 'filled=True'
    """

    chains.print_load_details = False # Just to silence messages

    mcsamples = []
    for i in range(0,len(coolest_obj_list)):
        chain_file_name = "mychain.csv" # Here get the chain file path for each coolest object

        # Get the chain file headers
        f = open(chain_file_name)
        header = f.readline()
        f.close()
        chain_file_headers = set(header.split(','))

        # Check that the given parameters are in the chain file
        parameter_id_set = set(parameter_id_list)
        assert parameter_id_set.issubset(chain_file_headers), "Not all given parameters are free parameters for model %d (not in the chain file: %s)!" % (i,chain_file_name)

        # Read parameter values and probability weights
        samples = np.loadtxt(chain_file_name,skiprows=1,delimiter=',')
        sample_par_values = samples[:,:-1]
        sample_prob_weight = samples[:,-1]

        # Create MCSamples object
        mysample = MCSamples(samples=sample_par_values,names=chain_file_headers,settings={"ignore_rows": 0.0,"smooth_scale_2D":0.3,"mult_bias_correction_order":1})
        mysample.reweightAddingLogLikes(sample_prob_weight)
        mcsamples.append(mysample)
        

    # Make the plot
    image = plots.getSubplotPlotter(subplot_size=2)

    # Set the labels for the given parameters
    par_labels = []
    if labels is None:
        par_labels = parameter_id_list
    else:
        for par_name in parameter_id_list:
            par_labels.append(labels[par_name])
    
    image.triangle_plot(mcsamples,params=parameter_id_list,legend_labels=par_labels,filled=True)

    return image




    




    

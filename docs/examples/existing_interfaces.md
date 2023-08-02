# Existing interfaces with COOLEST

Below is a list of lens modeling codes with a known interface with the COOLEST standard. The goal of such an interface is to transform code-dependent quantities and data containers into a directory, including the main template file, that is fully compatible with the COOLEST API.

The following modeling codes already have an interface with COOLEST:

- [__*Lenstronomy*__](https://github.com/lenstronomy/lenstronomy) (Birrer et al. [2018](https://ui.adsabs.harvard.edu/abs/2018PDU....22..189B/abstract), [2022](https://ui.adsabs.harvard.edu/abs/2021JOSS....6.3283B/abstract)), via its [`Util.coolest_interface`](https://github.com/lenstronomy/lenstronomy/tree/main/lenstronomy/Util/coolest_interface.py) submodule;

- [__*Herculens*__](https://github.com/lenstronomy/lenstronomy) ([Galan et al. 2022](https://ui.adsabs.harvard.edu/abs/2022A%26A...668A.155G/abstract)), via its [`Standard.coolest_exporter`](https://github.com/austinpeel/herculens/blob/main/herculens/Standard/coolest_exporter.py) submodule;

- [__*VKL*__](https://github.com/gvernard/verykool) ([Vernardos et al. 2022](https://ui.adsabs.harvard.edu/abs/2022MNRAS.516.1347V/abstract)).

If you have questions or comments about the development of a COOLEST interface for your modeling code, please [reach out to us](mailto:aymeric.galan@gmail.com). In case of an issue with the COOLEST API, we advise you to open an [issue on GitHub](https://github.com/aymgal/COOLEST/issues/new).

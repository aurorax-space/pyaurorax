Current coverage report:

```
Name                                                           Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------
pyaurorax/__init__.py                                              9      0   100%
pyaurorax/_util.py                                                 5      0   100%
pyaurorax/cli/cli.py                                              37      0   100%
pyaurorax/cli/search/__init__.py                                  16      0   100%
pyaurorax/cli/search/availability/commands.py                    127      0   100%
pyaurorax/cli/search/conjunctions/commands.py                    166      0   100%
pyaurorax/cli/search/data_products/commands.py                   162      0   100%
pyaurorax/cli/search/ephemeris/commands.py                       160      0   100%
pyaurorax/cli/search/helpers.py                                  120      0   100%
pyaurorax/cli/search/sources/commands.py                         242      0   100%
pyaurorax/cli/search/util/commands.py                             92      0   100%
pyaurorax/cli/templates.py                                         3      0   100%
pyaurorax/data/__init__.py                                        81      0   100%
pyaurorax/data/ucalgary/__init__.py                               97      0   100%
pyaurorax/data/ucalgary/read/__init__.py                          36      0   100%
pyaurorax/exceptions.py                                           28      0   100%
pyaurorax/models/__init__.py                                      10      0   100%
pyaurorax/models/atm/__init__.py                                  17      0   100%
pyaurorax/pyaurorax.py                                           206      0   100%
pyaurorax/search/__init__.py                                      93      0   100%
pyaurorax/search/api/__init__.py                                  20      0   100%
pyaurorax/search/api/classes/request.py                           33      0   100%
pyaurorax/search/api/classes/response.py                           9      0   100%
pyaurorax/search/availability/__init__.py                         14      0   100%
pyaurorax/search/availability/_availability.py                    21      0   100%
pyaurorax/search/availability/classes/availability_result.py       8      0   100%
pyaurorax/search/conjunctions/__init__.py                         31      0   100%
pyaurorax/search/conjunctions/_conjunctions.py                    91      0   100%
pyaurorax/search/conjunctions/classes/conjunction.py              39      0   100%
pyaurorax/search/conjunctions/classes/criteria_block.py           67      0   100%
pyaurorax/search/conjunctions/classes/search.py                  214      0   100%
pyaurorax/search/conjunctions/swarmaurora/__init__.py             15      0   100%
pyaurorax/search/conjunctions/swarmaurora/_swarmaurora.py         24      0   100%
pyaurorax/search/data_products/__init__.py                        32      0   100%
pyaurorax/search/data_products/_data_products.py                  81      0   100%
pyaurorax/search/data_products/classes/data_product.py            46      0   100%
pyaurorax/search/data_products/classes/search.py                 119      0   100%
pyaurorax/search/ephemeris/__init__.py                            29      0   100%
pyaurorax/search/ephemeris/_ephemeris.py                          75      0   100%
pyaurorax/search/ephemeris/classes/ephemeris.py                   41      0   100%
pyaurorax/search/ephemeris/classes/search.py                     118      0   100%
pyaurorax/search/location.py                                      29      0   100%
pyaurorax/search/metadata/__init__.py                             14      0   100%
pyaurorax/search/metadata/_metadata.py                            16      0   100%
pyaurorax/search/metadata_filters.py                              60      0   100%
pyaurorax/search/requests/__init__.py                             26      0   100%
pyaurorax/search/requests/_requests.py                            80      0   100%
pyaurorax/search/sources/__init__.py                              59      0   100%
pyaurorax/search/sources/_sources.py                             110      0   100%
pyaurorax/search/sources/classes/data_source.py                   66      0   100%
pyaurorax/search/sources/classes/data_source_stats.py             22      0   100%
pyaurorax/search/util/__init__.py                                 11      0   100%
pyaurorax/search/util/_calculate_btrace.py                        18      0   100%
pyaurorax/tools/__init__.py                                       61      7    89%   100, 107, 114, 121, 128, 135, 142
pyaurorax/tools/_display.py                                       35      0   100%
pyaurorax/tools/_movie.py                                         34      0   100%
pyaurorax/tools/_scale_intensity.py                               44      0   100%
pyaurorax/tools/_util.py                                          10      0   100%
pyaurorax/tools/bounding_box/__init__.py                           9      0   100%
pyaurorax/tools/bounding_box/extract_metric/__init__.py           23      3    87%   161, 207, 257
pyaurorax/tools/bounding_box/extract_metric/_azimuth.py           53      0   100%
pyaurorax/tools/bounding_box/extract_metric/_ccd.py               60      0   100%
pyaurorax/tools/bounding_box/extract_metric/_elevation.py         55     52     5%   21-97
pyaurorax/tools/bounding_box/extract_metric/_geo.py               95     92     3%   21-152
pyaurorax/tools/bounding_box/extract_metric/_mag.py               99     95     4%   22-163
pyaurorax/tools/calibration/__init__.py                           13      2    85%   81, 135
pyaurorax/tools/calibration/_common.py                            34     29    15%   27-55, 60-73, 78-94
pyaurorax/tools/calibration/_rego.py                              14     12    14%   35-58
pyaurorax/tools/calibration/_trex_nir.py                          14     12    14%   35-58
pyaurorax/tools/ccd_contour/__init__.py                           20      4    80%   80, 115, 167, 223
pyaurorax/tools/ccd_contour/_azimuth.py                           46     44     4%   20-89
pyaurorax/tools/ccd_contour/_elevation.py                         41     39     5%   20-81
pyaurorax/tools/ccd_contour/_geo.py                              123    120     2%   24-36, 41-234
pyaurorax/tools/ccd_contour/_mag.py                              133    129     3%   25-37, 42-254
pyaurorax/tools/classes/keogram.py                               152    134    12%   63-71, 74, 77-83, 90-103, 126-155, 183-237, 332-464
pyaurorax/tools/classes/montage.py                                64     50    22%   42-46, 49, 52-55, 62-68, 163-253
pyaurorax/tools/classes/mosaic.py                                313    265    15%   65, 69-82, 93-110, 143, 147-152, 159-169, 201, 204-215, 222-238, 350-522, 572-678, 732-838
pyaurorax/tools/grid_files/__init__.py                             9      1    89%   61
pyaurorax/tools/grid_files/_prep_grid_image.py                    34     31     9%   21-89
pyaurorax/tools/keogram/__init__.py                               15      2    87%   88, 152
pyaurorax/tools/keogram/_create.py                                66     62     6%   22-150
pyaurorax/tools/keogram/_create_custom.py                        174    164     6%   31-43, 52-64, 75-147, 152-329
pyaurorax/tools/montage/__init__.py                               11      1    91%   53
pyaurorax/tools/montage/_create.py                                10      8    20%   23-42
pyaurorax/tools/mosaic/__init__.py                                33     17    48%   119-144, 182, 220
pyaurorax/tools/mosaic/_create.py                                197    183     7%   38-379
pyaurorax/tools/mosaic/_prep_images.py                           142    135     5%   30-51, 56-273
pyaurorax/tools/mosaic/_prep_skymaps.py                          119    112     6%   26-141, 151-244
pyaurorax/tools/spectra/__init__.py                               10      1    90%   129
pyaurorax/tools/spectra/_plot.py                                 114    108     5%   42-233
--------------------------------------------------------------------------------------------
TOTAL                                                           5824   1914    67%

13 empty files skipped.
```

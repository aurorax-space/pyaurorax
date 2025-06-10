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
pyaurorax/data/ucalgary/read/__init__.py                          38      0   100%
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
pyaurorax/search/requests/_requests.py                           101      0   100%
pyaurorax/search/sources/__init__.py                              59      0   100%
pyaurorax/search/sources/_sources.py                             110      0   100%
pyaurorax/search/sources/classes/data_source.py                   66      0   100%
pyaurorax/search/sources/classes/data_source_stats.py             22      0   100%
pyaurorax/search/util/__init__.py                                 11      0   100%
pyaurorax/search/util/_calculate_btrace.py                        18      0   100%
pyaurorax/tools/__init__.py                                       67      0   100%
pyaurorax/tools/_display.py                                       33      0   100%
pyaurorax/tools/_movie.py                                         34      0   100%
pyaurorax/tools/_scale_intensity.py                               44      0   100%
pyaurorax/tools/_util.py                                          10      0   100%
pyaurorax/tools/bounding_box/__init__.py                           9      0   100%
pyaurorax/tools/bounding_box/extract_metric/__init__.py           23      0   100%
pyaurorax/tools/bounding_box/extract_metric/_azimuth.py           52      0   100%
pyaurorax/tools/bounding_box/extract_metric/_ccd.py               60      0   100%
pyaurorax/tools/bounding_box/extract_metric/_elevation.py         52      0   100%
pyaurorax/tools/bounding_box/extract_metric/_geo.py               92      0   100%
pyaurorax/tools/bounding_box/extract_metric/_mag.py               96      0   100%
pyaurorax/tools/calibration/__init__.py                           13      0   100%
pyaurorax/tools/calibration/_common.py                            34      0   100%
pyaurorax/tools/calibration/_rego.py                              14      0   100%
pyaurorax/tools/calibration/_trex_nir.py                          14      0   100%
pyaurorax/tools/ccd_contour/__init__.py                           20      0   100%
pyaurorax/tools/ccd_contour/_azimuth.py                           47      0   100%
pyaurorax/tools/ccd_contour/_elevation.py                         39      0   100%
pyaurorax/tools/ccd_contour/_geo.py                              106      0   100%
pyaurorax/tools/ccd_contour/_mag.py                              112      0   100%
pyaurorax/tools/classes/fov.py                                   293     10    97%   139, 153, 204, 219, 374-375, 393-394, 559, 562
pyaurorax/tools/classes/keogram.py                               232      4    98%   215-217, 490
pyaurorax/tools/classes/montage.py                                63      0   100%
pyaurorax/tools/classes/mosaic.py                                299      2    99%   467, 781
pyaurorax/tools/fov/__init__.py                                   13      0   100%
pyaurorax/tools/fov/_create_data.py                              122      0   100%
pyaurorax/tools/fov/_create_map.py                                 7      0   100%
pyaurorax/tools/grid_files/__init__.py                             9      0   100%
pyaurorax/tools/grid_files/_prep_grid_image.py                    36      0   100%
pyaurorax/tools/keogram/__init__.py                               15      0   100%
pyaurorax/tools/keogram/_create.py                                66      0   100%
pyaurorax/tools/keogram/_create_custom.py                        191     13    93%   121, 134, 137, 157, 161, 167, 183, 199, 203, 226, 235, 238, 342
pyaurorax/tools/montage/__init__.py                               11      0   100%
pyaurorax/tools/montage/_create.py                                 9      0   100%
pyaurorax/tools/mosaic/__init__.py                                33      9    73%   122-123, 125-127, 134-144
pyaurorax/tools/mosaic/_create.py                                189      4    98%   100, 188, 358, 366
pyaurorax/tools/mosaic/_prep_images.py                           162      1    99%   247
pyaurorax/tools/mosaic/_prep_skymaps.py                          118     22    81%   32-74
pyaurorax/tools/spectra/__init__.py                               13      0   100%
pyaurorax/tools/spectra/_get_intensity.py                         46      1    98%   82
pyaurorax/tools/spectra/_plot.py                                 116      4    97%   148, 150, 174, 195
--------------------------------------------------------------------------------------------
TOTAL                                                           6382     70    99%

13 empty files skipped.
```

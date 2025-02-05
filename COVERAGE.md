Current coverage report:

```
Name                                                           Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------
pyaurorax/__init__.py                                              9      0   100%
pyaurorax/_util.py                                                 5      0   100%
pyaurorax/cli/cli.py                                              37      0   100%
pyaurorax/cli/search/__init__.py                                  16      0   100%
pyaurorax/cli/search/availability/commands.py                    127      0   100%
pyaurorax/cli/search/conjunctions/commands.py                    171      6    96%   160, 193, 240-241, 368-369
pyaurorax/cli/search/data_products/commands.py                   167      4    98%   135, 168, 215-216
pyaurorax/cli/search/ephemeris/commands.py                       165      4    98%   133, 166, 213-214
pyaurorax/cli/search/helpers.py                                  158     31    80%   50-53, 59-60, 70, 120, 138, 148, 172-174, 179-181, 185-189, 207-224, 256-258
pyaurorax/cli/search/sources/commands.py                         305     75    75%   41, 51, 83, 85-97, 121, 141, 143, 156, 158, 160, 166, 199, 232, 290-292, 329-335, 341-347, 353-359, 368-370, 379, 411-413, 437-439, 464-476, 494-505, 518-523
pyaurorax/cli/search/util/commands.py                             98     11    89%   92, 167-169, 173-175, 192, 196, 211-212
pyaurorax/cli/templates.py                                         3      0   100%
pyaurorax/data/__init__.py                                        81      0   100%
pyaurorax/data/ucalgary/__init__.py                              107     10    91%   326-329, 430-433, 503-504
pyaurorax/data/ucalgary/read/__init__.py                          42      6    86%   152-155, 235-236
pyaurorax/exceptions.py                                           28      0   100%
pyaurorax/models/__init__.py                                      10      0   100%
pyaurorax/models/atm/__init__.py                                  21      4    81%   188-189, 296-297
pyaurorax/pyaurorax.py                                           204      2    99%   180, 404
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
pyaurorax/search/conjunctions/classes/search.py                  215      1    99%   366
pyaurorax/search/conjunctions/swarmaurora/__init__.py             15      0   100%
pyaurorax/search/conjunctions/swarmaurora/_swarmaurora.py         24      0   100%
pyaurorax/search/data_products/__init__.py                        33      0   100%
pyaurorax/search/data_products/_data_products.py                  84      2    98%   128, 145
pyaurorax/search/data_products/classes/data_product.py            47      1    98%   130
pyaurorax/search/data_products/classes/search.py                 121      0   100%
pyaurorax/search/ephemeris/__init__.py                            29      0   100%
pyaurorax/search/ephemeris/_ephemeris.py                          78      2    97%   142, 151
pyaurorax/search/ephemeris/classes/ephemeris.py                   42      1    98%   97
pyaurorax/search/ephemeris/classes/search.py                     118      0   100%
pyaurorax/search/location.py                                      29      0   100%
pyaurorax/search/metadata/__init__.py                             14      0   100%
pyaurorax/search/metadata/_metadata.py                            20      5    75%   29-31, 45, 54
pyaurorax/search/metadata_filters.py                              61     25    59%   63-66, 69, 73-78, 86-89, 135-137, 145, 147, 159-169
pyaurorax/search/requests/__init__.py                             28      2    93%   144, 207
pyaurorax/search/requests/_requests.py                           100     25    75%   49-50, 54, 88, 115, 122-125, 129, 136-139, 144, 152, 154, 156, 158, 167, 169, 177-184
pyaurorax/search/sources/__init__.py                              59     26    56%   183-240
pyaurorax/search/sources/_sources.py                             119     13    89%   132, 154-155, 208, 211, 213, 215, 217, 245-246, 257, 293-294
pyaurorax/search/sources/classes/data_source.py                   68     26    62%   170, 173, 186-212
pyaurorax/search/sources/classes/data_source_stats.py             22      9    59%   61, 64, 73-79
pyaurorax/search/util/__init__.py                                 11      0   100%
pyaurorax/search/util/_calculate_btrace.py                        18      0   100%
pyaurorax/tools/__init__.py                                       61     12    80%   93, 100, 107, 114, 121, 128, 135, 142, 222, 256, 298, 313
pyaurorax/tools/_display.py                                       35     31    11%   22-84
pyaurorax/tools/_movie.py                                         37     32    14%   21, 34-95
pyaurorax/tools/_scale_intensity.py                               45     42     7%   20-63, 67-102
pyaurorax/tools/_util.py                                          10      7    30%   20-27
pyaurorax/tools/bounding_box/__init__.py                           9      1    89%   45
pyaurorax/tools/bounding_box/extract_metric/__init__.py           23      5    78%   80, 118, 161, 207, 257
pyaurorax/tools/bounding_box/extract_metric/_azimuth.py           57     54     5%   21-99
pyaurorax/tools/bounding_box/extract_metric/_ccd.py               61     58     5%   21-98
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
TOTAL                                                           6023   2437    60%

13 empty files skipped.
```

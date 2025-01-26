Current coverage report:

```
Name                                                           Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------
pyaurorax/__init__.py                                              9      0   100%
pyaurorax/_util.py                                                 5      0   100%
pyaurorax/cli/cli.py                                              41     41     0%   15-93
pyaurorax/cli/search/__init__.py                                  16     16     0%   15-35
pyaurorax/cli/search/availability/commands.py                    138    138     0%   15-241
pyaurorax/cli/search/conjunctions/commands.py                    182    182     0%   15-366
pyaurorax/cli/search/data_products/commands.py                   175    175     0%   15-337
pyaurorax/cli/search/ephemeris/commands.py                       173    173     0%   15-323
pyaurorax/cli/search/helpers.py                                  158    158     0%   15-276
pyaurorax/cli/search/sources/commands.py                         315    315     0%   15-544
pyaurorax/cli/search/util/commands.py                            124    124     0%   15-294
pyaurorax/cli/templates.py                                         3      3     0%   19-90
pyaurorax/data/__init__.py                                        81     64    21%   49, 78-90, 125-164, 187-201, 233-245, 280-319
pyaurorax/data/ucalgary/__init__.py                              110     81    26%   35, 68, 96-104, 126-129, 160-163, 172, 193, 311-329, 419-433, 494-504, 586, 639-675, 719-755, 799-835
pyaurorax/data/ucalgary/read/__init__.py                          43     21    51%   22, 41, 62, 141-155, 224-236, 305, 383, 462, 541, 619, 667, 711, 786
pyaurorax/exceptions.py                                           28      0   100%
pyaurorax/models/__init__.py                                      10      1    90%   49
pyaurorax/models/atm/__init__.py                                  22      9    59%   38, 168-189, 279-297
pyaurorax/pyaurorax.py                                           222     75    66%   147, 173, 180, 187, 207, 211, 259, 296-301, 308, 312, 339-347, 426, 459-537
pyaurorax/search/__init__.py                                      92      0   100%
pyaurorax/search/api/__init__.py                                  20      0   100%
pyaurorax/search/api/classes/request.py                           73     26    64%   70-71, 79, 111-112, 116-123, 133-135, 139, 143-147, 151, 155-159, 165, 169, 183, 186
pyaurorax/search/api/classes/response.py                          11      2    82%   43, 46
pyaurorax/search/availability/__init__.py                         14      0   100%
pyaurorax/search/availability/_availability.py                    21      0   100%
pyaurorax/search/availability/classes/availability_result.py       8      0   100%
pyaurorax/search/conjunctions/__init__.py                         26      2    92%   59, 206
pyaurorax/search/conjunctions/_conjunctions.py                    53     22    58%   38, 43-45, 53, 59, 63, 68, 82-85, 103-117
pyaurorax/search/conjunctions/classes/conjunction.py              21      2    90%   100, 103
pyaurorax/search/conjunctions/classes/criteria_block.py           67     49    27%   45-48, 51, 54, 66-76, 107-111, 114, 117, 130-141, 144-147, 166-168, 171, 174, 185-194
pyaurorax/search/conjunctions/classes/search.py                  197     63    68%   35, 140, 143, 154-195, 301-306, 313-320, 329-335, 352, 394, 398, 420-421, 432-433
pyaurorax/search/conjunctions/swarmaurora/__init__.py             15      3    80%   46, 65, 87
pyaurorax/search/conjunctions/swarmaurora/_swarmaurora.py         25     18    28%   25, 29-35, 41-58
pyaurorax/search/data_products/__init__.py                        33      2    94%   124, 234
pyaurorax/search/data_products/_data_products.py                 100     31    69%   40-44, 71, 76-78, 86, 92, 96, 101, 128, 143-145, 154, 169, 177-204, 211-214
pyaurorax/search/data_products/classes/data_product.py            42      2    95%   130, 154
pyaurorax/search/data_products/classes/search.py                 123     42    66%   33, 142, 145, 156-197, 209, 235, 272, 291-292, 300-301
pyaurorax/search/ephemeris/__init__.py                            30      1    97%   119
pyaurorax/search/ephemeris/_ephemeris.py                          88     21    76%   38-42, 68, 73-75, 83, 89, 93, 98, 125, 140-142, 151, 167, 177-180
pyaurorax/search/ephemeris/classes/ephemeris.py                   42      1    98%   97
pyaurorax/search/ephemeris/classes/search.py                     124     45    64%   33, 138, 141, 152-193, 203-208, 230, 241, 274, 292-293, 301-302
pyaurorax/search/location.py                                      29      6    79%   52-55, 63-66
pyaurorax/search/metadata/__init__.py                             14      0   100%
pyaurorax/search/metadata/_metadata.py                            20      5    75%   29-31, 45, 54
pyaurorax/search/metadata_filters.py                              61     39    36%   53-55, 59, 63-66, 69, 73-78, 86-89, 95, 126-127, 131, 135-137, 140, 144-152, 159-169, 175
pyaurorax/search/requests/__init__.py                             28      3    89%   144, 191, 207
pyaurorax/search/requests/_requests.py                            97     44    55%   51, 85, 96, 101, 112, 119-122, 126, 132-169, 174-181
pyaurorax/search/sources/__init__.py                              59     26    56%   183-240
pyaurorax/search/sources/_sources.py                             119     16    87%   50, 52, 132, 154-155, 189, 208, 211, 213, 215, 217, 245-246, 257, 293-294
pyaurorax/search/sources/classes/data_source.py                   57     26    54%   170, 173, 186-212
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
TOTAL                                                           6103   4228    31%

13 empty files skipped.
```

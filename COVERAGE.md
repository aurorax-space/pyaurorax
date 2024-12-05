Current coverage report:

```
Name                                                           Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------
pyaurorax/__init__.py                                              8      0   100%
pyaurorax/cli/cli.py                                              41     41     0%   15-93
pyaurorax/cli/search/__init__.py                                  16     16     0%   15-35
pyaurorax/cli/search/availability/commands.py                    138    138     0%   15-241
pyaurorax/cli/search/conjunctions/commands.py                    184    184     0%   15-370
pyaurorax/cli/search/data_products/commands.py                   175    175     0%   15-337
pyaurorax/cli/search/ephemeris/commands.py                       173    173     0%   15-323
pyaurorax/cli/search/helpers.py                                  158    158     0%   15-276
pyaurorax/cli/search/sources/commands.py                         315    315     0%   15-544
pyaurorax/cli/search/util/commands.py                            124    124     0%   15-294
pyaurorax/cli/templates.py                                         3      3     0%   19-90
pyaurorax/data/__init__.py                                        81     64    21%   49, 74-86, 113-152, 175-189, 221-233, 268-307
pyaurorax/data/ucalgary/__init__.py                              110     81    26%   35, 68, 92-99, 121-124, 155-158, 167, 188, 301-319, 404-418, 479-489, 571, 620-656, 696-732, 772-808
pyaurorax/data/ucalgary/read/__init__.py                          43     21    51%   22, 41, 62, 141-155, 206-218, 287, 365, 444, 523, 601, 649, 693, 768
pyaurorax/exceptions.py                                           28      0   100%
pyaurorax/models/__init__.py                                      10      1    90%   49
pyaurorax/models/atm/__init__.py                                  22      9    59%   38, 168-189, 279-297
pyaurorax/pyaurorax.py                                           193     58    70%   135, 158, 165, 172, 236, 269, 273, 365, 398-476
pyaurorax/search/__init__.py                                      61      0   100%
pyaurorax/search/api/__init__.py                                  20      0   100%
pyaurorax/search/api/classes/request.py                           71     25    65%   59-60, 68, 98-99, 103-110, 120-122, 126-130, 134, 138-142, 148, 152, 166, 169
pyaurorax/search/api/classes/response.py                          10      2    80%   37, 40
pyaurorax/search/availability/__init__.py                         14      0   100%
pyaurorax/search/availability/_availability.py                    21      0   100%
pyaurorax/search/availability/classes/availability_result.py       8      0   100%
pyaurorax/search/conjunctions/__init__.py                         22      1    95%   53
pyaurorax/search/conjunctions/_conjunctions.py                    40     11    72%   39, 44-46, 54, 60, 64, 69, 83-86
pyaurorax/search/conjunctions/classes/conjunction.py              21      2    90%   83, 86
pyaurorax/search/conjunctions/classes/search.py                  132      9    93%   33, 153, 156, 309, 313, 335-336, 347-348
pyaurorax/search/conjunctions/swarmaurora/__init__.py             15      3    80%   45, 59, 76
pyaurorax/search/conjunctions/swarmaurora/_swarmaurora.py         25     18    28%   25, 29-35, 41-58
pyaurorax/search/data_products/__init__.py                        29      1    97%   189
pyaurorax/search/data_products/_data_products.py                 100     31    69%   40-44, 71, 76-78, 86, 92, 96, 101, 128, 143-145, 154, 169, 177-204, 211-214
pyaurorax/search/data_products/classes/data_product.py            42      2    95%   121, 145
pyaurorax/search/data_products/classes/search.py                  84      8    90%   32, 114, 117, 178, 197-198, 206-207
pyaurorax/search/ephemeris/__init__.py                            26      0   100%
pyaurorax/search/ephemeris/_ephemeris.py                          88     21    76%   38-42, 68, 73-75, 83, 89, 93, 98, 125, 140-142, 151, 167, 177-180
pyaurorax/search/ephemeris/classes/ephemeris.py                   42      1    98%   84
pyaurorax/search/ephemeris/classes/search.py                      85      9    89%   32, 111, 114, 149, 181, 200-201, 209-210
pyaurorax/search/location.py                                      29      6    79%   52-55, 63-66
pyaurorax/search/metadata/__init__.py                             14      0   100%
pyaurorax/search/metadata/_metadata.py                            20      5    75%   29-31, 45, 54
pyaurorax/search/requests/__init__.py                             28      3    89%   129, 164, 180
pyaurorax/search/requests/_requests.py                            97     44    55%   51, 94, 105, 110, 121, 128-131, 135, 141-178, 183-190
pyaurorax/search/sources/__init__.py                              31      0   100%
pyaurorax/search/sources/_sources.py                             119     16    87%   50, 52, 132, 154-155, 189, 208, 211, 213, 215, 217, 245-246, 257, 293-294
pyaurorax/search/sources/classes/data_source.py                   29      0   100%
pyaurorax/search/sources/classes/data_source_stats.py             11      0   100%
pyaurorax/search/util/__init__.py                                 11      0   100%
pyaurorax/search/util/_calculate_btrace.py                        18      0   100%
pyaurorax/tools/__init__.py                                       15      0   100%
pyaurorax/tools/_display.py                                       37     31    16%   97-159
pyaurorax/tools/_movie.py                                         39     32    18%   23, 66-127
pyaurorax/tools/_scale_intensity.py                               46     42     9%   21-64, 107-148
pyaurorax/tools/_util.py                                          10      7    30%   32-39
pyaurorax/tools/bounding_box/__init__.py                           2      0   100%
pyaurorax/tools/bounding_box/extract_metric/__init__.py            6      0   100%
pyaurorax/tools/bounding_box/extract_metric/_azimuth.py           58     52    10%   63-138
pyaurorax/tools/bounding_box/extract_metric/_ccd.py               63     58     8%   58-134
pyaurorax/tools/bounding_box/extract_metric/_elevation.py         58     52    10%   64-139
pyaurorax/tools/bounding_box/extract_metric/_geo.py               98     92     6%   67-197
pyaurorax/tools/bounding_box/extract_metric/_mag.py              103     95     8%   70-211
pyaurorax/tools/calibration/__init__.py                            3      0   100%
pyaurorax/tools/calibration/_common.py                            34     29    15%   27-55, 60-73, 78-94
pyaurorax/tools/calibration/_rego.py                              17     12    29%   72-95
pyaurorax/tools/calibration/_trex_nir.py                          17     12    29%   72-95
pyaurorax/tools/ccd_contour/__init__.py                            5      0   100%
pyaurorax/tools/ccd_contour/_azimuth.py                           46     42     9%   62-127
pyaurorax/tools/ccd_contour/_elevation.py                         43     39     9%   54-115
pyaurorax/tools/ccd_contour/_geo.py                              125    120     4%   26-38, 92-285
pyaurorax/tools/ccd_contour/_mag.py                              136    129     5%   28-40, 98-310
pyaurorax/tools/classes/keogram.py                               138    121    12%   55-62, 65, 68-74, 97-126, 154-208, 303-433
pyaurorax/tools/classes/montage.py                                54     41    24%   42-46, 49, 52-55, 121-195
pyaurorax/tools/classes/mosaic.py                                250    208    17%   61, 64-76, 107, 110-114, 135, 138-149, 247-361, 408-513, 564-669
pyaurorax/tools/grid_files/__init__.py                             2      0   100%
pyaurorax/tools/grid_files/_prep_grid_image.py                    36     31    14%   46-105
pyaurorax/tools/keogram/__init__.py                                3      0   100%
pyaurorax/tools/keogram/_create.py                                28     23    18%   45-85
pyaurorax/tools/keogram/_create_custom.py                        180    168     7%   33-45, 54-66, 77-146, 211-382
pyaurorax/tools/montage/__init__.py                                2      0   100%
pyaurorax/tools/montage/_create.py                                13      8    38%   42-61
pyaurorax/tools/mosaic/__init__.py                                 4      0   100%
pyaurorax/tools/mosaic/_create.py                                136    123    10%   92-322
pyaurorax/tools/mosaic/_prep_images.py                            98     90     8%   31-52, 74-213
pyaurorax/tools/mosaic/_prep_skymaps.py                           90     81    10%   26-89, 133-217
--------------------------------------------------------------------------------------------
TOTAL                                                           5180   3517    32%

13 empty files skipped.
```

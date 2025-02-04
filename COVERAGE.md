Current coverage report:

```
Name                                                           Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------
pyaurorax/__init__.py                                              9      0   100%
pyaurorax/_util.py                                                 5      3    40%   25-27
pyaurorax/cli/cli.py                                              37      0   100%
pyaurorax/cli/search/__init__.py                                  16      0   100%
pyaurorax/cli/search/availability/commands.py                    127      0   100%
pyaurorax/cli/search/conjunctions/commands.py                    184    114    38%   62-79, 84, 102-113, 137-154, 168-184, 201, 215-241, 252-257, 285-340, 355-370
pyaurorax/cli/search/data_products/commands.py                   175    111    37%   36-58, 63, 81-92, 115-129, 143-159, 176, 190-216, 227-232, 252-297, 322-337
pyaurorax/cli/search/ephemeris/commands.py                       173    109    37%   36-56, 61, 79-90, 113-127, 141-157, 174, 188-214, 225-230, 250-293, 308-323
pyaurorax/cli/search/helpers.py                                  158    140    11%   32-35, 46-86, 97-148, 160-276
pyaurorax/cli/search/sources/commands.py                         315    240    24%   40-51, 60-114, 118-167, 172-255, 260, 282-304, 326-382, 405-416, 435-442, 456-463, 485-497, 515-526, 539-544
pyaurorax/cli/search/util/commands.py                            124     81    35%   29-108, 113, 142-153, 182-193, 244-281, 293-294
pyaurorax/cli/templates.py                                         3      0   100%
pyaurorax/data/__init__.py                                        81     64    21%   49, 78-90, 125-164, 187-201, 233-245, 280-319
pyaurorax/data/ucalgary/__init__.py                              110     81    26%   35, 68, 96-104, 126-129, 160-163, 172, 193, 311-329, 419-433, 494-504, 586, 639-675, 719-755, 799-835
pyaurorax/data/ucalgary/read/__init__.py                          43     21    51%   22, 41, 62, 141-155, 224-236, 305, 383, 462, 541, 619, 667, 711, 786
pyaurorax/exceptions.py                                           28      0   100%
pyaurorax/models/__init__.py                                      10      1    90%   49
pyaurorax/models/atm/__init__.py                                  22      9    59%   38, 168-189, 279-297
pyaurorax/pyaurorax.py                                           222    114    49%   147, 173, 180, 187, 202, 207, 211, 223-233, 244-248, 270-272, 283-285, 292, 296-301, 308, 312, 318, 321, 339-347, 391-401, 421-431, 459-537
pyaurorax/search/__init__.py                                      93      6    94%   169, 197, 204, 211, 218, 225
pyaurorax/search/api/__init__.py                                  20      0   100%
pyaurorax/search/api/classes/request.py                           73     32    56%   70-71, 79, 111-112, 116-123, 127-135, 139, 143-147, 151, 155-159, 165, 169-174, 183, 186
pyaurorax/search/api/classes/response.py                          11      2    82%   43, 46
pyaurorax/search/availability/__init__.py                         14      0   100%
pyaurorax/search/availability/_availability.py                    21      0   100%
pyaurorax/search/availability/classes/availability_result.py       8      0   100%
pyaurorax/search/conjunctions/__init__.py                         29      6    79%   61, 132, 190, 210, 226, 258
pyaurorax/search/conjunctions/_conjunctions.py                    94     81    14%   31-79, 84-147, 152-165, 169-170, 175-191
pyaurorax/search/conjunctions/classes/conjunction.py              24     11    54%   88-96, 99, 102
pyaurorax/search/conjunctions/classes/criteria_block.py           84     60    29%   45-48, 51, 54, 66-76, 107-111, 114, 117, 130-141, 144-147, 166-168, 171, 174, 185-194, 209, 212, 215, 221-222, 225-233
pyaurorax/search/conjunctions/classes/search.py                  215    179    17%   40, 124-145, 148, 151, 162-203, 207-220, 232-245, 259-279, 289, 294-298, 309-373, 377, 387-403, 418-432, 445-446, 456-474, 491-492, 519-520, 530-535
pyaurorax/search/conjunctions/swarmaurora/__init__.py             15      3    80%   46, 65, 87
pyaurorax/search/conjunctions/swarmaurora/_swarmaurora.py         25     18    28%   25, 29-35, 41-58
pyaurorax/search/data_products/__init__.py                        33      8    76%   122-129, 175, 199, 234, 251, 268
pyaurorax/search/data_products/_data_products.py                 100     83    17%   38-54, 60-106, 111-148, 153-172, 177-204, 209-222, 226-227
pyaurorax/search/data_products/classes/data_product.py            47     29    38%   102-107, 118-141, 144, 148-157
pyaurorax/search/data_products/classes/search.py                 128    101    21%   33, 118-139, 142, 145, 156-197, 205-231, 235, 242-255, 267-281, 291-292, 299-316, 330-331, 360-361, 371-376
pyaurorax/search/ephemeris/__init__.py                            30      7    77%   117-124, 163, 191, 208, 224
pyaurorax/search/ephemeris/_ephemeris.py                          88     73    17%   36-52, 58-103, 108-145, 150-170, 175-188, 192-193
pyaurorax/search/ephemeris/classes/ephemeris.py                   42     33    21%   60-66, 77-108, 111, 115-121
pyaurorax/search/ephemeris/classes/search.py                     129    102    21%   33, 115-135, 138, 141, 152-193, 201-226, 230, 240-257, 269-283, 292-293, 300-317, 330-331, 360-361, 371-376
pyaurorax/search/location.py                                      29     15    48%   40-44, 48, 52-55, 59, 63-66, 76, 79, 82
pyaurorax/search/metadata/__init__.py                             14      3    79%   57, 70, 83
pyaurorax/search/metadata/_metadata.py                            20     15    25%   24-34, 39-45, 50-56
pyaurorax/search/metadata_filters.py                              61     39    36%   53-55, 59, 63-66, 69, 73-78, 86-89, 95, 126-127, 131, 135-137, 140, 144-152, 159-169, 175
pyaurorax/search/requests/__init__.py                             28      7    75%   58, 80, 93, 112, 144, 191, 207
pyaurorax/search/requests/_requests.py                            97     83    14%   34-38, 43-74, 79-85, 90-102, 107-127, 132-169, 174-181
pyaurorax/search/sources/__init__.py                              59     33    44%   118, 183-240, 284, 385, 419, 437, 456, 523
pyaurorax/search/sources/_sources.py                             119     85    29%   39-55, 89, 92, 107-135, 153-157, 162-173, 178-192, 207-246, 251-262, 268-294
pyaurorax/search/sources/classes/data_source.py                   68     26    62%   170, 173, 186-212
pyaurorax/search/sources/classes/data_source_stats.py             22     15    32%   53-58, 61, 64, 73-79
pyaurorax/search/util/__init__.py                                 11      2    82%   52, 72
pyaurorax/search/util/_calculate_btrace.py                        18     12    33%   26-35, 40-46, 51-57
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
TOTAL                                                           6199   4403    29%

13 empty files skipped.
```

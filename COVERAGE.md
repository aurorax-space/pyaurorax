Current coverage report:

```
Name                                                           Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------------------
pyaurorax/__init__.py                                              8      0   100%
pyaurorax/cli/cli.py                                              41     41     0%   1-79
pyaurorax/cli/search/__init__.py                                  16     16     0%   1-21
pyaurorax/cli/search/availability/commands.py                    138    138     0%   1-227
pyaurorax/cli/search/conjunctions/commands.py                    184    184     0%   1-356
pyaurorax/cli/search/data_products/commands.py                   175    175     0%   1-323
pyaurorax/cli/search/ephemeris/commands.py                       173    173     0%   1-309
pyaurorax/cli/search/helpers.py                                  158    158     0%   1-262
pyaurorax/cli/search/sources/commands.py                         315    315     0%   1-530
pyaurorax/cli/search/util/commands.py                            124    124     0%   1-280
pyaurorax/cli/templates.py                                         3      3     0%   6-77
pyaurorax/data/__init__.py                                         9      1    89%   32
pyaurorax/data/ucalgary/__init__.py                               52     29    44%   20, 44, 68-71, 99-102, 111, 132, 245-263, 348-362, 423-433, 495
pyaurorax/data/ucalgary/read/__init__.py                          39     20    49%   6, 25, 46, 105-117, 166-176, 225, 281, 338, 394, 450, 494, 536
pyaurorax/exceptions.py                                           28      0   100%
pyaurorax/models/__init__.py                                      10      1    90%   36
pyaurorax/models/atm/__init__.py                                  22      9    59%   24, 145-166, 252-269
pyaurorax/pyaurorax.py                                           140      7    95%   119, 142, 149, 156, 220, 253, 257
pyaurorax/search/__init__.py                                      61      0   100%
pyaurorax/search/api/__init__.py                                  20      0   100%
pyaurorax/search/api/classes/request.py                           71     25    65%   46-47, 55, 85-86, 90-97, 107-109, 113-117, 121, 125-129, 135, 139, 153, 156
pyaurorax/search/api/classes/response.py                          10      2    80%   24, 27
pyaurorax/search/availability/__init__.py                         14      0   100%
pyaurorax/search/availability/_availability.py                    21      0   100%
pyaurorax/search/availability/classes/availability_result.py       8      0   100%
pyaurorax/search/conjunctions/__init__.py                         22      1    95%   40
pyaurorax/search/conjunctions/_conjunctions.py                    40     11    72%   26, 31-33, 41, 47, 51, 56, 70-73
pyaurorax/search/conjunctions/classes/conjunction.py              20      2    90%   64, 67
pyaurorax/search/conjunctions/classes/search.py                  132      9    93%   20, 140, 143, 296, 300, 322-323, 334-335
pyaurorax/search/conjunctions/swarmaurora/__init__.py             15      3    80%   31, 46, 64
pyaurorax/search/conjunctions/swarmaurora/_swarmaurora.py         25     18    28%   12, 16-22, 28-45
pyaurorax/search/data_products/__init__.py                        29      1    97%   178
pyaurorax/search/data_products/_data_products.py                 100     31    69%   27-31, 58, 63-65, 73, 79, 83, 88, 115, 130-132, 141, 156, 164-191, 198-201
pyaurorax/search/data_products/classes/data_product.py            42      2    95%   108, 132
pyaurorax/search/data_products/classes/search.py                  84      8    90%   19, 101, 104, 165, 184-185, 193-194
pyaurorax/search/ephemeris/__init__.py                            26      0   100%
pyaurorax/search/ephemeris/_ephemeris.py                          88     21    76%   25-29, 55, 60-62, 70, 76, 80, 85, 112, 127-129, 138, 154, 164-167
pyaurorax/search/ephemeris/classes/ephemeris.py                   42      1    98%   71
pyaurorax/search/ephemeris/classes/search.py                      85      9    89%   19, 98, 101, 136, 168, 187-188, 196-197
pyaurorax/search/location.py                                      29      6    79%   39-42, 50-53
pyaurorax/search/metadata/__init__.py                             14      0   100%
pyaurorax/search/metadata/_metadata.py                            20      5    75%   16-18, 32, 41
pyaurorax/search/requests/__init__.py                             28      3    89%   116, 151, 167
pyaurorax/search/requests/_requests.py                            97     44    55%   38, 81, 92, 97, 108, 115-118, 122, 128-165, 170-177
pyaurorax/search/sources/__init__.py                              31      0   100%
pyaurorax/search/sources/_sources.py                             119     16    87%   36, 38, 118, 140-141, 175, 194, 197, 199, 201, 203, 231-232, 243, 279-280
pyaurorax/search/sources/classes/data_source.py                   29      0   100%
pyaurorax/search/sources/classes/data_source_stats.py             11      0   100%
pyaurorax/search/util/__init__.py                                 11      0   100%
pyaurorax/search/util/_calculate_btrace.py                        18      0   100%
pyaurorax/tools/__init__.py                                        7      0   100%
pyaurorax/tools/_display.py                                        8      4    50%   42-45
pyaurorax/tools/_movie.py                                          2      1    50%   2
pyaurorax/tools/_scale_intensity.py                               24     21    12%   33-66
pyaurorax/tools/_util.py                                          10      7    30%   18-25
pyaurorax/tools/classes/keogram.py                                92     77    16%   40-47, 50, 53-59, 86-100, 132-154, 221-283
pyaurorax/tools/keogram/__init__.py                                2      0   100%
pyaurorax/tools/keogram/_create.py                                16     11    31%   32-50
--------------------------------------------------------------------------------------------
TOTAL                                                           3158   1733    45%

13 empty files skipped.
```

import unittest
from main import point_in_polygon, parse_command, get_results_for_region, get_results_for_location


class LocationMatcherTests(unittest.TestCase):
    def test_parse_command_with_all_required_arguments(self):
        command = ["main.py", "--regions=regions.json", "--locations=locations.json", "--output=results.json"]
        pg_mode, rg_path, lc_path, rs_path = parse_command(command)
        self.assertEqual(pg_mode, "1")
        self.assertEqual(rg_path, "regions.json")
        self.assertEqual(lc_path, "locations.json")
        self.assertEqual(rs_path, "results.json")

    def test_parse_command_without_output_argument(self):
        command = ["main.py", "--regions=regions.json", "--locations=locations.json"]
        pg_mode, rg_path, lc_path, rs_path = parse_command(command)
        self.assertEqual(pg_mode, "1")
        self.assertEqual(rg_path, "regions.json")
        self.assertEqual(lc_path, "locations.json")
        self.assertIsNone(rs_path)

    def test_parse_command_without_regions_argument(self):
        command = ["main.py", "--locations=locations.json", "--output=results.json"]
        pg_mode, rg_path, lc_path, rs_path = parse_command(command)
        self.assertEqual(pg_mode, "1")
        self.assertIsNone(rg_path)
        self.assertEqual(lc_path, "locations.json")
        self.assertEqual(rs_path, "results.json")

    def test_parse_command_without_locations_argument(self):
        command = ["main.py", "--regions=input/regions.json", "--output=output/results.json"]
        pg_mode, rg_path, lc_path, rs_path = parse_command(command)
        self.assertEqual(pg_mode, "1")
        self.assertEqual(rg_path, "input/regions.json")
        self.assertIsNone(lc_path)
        self.assertEqual(rs_path, "output/results.json")

    def test_parse_command_with_all_arguments(self):
        command = ["main.py", "--mode=2", "--regions=regions.json",
                   "--locations=locations.json", "--output=results.json"]
        pg_mode, rg_path, lc_path, rs_path = parse_command(command)
        self.assertEqual(pg_mode, "2")
        self.assertEqual(rg_path, "regions.json")
        self.assertEqual(lc_path, "locations.json")
        self.assertEqual(rs_path, "results.json")

    def test_point_inside_polygon(self):
        polygon = [[0, 0], [0, 4], [4, 4], [4, 0]]
        self.assertTrue(point_in_polygon([2, 2], polygon))

    def test_point_outside_polygon(self):
        polygon = [[0, 0], [0, 4], [4, 4], [4, 0]]
        self.assertFalse(point_in_polygon([5, 5], polygon))

    def test_result_for_regions_1(self):
        regions = [
            {
                "name": "test1",
                "coordinates": [
                    [
                        [
                            18.486901119544115,
                            54.42225054934434
                        ],
                        [
                            18.482301965775804,
                            54.44874651928285
                        ],
                        [
                            18.4404454012778,
                            54.41233509354086
                        ],
                        [
                            18.44108131793493,
                            54.38129764673721
                        ],
                        [
                            18.541657398596953,
                            54.33562994568271
                        ],
                        [
                            18.604846036718016,
                            54.315624757250106
                        ],
                        [
                            18.93496987211128,
                            54.34850014694035
                        ],
                        [
                            18.70119504595141,
                            54.402464165062355
                        ],
                        [
                            18.59848784875257,
                            54.42572521244762
                        ],
                        [
                            18.54022722944734,
                            54.42319609355408
                        ],
                        [
                            18.486901119544115,
                            54.42225054934434
                        ]
                    ]
                ]
            }
        ]
        locations = [
            {
                "name": "out2",
                "coordinates": [
                    18.84076890034507,
                    54.33873029905652
                ]
            },
            {
                "name": "incorner2",
                "coordinates": [
                    18.931950917171378,
                    54.348577611002554
                ]
            },
            {
                "name": "out1",
                "coordinates": [
                    18.490537977962674,
                    54.42694956132851
                ]
            },
            {
                "name": "incorner1",
                "coordinates": [
                    18.441896668860096,
                    54.381759043498334
                ]
            },
            {
                "name": "inside",
                "coordinates": [
                    18.650962845792463,
                    54.36009034535789
                ]
            }
        ]
        results = get_results_for_region(regions, locations)
        self.assertEqual(results, [
            {
                "region": "test1",
                "matched_locations": [
                    "incorner2",
                    "incorner1",
                    "inside"
                ]
            }
        ])

    def test_result_for_regions_2(self):
        regions = [
            {
                "name": "test2",
                "coordinates": [
                    [
                        [
                            -152.92947880874874,
                            63.63428063223677
                        ],
                        [
                            -60.90244079500921,
                            63.63428063223677
                        ],
                        [
                            -60.90244079500921,
                            74.40041291697725
                        ],
                        [
                            -152.92947880874874,
                            74.40041291697725
                        ],
                        [
                            -152.92947880874874,
                            63.63428063223677
                        ]
                    ]
                ]
            }
        ]
        locations = [
            {
                "name": "el_1",
                "coordinates": [
                    -114.10135634201121,
                    64.25206301530983
                ]
            },
            {
                "name": "el_2",
                "coordinates": [
                    -111.060947419213,
                    74.54689210787211
                ]
            },
            {
                "name": "el_3",
                "coordinates": [
                    -152.3566135788395,
                    74.26860732688252
                ]
            }
        ]
        self.assertEqual(get_results_for_region(regions, locations), [
            {
                'region': 'test2',
                'matched_locations': [
                    'el_1',
                    'el_3'
                ]
            }
        ])

    def test_result_for_regions_3(self):
        regions = [
            {
                "name": "region1",
                "coordinates": [
                    [
                        [
                            25.13573603154873,
                            54.67922829209249
                        ],
                        [
                            25.156131289233258,
                            54.58478594629585
                        ],
                        [
                            25.286660938416787,
                            54.5942400514071
                        ],
                        [
                            25.429427742209867,
                            54.64619841630662
                        ],
                        [
                            25.36416291761924,
                            54.77109854334182
                        ],
                        [
                            25.13573603154873,
                            54.77109854334182
                        ],
                        [
                            25.13573603154873,
                            54.67922829209249
                        ]
                    ]
                ]
            },
            {
                "name": "region2",
                "coordinates": [
                    [
                        [
                            23.728463251292055,
                            54.85806510526285
                        ],
                        [
                            23.834518591254124,
                            54.815780434232124
                        ],
                        [
                            24.02623401349132,
                            54.815780434232124
                        ],
                        [
                            24.07110358039847,
                            54.87215015295382
                        ],
                        [
                            24.042550219638912,
                            54.98465349182413
                        ],
                        [
                            23.728463251292055,
                            54.98465349182413
                        ],
                        [
                            23.728463251292055,
                            54.85806510526285
                        ]
                    ]
                ]
            },
            {
                "name": "region3",
                "coordinates": [
                    [
                        [
                            21.099044587495996,
                            55.697364539462455
                        ],
                        [
                            21.13167699979246,
                            55.63985211052827
                        ],
                        [
                            21.233653288216374,
                            55.6766698024725
                        ],
                        [
                            21.201020875921074,
                            55.741017470855724
                        ],
                        [
                            21.135756051329366,
                            55.80067402588713
                        ],
                        [
                            21.099044587495996,
                            55.697364539462455
                        ]
                    ],
                    [
                        [
                            21.100737600741354,
                            55.64456937538671
                        ],
                        [
                            21.08556244179519,
                            55.48839930587644
                        ],
                        [
                            20.97630129738701,
                            55.30743065067017
                        ],
                        [
                            21.049142060326403,
                            55.31952101226224
                        ],
                        [
                            21.115912759686722,
                            55.495276974748975
                        ],
                        [
                            21.131087918632034,
                            55.630865024154645
                        ],
                        [
                            21.100737600741354,
                            55.64456937538671
                        ]
                    ]
                ]
            }
        ]
        locations = [
            {
                "name": "location1",
                "coordinates": [
                    25.21051562929364,
                    54.64057937965808
                ]
            },
            {
                "name": "location2",
                "coordinates": [
                    25.217719661438338,
                    54.69890349790981
                ]
            },
            {
                "name": "location3",
                "coordinates": [
                    23.85255556998709,
                    54.87130112002856
                ]
            },
            {
                "name": "location4",
                "coordinates": [
                    23.982228148594658,
                    54.85056925096666
                ]
            },
            {
                "name": "location5",
                "coordinates": [
                    24.01824830931949,
                    54.90237894285653
                ]
            },
            {
                "name": "location6",
                "coordinates": [
                    24.47678240050834,
                    55.15818800439831
                ]
            }
        ]
        self.assertEqual(get_results_for_region(regions, locations), [
            {
                "region": "region1",
                "matched_locations": [
                    "location1",
                    "location2"
                ]
            },
            {
                "region": "region2",
                "matched_locations": [
                    "location3",
                    "location4",
                    "location5"
                ]
            },
            {
                "region": "region3",
                "matched_locations": []
            }
        ])

    def test_result_for_regions_4(self):
        regions = [
            {
                "name": "test_polygon_4",
                "coordinates": [
                    [
                        [
                            -116.34917323602983,
                            46.87666764516911
                        ],
                        [
                            -116.34917323602983,
                            -68.22318749903037
                        ],
                        [
                            -72.13400970005421,
                            -68.22318749903037
                        ],
                        [
                            -72.13400970005421,
                            46.87666764516911
                        ],
                        [
                            -116.34917323602983,
                            46.87666764516911
                        ]
                    ]
                ]
            }
        ]
        locations = [
            {
                "name": "el_1",
                "coordinates": [
                    -72.13369334822063,
                    24.171830611872608
                ]
            }
        ]
        self.assertEqual(get_results_for_region(regions, locations), [
            {
                'region': 'test_polygon_4',
                'matched_locations': []
            }
        ])

    def test_result_for_regions_5(self):
        regions = [
            {
                "name": "region1",
                "coordinates": [
                    [
                        [
                            5,
                            5
                        ],
                        [
                            7,
                            -3
                        ],
                        [
                            -3,
                            -3
                        ],
                        [
                            -1,
                            -1
                        ],
                        [
                            -4,
                            2
                        ],
                        [
                            -2,
                            4
                        ],
                        [
                            0,
                            7
                        ]
                    ]
                ]
            }
        ]
        locations = [
            {
                "name": "location1",
                "coordinates": [
                    2.5,
                    6
                ]
            },
            {
                "name": "location2",
                "coordinates": [
                    3.34,
                    5.61
                ]
            },
            {
                "name": "location3",
                "coordinates": [
                    5,
                    5
                ]
            },
            {
                "name": "location4",
                "coordinates": [
                    0,
                    7
                ]
            },
            {
                "name": "location5",
                "coordinates": [
                    -1.34,
                    4.99
                ]
            }
        ]
        self.assertEqual(get_results_for_region(regions, locations), [
            {
                'region': 'region1',
                'matched_locations': [
                    'location1',
                    'location2',
                    'location3'
                ]
            }
        ])

    def test_result_for_locations_1(self):
        regions = [
            {
                "name": "test1",
                "coordinates": [
                    [
                        [
                            18.486901119544115,
                            54.42225054934434
                        ],
                        [
                            18.482301965775804,
                            54.44874651928285
                        ],
                        [
                            18.4404454012778,
                            54.41233509354086
                        ],
                        [
                            18.44108131793493,
                            54.38129764673721
                        ],
                        [
                            18.541657398596953,
                            54.33562994568271
                        ],
                        [
                            18.604846036718016,
                            54.315624757250106
                        ],
                        [
                            18.93496987211128,
                            54.34850014694035
                        ],
                        [
                            18.70119504595141,
                            54.402464165062355
                        ],
                        [
                            18.59848784875257,
                            54.42572521244762
                        ],
                        [
                            18.54022722944734,
                            54.42319609355408
                        ],
                        [
                            18.486901119544115,
                            54.42225054934434
                        ]
                    ]
                ]
            }
        ]
        locations = [
            {
                "name": "out2",
                "coordinates": [
                    18.84076890034507,
                    54.33873029905652
                ]
            },
            {
                "name": "incorner2",
                "coordinates": [
                    18.931950917171378,
                    54.348577611002554
                ]
            },
            {
                "name": "out1",
                "coordinates": [
                    18.490537977962674,
                    54.42694956132851
                ]
            },
            {
                "name": "incorner1",
                "coordinates": [
                    18.441896668860096,
                    54.381759043498334
                ]
            },
            {
                "name": "inside",
                "coordinates": [
                    18.650962845792463,
                    54.36009034535789
                ]
            }
        ]
        results = get_results_for_location(regions, locations)
        self.assertEqual(results, [
            {
                "location": "out2",
                "matched_regions": []
            },
            {
                "location": "incorner2",
                "matched_regions": [
                    "test1"
                ]
            },
            {
                "location": "out1",
                "matched_regions": []
            },
            {
                "location": "incorner1",
                "matched_regions": [
                    "test1"
                ]
            },
            {
                "location": "inside",
                "matched_regions": [
                    "test1"
                ]
            }
        ])

    def test_result_for_locations_2(self):
        regions = [
            {
                "name": "test2",
                "coordinates": [
                    [
                        [
                            -152.92947880874874,
                            63.63428063223677
                        ],
                        [
                            -60.90244079500921,
                            63.63428063223677
                        ],
                        [
                            -60.90244079500921,
                            74.40041291697725
                        ],
                        [
                            -152.92947880874874,
                            74.40041291697725
                        ],
                        [
                            -152.92947880874874,
                            63.63428063223677
                        ]
                    ]
                ]
            }
        ]
        locations = [
            {
                "name": "el_1",
                "coordinates": [
                    -114.10135634201121,
                    64.25206301530983
                ]
            },
            {
                "name": "el_2",
                "coordinates": [
                    -111.060947419213,
                    74.54689210787211
                ]
            },
            {
                "name": "el_3",
                "coordinates": [
                    -152.3566135788395,
                    74.26860732688252
                ]
            }
        ]
        self.assertEqual(get_results_for_location(regions, locations), [
            {
                "location": "el_1",
                "matched_regions": [
                    "test2"
                ]
            },
            {
                "location": "el_2",
                "matched_regions": []
            },
            {
                "location": "el_3",
                "matched_regions": [
                    "test2"
                ]
            }
        ])

    def test_result_for_locations_3(self):
        regions = [
            {
                "name": "region1",
                "coordinates": [
                    [
                        [
                            25.13573603154873,
                            54.67922829209249
                        ],
                        [
                            25.156131289233258,
                            54.58478594629585
                        ],
                        [
                            25.286660938416787,
                            54.5942400514071
                        ],
                        [
                            25.429427742209867,
                            54.64619841630662
                        ],
                        [
                            25.36416291761924,
                            54.77109854334182
                        ],
                        [
                            25.13573603154873,
                            54.77109854334182
                        ],
                        [
                            25.13573603154873,
                            54.67922829209249
                        ]
                    ]
                ]
            },
            {
                "name": "region2",
                "coordinates": [
                    [
                        [
                            23.728463251292055,
                            54.85806510526285
                        ],
                        [
                            23.834518591254124,
                            54.815780434232124
                        ],
                        [
                            24.02623401349132,
                            54.815780434232124
                        ],
                        [
                            24.07110358039847,
                            54.87215015295382
                        ],
                        [
                            24.042550219638912,
                            54.98465349182413
                        ],
                        [
                            23.728463251292055,
                            54.98465349182413
                        ],
                        [
                            23.728463251292055,
                            54.85806510526285
                        ]
                    ]
                ]
            },
            {
                "name": "region3",
                "coordinates": [
                    [
                        [
                            21.099044587495996,
                            55.697364539462455
                        ],
                        [
                            21.13167699979246,
                            55.63985211052827
                        ],
                        [
                            21.233653288216374,
                            55.6766698024725
                        ],
                        [
                            21.201020875921074,
                            55.741017470855724
                        ],
                        [
                            21.135756051329366,
                            55.80067402588713
                        ],
                        [
                            21.099044587495996,
                            55.697364539462455
                        ]
                    ],
                    [
                        [
                            21.100737600741354,
                            55.64456937538671
                        ],
                        [
                            21.08556244179519,
                            55.48839930587644
                        ],
                        [
                            20.97630129738701,
                            55.30743065067017
                        ],
                        [
                            21.049142060326403,
                            55.31952101226224
                        ],
                        [
                            21.115912759686722,
                            55.495276974748975
                        ],
                        [
                            21.131087918632034,
                            55.630865024154645
                        ],
                        [
                            21.100737600741354,
                            55.64456937538671
                        ]
                    ]
                ]
            }
        ]
        locations = [
            {
                "name": "location1",
                "coordinates": [
                    25.21051562929364,
                    54.64057937965808
                ]
            },
            {
                "name": "location2",
                "coordinates": [
                    25.217719661438338,
                    54.69890349790981
                ]
            },
            {
                "name": "location3",
                "coordinates": [
                    23.85255556998709,
                    54.87130112002856
                ]
            },
            {
                "name": "location4",
                "coordinates": [
                    23.982228148594658,
                    54.85056925096666
                ]
            },
            {
                "name": "location5",
                "coordinates": [
                    24.01824830931949,
                    54.90237894285653
                ]
            },
            {
                "name": "location6",
                "coordinates": [
                    24.47678240050834,
                    55.15818800439831
                ]
            }
        ]
        self.assertEqual(get_results_for_location(regions, locations), [
            {
                "location": "location1",
                "matched_regions": [
                    "region1"
                ]
            },
            {
                "location": "location2",
                "matched_regions": [
                    "region1"
                ]
            },
            {
                "location": "location3",
                "matched_regions": [
                    "region2"
                ]
            },
            {
                "location": "location4",
                "matched_regions": [
                    "region2"
                ]
            },
            {
                "location": "location5",
                "matched_regions": [
                    "region2"
                ]
            },
            {
                "location": "location6",
                "matched_regions": []
            }
        ])

    def test_result_for_locations_4(self):
        regions = [
            {
                "name": "test_polygon_4",
                "coordinates": [
                    [
                        [
                            -116.34917323602983,
                            46.87666764516911
                        ],
                        [
                            -116.34917323602983,
                            -68.22318749903037
                        ],
                        [
                            -72.13400970005421,
                            -68.22318749903037
                        ],
                        [
                            -72.13400970005421,
                            46.87666764516911
                        ],
                        [
                            -116.34917323602983,
                            46.87666764516911
                        ]
                    ]
                ]
            }
        ]
        locations = [
            {
                "name": "el_1",
                "coordinates": [
                    -72.13369334822063,
                    24.171830611872608
                ]
            }
        ]
        self.assertEqual(get_results_for_location(regions, locations), [
            {
                "location": "el_1",
                "matched_regions": []
            }
        ])

    def test_result_for_locations_5(self):
        regions = [
            {
                "name": "region1",
                "coordinates": [
                    [
                        [
                            5,
                            5
                        ],
                        [
                            7,
                            -3
                        ],
                        [
                            -3,
                            -3
                        ],
                        [
                            -1,
                            -1
                        ],
                        [
                            -4,
                            2
                        ],
                        [
                            -2,
                            4
                        ],
                        [
                            0,
                            7
                        ]
                    ]
                ]
            }
        ]
        locations = [
            {
                "name": "location1",
                "coordinates": [
                    2.5,
                    6
                ]
            },
            {
                "name": "location2",
                "coordinates": [
                    3.34,
                    5.61
                ]
            },
            {
                "name": "location3",
                "coordinates": [
                    5,
                    5
                ]
            },
            {
                "name": "location4",
                "coordinates": [
                    0,
                    7
                ]
            },
            {
                "name": "location5",
                "coordinates": [
                    -1.34,
                    4.99
                ]
            }
        ]
        self.assertEqual(get_results_for_location(regions, locations), [
            {
                'location': 'location1',
                'matched_regions': [
                    'region1'
                ]
            },
            {
                'location': 'location2',
                'matched_regions': [
                    'region1'
                ]
            },
            {
                'location': 'location3',
                'matched_regions': [
                    'region1'
                ]
            },
            {
                'location': 'location4',
                'matched_regions': []
            },
            {
                'location': 'location5',
                'matched_regions': []
            }
        ])


if __name__ == "__main__":
    unittest.main()

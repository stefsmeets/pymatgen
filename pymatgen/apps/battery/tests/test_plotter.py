# coding: utf-8
# Copyright (c) Pymatgen Development Team.
# Distributed under the terms of the MIT License.


import json
import os
import unittest

from pymatgen import Composition, MontyDecoder
from pymatgen.apps.battery.conversion_battery import ConversionElectrode
from pymatgen.apps.battery.insertion_battery import InsertionElectrode
from pymatgen.apps.battery.plotter import VoltageProfilePlotter
from pymatgen.entries.computed_entries import ComputedEntry

try:
    test_dir = os.environ["PMG_TEST_FILES_DIR"]
except KeyError:
    test_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "test_files")


class VoltageProfilePlotterTest(unittest.TestCase):
    def setUp(self):
        entry_Li = ComputedEntry("Li", -1.90753119)

        with open(os.path.join(test_dir, "LiTiO2_batt.json"), "r") as f:
            entries_LTO = json.load(f, cls=MontyDecoder)
            self.ie_LTO = InsertionElectrode.from_entries(entries_LTO, entry_Li)

        with open(os.path.join(test_dir, "FeF3_batt.json"), "r") as fid:
            entries = json.load(fid, cls=MontyDecoder)
            self.ce_FF = ConversionElectrode.from_composition_and_entries(
                Composition("FeF3"), entries
            )

    def testName(self):
        plotter = VoltageProfilePlotter(xaxis="frac_x")
        plotter.add_electrode(self.ie_LTO, "LTO insertion")
        plotter.add_electrode(self.ce_FF, "FeF3 conversion")
        self.assertIsNotNone(plotter.get_plot_data(self.ie_LTO))
        self.assertIsNotNone(plotter.get_plot_data(self.ce_FF))

    def testPlotly(self):
        plotter = VoltageProfilePlotter(xaxis="frac_x")
        plotter.add_electrode(self.ie_LTO, "LTO insertion")
        plotter.add_electrode(self.ce_FF, "FeF3 conversion")
        fig = plotter.get_plotly_figure()
        self.assertEqual(fig.layout.xaxis.title.text, "Atomic Fraction of Li")
        plotter = VoltageProfilePlotter(xaxis="x_form")
        plotter.add_electrode(self.ce_FF, "FeF3 conversion")
        fig = plotter.get_plotly_figure()
        self.assertEqual(fig.layout.xaxis.title.text, "x in Li<sub>x</sub>FeF3")

        plotter.add_electrode(self.ie_LTO, "LTO insertion")
        fig = plotter.get_plotly_figure()
        self.assertEqual(fig.layout.xaxis.title.text, "x Workion Ion per Host F.U.")


if __name__ == "__main__":
    unittest.main()

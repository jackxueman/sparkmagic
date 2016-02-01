# Copyright (c) 2015  aggftw@gmail.com
# Distributed under the terms of the Modified BSD License.

import pandas as pd
from ipywidgets import FlexBox

from remotespark.utils.ipywidgetfactory import IpyWidgetFactory
from .encoding import Encoding


class EncodingWidget(FlexBox):
    def __init__(self, df, encoding, change_hook, ipywidget_factory=None, testing=False, **kwargs):
        assert encoding is not None
        assert df is not None
        assert type(df) is pd.DataFrame
        assert len(df.columns) > 0

        kwargs['orientation'] = 'vertical'
        if not testing:
            super(EncodingWidget, self).__init__((), **kwargs)

        if ipywidget_factory is None:
            ipywidget_factory = IpyWidgetFactory()
        self.ipywidget_factory = ipywidget_factory

        self.df = df
        self.encoding = encoding
        self.change_hook = change_hook

        self.widget = self.ipywidget_factory.get_vbox()

        self.title = self.ipywidget_factory.get_html('Encoding:', width='148px', height='32px')

        # X view
        options_x_view = {str(i): str(i) for i in self.df.columns}
        options_x_view["-"] = None
        self.x_view = self.ipywidget_factory.get_dropdown(options=options_x_view,
                                                          description="X", value=self.encoding.x)
        self.x_view.on_trait_change(self._x_changed_callback, 'value')

        # Y
        options_y_view = {str(i): str(i) for i in self.df.columns}
        options_y_view["-"] = None
        y_column_view = self.ipywidget_factory.get_dropdown(options=options_y_view,
                                                            description="Y", value=self.encoding.y)
        y_column_view.on_trait_change(self._y_changed_callback, 'value')

        # Y aggregator
        value_for_view = self._get_value_for_aggregation(self.encoding.y_aggregation)
        self.y_agg_view = self.ipywidget_factory.get_dropdown(
            options={"-": Encoding.y_agg_none,
                     Encoding.y_agg_avg: Encoding.y_agg_avg,
                     Encoding.y_agg_min: Encoding.y_agg_min,
                     Encoding.y_agg_max: Encoding.y_agg_max,
                     Encoding.y_agg_sum: Encoding.y_agg_sum,
                     Encoding.y_agg_count: Encoding.y_agg_count},
            description="Func.",
            value=value_for_view)
        self.y_agg_view.on_trait_change(self._y_agg_changed_callback, 'value')

        # Y view
        self.y_view = self.ipywidget_factory.get_hbox()
        self.y_view.children = [y_column_view, self.y_agg_view]

        # Logarithmic X axis
        self.logarithmic_x_axis = self.ipywidget_factory.get_checkbox(
            description="Log scale X", value=encoding.logarithmic_x_axis)
        self.logarithmic_x_axis.on_trait_change(self._logarithmic_x_callback, "value")

        # Logarithmic Y axis
        self.logarithmic_y_axis = self.ipywidget_factory.get_checkbox(
            description="Log scale Y", value=encoding.logarithmic_y_axis)
        self.logarithmic_y_axis.on_trait_change(self._logarithmic_y_callback, "value")

        children = [self.title, self.x_view, self.y_view, self.logarithmic_x_axis, self.logarithmic_y_axis]
        self.widget.children = children

        self.children = [self.widget]

    def show_x(self, boolean):
        self.x_view.visible = boolean

    def show_logarithmic_x_axis(self, boolean):
        self.logarithmic_x_axis.visible = boolean

    def show_logarithmic_y_axis(self, boolean):
        self.logarithmic_y_axis.visible = boolean

    def show_y(self, boolean):
        self.y_view.visible = boolean

    def show_controls(self, boolean):
        self.widget.visible = boolean

    def _get_value_for_aggregation(self, y_aggregation):
        if y_aggregation is not None:
            return y_aggregation

        return "none"

    def _x_changed_callback(self, name, old_value, new_value):
            self.encoding.x = new_value
            return self.change_hook()

    def _y_changed_callback(self, name, old_value, new_value):
            self.encoding.y = new_value
            return self.change_hook()

    def _y_agg_changed_callback(self, name, old_value, new_value):
            if new_value == "none":
                self.encoding.y_aggregation = None
            else:
                self.encoding.y_aggregation = new_value
            return self.change_hook()

    def _logarithmic_x_callback(self, name, old_value, new_value):
            self.encoding.logarithmic_x_axis = new_value
            return self.change_hook()

    def _logarithmic_y_callback(self, name, old_value, new_value):
            self.encoding.logarithmic_y_axis = new_value
            return self.change_hook()

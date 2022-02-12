# -*- coding: utf-8 -*-
# @Time    : 1/24/22 02:37
# @Author  : godot
# @FileName: introduction.py
# @Project : prevoyance
# @Software: PyCharm
from dash import html


def intro():
    return html.Div(children=[
        html.H1(children='Prevoyance'),
        html.B("Description:"),
        '''
            Prevoyance is an application that can compute D-optimal designs for Dose-Response design which can be described by a general family of models.
        ''',
        html.Div(children=
        [
            html.B("Models:"),
            html.P("$$\\text{Model 1:}\quad y = a \\text{ with }a>0$$"),
            html.P("$$\\text{Model 2:}\quad y = a \exp{(x/b)} \\text{ with }a>0$$"),
            html.P("$$\\text{Model 3:}\quad y = a \exp{(\pm(x/b)^d)} \\text{ with }a>0, b>0, d\geq1$$"),
            html.P("$$\\text{Model 4:}\quad y = a [c - (c -1)\exp{(-x/b)}] \\text{ with }a>0, b>0, c>0$$"),
            html.P("$$\\text{Model 5:}\quad y = a [c - (c -1)\exp{(-(x/b)^d)}] \\text{ with }a>0, b>0, c>0,d\geq1$$")
        ]
        ),
        html.P(
            "This four models can be used for describing the change in any continuous endpoint as a function of dose."),
        html.P("$y$ is any continuous endpoint, and $x$ denotes the dose."),
        html.P(
            "In all models the parameter $a$ represents the level of the endpoint at dose 0, and $b$ can be considered as the parameter reﬂecting the efﬁcacy of the chemical (or the sensitivity of the subject)."),
        html.P(
            "At high doses Models 3 and 4 level off to the value $ac$, so the parameter $c$ can be interpreted as the maximum relative change."),
        html.P(
            "The parameter $d$ is constrained to values $\geq$ 1, to prevent the slope of the function at dose 0 being inﬁnite, which seems biologically implausible."),
        html.Br()
    ])

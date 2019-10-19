# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc
import pandas as pd
import os.path
import copy
from six.moves.urllib.parse import quote

scenarios = ['BAU', 'Current Policies', 'SDG7']

my_path = os.path.abspath(os.path.dirname(__file__))
folder = os.path.join(my_path, 'Data')
descriptions = {'bau_scenario': open(os.path.join(folder, 'Descriptions', 'bau_scenario.txt')).read(),
                'current_policies_scenario': open(os.path.join(folder, 'Descriptions', 'current_policies_scenario.txt')).read(),
                'sdg7_scenario': open(os.path.join(folder, 'Descriptions', 'sdg7_scenario.txt')).read(),
                'electricity': open(os.path.join(folder, 'Descriptions', 'electricity.txt')).read(),
                'sdg7.1.1': open(os.path.join(folder, 'Descriptions', 'sdg7.1.1.txt')).read(),
                'sdg7.1.2': open(os.path.join(folder, 'Descriptions', 'sdg7.1.2.txt')).read(),
                'sdg7.2': open(os.path.join(folder, 'Descriptions', 'sdg7.2.txt')).read(),
                'sdg7.3': open(os.path.join(folder, 'Descriptions', 'sdg7.3.txt')).read(),
                'tfec': open(os.path.join(folder, 'Descriptions', 'tfec.txt')).read(),
                }
economic_parameters = pd.read_excel(os.path.join(folder, 'economic_parameters.xlsx'))
economic_parameters = economic_parameters.set_index('scenario').to_dict()
input_tfec = pd.read_excel(os.path.join(folder, 'TFEC.xlsx'))
input_production = pd.read_excel(os.path.join(folder, 'Electricity_generation.xlsx'))
input_tfec_re = pd.read_excel(os.path.join(folder, 'TFEC_renewables.xlsx'))
input_elec_demand = pd.read_excel(os.path.join(folder, 'Electricity_demand.xlsx'))
input_elec_access = pd.read_excel(os.path.join(folder, 'SDG7_1.xlsx'))
input_cooking = pd.read_excel(os.path.join(folder, 'Cooking.xlsx'))
input_efficiency = pd.read_excel(os.path.join(folder, 'EnergyEfficiency.xlsx'))
input_re_capacity = pd.read_excel(os.path.join(folder, 'Renewables.xlsx'))
tfec_variable = 'UseByTechnologyAnnual'
tfec_re_variable = 'UseByTechnologyAnnual'
df_tfec = pd.DataFrame(columns=['y', 't', 'f', tfec_variable, 'Scenario'])
df_tfec_re = pd.DataFrame(columns=['y', 't', 'f', tfec_re_variable, 'Scenario'])
supply_variable = 'ProductionByTechnologyAnnual'
df_supply = pd.DataFrame(columns=['y', 't', 'f', supply_variable, 'Scenario'])
emissions_variable = 'AnnualTechnologyEmission'
df_emissions = pd.DataFrame(columns=['e', 't', 'y', emissions_variable, 'Scenario'])
elec_demand_variable = 'UseByTechnologyAnnual'
df_elec_demand = pd.DataFrame(columns=['y', 't', 'f', elec_demand_variable, 'Scenario'])
elec_access_variable = cooking_variable = 'UseByTechnologyAnnual'
df_elec_access = pd.DataFrame(columns=['y', 't', 'f', elec_access_variable, 'Scenario'])
df_cooking = pd.DataFrame(columns=['y', 't', 'f', cooking_variable, 'Scenario'])
efficiency_variable = 'ProductionByTechnologyAnnual'
df_efficiency = pd.DataFrame(columns=['y', 't', 'f', efficiency_variable, 'Scenario'])
re_capacity_variable = 'TotalCapacityAnnual'
df_re_capacity = pd.DataFrame(columns=['y', 't', re_capacity_variable, 'Scenario'])
investment_variable = 'CapitalInvestment'
df_re_investment = pd.DataFrame(columns=['y', 't', investment_variable, 'Scenario'])
df_investment = pd.DataFrame(columns=['y', 't', investment_variable, 'Scenario'])
cost_variable = 'TotalDiscountedCost'
df_cost = pd.DataFrame(columns=['y', cost_variable, 'Scenario'])

for scenario in scenarios:
    ##tfec##
    df_tfec_temp = pd.read_csv(os.path.join(folder, scenario, tfec_variable + '.csv'))
    df_tfec_temp.drop(columns=['r'], inplace=True)
    df_tfec_temp = df_tfec_temp.loc[df_tfec_temp[tfec_variable] > 0]
    df_tfec_temp = df_tfec_temp[df_tfec_temp['t'].isin(input_tfec['OSEMOSYS'])]
    df_tfec_temp['Scenario'] = scenario
    df_tfec_temp = df_tfec_temp.reset_index(drop=True)
    df_tfec_temp['Fuel'] = df_tfec_temp['t'].map(input_tfec.set_index('OSEMOSYS')['Fuel'].T.to_dict())
    df_tfec_temp['Sector'] = df_tfec_temp['t'].map(input_tfec.set_index('OSEMOSYS')['Sector'].T.to_dict())
    df_tfec = df_tfec.append(df_tfec_temp, ignore_index=True, sort=False)

    ##tfec renewable##
    df_tfec_re_temp = pd.read_csv(os.path.join(folder, scenario, tfec_re_variable + '.csv'))
    df_tfec_re_temp.drop(columns=['r'], inplace=True)
    df_tfec_re_temp = df_tfec_re_temp.loc[df_tfec_re_temp[tfec_re_variable] > 0]
    df_tfec_re_temp = df_tfec_re_temp[df_tfec_re_temp['t'].isin(input_tfec_re['OSEMOSYS'])]
    df_tfec_re_temp['Scenario'] = scenario
    df_tfec_re_temp = df_tfec_re_temp.reset_index(drop=True)
    df_tfec_re_temp['RE'] = df_tfec_re_temp['t'].map(input_tfec_re.set_index('OSEMOSYS')['Renewable'].T.to_dict())
    df_tfec_re = df_tfec_re.append(df_tfec_re_temp, ignore_index=True, sort=False)

    ##Supply##
    df_supply_temp = pd.read_csv(os.path.join(folder, scenario, supply_variable + '.csv'))
    df_supply_temp.drop(columns=['r'], inplace=True)
    df_supply_temp = df_supply_temp.loc[df_supply_temp[supply_variable] > 0]
    df_supply_temp = df_supply_temp.loc[df_supply_temp['t'].isin(input_production['OSEMOSYS'])]
    df_supply_temp['Scenario'] = scenario
    df_supply_temp = df_supply_temp.reset_index(drop=True)
    df_supply_temp['Use'] = df_supply_temp['t'].map(input_production.set_index('OSEMOSYS')['Use'].T.to_dict())
    df_supply_temp['Source'] = df_supply_temp['t'].map(input_production.set_index('OSEMOSYS')['Source'].T.to_dict())
    df_supply_temp['Type'] = df_supply_temp['t'].map(input_production.set_index('OSEMOSYS')['Type'].T.to_dict())
    df_supply = df_supply.append(df_supply_temp, ignore_index=True, sort=False)

    ##Emissions##
    df_emissions_temp = pd.read_csv(os.path.join(folder, scenario, emissions_variable + '.csv'))
    df_emissions_temp.drop(columns=['r'], inplace=True)
    df_emissions_temp = df_emissions_temp.loc[df_emissions_temp[emissions_variable] > 0]
    # df_emissions_temp = df_emissions_temp.loc[df_emissions_temp['t'].isin(input_production['OSEMOSYS'])]
    df_emissions_temp['Scenario'] = scenario
    df_emissions_temp = df_emissions_temp.reset_index(drop=True)
    df_emissions_temp['Use'] = df_emissions_temp['t'].map(input_production.set_index('OSEMOSYS')['Use'].T.to_dict())
    df_emissions_temp['Source'] = df_emissions_temp['t'].map(input_production.set_index('OSEMOSYS')['Source'].T.to_dict())
    df_emissions_temp['Type'] = df_emissions_temp['t'].map(input_production.set_index('OSEMOSYS')['Type'].T.to_dict())
    df_emissions = df_emissions.append(df_emissions_temp, ignore_index=True, sort=False)

    ##Electricity demand##
    df_elec_demand_temp = pd.read_csv(os.path.join(folder, scenario, elec_demand_variable + '.csv'))
    df_elec_demand_temp.drop(columns=['r'], inplace=True)
    df_elec_demand_temp = df_elec_demand_temp.loc[df_elec_demand_temp[elec_demand_variable] > 0]
    df_elec_demand_temp = df_elec_demand_temp[df_elec_demand_temp['t'].isin(input_elec_demand['OSEMOSYS'])]
    df_elec_demand_temp['Scenario'] = scenario
    df_elec_demand_temp = df_elec_demand_temp.reset_index(drop=True)
    df_elec_demand_temp['Use'] = df_elec_demand_temp['t'].map(input_elec_demand.set_index('OSEMOSYS')['Use'].T.to_dict())
    df_elec_demand_temp['Sector'] = df_elec_demand_temp['t'].map(input_elec_demand.set_index('OSEMOSYS')['Sector'].T.to_dict())
    df_elec_demand = df_elec_demand.append(df_elec_demand_temp, ignore_index=True, sort=False)

    ##Electricity access##
    df_elec_access_temp = pd.read_csv(os.path.join(folder, scenario, elec_access_variable + '.csv'))
    df_elec_access_temp.drop(columns=['r'], inplace=True)
    df_elec_access_temp = df_elec_access_temp.loc[df_elec_access_temp[elec_access_variable] > 0]
    df_elec_access_temp = df_elec_access_temp[df_elec_access_temp['t'].isin(input_elec_access['OSEMOSYS'])]
    df_elec_access_temp['Scenario'] = scenario
    df_elec_access_temp = df_elec_access_temp.reset_index(drop=True)
    df_elec_access_temp['VISUALIZATION'] = df_elec_access_temp['t'].map(input_elec_access.set_index('OSEMOSYS')['VISUALIZATION'].T.to_dict())
    df_elec_access = df_elec_access.append(df_elec_access_temp, ignore_index=True, sort=False)

    ##Clean cooking access##
    df_cooking_temp = pd.read_csv(os.path.join(folder, scenario, cooking_variable + '.csv'))
    df_cooking_temp.drop(columns=['r'], inplace=True)
    df_cooking_temp = df_cooking_temp.loc[df_cooking_temp[cooking_variable] > 0]
    df_cooking_temp = df_cooking_temp[df_cooking_temp['t'].isin(input_cooking['OSEMOSYS'])]
    df_cooking_temp['Scenario'] = scenario
    df_cooking_temp = df_cooking_temp.reset_index(drop=True)
    df_cooking_temp['VISUALIZATION'] = df_cooking_temp['t'].map(input_cooking.set_index('OSEMOSYS')['VISUALIZATION'].T.to_dict())
    df_cooking = df_cooking.append(df_cooking_temp, ignore_index=True, sort=False)

    ##Energy efficiency##
    df_efficency_temp = pd.read_csv(os.path.join(folder, scenario, efficiency_variable + '.csv'))
    df_efficency_temp.drop(columns=['r'], inplace=True)
    df_efficency_temp = df_efficency_temp.loc[df_efficency_temp[efficiency_variable] > 0]
    df_efficency_temp = df_efficency_temp.loc[df_efficency_temp['t'].isin(input_efficiency['OSEMOSYS'])]
    df_efficency_temp['Scenario'] = scenario
    df_efficency_temp = df_efficency_temp.reset_index(drop=True)
    df_efficency_temp['VISUALIZATION'] = df_efficency_temp['t'].map(input_efficiency.set_index('OSEMOSYS')['VISUALIZATION'].T.to_dict())
    df_efficiency = df_efficiency.append(df_efficency_temp, ignore_index=True, sort=False)

    ##RE capacity##
    df_re_capacity_temp = pd.read_csv(os.path.join(folder, scenario, re_capacity_variable + '.csv'))
    df_re_capacity_temp.drop(columns=['r'], inplace=True)
    df_re_capacity_temp = df_re_capacity_temp.loc[df_re_capacity_temp[re_capacity_variable] > 0]
    df_re_capacity_temp = df_re_capacity_temp.loc[df_re_capacity_temp['t'].isin(input_re_capacity['OSEMOSYS'])]
    df_re_capacity_temp['Scenario'] = scenario
    df_re_capacity_temp = df_re_capacity_temp.reset_index(drop=True)
    df_re_capacity_temp['VISUALIZATION'] = df_re_capacity_temp['t'].map(input_re_capacity.set_index('OSEMOSYS')['VISUALIZATION'].T.to_dict())
    df_re_capacity = df_re_capacity.append(df_re_capacity_temp, ignore_index=True, sort=False)

    ##Investment##
    df_investment_temp = pd.read_csv(os.path.join(folder, scenario, investment_variable + '.csv'))
    df_investment_temp.drop(columns=['r'], inplace=True)
    df_investment_temp = df_investment_temp.loc[df_investment_temp[investment_variable] > 0]
    df_investment_temp = df_investment_temp.loc[df_investment_temp['t'].isin(input_production['OSEMOSYS'])]
    df_investment_temp['Scenario'] = scenario
    df_investment_temp = df_investment_temp.reset_index(drop=True)
    df_investment_temp['VISUALIZATION'] = df_investment_temp['t'].map(input_production.set_index('OSEMOSYS')['VISUALIZATION'].T.to_dict())
    df_investment = df_investment.append(df_investment_temp, ignore_index=True, sort=False)

    ##RE Investment##
    df_re_investment_temp = pd.read_csv(os.path.join(folder, scenario, investment_variable + '.csv'))
    df_re_investment_temp.drop(columns=['r'], inplace=True)
    df_re_investment_temp = df_re_investment_temp.loc[df_re_investment_temp[investment_variable] > 0]
    df_re_investment_temp = df_re_investment_temp.loc[df_re_investment_temp['t'].isin(input_re_capacity['OSEMOSYS'])]
    df_re_investment_temp['Scenario'] = scenario
    df_re_investment_temp = df_re_investment_temp.reset_index(drop=True)
    df_re_investment_temp['VISUALIZATION'] = df_re_investment_temp['t'].map(input_re_capacity.set_index('OSEMOSYS')['VISUALIZATION'].T.to_dict())
    df_re_investment = df_re_investment.append(df_re_investment_temp, ignore_index=True, sort=False)

    ##Generation cost##
    df_cost_temp = pd.read_csv(os.path.join(folder, scenario, cost_variable + '.csv'))
    df_cost_temp.drop(columns=['r'], inplace=True)
    df_cost_temp = df_cost_temp.loc[df_cost_temp[cost_variable] > 0]
    df_cost_temp['Scenario'] = scenario
    df_cost_temp = df_cost_temp.reset_index(drop=True)
    df_cost = df_cost.append(df_cost_temp, ignore_index=True, sort=False)

df_emissions = df_emissions[df_emissions['e'] == 'CO2']

years = df_tfec['y'].unique()

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    xaxis={'tickformat': 'd'},
    showlegend=True,
)

hover_template = '<b>Value</b>: %{y:.2f}' + '<br><b>Year</b>: %{x}'

units_dict = {'PJ': 1, 'Mtoe': 0.0238845897, 'MMboe': 0.163456, 'TWh': 0.277777778, None: 1}

##### Helper functions #####
def tfec_re_share(scenario, year_slider, layout_tfec):
    dff = df_tfec_re.loc[(df_tfec_re['Scenario'] == scenario) & ((df_tfec_re['y'] >= year_slider[0]) & (df_tfec_re['y'] <= year_slider[1]))]
    dff = dff.groupby(['y', 'RE']).agg({tfec_re_variable: 'sum'})
    dff = dff.reset_index()
    dff['Total'] = dff['y'].map(dff.groupby(['y']).agg({tfec_re_variable: 'sum'})[tfec_re_variable].T.to_dict())
    dff['Share'] = dff[tfec_re_variable] / dff['Total']
    data = [
        dict(
            type="bar",
            x=dff.loc[dff['RE'] == RE]['y'],
            y=dff.loc[dff['RE'] == RE]['Share'],
            name=RE,
            hovertemplate=hover_template,
        )
        for RE in input_tfec_re['Renewable'].unique()
    ]

    layout_tfec["barmode"] = 'stack'
    layout_tfec["title"] = "Share of Renewables in TFEC"

    return data, layout_tfec, dff

def get_general_graph(df, year_slider, variable, layout, title, units = None):
    dff = df.loc[(df['y'] >= year_slider[0]) & (df['y'] <= year_slider[1])]
    dff = dff.groupby(['y', 'Scenario']).agg({variable: 'sum'})
    dff = dff.reset_index()
    dff.loc[:, variable] *= units_dict[units]

    data = [
        dict(
            type="scatter",
            mode='lines',
            x=dff.loc[dff['Scenario'] == scenario]['y'],
            y=dff.loc[dff['Scenario'] == scenario][variable],
            name=scenario,
            hovertemplate=hover_template
        )
        for scenario in scenarios
    ]

    layout["title"] = title

    return data, layout, dff

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(
    [   dbc.Nav(
            children=[
                dbc.DropdownMenu(
                    nav=True,
                    in_navbar=True,
                    label="About",
                    right=True,
                    children=[
                        dbc.DropdownMenuItem("Model and Results:", header = True, style = {'fontSize': 18}),
                        dbc.DropdownMenuItem("Copyright CCBY 4.0 Francesco Gardumi",
                                             href='https://creativecommons.org/licenses/by/4.0/',
                                             style = {'fontSize': 14}),
                        dbc.DropdownMenuItem("Interface:", header = True, style = {'fontSize': 18}),
                        dbc.DropdownMenuItem('MIT License Copyright 2019 Camilo Ramirez',
                                             href='https://choosealicense.com/licenses/mit/',
                                             style = {'fontSize': 14})
                    ],
                ),
                dbc.NavItem(dbc.NavLink("Github", href="https://github.com/KTH-dESA/unescap")),
            ],
            horizontal = 'end',
        ),
        html.Div(
            [
                html.Div(
                    [
                        # html.Img(
                        #     src="https://intra.kth.se/polopoly_fs/1.858858!/image/KTH_Logotyp_RGB_2013.png",
                        #     id="kth-image",
                        #     style={
                        #         "height": "60px",
                        #         "width": "auto",
                        #         "margin-bottom": "25px",
                        #     },
                        # )
                    ],
                    className="one-third column",
                ),

                html.Div(
                    [
                        html.H3(
                            'Indonesia Energy Model',
                            style={"margin-bottom": "0px"},
                        ),
                        html.H5(
                            "OSeMOSYS application",
                            style={"margin-top": "0px"},
                        ),
                    ],
                    className="one-half column",
                    id="title",
                ),

                html.Div(
                    [
                        # html.Img(
                        #     src="https://cdn.britannica.com/48/1648-004-644EBE62/Flag-Indonesia.jpg",
                        #     id="singapore-flag",
                        #     style={
                        #         "height": "60px",
                        #         "width": "auto",
                        #         "margin-bottom": "25px",
                        #         'float': 'right',
                        #     },
                        # )
                    ],
                    className="one-third column",
                ),

            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        dbc.Button(
                            "Settings",
                            id="settings-button",
                            # className="mb-3",
                            # color="primary",
                        ),
                    ],
                    className="container",
                    style={'margin-bottom': '25px', 'margin-right': '25px'}
                ),
                html.Div(
                    [
                        dbc.Button("Reference Energy System", id="open-res", style={'float': 'right'}),
                    ],
                    className="container",
                    style={'margin-bottom': '25px', 'margin-right': '25px'}
                ),

                dbc.Modal(
                    [
                        dbc.ModalHeader("Reference Energy System"),
                        dbc.ModalBody([
                            html.P("Simplified graphical representation"),
                            html.Img(
                                src="/assets/Indonesia-RES.svg",
                                id="singapore-res",
                            )]
                        ),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close-res", className="ml-auto")
                        ),
                    ],
                    id="modal-res",
                    size="xl",
                ),

                html.Div(
                    [
                        dbc.Button("Scenario Descriptions", id="open-scenarios"),
                    ],
                    className="container",
                    style={'margin-bottom': '25px'}
                ),

                dbc.Modal(
                    [
                        dbc.ModalHeader("Reference Energy System"),
                        dbc.ModalBody(
                            [
                                html.H6("Business as usual (BAU):"),
                                html.P(descriptions['bau_scenario']),
                                html.H6("Current Policies:"),
                                html.P(descriptions['current_policies_scenario']),
                                html.H6("SDG7:"),
                                html.P(descriptions['sdg7_scenario'])
                            ]
                        ),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close-scenarios", className="ml-auto")
                        ),
                    ],
                    id="modal-scenarios",
                    size="xl",
                ),
            ],
            className="row flex-display",
            style={'margin': 'auto', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}
        ),

        dbc.Collapse(
            dbc.Card(
                [
                    dbc.CardHeader("Units settings"),
                    dbc.CardBody(
                        [
                            html.Div(
                                [
                                    html.P(
                                        [
                                            'Select energy ',
                                            html.Span(
                                                "units", id="units-tooltip-target"
                                            ),
                                        ],
                                        className="control_label",
                                    ),
                                    dbc.Tooltip(
                                        [
                                            html.P('PJ: Peta Joule', style={'font-size': '12px'}),
                                            html.P('Mtoe: Mega tonne oil equivalent', style={'font-size': '12px'}),
                                            html.P('MMboe: Million barrels of oil equivalent', style={'font-size': '12px'}),
                                        ],
                                        style={'text-align': 'left', 'max-width': '500px'},
                                        target="units-tooltip-target",
                                    ),
                                    dcc.Dropdown(
                                        id='energy_units',
                                        options=[
                                            {'label': 'PJ', 'value': 'PJ'},
                                            {'label': 'Mtoe', 'value': 'Mtoe'},
                                            {'label': 'MMboe', 'value': 'MMboe'},
                                        ],
                                        value='Mtoe',
                                        clearable=False,
                                    ),
                                    html.P(
                                        [
                                            'Select electricity ',
                                            html.Span(
                                                    "units", id="el-units-tooltip-target"
                                            ),
                                        ],
                                        className="control_label",
                                    ),
                                    dbc.Tooltip(
                                        [
                                            html.P('PJ: Peta Joule', style={'font-size': '12px'}),
                                            html.P('TWh: Terawatts hour', style={'font-size': '12px'}),
                                        ],
                                        style={'text-align': 'left', 'max-width': '500px'},
                                        target="el-units-tooltip-target",
                                    ),
                                    dcc.Dropdown(
                                        id='electricity_units',
                                        options=[
                                            {'label': 'PJ', 'value': 'PJ'},
                                            {'label': 'TWh', 'value': 'TWh'},
                                        ],
                                        value='TWh',
                                        clearable=False,
                                    ),
                                ],
                                className="container",
                            ),
                            # html.Div(
                            #     [
                            #         dcc.Graph(
                            #             id='projection_graph',
                            #         ),
                            #     ]
                            # )
                        ],
                        className="row flex-display",
                    )
                ]
            ),
            id="settings",
            className="container"
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.P('Total Final Energy Consumption', style={'text-align': 'center', 'font-size': '12px'}),
                        daq.BooleanSwitch(id='tfec-switch', on=True)
                    ],
                    id='tfec-mini',
                    className="mini_container",
                ),
                html.Div(
                    [
                        html.P('Electricity supply and demand', style={'text-align': 'center', 'font-size': '12px'}),
                        daq.BooleanSwitch(id='el-switch', on=False)
                    ],
                    id='el-mini',
                    className="mini_container",
                ),
                html.Div(
                    [
                        html.P('SDG7.1.1 - Access to electricity', style={'text-align': 'center', 'font-size': '12px'}),
                        daq.BooleanSwitch(id='el-access-switch', on=False)
                    ],
                    id='el-access-mini',
                    className="mini_container",
                ),
                html.Div(
                    [
                        html.P('SDG7.1.2 - Access to clean cooking fuel', style={'text-align': 'center', 'font-size': '12px'}),
                        daq.BooleanSwitch(id='clean-cooking-switch', on=False)
                    ],
                    id='cooking-mini',
                    className="mini_container",
                ),
                html.Div(
                    [
                        html.P('SDG7.2 - Renewable energy', style={'text-align': 'center', 'font-size': '12px'}),
                        daq.BooleanSwitch(id='re-switch', on=False)
                    ],
                    id='re-mini',
                    className="mini_container",
                ),
                html.Div(
                    [
                        html.P('SDG7.3 - Energy efficiency', style={'text-align': 'center', 'font-size': '12px'}),
                        daq.BooleanSwitch(id='eff-switch', on=False)
                    ],
                    id='eff-mini',
                    className="mini_container",
                ),
            ],
            className="row flex-display",
            # style={'margin': 'auto', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.H6('Total Final Energy Consumption (TFEC)'),
                        html.Div(
                            [
                                html.P(
                                    'Select the visualization:',
                                    className="control_label",
                                ),
                                dcc.Dropdown(
                                    id='tfec_visualization_drop',
                                    options=[
                                        {'label': 'Total Final Energy Consumption', 'value': 'tfect_plot'},
                                        {'label': 'RE share in TFEC', 'value': 'tfec_re'},
                                        {'label': 'CO2 emissions in TFEC', 'value': 'tfec_co2'},
                                    ],
                                    value='tfect_plot',
                                    clearable=False,
                                ),

                                html.P(
                                    'Select the scenario:',
                                    className="control_label",
                                ),
                                dcc.Dropdown(
                                    id='tfec_scenario',
                                    value='All',
                                    clearable=False
                                ),
                                html.P("Filter by:", className="control_label"),
                                dcc.Dropdown(
                                    id='tfec_type_drop',
                                    options=[{'label': 'Select...', 'value': 'Select'}],
                                    value='Select',
                                    clearable=False
                                ),
                                html.Div(
                                    [
                                        html.P("Select sector:", className="control_label"),
                                        dcc.Dropdown(
                                            id='tfec_sector',
                                            value='All',
                                            clearable=False,
                                        ),
                                    ],
                                    id='tfec_sector_div',
                                ),

                                html.P(
                                    'Select the range of years to visualize:',
                                    className="control_label",
                                ),
                                dcc.RangeSlider(
                                    id="year_slider",
                                    min=years.min(),
                                    max=2030,
                                    value=[years.min(), 2030],
                                    marks={y: y for y in range(int(years.min()), 2031, 2)},
                                    className="dcc_control",
                                ),
                            ],
                            id='tfec-controls'
                        ),

                        html.Div(
                            html.P(descriptions['tfec']),
                            id='tfec-description',
                            style={'display': 'none'}
                        ),
                        html.Div(
                            [
                                html.Button(
                                    'Toggle description',
                                    id='toggle-tfec',
                                    className='toggle-button'
                                ),
                                html.A(
                                    'Download Data',
                                    id='download-link-tfec',
                                    download="rawdata.csv",
                                    href="",
                                    target="_blank",
                                    className='download-link'
                                ),
                            ],
                            style={'height': '30px'},
                        ),
                    ],
                    className="pretty_container five columns",
                    id="scenario-options",
                ),

                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6("NPV of total system cost", style={'text-align': 'center'}),
                                     html.P(style={'text-align': 'center'}, id="npvText")],
                                    id="npv",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6("Savings in subsidies", style={'text-align': 'center'}),
                                     html.P(style={'text-align': 'center'}, id="savingsText")],
                                    id="savings",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id='tfec_graph',
                                ),
                            ],
                            id="tfecGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    className="seven columns",
                ),
            ],
            className="row flex-display",
            id='tfec-div',
        ),

        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id='supply_graph',
                        ),
                    ],
                    id="supplyGraphContainer",
                    className="pretty_container seven columns",
                ),

                html.Div(
                    [
                        html.H6('Electricity supply and demand'),
                        html.Div(
                            [
                                html.P(
                                    'Select the visualization:',
                                    className="control_label",
                                ),
                                dcc.Dropdown(
                                    id='electricity_visualization_drop',
                                    options=[
                                        {'label': 'Electricity demand', 'value': 'el_demand'},
                                        {'label': 'Electricity supply', 'value': 'el_prod'},
                                        {'label': 'CO2 emissions', 'value': 'el_co2'},
                                        {'label': 'Annual investment required', 'value': 'el_inv'},
                                        {'label': 'Annual discounted cost', 'value': 'el_cost'},
                                    ],
                                    value='el_demand',
                                    clearable = False,
                                ),

                                html.P(
                                    'Select the scenario:',
                                    className="control_label",
                                ),
                                dcc.Dropdown(
                                    id='electricity_scenario',
                                    options=[{'label': 'All', 'value': 'All'}]+[{'label': i, 'value': i} for i in scenarios],
                                    value='All',
                                    clearable=False
                                ),
                                html.P("Filter by:", className="control_label"),
                                dcc.Dropdown(
                                    id='electricity_type_drop',
                                    options=[{'label': 'Select...', 'value': 'Select'}],
                                    value='Select',
                                    clearable=False
                                ),
                                html.Div(
                                    [
                                        html.P("Select sector:", className="control_label"),
                                        dcc.Dropdown(
                                            id='electricity_sector',
                                            value='All',
                                            clearable=False,
                                        ),
                                    ],
                                    id='electricity_sector_div',
                                ),

                                html.P(
                                    'Select the range of years to visualize:',
                                    className="control_label",
                                ),
                                dcc.RangeSlider(
                                    id="year_slider_supply",
                                    min=years.min(),
                                    max=2030,
                                    value=[years.min(), 2030],
                                    marks={y: y for y in range(int(years.min()), 2031, 2)},
                                    className="dcc_control",
                                ),
                            ],
                            id='elec-controls',
                        ),
                        html.Div(
                            html.P(descriptions['electricity']),
                            id='elec-description',
                            style={'display': 'none'}
                        ),
                        html.Div(
                            [
                                html.Button('Toggle description',
                                            id='toggle-elec',
                                            className='toggle-button'
                                            ),
                                html.A(
                                    'Download Data',
                                    id='download-link-el',
                                    download="rawdata.csv",
                                    href="",
                                    target="_blank",
                                    className='download-link'
                                ),
                            ],
                            style={'height': '30px'},
                        )
                    ],
                    className="pretty_container five columns",
                    id="scenario-options-supply",
                ),
            ],
            className="row flex-display",
            id='el-div'
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H6('SDG7.1.1 - Access to electricity'),
                        html.Div(
                            html.P(descriptions['sdg7.1.1']),
                            id='sdg7.1.1-description',
                        ),
                        html.A(
                            'Download Data',
                            id='download-link-el-access',
                            download="rawdata.csv",
                            href="",
                            target="_blank",
                            className='download-link'
                        ),
                    ],
                    className="pretty_container five columns",
                ),
                html.Div(
                    [
                        # html.H6('SDG7.1.1 - Access to electricity'),
                        dcc.Graph(
                            id='el_access_graph',
                        ),
                        html.P(
                            'Select the range of years to visualize:',
                            className="control_label",
                        ),
                        dcc.RangeSlider(
                            id="year_slider_el_access",
                            min=years.min(),
                            max=2030,
                            value=[years.min(), 2030],
                            marks={y: y for y in range(years.min(), 2031, 2)},
                            className="dcc_control",
                        ),
                        html.Br()
                    ],
                    className="pretty_container seven columns",
                ),
            ],
            id="el-access-div",
            className="row flex-display",
        ),

        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id='cooking_graph',
                        ),
                        html.P(
                            'Select the range of years to visualize:',
                            className="control_label",
                        ),
                        dcc.RangeSlider(
                            id="year_slider_cooking",
                            min=years.min(),
                            max=2030,
                            value=[years.min(), 2030],
                            marks={y: y for y in range(years.min(), 2031, 2)},
                            className="dcc_control",
                        ),
                        html.Br()
                    ],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [
                        html.H6('SDG7.1.2 - Access to clean cooking fuel'),
                        html.Div(
                            html.P(descriptions['sdg7.1.2']),
                            id='sdg7.1.2-description',
                        ),
                        html.A(
                            'Download Data',
                            id='download-link-cooking',
                            download="rawdata.csv",
                            href="",
                            target="_blank",
                            className='download-link'
                        ),
                    ],
                    className="pretty_container five columns",
                ),
            ],
            id="cooking-div",
            className="row flex-display",
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.H6('SDG7.2 - Renewable Energy'),
                        html.Div(
                            html.P(descriptions['sdg7.2']),
                            id='sdg7.2-description',
                        ),
                        html.A(
                            'Download Data',
                            id='download-link-re',
                            download="rawdata.csv",
                            href="",
                            target="_blank",
                            className='download-link'
                        ),
                    ],
                    className="pretty_container five columns",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.P(
                                                    "Select the visualization:",
                                                    className="control_label",
                                                ),
                                                dcc.Dropdown(
                                                    id='re_drop',
                                                    options=[
                                                        {'label': 'RE accumulated capacity', 'value': 're_capacity'},
                                                        {'label': 'RE share in TFEC', 'value': 're_tfec'},
                                                        {'label': 'RE share in energy sector', 'value': 're_energy_sector'},
                                                        {'label': 'Annual RE investment', 'value': 're_investment'},
                                                    ],
                                                    value='re_capacity',
                                                    style={'width': '90%'},
                                                ),
                                            ],
                                            className="container"
                                        ),

                                        html.Div(
                                            [
                                                html.P(
                                                    'Select the range of years to visualize:',
                                                    className="control_label",
                                                ),
                                                dcc.RangeSlider(
                                                    id="year_slider_re",
                                                    min=years.min(),
                                                    max=2030,
                                                    value=[years.min(), 2030],
                                                    marks={y: y for y in range(int(years.min()), 2031, 2)},
                                                ),
                                            ],
                                            className="container"
                                        ),
                                    ],
                                    className="row container-display",
                                    #style={'margin': 'auto', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}
                                ),
                            ],
                            className="pretty_container",
                            id="scenario-options-re",
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id='re_graph',
                                ),
                            ],
                            className="pretty_container",
                        ),
                    ],
                    className="seven columns",
                ),
            ],
            className="row flex-display",
            id="re-div",
        ),

        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id='efficiency_graph',
                        ),
                        html.P(
                            'Select the range of years to visualize:',
                            className="control_label",
                        ),
                        dcc.RangeSlider(
                            id="year_slider_efficiency",
                            min=years.min(),
                            max=2030,
                            value=[years.min(), 2030],
                            marks={y: y for y in range(years.min(), 2031, 2)},
                            className="dcc_control",
                        ),
                        html.Br()
                    ],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [
                        html.H6('SDG7.3 - Energy Efficiency'),
                        html.Div(
                            html.P(descriptions['sdg7.3']),
                            id='sdg7.3-description',
                        ),
                        html.A(
                            'Download Data',
                            id='download-link-eff',
                            download="rawdata.csv",
                            href="",
                            target="_blank",
                            className='download-link'
                        ),
                    ],
                    className="pretty_container five columns",
                ),

            ],
            id="efficiency-div",
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

##### Callbacks #####
@app.callback(
    [
        Output('tfec_scenario', 'disabled'),
        Output('tfec_scenario', 'value'),
        Output('tfec_type_drop', 'value'),
    ],
    [
        Input('tfec_visualization_drop', 'value'),
    ],
)
def update_elec_value(value):
    if value == 'tfec_co2':
        scenario = 'All'
        state = True
    elif value == 'tfec_re':
        scenario = 'BAU'
        state = False
    else:
        scenario = 'All'
        state = False
    return state, scenario, 'Select'

@app.callback(
    [
        Output('tfec_scenario', 'options'),
    ],
    [
        Input('tfec_visualization_drop', 'value'),
    ],
)
def update_elec_value(value):
    if value == 'tfec_re':
        options = [{'label': i, 'value': i} for i in scenarios],
    else:
        options = [{'label': 'All', 'value': 'All'}] + [{'label': i, 'value': i} for i in scenarios],
    return options

@app.callback(
    [
        Output('tfec_type_drop', 'options'),
        Output('npvText', 'children'),
        Output('savingsText', 'children'),
    ],
    [
        Input('tfec_scenario', 'value'),
    ],
)
def update_elec_type(scenario):
    if scenario == 'All':
        options = [
            {'label': 'Select...', 'value': 'Select', 'disabled': True},
        ]
        npv = '-'
        savings = '-'
    else:
        options = [
            {'label': 'Sector', 'value': 'Sector'},
            {'label': 'Fuel', 'value': 'Fuel'},
            {'label': 'Select...', 'value': 'Select', 'disabled': True},
        ]
        npv = '{} M$'.format(economic_parameters['npv'][scenario])
        savings = '{} M$'.format(economic_parameters['savings'][scenario])
    return options, npv, savings

@app.callback(
    Output('tfec_type_drop', 'disabled'),
    [
        Input('tfec_scenario', 'value'),
        Input('tfec_visualization_drop', 'value'),
    ],
)
def set_state(scenario, visualization):
    if (scenario == 'All') or (visualization == 'tfec_re') or (visualization == 'tfec_co2'):
        state = True
    else:
        state = False
    return state

@app.callback(
    Output('tfec_sector_div', 'style'),
    [
        Input('tfec_type_drop', 'value'),
    ],
)
def set_state(value):
    if value == 'Fuel':
        style = None
    else:
        style = {'display': 'none'}
    return style

@app.callback(
    Output('tfec_sector', 'options'),
    [
        Input('tfec_type_drop', 'value'),
        Input('tfec_scenario', 'value'),
        Input('year_slider', 'value'),
    ],
)
def set_state(value, scenario, year_slider):
    dff = df_tfec.loc[
        (df_tfec['Scenario'] == scenario) & (
                    (df_tfec['y'] >= year_slider[0]) & (df_tfec['y'] <= year_slider[1]))]
    options = ''
    if value == 'Fuel':
        options = [{'label': 'All', 'value': 'All'}] + [{'label': i, 'value': i} for i in dff['Sector'].unique()]
    return options

@app.callback(
    [
        Output('electricity_scenario', 'value'),
        Output('electricity_scenario', 'disabled'),
        Output('electricity_type_drop', 'value'),
    ],
    [
        Input('electricity_visualization_drop', 'value'),
    ],
)
def update_elec_value(value):
    if value == 'el_cost':
        state = True
    else:
        state = False
    return 'All', state, 'Select'

@app.callback(
    Output('electricity_type_drop', 'options'),
    [
        Input('electricity_visualization_drop', 'value'),
        Input('electricity_scenario', 'value'),
    ],
)
def update_elec_type(visualization, scenario):
    if scenario == 'All':
        options = [
            {'label': 'Select...', 'value': 'Select', 'disabled': True},
        ]
    else:
        if visualization == 'el_prod':
            options = [
                {'label': 'Source', 'value': 'Source'},
                {'label': 'Type', 'value': 'Type'},
                {'label': 'Select...', 'value': 'Select', 'disabled': True},
            ]
        elif visualization == 'el_demand':
            options = [
                {'label': 'Sector', 'value': 'Sector'},
                {'label': 'Use', 'value': 'Use'},
                {'label': 'Select...', 'value': 'Select', 'disabled': True},
            ]
        elif visualization == 'el_co2':
            options = [
                {'label': 'Source', 'value': 'Source'},
                {'label': 'Type', 'value': 'Type'},
                {'label': 'Select...', 'value': 'Select', 'disabled': True},
            ]
        elif (visualization == 'el_inv') or (visualization == 'el_cost'):
            options = [
                {'label': 'Select...', 'value': 'Select', 'disabled': True},
            ]
    return options

@app.callback(
    Output('electricity_type_drop', 'disabled'),
    [
        Input('electricity_scenario', 'value'),
        Input('electricity_visualization_drop', 'value'),
    ],
)
def set_state(scenario, visualization):
    if (scenario == 'All') or (visualization == 'el_inv') or (visualization == 'el_cost'):
        state = True
    else:
        state = False
    return state

@app.callback(
    Output('electricity_sector_div', 'style'),
    [
        Input('electricity_type_drop', 'value'),
    ],
)
def set_state(value):
    if value == 'Use':
        style = None
    else:
        style = {'display': 'none'}
    return style

@app.callback(
    Output('electricity_sector', 'options'),
    [
        Input('electricity_type_drop', 'value'),
        Input('electricity_scenario', 'value'),
        Input('year_slider_supply', 'value'),
    ],
)
def set_state(value, scenario, year_slider):
    dff = df_elec_demand.loc[
        (df_elec_demand['Scenario'] == scenario) & (
                    (df_elec_demand['y'] >= year_slider[0]) & (df_elec_demand['y'] <= year_slider[1]))]
    options = ''
    if value == 'Use':
        options = [{'label': 'All', 'value': 'All'}] + [{'label': i, 'value': i} for i in dff['Sector'].unique()]
    return options

@app.callback(
    [
        Output('tfec_graph', 'figure'),
        Output('download-link-tfec', 'href')
    ],
    [
        Input('tfec_scenario', 'value'),
        Input('year_slider', 'value'),
        Input('tfec_visualization_drop', 'value'),
        Input('tfec_type_drop', 'value'),
        Input('energy_units', 'value'),
        Input('tfec_sector', 'value'),
    ],
)
def update_tfec(scenario, year_slider, visualization, type, units, sector):
    layout_tfec = copy.deepcopy(layout)
    data = ''
    if visualization == 'tfect_plot':
        if scenario == 'All':
            data, layout_tfec, dff = get_general_graph(df_tfec, year_slider, tfec_variable, layout,
                                                  "Total Final Energy Consumption ({})".format(units), units)
        elif scenario != 'Select':
            dff = df_tfec.loc[
                (df_tfec['Scenario'] == scenario) & ((df_tfec['y'] >= year_slider[0]) & (df_tfec['y'] <= year_slider[1]))]
            dff.loc[:, tfec_variable] *= units_dict[units]
            if (type == 'Fuel') & (sector != 'All'):
                data = [
                    dict(
                        type="bar",
                        x=dff.loc[(dff['Sector'] == sector) & (dff[type] == tech)].groupby('y').sum().index,
                        y=dff.loc[(dff['Sector'] == sector) & (dff[type] == tech)].groupby('y').sum()[tfec_variable],
                        name=tech,
                        hovertemplate=hover_template,
                        marker={'line': {'width': '0.5', 'color': layout['plot_bgcolor']}},
                    )

                    for tech in input_tfec[type].unique()
                ]

                layout_tfec["title"] = "Total final energy consumption in the {} sector ({})".format(sector, units)
                layout_tfec["barmode"] = 'stack'
            elif (sector != 'Select') & (type != 'Select'):
                data = [
                    dict(
                        type="bar",
                        x=dff.loc[dff[type] == tech].groupby('y').sum().index,
                        y=dff.loc[dff[type] == tech].groupby('y').sum()[tfec_variable],
                        name=tech,
                        hovertemplate=hover_template,
                        marker={'line': {'width': '0.5', 'color': layout['plot_bgcolor']}},
                    )

                    for tech in input_tfec[type].unique()
                ]

                layout_tfec["title"] = "Total final energy consumption ({})".format(units)
                layout_tfec["barmode"] = 'stack'

    elif visualization == 'tfec_co2':
        if scenario == 'All':
            data, layout_tfec, dff = get_general_graph(df_emissions, year_slider, emissions_variable, layout,
                                                    "Total CO2 Emissions (Mton)")

    elif visualization == 'tfec_re':
        data, layout_tfec, dff = tfec_re_share(scenario, year_slider, layout_tfec)

    figure = dict(data=data, layout=layout_tfec)

    csv_string = dff.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(csv_string)

    return figure, csv_string

@app.callback(
    [
        Output('supply_graph', 'figure'),
        Output('download-link-el', 'href'),
    ],
    [
        Input('electricity_scenario', 'value'),
        Input('year_slider_supply', 'value'),
        Input('electricity_visualization_drop', 'value'),
        Input('electricity_type_drop', 'value'),
        Input('electricity_units', 'value'),
        Input('electricity_sector', 'value'),
    ],
)
def update_supply(scenario, year_slider, visualization, type, units, sector):
    layout_supply = copy.deepcopy(layout)
    data = ''
    if visualization == 'el_demand':
        if scenario == 'All':
            data, layout_supply, dff = get_general_graph(df_elec_demand, year_slider, elec_demand_variable, layout,
                                                  "Electricity demand ({})".format(units), units)
        elif scenario != 'Select':
            dff = df_elec_demand.loc[
                (df_elec_demand['Scenario'] == scenario) & ((df_elec_demand['y'] >= year_slider[0]) & (df_elec_demand['y'] <= year_slider[1]))]
            dff.loc[:, elec_demand_variable] *= units_dict[units]
            if (type == 'Use') & (sector != 'All'):
                data = [
                    dict(
                        type="bar",
                        x=dff.loc[(dff['Sector'] == sector) & (dff[type] == tech)].groupby('y').sum().index,
                        y=dff.loc[(dff['Sector'] == sector) & (dff[type] == tech)].groupby('y').sum()[elec_demand_variable],
                        name=tech,
                        hovertemplate=hover_template,
                        marker={'line': {'width': '0.5', 'color': layout['plot_bgcolor']}},
                    )

                    for tech in input_elec_demand[type].unique()
                ]

                layout_supply["title"] = "Electricity demand in the {} sector ({})".format(sector, units)
                layout_supply["barmode"] = 'stack'
            elif (sector != 'Select') & (type != 'Select'):
                data = [
                    dict(
                        type="bar",
                        x=dff.loc[dff[type] == tech].groupby('y').sum().index,
                        y=dff.loc[dff[type] == tech].groupby('y').sum()[elec_demand_variable],
                        name=tech,
                        hovertemplate=hover_template,
                        marker={'line': {'width': '0.5', 'color': layout['plot_bgcolor']}},
                    )

                    for tech in input_elec_demand[type].unique()
                ]

                layout_supply["title"] = "Electricity demand ({})".format(units)
                layout_supply["barmode"] = 'stack'

    elif visualization == 'el_prod':
        if scenario == 'All':
            data, layout_supply, dff = get_general_graph(df_supply, year_slider, supply_variable, layout,
                                                  "Electricity supply ({})".format(units), units)
        elif (sector != 'Select') & (type != 'Select'):
            dff = df_supply.loc[
                (df_supply['Scenario'] == scenario) & ((df_supply['y'] >= year_slider[0]) & (df_supply['y'] <= year_slider[1]))]
            dff.loc[:, supply_variable] *= units_dict[units]

            data = [
                dict(
                    type="bar",
                    x=dff.loc[dff[type] == tech].groupby('y').sum().index,
                    y=dff.loc[dff[type] == tech].groupby('y').sum()[supply_variable],
                    name=tech,
                    hovertemplate=hover_template,
                    marker={'line': {'width': '0.5', 'color': layout['plot_bgcolor']}},
                )
                for tech in input_production[type].unique()
            ]

            layout_supply["title"] = "Electricity supply ({})".format(units)
            layout_supply["barmode"] = 'stack'

    elif visualization == 'el_co2':
        dff = df_emissions.loc[df_emissions['t'].isin(input_production['OSEMOSYS'])]
        if scenario == 'All':
            data, layout_supply, dff = get_general_graph(dff, year_slider, emissions_variable, layout,
                                                  "Total CO2 Emissions (Mton)")

        elif (sector != 'Select') & (type != 'Select'):
            dff = dff.loc[
                (dff['Scenario'] == scenario) & (
                            (dff['y'] >= year_slider[0]) & (dff['y'] <= year_slider[1]))]

            data = [
                dict(
                    type="bar",
                    x=dff.loc[dff[type] == tech].groupby('y').sum().index,
                    y=dff.loc[dff[type] == tech].groupby('y').sum()[emissions_variable],
                    name=tech,
                    hovertemplate=hover_template,
                    marker={'line': {'width': '0.5', 'color': layout['plot_bgcolor']}},
                )
                for tech in input_production[type].unique()
            ]

            layout_supply["title"] = "Total CO2 emissions (MTon)"
            layout_supply["barmode"] = 'stack'

    elif visualization == 'el_inv':
        if scenario == 'All':
            data, layout_supply, dff = get_general_graph(df_investment, year_slider, investment_variable, layout,
                                                  "Capital Investment (M$)")
        else:
            dff = df_investment.loc[
                (df_investment['Scenario'] == scenario) & ((df_investment['y'] >= year_slider[0]) & (df_investment['y'] <= year_slider[1]))]

            data = [
                dict(
                    type="bar",
                    x=dff.loc[dff['VISUALIZATION'] == tech].groupby('y').sum().index,
                    y=dff.loc[dff['VISUALIZATION'] == tech].groupby('y').sum()[investment_variable],
                    name=tech,
                    hovertemplate=hover_template,
                    marker={'line': {'width': '0.5', 'color': layout['plot_bgcolor']}},
                )

                for tech in input_production['VISUALIZATION'].unique()
            ]

            layout_supply["title"] = "Capital Investment (M$)"
            layout_supply["barmode"] = 'stack'

    elif visualization == 'el_cost':
        dff = df_cost.loc[(df_cost['y'] >= year_slider[0]) & (df_cost['y'] <= year_slider[1])]
        dff = dff.groupby(['y', 'Scenario']).agg({cost_variable: 'sum'})
        dff = dff.reset_index()

        data = [
            dict(
                type="scatter",
                mode='lines',
                x=dff.loc[dff['Scenario'] == scenario].groupby('y').sum().index,
                y=dff.loc[dff['Scenario'] == scenario].groupby('y').sum()[cost_variable],
                name=scenario,
                hovertemplate=hover_template
            )
            for scenario in scenarios
        ]

        layout_supply["title"] = "Total annual discounted cost (M$)"

    figure = dict(data=data, layout=layout_supply)

    csv_string = dff.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(csv_string)

    return figure, csv_string

@app.callback(
    [
        Output('el_access_graph', 'figure'),
        Output('download-link-el-access', 'href')
    ],
    [
        Input('year_slider_el_access', 'value'),
        Input('electricity_units', 'value'),
    ],
)
def el_access_graph(year_slider, units):
    layout_access = copy.deepcopy(layout)

    dff = df_elec_access.loc[(df_elec_access['Scenario'] == 'SDG7') & ((df_elec_access['y'] >= year_slider[0]) & (df_elec_access['y'] <= year_slider[1]))]
    dff.loc[:, elec_access_variable] *= units_dict[units]

    data = [
        dict(
            type="bar",
            x=dff.loc[dff['VISUALIZATION'] == tech].groupby('y').sum().index,
            y=dff.loc[dff['VISUALIZATION'] == tech].groupby('y').sum()[elec_access_variable],
            name=tech,
            hovertemplate=hover_template,
            marker={'line': {'width': '0.5', 'color': layout['plot_bgcolor']}},
        )

        for tech in input_elec_access['VISUALIZATION'].unique()
    ]

    layout_access["title"] = "Additional electricity needed for universal access ({})".format(units)
    layout_access["barmode"] = 'stack'

    figure = dict(data=data, layout=layout_access)
    csv_string = dff.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(csv_string)
    return figure, csv_string

@app.callback(
    [
        Output('cooking_graph', 'figure'),
        Output('download-link-cooking', 'href')
    ],
    [
        Input('year_slider_cooking', 'value'),
        Input('energy_units', 'value'),
    ],
)
def cooking_graph(year_slider, units):
    layout_cooking = copy.deepcopy(layout)

    dff = df_cooking.loc[(df_cooking['Scenario'] == 'SDG7') & ((df_cooking['y'] >= year_slider[0]) & (df_cooking['y'] <= year_slider[1]))]
    dff.loc[:, cooking_variable] *= units_dict[units]

    data = [
        dict(
            type="bar",
            x=dff.loc[dff['VISUALIZATION'] == tech].groupby('y').sum().index,
            y=dff.loc[dff['VISUALIZATION'] == tech].groupby('y').sum()[cooking_variable],
            name=tech,
            hovertemplate=hover_template,
            marker={'line': {'width': '0.5', 'color': layout['plot_bgcolor']}},
        )

        for tech in input_cooking['VISUALIZATION'].unique()
    ]

    layout_cooking["title"] = "Additional energy needed for universal access<br>to clean cooking fuels ({})".format(units)
    layout_cooking["barmode"] = 'stack'

    figure = dict(data=data, layout=layout_cooking)
    csv_string = dff.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(csv_string)
    return figure, csv_string

@app.callback(
    [
        Output('efficiency_graph', 'figure'),
        Output('download-link-eff', 'href')
    ],
    [
        Input('year_slider_efficiency', 'value'),
        Input('energy_units', 'value'),
    ],
)
def efficiency_graph(year_slider, units):
    layout_efficiency = copy.deepcopy(layout)

    dff = df_efficiency.loc[
        (df_efficiency['Scenario'] == 'SDG7') & ((df_efficiency['y'] >= year_slider[0]) & (df_efficiency['y'] <= year_slider[1]))]
    dff.loc[:, efficiency_variable] *= units_dict[units]

    data = [
        dict(
            type="bar",
            x=dff.loc[dff['VISUALIZATION'] == tech].groupby('y').sum().index,
            y=dff.loc[dff['VISUALIZATION'] == tech].groupby('y').sum()[efficiency_variable],
            name=tech,
            hovertemplate=hover_template,
            marker={'line': {'width': '0.5', 'color': layout['plot_bgcolor']}},
        )

        for tech in input_efficiency['VISUALIZATION'].unique()
    ]

    layout_efficiency["title"] = "Reduction in energy consumption needed<br>to achieve energy efficiency target ({})".format(units)
    layout_efficiency["barmode"] = 'stack'

    figure = dict(data=data, layout=layout_efficiency)
    csv_string = dff.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(csv_string)
    return figure, csv_string

@app.callback(
    [
        Output('re_graph', 'figure'),
        Output('download-link-re', 'href')
    ],
    [
        Input('year_slider_re', 'value'),
        Input('re_drop', 'value'),
    ],
)
def re_graph(year_slider, visualization):
    layout_re= copy.deepcopy(layout)

    if visualization == 're_capacity':
        dff = df_re_capacity.loc[
            (df_re_capacity['Scenario'] == 'SDG7') & ((df_re_capacity['y'] >= year_slider[0]) & (df_re_capacity['y'] <= year_slider[1]))]

        data = [
            dict(
                type="bar",
                x=dff.loc[dff['VISUALIZATION'] == tech].groupby('y').sum().index,
                y=dff.loc[dff['VISUALIZATION'] == tech].groupby('y').sum()[re_capacity_variable],
                name=tech,
                hovertemplate=hover_template,
                marker={'line': {'width': '0.5', 'color': layout['plot_bgcolor']}},
            )

            for tech in input_re_capacity['VISUALIZATION'].unique()
        ]

        layout_re["title"] = "Optimal capacity to achieve RE target (GW)"
        layout_re["barmode"] = 'stack'

    elif visualization == 're_tfec':
        data, layout_re, dff = tfec_re_share('SDG7', year_slider, layout_re)

    elif visualization == 're_energy_sector':
        dff = df_supply.loc[
            (df_supply['Scenario'] == 'SDG7') & ((df_supply['y'] >= year_slider[0]) & (df_supply['y'] <= year_slider[1]))]
        dff = dff.groupby(['y', 'Type']).agg({supply_variable: 'sum'})
        dff = dff.reset_index()
        dff['Total'] = dff['y'].map(dff.groupby(['y']).agg({supply_variable: 'sum'})[supply_variable].T.to_dict())
        dff['Share'] = dff[supply_variable] / dff['Total']
        data = [
            dict(
                type="bar",
                x=dff.loc[dff['Type'] == type]['y'],
                y=dff.loc[dff['Type'] == type]['Share'],
                name=type,
                hovertemplate=hover_template,
                marker={'line': {'width': '0.5', 'color': layout['plot_bgcolor']}},
            )
            for type in input_production['Type'].unique()
        ]

        layout_re["title"] = "Share of renewables in electricity production"
        layout_re["barmode"] = 'stack'

    elif visualization == 're_investment':
        dff = df_re_investment.loc[
            (df_re_investment['Scenario'] == 'SDG7') & ((df_re_investment['y'] >= year_slider[0]) & (df_re_investment['y'] <= year_slider[1]))]

        data = [
            dict(
                type="bar",
                x=dff.loc[dff['VISUALIZATION'] == tech].groupby('y').sum().index,
                y=dff.loc[dff['VISUALIZATION'] == tech].groupby('y').sum()[investment_variable],
                name=tech,
                hovertemplate=hover_template,
                marker={'line': {'width': '0.5', 'color': layout['plot_bgcolor']}},
            )

            for tech in input_re_capacity['VISUALIZATION'].unique()
        ]

        layout_re["title"] = "Capital Investment to achieve RE target (M$)"
        layout_re["barmode"] = 'stack'

    figure = dict(data=data, layout=layout_re)
    csv_string = dff.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(csv_string)
    return figure, csv_string

@app.callback(
    Output('tfec-div', 'style'),
    [
        Input('tfec-switch', 'on'),
    ],
)
def set_state(on):
    if on:
        return None
    else:
        return {'display': 'none'}

@app.callback(
    Output('el-div', 'style'),
    [
        Input('el-switch', 'on'),
    ],
)
def set_state(on):
    if on:
        return None
    else:
        return {'display': 'none'}

@app.callback(
    Output('el-access-div', 'style'),
    [
        Input('el-access-switch', 'on'),
    ],
)
def set_state(on):
    if on:
        return None
    else:
        return {'display': 'none'}

@app.callback(
    Output('cooking-div', 'style'),
    [
        Input('clean-cooking-switch', 'on'),
    ],
)
def set_state(on):
    if on:
        return None
    else:
        return {'display': 'none'}

@app.callback(
    Output('efficiency-div', 'style'),
    [
        Input('eff-switch', 'on'),
    ],
)
def set_state(on):
    if on:
        return None
    else:
        return {'display': 'none'}

@app.callback(
    Output('re-div', 'style'),
    [
        Input('re-switch', 'on'),
    ],
)
def set_state(on):
    if on:
        return None
    else:
        return {'display': 'none'}

@app.callback(
    Output("modal-res", "is_open"),
    [Input("open-res", "n_clicks"), Input("close-res", "n_clicks")],
    [State("modal-res", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("modal-scenarios", "is_open"),
    [Input("open-scenarios", "n_clicks"), Input("close-scenarios", "n_clicks")],
    [State("modal-scenarios", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("settings", "is_open"),
    [Input("settings-button", "n_clicks")],
    [State("settings", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    [
        Output("tfec-description", "style"),
        Output("tfec-controls", "style"),
    ],
    [Input("toggle-tfec", "n_clicks")],
)
def toggle_description(n):
    try:
        if n % 2 != 0:
            return {'display': 'block'}, {'display': 'none'}
    except:
        pass
    return {'display': 'none'}, {'display': 'block'}

@app.callback(
    [
        Output("elec-description", "style"),
        Output("elec-controls", "style"),
    ],
    [Input("toggle-elec", "n_clicks")],
)
def toggle_description(n):
    try:
        if n % 2 != 0:
            return {'display': 'block'}, {'display': 'none'}
    except:
        pass
    return {'display': 'none'}, {'display': 'block'}

if __name__ == '__main__':
    app.run_server(debug=False)

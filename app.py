import plotly.express as px
from shiny import App, ui, render
from shinywidgets import output_widget, render_widget
import seaborn as sns
import matplotlib.pyplot as plt
from palmerpenguins import load_penguins

penguins_df = load_penguins()

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.sidebar(
            ui.h2("Sidebar"),
            ui.input_selectize(
                "selected_attribute",
                "Select attribute",
                ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
            ),
            ui.input_numeric(
                "plotly_bin_count",
                "Plotly Histogram Bins",
                value=20
            ),
            ui.input_slider(
                "seaborn_bin_count",
                "Seaborn Histogram Bins",
                5, 40, 17
            ),
            ui.input_checkbox_group(
                "selected_species_list",
                "Filter Species",
                ["Adelie", "Gentoo", "Chinstrap"],
                selected=["Adelie", "Gentoo", "Chinstrap"],
                inline=True
            ),
            ui.hr(),
            ui.a(
                "GitHub",
                href="https://github.com/sydsailors/cintel-02-data",
                target="_blank"
            ),
            open="open"
        ),
        ui.layout_columns(
            ui.output_data_frame("data_table"),
            ui.output_data_frame("data_grid")
        ),
        ui.layout_columns(
            output_widget("plotly_histogram"),
            ui.output_plot("seaborn_histogram"),
            ui.card(
                ui.card_header("Plotly Scatterplot: Species"),
                output_widget("plotly_scatterplot"),
                full_screen=True
            )
        )
    )
)

def server(input, output, session):
    @render.data_frame
    def data_table():
        return penguins_df

    @render.data_frame
    def data_grid():
        return penguins_df

    @render_widget
    def plotly_histogram():
        col = input.selected_attribute()
        bins = input.plotly_bin_count()
        if not bins:
            bins = 17
        fig = px.histogram(
            penguins_df,
            x=col,
            nbins=int(bins),
            color="species",
            title=f"Plotly Histogram of {col}"
        )
        return fig

    @render.plot
    def seaborn_histogram():
        col = input.selected_attribute()
        bins = input.seaborn_bin_count()
        if not bins:
            bins = 17
        fig, ax = plt.subplots()
        sns.histplot(
            data=penguins_df,
            x=col,
            bins=int(bins),
            hue="species",
            ax=ax
        )
        ax.set_title(f"Seaborn Histogram of {col}")
        return fig

    @render_widget
    def plotly_scatterplot():
        fig = px.scatter(
            penguins_df,
            x="bill_length_mm",
            y="body_mass_g",
            color="species",
            symbol="species",
            hover_data=["island"],
            labels={
                "bill_length_mm": "Bill Length (mm)",
                "body_mass_g": "Body Mass (g)"
            },
            title="Bill Length vs Body Mass by Species"
        )
        return fig

app = App(app_ui, server)

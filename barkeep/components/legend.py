import hydra
import matplotlib


with hydra.initialize(config_path="../conf", version_base=None):
    cfg = hydra.compose(config_name="config")


def plot(handles: list,
         labels: list,
         ax: matplotlib.axes.Axes,
         title=None) -> None:

    box = ax.get_position()
    ax.set_position([box.x0 * .97, box.y0, box.width, box.height])

    # legend font properties
    legend_font = matplotlib.font_manager.FontProperties(family=cfg.font.name,
                                                         style='normal',
                                                         size=cfg.font.size.s)

    ax.legend(
        handles,
        labels,
        bbox_to_anchor=(0, 0.5),
        loc="center left",
        prop=legend_font,
        title=title,
        title_fontsize=cfg.font.size.s
    )

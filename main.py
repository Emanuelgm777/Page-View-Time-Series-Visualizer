from time_series_visualizer import draw_line_plot, draw_bar_plot, draw_box_plot

if __name__ == "__main__":
    # Genera las 3 figuras y guarda archivos PNG (no abre ventanas en entorno headless)
    draw_line_plot()
    draw_bar_plot()
    draw_box_plot()
    print("Figuras generadas: line_plot.png, bar_plot.png, box_plot.png")

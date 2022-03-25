#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
import platform

from locale import gettext as _tr

from Config import Config
from Performance import Performance


# Define class
class Cpu:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/CpuTab.ui")

        # Get GUI objects
        self.grid1101 = builder.get_object('grid1101')
        self.drawingarea1101 = builder.get_object('drawingarea1101')
        self.button1101 = builder.get_object('button1101')
        self.label1101 = builder.get_object('label1101')
        self.label1102 = builder.get_object('label1102')
        self.label1103 = builder.get_object('label1103')
        self.label1104 = builder.get_object('label1104')
        self.label1105 = builder.get_object('label1105')
        self.label1106 = builder.get_object('label1106')
        self.label1107 = builder.get_object('label1107')
        self.label1108 = builder.get_object('label1108')
        self.label1109 = builder.get_object('label1109')
        self.label1110 = builder.get_object('label1110')
        self.label1111 = builder.get_object('label1111')
        self.label1112 = builder.get_object('label1112')
        self.label1113 = builder.get_object('label1113')

        # Connect GUI signals
        self.button1101.connect("clicked", self.on_button1101_clicked)
        self.drawingarea1101.connect("draw", self.on_drawingarea1101_draw)

        # Run initial function
        self.cpu_initial_func()


    # ----------------------- "customizations menu" Button -----------------------
    def on_button1101_clicked(self, widget):

        from CpuMenu import CpuMenu
        CpuMenu.popover1101p.set_relative_to(widget)
        CpuMenu.popover1101p.set_position(1)
        CpuMenu.popover1101p.popup()


    # ----------------------- Called for drawing average or per-core CPU usage as line/bar chart -----------------------
    def on_drawingarea1101_draw(self, widget, ctx):

        # Draw "average CPU usage" if preferred.
        if Config.show_cpu_usage_per_core == 0:

            # Get values from "Config and Peformance" modules and use this defined values in order to avoid multiple uses of variables from another module since CPU usage is higher for this way.
            chart_data_history = Config.chart_data_history
            chart_x_axis = list(range(0, chart_data_history))

            cpu_usage_percent_ave = Performance.cpu_usage_percent_ave

            chart_line_color = Config.chart_line_color_cpu_percent
            chart_background_color = Config.chart_background_color_all_charts

            # Chart foreground and chart fill below line colors may be set different for charts in different style (line, bar, etc.) and different places (tab pages, headerbar, etc.).
            # Set chart foreground color (chart outer frame and gridline colors) same as "chart_line_color" in multiplication with transparency factor "0.4".
            chart_foreground_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.4 * chart_line_color[3]]
            # Set chart fill below line color same as "chart_line_color" in multiplication with transparency factor "0.15".
            chart_fill_below_line_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.15 * chart_line_color[3]]

            # Get drawingarea width and height. Therefore chart width and height is updated dynamically by using these values when window size is changed by user.
            chart1101_width = Gtk.Widget.get_allocated_width(widget)
            chart1101_height = Gtk.Widget.get_allocated_height(widget)

            # Set color for chart background, draw chart background rectangle and fill the inner area.
            # Only one drawing style with multiple properties (color, line width, dash style) can be set at the same time.
            # As a result style should be set, drawing should be done and another style shpuld be set for next drawing.
            ctx.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
            ctx.rectangle(0, 0, chart1101_width, chart1101_height)
            ctx.fill()

            # Change line width, dash style (if [4, 3] is used, this means draw 4 pixels, skip 3 pixels) and color for chart gridlines.
            ctx.set_line_width(1)
            ctx.set_dash([4, 3])
            ctx.set_source_rgba(chart_foreground_color[0], chart_foreground_color[1], chart_foreground_color[2], chart_foreground_color[3])
            # Draw horizontal gridlines (range(3) means 3 gridlines will be drawn)
            for i in range(3):
                ctx.move_to(0, chart1101_height/4*(i+1))
                ctx.line_to(chart1101_width, chart1101_height/4*(i+1))
            # Draw vertical gridlines
            for i in range(4):
                ctx.move_to(chart1101_width/5*(i+1), 0)
                ctx.line_to(chart1101_width/5*(i+1), chart1101_height)
            ctx.stroke()    # "stroke" command draws line (line or closed shapes with empty inner area). "fill" command should be used for filling inner areas.

            # Change line style (solid line) for chart foreground.
            ctx.set_dash([], 0)
            # Draw chart outer rectange.
            ctx.rectangle(0, 0, chart1101_width, chart1101_height)
            ctx.stroke()

            # Change the color for drawing data line (curve).
            ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
            # Move drawing point (cairo context which is used for drawing on drawable objects) from data point to data point and connect them by a line in order to draw a curve.
            # First, move drawing point to the lower left corner of the chart and draw all data points one by one by going to the right direction.
            ctx.move_to(chart1101_width*chart_x_axis[0]/(chart_data_history-1), chart1101_height - chart1101_height*cpu_usage_percent_ave[0]/100)
            # Move drawing point to the next data points and connect them by a line.
            for i in range(len(chart_x_axis) - 1):
                # Distance to move on the horizontal axis
                delta_x_chart1101 = (chart1101_width * chart_x_axis[i+1]/(chart_data_history-1)) - (chart1101_width * chart_x_axis[i]/(chart_data_history-1))
                # Distance to move on the vertical axis
                delta_y_chart1101 = (chart1101_height*cpu_usage_percent_ave[i+1]/100) - (chart1101_height*cpu_usage_percent_ave[i]/100)
                # Move
                ctx.rel_line_to(delta_x_chart1101, -delta_y_chart1101)

            # Move drawing point 10 pixel right in order to go out of the visible drawing area for drawing a closed shape for filling the inner area.
            ctx.rel_line_to(10, 0)
            # Move drawing point "chart_height+10" down in order to stay out of the visible drawing area for drawing a closed shape for filling the inner area.
            ctx.rel_line_to(0, chart1101_height+10)
            # Move drawing point "chart1101_width+20" pixel left (by using a minus sign) in order to stay out of the visible drawing area for drawing a closed shape for filling the inner area.
            ctx.rel_line_to(-(chart1101_width+20), 0)
            # Move drawing point "chart_height+10" up in order to stay out of the visible drawing area for drawing a closed shape for filling the inner area.
            ctx.rel_line_to(0, -(chart1101_height+10))
            # Finally close the curve in order to fill the inner area which will represent a curve with a filled "below" area.
            ctx.close_path()
            # Use "stroke_preserve" in order to use the same area for filling. 
            ctx.stroke_preserve()
            # Change the color for filling operation.
            ctx.set_source_rgba(chart_fill_below_line_color[0], chart_fill_below_line_color[1], chart_fill_below_line_color[2], chart_fill_below_line_color[3])
            # Fill the area
            ctx.fill()

        # Draw "per-core CPU usage" if preferred.
        else:

            logical_core_list_system_ordered = Performance.logical_core_list_system_ordered

            logical_core_list = Performance.logical_core_list
            cpu_usage_percent_per_core = Performance.cpu_usage_percent_per_core

            chart_line_color = Config.chart_line_color_cpu_percent
            chart_background_color = Config.chart_background_color_all_charts

            chart_foreground_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.8 * chart_line_color[3]]
            chart_fill_below_line_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.4 * chart_line_color[3]]

            chart1101_width = Gtk.Widget.get_allocated_width(widget)
            chart1101_height = Gtk.Widget.get_allocated_height(widget)

            chart1101_width_per_core = chart1101_width / Performance.number_of_logical_cores
            # Chart height and chart height per core is same because charts for all cores will be bars next to each other (like columns).
            chart1101_height_per_core = chart1101_height
            # Spacing 5 from left and right
            chart1101_width_per_core_w_spacing = chart1101_width_per_core - 10
            # Spacing 5 from top and bottom
            chart1101_height_per_core_w_spacing = chart1101_height - 10

            for i, cpu_core in enumerate(logical_core_list_system_ordered):
                ctx.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
                ctx.rectangle(i*chart1101_width_per_core, 0, chart1101_width_per_core, chart1101_height_per_core)
                ctx.fill()

                ctx.set_line_width(1)
                ctx.set_source_rgba(chart_foreground_color[0], chart_foreground_color[1], chart_foreground_color[2], chart_foreground_color[3])
                ctx.rectangle(i*chart1101_width_per_core+5, 5, chart1101_width_per_core_w_spacing, chart1101_height_per_core_w_spacing)
                ctx.stroke()
                ctx.set_source_rgba(chart_fill_below_line_color[0], chart_fill_below_line_color[1], chart_fill_below_line_color[2], chart_fill_below_line_color[3])
                ctx.rectangle(i*chart1101_width_per_core+5, (chart1101_height_per_core_w_spacing-chart1101_height_per_core_w_spacing*cpu_usage_percent_per_core[logical_core_list.index(cpu_core)]/100)+5, chart1101_width_per_core_w_spacing, chart1101_height_per_core_w_spacing*cpu_usage_percent_per_core[logical_core_list.index(cpu_core)]/100)
                ctx.fill()
                ctx.set_source_rgba(chart_foreground_color[0], chart_foreground_color[1], chart_foreground_color[2], 2*chart_foreground_color[3])
                ctx.move_to(i*chart1101_width_per_core+8, 16)
                ctx.show_text(f'{cpu_core.split("cpu")[-1]}')


    # ----------------------------------- CPU - Initial Function (contains initial code which which is not wanted to be run in every loop) -----------------------------------
    def cpu_initial_func(self):

        logical_core_list_system_ordered = Performance.logical_core_list_system_ordered
        selected_cpu_core = Performance.selected_cpu_core
        selected_cpu_core_number_only = selected_cpu_core.split("cpu")[1]

        # Get maximum and minimum frequencies of the selected CPU core
        try:
            with open("/sys/devices/system/cpu/cpufreq/policy" + selected_cpu_core_number_only + "/scaling_max_freq") as reader:
                cpu_max_frequency_selected_core = float(reader.read().strip()) / 1000000
            with open("/sys/devices/system/cpu/cpufreq/policy" + selected_cpu_core_number_only + "/scaling_min_freq") as reader:
                cpu_min_frequency_selected_core = float(reader.read().strip()) / 1000000
        except FileNotFoundError:
            cpu_max_frequency_selected_core = "-"
            cpu_min_frequency_selected_core = "-"

        # Get cache memory values of the selected CPU core
        # Get l1d cache value
        try:
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index0/level") as reader:
                cache_level = reader.read().strip()
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index0/type") as reader:
                cache_type = reader.read().strip()
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index0/size") as reader:
                cache_size = reader.read().strip()
            if cache_level == "1" and cache_type == "Data":
                cpu_l1d_cache_value_selected_core = cache_size
        except FileNotFoundError:
            cpu_l1d_cache_value_selected_core = "-"
        # Get li cache value
        try:
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index1/level") as reader:
                cache_level = reader.read().strip()
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index1/type") as reader:
                cache_type = reader.read().strip()
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index1/size") as reader:
                cache_size = reader.read().strip()
            if cache_level == "1" and cache_type == "Instruction":
                cpu_l1i_cache_value_selected_core = cache_size
        except FileNotFoundError:
            cpu_l1i_cache_value_selected_core = "-"
        # Get l2 cache value
        try:
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index2/level") as reader:
                cache_level = reader.read().strip()
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index2/size") as reader:
                cache_size = reader.read().strip()
            if cache_level == "2":
                cpu_l2_cache_value_selected_core = cache_size
        except FileNotFoundError:
            cpu_l2_cache_value_selected_core = "-"
        # Get l3 cache value
        try:
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index3/level") as reader:
                cache_level = reader.read().strip()
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index3/size") as reader:
                cache_size = reader.read().strip()
            if cache_level == "3":
                cpu_l3_cache_value_selected_core = cache_size
        except FileNotFoundError:
            cpu_l3_cache_value_selected_core = "-"

        # Get CPU architecture
        cpu_architecture = platform.processor()
        if cpu_architecture == "":
            cpu_architecture = platform.machine()
            if cpu_architecture == "":
                cpu_architecture = "-"


        # Set CPU tab label texts by using information get
        show_cpu_usage_per_core = Config.show_cpu_usage_per_core
        if show_cpu_usage_per_core == 0:
            self.label1113.set_text(_tr("CPU Usage (Average)"))
        if show_cpu_usage_per_core == 1:
            self.label1113.set_text(_tr("CPU Usage (Per Core)"))
        if isinstance(cpu_max_frequency_selected_core, str) is False:
            self.label1105.set_text(f'{cpu_min_frequency_selected_core:.2f} - {cpu_max_frequency_selected_core:.2f} GHz')
        else:
            self.label1105.set_text(f'{cpu_min_frequency_selected_core} - {cpu_max_frequency_selected_core}')
        self.label1108.set_text(cpu_architecture)
        self.label1109.set_text(f'{cpu_l1i_cache_value_selected_core} - {cpu_l1d_cache_value_selected_core}')
        self.label1110.set_text(f'{cpu_l2_cache_value_selected_core} - {cpu_l3_cache_value_selected_core}')


    # ----------------------------------- CPU - Get CPU Data Function (gets CPU data, shows on the labels on the GUI) -----------------------------------
    def cpu_loop_func(self):

        number_of_logical_cores = Performance.number_of_logical_cores
        cpu_usage_percent_ave = Performance.cpu_usage_percent_ave
        selected_cpu_core_number = Performance.selected_cpu_core_number
        selected_cpu_core = Performance.selected_cpu_core
        selected_cpu_core_number_only = selected_cpu_core.split("cpu")[1]
        # Run "cpu_initial_func" if selected CPU core is changed since the last loop.
        try:                                                                                      
            if self.selected_cpu_core_prev != selected_cpu_core:
                self.cpu_initial_func()
        # try-except is used in order to avoid error if this is first loop of the function. Because "selected_cpu_core_prev" variable is not defined in this situation.
        except AttributeError:
            pass
        self.selected_cpu_core_prev = selected_cpu_core

        self.drawingarea1101.queue_draw()

        # Get number of physical cores, number_of_cpu_sockets, cpu_model_names
        with open("/proc/cpuinfo") as reader:
            proc_cpuinfo_output = reader.read()
        proc_cpuinfo_output_lines = proc_cpuinfo_output.split("\n")
        # Get number of physical cores, number_of_cpu_sockets, cpu_model_names for "x86_64" architecture. Physical and logical cores and model name per core information are tracked easily on this platform.
        if "physical id" in proc_cpuinfo_output:
            cpu_model_names = []
            number_of_physical_cores = 0
            physical_id = 0
            physical_id_prev = 0
            for line in proc_cpuinfo_output_lines:
                if line.startswith("physical id"):
                    physical_id_prev = physical_id
                    physical_id = line.split(":")[1].strip()
                if physical_id != physical_id_prev and line.startswith("cpu cores"):
                    number_of_physical_cores = number_of_physical_cores + int(line.split(":")[1].strip())
                if line.startswith("model name"):
                    cpu_model_names.append(line.split(":")[1].strip())
            number_of_cpu_sockets = int(physical_id) + 1
        # Get number of physical cores, number_of_cpu_sockets, cpu_model_names for "ARM" architecture. Physical and logical cores and model name per core information are not tracked easily on this platform. Different ARM processors (v6, v7, v8 or models of same ARM vX processors) may have different information in "/proc/cpuinfo" file.
        if "physical id" not in proc_cpuinfo_output:
            cpu_model_names = []
            number_of_physical_cores = number_of_logical_cores
            # Initial value of "number_of_cpu_sockets". This value may not be detected on systems with ARM CPUs.
            number_of_cpu_sockets = f'[{_tr("Unknown")}]'
            # Some processors have "processor", some processors have "Processor" and some processors have both "processor" and "Processor". "processor" is used for core number and "Processor" is used for model name. But "model name" is used for model name on some ARM processors. Model name is repeated for all cores on these processors. "Processor" is used for one time for the processor.
            if "model name" in proc_cpuinfo_output:
                for line in proc_cpuinfo_output_lines:
                    if line.startswith("model name"):
                        cpu_model_names.append(line.split(":")[1].strip())
            if "model name" not in proc_cpuinfo_output and "Processor" in proc_cpuinfo_output:
                for line in proc_cpuinfo_output_lines:
                    if line.startswith("Processor"):
                        cpu_model_names.append(line.split(":")[1].strip())
            if len(cpu_model_names) == 1:
                cpu_model_names = cpu_model_names * number_of_logical_cores
            if "Processor" in proc_cpuinfo_output:
                number_of_cpu_sockets = 0
                number_of_cpu_sockets = number_of_cpu_sockets + 1
            # Some ARM processors do not have model name information in "/proc/cpuinfo" file.
            if cpu_model_names == []:
                cpu_model_names = [_tr("Unknown")]

        # Get current frequency of the selected CPU core
        try:
            with open("/sys/devices/system/cpu/cpufreq/policy" + selected_cpu_core_number_only + "/scaling_cur_freq") as reader:
                cpu_current_frequency_selected_core = float(reader.read().strip()) / 1000000
        except FileNotFoundError:
            with open("/proc/cpuinfo") as reader:
                proc_cpuinfo_all_cores = reader.read().strip().split("\n\n")
            proc_cpuinfo_all_cores_lines = proc_cpuinfo_all_cores[int(selected_cpu_core_number_only)].split("\n")
            for line in proc_cpuinfo_all_cores_lines:
                if line.startswith("cpu MHz"):
                    cpu_current_frequency_selected_core = float(line.split(":")[1].strip()) / 1000
                    break

        # Get number_of_total_threads and number_of_total_processes
        thread_count_list = []
        pid_list = [filename for filename in os.listdir("/proc/") if filename.isdigit()]
        for pid in pid_list:
            try:
                with open("/proc/" + pid + "/status") as reader:
                    proc_status_output = reader.read()
            # try-except is used in order to skip to the next loop without application error if a "FileNotFoundError" error is encountered when process is ended after process list is get.
            except (FileNotFoundError, ProcessLookupError) as me:
                continue
            # Append number of threads of the process
            thread_count_list.append(int(proc_status_output.split("\nThreads:", 1)[1].split("\n", 1)[0].strip()))
        number_of_total_processes = len(thread_count_list)
        number_of_total_threads = sum(thread_count_list)

        # Get system up time (sut) information
        with open("/proc/uptime") as reader:
            sut_read = float(reader.read().split(" ")[0].strip())
        sut_days = sut_read/60/60/24
        sut_days_int = int(sut_days)
        sut_hours = (sut_days -sut_days_int) * 24
        sut_hours_int = int(sut_hours)
        sut_minutes = (sut_hours - sut_hours_int) * 60
        sut_minutes_int = int(sut_minutes)
        sut_seconds = (sut_minutes - sut_minutes_int) * 60
        sut_seconds_int = int(sut_seconds)


        # Set and update CPU tab label texts by using information get
        self.label1101.set_text(cpu_model_names[selected_cpu_core_number])
        self.label1102.set_text(selected_cpu_core)
        self.label1111.set_text(f'{number_of_total_processes} - {number_of_total_threads}')
        self.label1112.set_text(f'{sut_days_int:02}:{sut_hours_int:02}:{sut_minutes_int:02}:{sut_seconds_int:02}')
        self.label1103.set_text(f'{cpu_usage_percent_ave[-1]:.{Config.performance_cpu_usage_percent_precision}f} %')
        self.label1104.set_text(f'{cpu_current_frequency_selected_core:.2f} GHz')
        self.label1106.set_text(f'{number_of_cpu_sockets}')
        self.label1107.set_text(f'{number_of_physical_cores} - {number_of_logical_cores}')


# Generate object
Cpu = Cpu()

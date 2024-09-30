import os
import h5py
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# User-defined variables
folder_path = r'K:\22001017-Coolidge\Project Documents\Engineering-Planning-Power and Energy\Reports\Drainage\Reference\Randolph_RAS2D'
hdf_file_path = os.path.join(folder_path, 'Randolph.p19.hdf')
pdf_output_path = os.path.join(folder_path, '_culv_plots.pdf')
time_step = 5  # Time step in minutes

def extract_culvert_data(hdf_group):
    """
    Recursively search for datasets in the HDF group and extract culvert data.

    Args:
        hdf_group (h5py.Group): The HDF5 group to search.

    Returns:
        dict: A dictionary containing culvert data as DataFrames.
    """
    culvert_data = {}
    for key, item in hdf_group.items():
        if isinstance(item, h5py.Group):  # If it's a group, recurse into it
            culvert_data.update(extract_culvert_data(item))
        elif isinstance(item, h5py.Dataset):  # If it's a dataset, extract the data
            if 'Culvert Groups' in item.name:
                culvert_name = item.name.split('/')[-3]
                group_name = item.name.split('/')[-1]
                # Read the dataset
                data = item[:]
                # Convert to DataFrame with proper column names
                df = pd.DataFrame(data, columns=['Discharge (cfs)', 'Headwater Stage (ft)', 'Tailwater Stage (ft)'])
                culvert_data[f"{culvert_name}_{group_name}"] = df
    return culvert_data

def create_dual_yaxis_plot(ax, df, title):
    """
    Create a dual y-axis plot on the given Axes with peak and max stage annotations.

    Args:
        ax (matplotlib.axes.Axes): The Axes to plot on.
        df (pd.DataFrame): The DataFrame containing the data.
        title (str): The title of the plot.

    Returns:
        None
    """
    ax.set_title(title, color='black')  # Set title with black text
    ax.set_xlabel(f'Time Index ({time_step}-min intervals)', color='black')  # Set x-label with black text
    ax.tick_params(axis='x', colors='black')  # Set x-axis ticks to black
    ax.tick_params(axis='y', colors='black')  # Set y-axis ticks to black

    # Plot Discharge
    discharge_line, = ax.plot(df.index, df['Discharge (cfs)'], 'b-', label='Q (cfs)')
    ax.set_ylabel('Discharge (cfs)', color='black')  # Set y-label with black text
    ax.tick_params(axis='y', colors='black')  # Set y-axis ticks to black

    # Create a twin y-axis for Headwater and Tailwater Stages
    ax2 = ax.twinx()
    headwater_line, = ax2.plot(df.index, df['Headwater Stage (ft)'], 'r-', label='HW (ft)')
    tailwater_line, = ax2.plot(df.index, df['Tailwater Stage (ft)'], 'g-', label='TW (ft)')
    ax2.set_ylabel('Stage (ft)', color='black')  # Set y-label with black text
    ax2.tick_params(axis='y', colors='black')  # Set y-axis ticks to black

    # Add grid lines
    ax.grid(True)

    # Combine legends from both axes and place on the bottom right
    lines = [discharge_line, headwater_line, tailwater_line]
    labels = [line.get_label() for line in lines]
    ax.legend(lines, labels, loc='lower right')  # Legend moved to bottom right

    # Calculate peak discharge and time to peak
    peak_discharge = df['Discharge (cfs)'].max()
    peak_index = df['Discharge (cfs)'].idxmax()
    time_to_peak_minutes = peak_index * time_step
    time_to_peak_hours = time_to_peak_minutes / 60.0

    # Calculate max headwater and tailwater stages
    max_hw_stage = df['Headwater Stage (ft)'].max()
    max_tw_stage = df['Tailwater Stage (ft)'].max()

    # Add annotations for peak values
    annotation_text = (
        f"Peak Q: {peak_discharge:.2f} cfs\n"
        f"Time to Peak: {time_to_peak_hours:.2f} hrs\n"
        f"Max HW Stage: {max_hw_stage:.2f} ft\n"
        f"Max TW Stage: {max_tw_stage:.2f} ft"
    )
    ax.annotate(
        annotation_text,
        xy=(0.05, 0.95),
        xycoords='axes fraction',
        verticalalignment='top',
        bbox=dict(boxstyle="round,pad=0.5", fc="white", alpha=0.8),
        fontsize=8
    )

def main():
    """
    Main function to extract culvert data and generate PDF plots.

    Returns:
        None
    """
    # Open the HDF file
    hdf_file = h5py.File(hdf_file_path, 'r')

    # Extract data for all SA 2D Area Conn
    culvert_data = extract_culvert_data(hdf_file['/Results/Unsteady/Output/Output Blocks/DSS Profile Output/Unsteady Time Series/SA 2D Area Conn'])

    # Close the HDF file
    hdf_file.close()

    # Create a PDF for the plots with specified size
    pp = PdfPages(pdf_output_path)

    # Number of plots per page
    plots_per_page = 4
    # Calculate total number of pages
    total_pages = (len(culvert_data) + plots_per_page - 1) // plots_per_page

    culvert_items = list(culvert_data.items())

    for page in range(total_pages):
        # Create a new figure for each page with 2x2 subplots
        fig, axes = plt.subplots(2, 2, figsize=(8.5, 11))  # 8.5" x 11" for US Letter
        fig.subplots_adjust(hspace=0.4, wspace=0.4)  # Adjust spacing between subplots
        for i in range(plots_per_page):
            index = page * plots_per_page + i
            if index >= len(culvert_items):
                # Remove unused subplots if any
                fig.delaxes(axes.flatten()[i])
                continue  # No more plots to add
            culvert_name, df = culvert_items[index]
            row = i // 2
            col = i % 2
            ax = axes[row, col]
            create_dual_yaxis_plot(ax, df, culvert_name)
        # Add the figure to the PDF
        pp.savefig(fig)
        plt.close(fig)

    # Close the PDF file
    pp.close()

if __name__ == "__main__":
    main()
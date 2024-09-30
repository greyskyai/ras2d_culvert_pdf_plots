# RAS2D Culvert Time Series Plots

This Python script generates time series plots for culvert data extracted from HEC-RAS 2D model results. It creates a PDF document with multiple pages, each containing four plots in a 2x2 grid layout.

## Features

- Extracts culvert data from HEC-RAS 2D HDF5 output files
- Generates dual y-axis plots for discharge and stage data
- Creates a multi-page PDF with 2x2 grid layout (4 plots per page)
- Annotates peak discharge, time to peak, and maximum stages
- Customizable plot appearance and layout

## Requirements

- Python 3.x
- Required Python packages:
  - h5py
  - pandas
  - matplotlib

## Usage

1. Update the following variables in the script:
   - `hdf_file_path`: Path to the HEC-RAS 2D HDF5 output file
   - `pdf_output_path`: Desired path for the output PDF file
   - `time_step`: Time step in minutes (default is 5)

2. Run the script:
   ```
   python ras2d_culvert_time_series_plots.py
   ```

3. The script will generate a PDF file with the culvert time series plots at the specified output path.

## Customization

You can modify the following aspects of the plots:
- Figure size and layout
- Plot titles and labels
- Legend position
- Annotation content and position
- Line colors and styles

## Functions

- `extract_culvert_data(hdf_group)`: Recursively extracts culvert data from the HDF5 file
- `create_dual_yaxis_plot(ax, df, title)`: Creates a dual y-axis plot for a single culvert
- `main()`: Main function that orchestrates the data extraction and plot generation

## Output

The script produces a PDF file with the following characteristics:
- Page size: 8.5" x 11" (US Letter)
- 2x2 grid layout (4 plots per page)
- Dual y-axis plots showing discharge and stage data
- Annotations for peak discharge, time to peak, and maximum stages
- Legend in the bottom right corner of each plot

## Notes

- Ensure that the HDF5 file path is correct and accessible
- The script assumes a specific structure for the HDF5 file; modifications may be needed for different file structures
- Large datasets may require significant processing time and memory

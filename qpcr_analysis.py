import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import yaml
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='qPCR Analysis Pipeline')
    parser.add_argument('--config', '-c', type=str,help='Path to config YAML file', required=True)
    parser.add_argument('--plots', '-p', type=str, choices=['yes', 'no'], help='Do you want to calculate ANOVA test? (yes/no)', required=True)
    return parser.parse_args()


def process_from_config(config_path):
    """Read and process qPCR configuration file"""
    with open(config_path) as stream:
        config = yaml.safe_load(stream)
    
    return {
        "input_file": config["input_file"],
        "reference_gene": config["reference_gene"]["name"],
        "target_genes": [gene["name"] for gene in config["target_genes"]],
        "control_samples": [ctrl["name"] for ctrl in config["control"]],
        "replicates": config["replicates"]["number"],
        "technical_replicates": config["replicates"]["technical"]
    }

def extract_table_from_excel():

    '''
    Read qPCR results from an Excel file, specifically extracting Sample Name, Target Name, and CT values
    from the 'results' sheet to create pandas dataframe.

    Returns:
    --------
    pd.DataFrame
        DataFrame containing only Sample Name, Target Name, and CT columns
    
    Raises:
    -------
    FileNotFoundError: If the file doesn't exist
    ValueError: If the required sheet or columns are not found
    '''
    
    config = process_from_config("config_file.yaml")
    file_path = config['input_file']
    
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist")
            
        if not file_path.endswith(('.xls', '.xlsx')):
            raise ValueError("File must be an Excel file (.xls or .xlsx)")
        
        sheet_name = "Results"
        xls = pd.ExcelFile(file_path)
        sheet_df = pd.read_excel(xls, sheet_name=sheet_name, header=None)

        required_columns = {"Sample Name", "Target Name", "CT"}
        for idx, row in sheet_df.iterrows():
            if required_columns.issubset(set(row)):
                table_start_row = idx
                break
        else:
            raise ValueError("Table headers not found in the sheet")

        table_df = pd.read_excel(
            xls,
            sheet_name=sheet_name,
            skiprows=table_start_row,
            usecols=["Sample Name", "Target Name", "CT"]
        )

        rel_df = table_df[table_df['CT'] != 'Undetermined']
        return rel_df.dropna(how="all").reset_index(drop=True)
        
    except Exception as e:
        print(f"Error reading qPCR results: {str(e)}")
        raise

def check_control_samples(rel_df):
    '''
    Check the control samples- NTC (no template control) from the qPCR results. 
    'Undetermined' values in controls indicate clean samples (no contamination).
    Only numeric CT values >= 35 indicate contamination.

    Returns:
    --------
    pd.DataFrame
        DataFrame not containing contaminated control samples.

    Raises:
    -------
    ValueError: If the control sample not found.
    ValueError: If CT value of control sample not found.
    ValueError: If control samples have numeric CT values >= 35.
    '''

    config = process_from_config("config_file.yaml")
    control_sample_names = config['control_samples'] + ['NCT', 'NRT']  # Add common variations
    
    unclean_targets = []
    error_messages = []
    filtered_df = rel_df[~rel_df['Sample Name'].isin(control_sample_names)].copy()
    
    for control in control_sample_names:
        if control not in rel_df["Sample Name"].values:
            error_messages.append(f"Control sample '{control}' not found in DataFrame")
            continue
            
        control_data = rel_df[rel_df["Sample Name"] == control]
        if control_data.empty:
            error_messages.append(f"No CT values found for control sample '{control}'")
            continue
        
        numeric_mask = control_data['CT'] != 'Undetermined'
        contaminated_data = control_data[numeric_mask & (control_data['CT'].astype(float) >= 35)]
        
        if not contaminated_data.empty:
            unclean_targets.extend(contaminated_data['Target Name'].unique().tolist())
    
    if error_messages or unclean_targets:
        warning_text = "\n".join(error_messages)
        if unclean_targets:
            warning_text += f"\nWarning: Control is not clean for targets: {', '.join(unclean_targets)}"
        print(warning_text)
        
    return filtered_df

def analyze_results(filtered_df):
    '''
    Take the qPCR results from the data frame and calculating the ΔCt,ΔΔCt and fold change for each gene. 
    
    Returns:
    --------
    pd.DataFrame
        DataFrame containing for each Sample Name the calculated values: ΔCt,ΔΔCt and fold change.
    
    Raises:
    -------
    ValueError: If the required referance gene not found.
    ValueError: If one of the required tartet genes not found.
    '''

    config = process_from_config("config_file.yaml")
    ref_gene_name = config['reference_gene']
    target_gene_name = config['target_genes']
    
    filtered_df = filtered_df.copy()

    if ref_gene_name not in filtered_df['Target Name'].values:
        raise ValueError(f"Reference gene '{ref_gene_name}' not found in DataFrame")
    
    for target in target_gene_name:
        if target not in filtered_df['Target Name'].values:
            raise ValueError(f"Target gene '{target}' not found in DataFrame")

    filtered_df = filtered_df[filtered_df['CT'] != 'Undetermined']
    
    ref_data = filtered_df.loc[filtered_df["Target Name"] == ref_gene_name]
    if ref_data.empty:
        raise ValueError(f"No data found for reference gene '{ref_gene_name}'")

    reference_averages = ref_data.groupby('Sample Name')['CT'].mean().to_dict()

    filtered_df['Reference_Mean'] = filtered_df['Sample Name'].map(reference_averages)
    filtered_df['ΔCt'] = filtered_df['CT'] - filtered_df['Reference_Mean']

    filtered_df['ΔΔCt'] = np.nan

    for target in target_gene_name:
        target_samples = filtered_df[filtered_df['Target Name'] == target]
        if not target_samples.empty:
            first_sample_delta_ct = target_samples['ΔCt'].iloc[0]
            filtered_df.loc[filtered_df['Target Name'] == target, 'ΔΔCt'] = \
                filtered_df.loc[filtered_df['Target Name'] == target, 'ΔCt'] - first_sample_delta_ct

    filtered_df['Fold Change'] = np.where(
        filtered_df['ΔΔCt'].notna(),
        2 ** (-filtered_df['ΔΔCt']),
        np.nan
    )

    return filtered_df

def create_bar_plot(analyzed_df):
    '''
    Create a bar plot containing statistical results using a one-way ANOVA test.

    Returns:
    --------
    results : dict
        Dictionary containing ANOVA results (F-statistic and p-value) for each gene.
    Bar plots for each target gene grouped by 'Sample Name'.
    '''

    config = process_from_config("config_file.yaml")
    target_gene_name = config['target_genes']
    reference_gene = config['reference_gene']
    
    results = {}

    for gene in target_gene_name:
        gene_data = analyzed_df.loc[analyzed_df['Target Name'] == gene, ['Sample Name', 'Fold Change']]
        grouped_data = gene_data.groupby('Sample Name')['Fold Change'].apply(list).to_dict()
        
        days = sorted(grouped_data.keys())
        gene_values = [grouped_data[day] for day in days]
        
        f_stat, p_val = stats.f_oneway(*gene_values)
        results[gene] = {'f_statistic': f_stat, 'p_value': p_val}
        
        means = [np.mean(values) for values in gene_values]
        sems = [np.std(values, ddof=1) / np.sqrt(len(values)) for values in gene_values]
        
        plt.figure(figsize=(10, 6))
        plt.bar(days, means, yerr=sems, capsize=5, color='skyblue', alpha=0.7, label='Mean ± SEM')
        
        for i, day in enumerate(days):
            plt.scatter([i] * len(gene_values[i]), gene_values[i], color='black', alpha=0.5, zorder=3)
        
        plt.yscale('log')
        plt.xticks(ticks=range(len(days)), labels=days)
        plt.ylabel(f'Fold change in {gene}/{reference_gene}')
        plt.title(f'Expression Levels for {gene}\nANOVA p-value: {p_val:.4e}')
        
        if p_val < 0.05:
            plt.text(0.5, 0.95, '*p < 0.05', transform=plt.gca().transAxes, 
                     ha='center', va='center', fontsize=12, color='red')
        
        plt.legend()
        plt.show()
        
        print(f"\nResults for {gene}:")
        print(f"F-statistic: {f_stat:.4f}")
        print(f"p-value: {p_val:.4e}")
        
        if p_val < 0.05:
            print("\nMean expression values:")
            for day, mean in zip(days, means):
                print(f"{day}: {mean:.3f}")

    return results

def main():
    args = parse_args()
    
    # Read data from Excel
    df = extract_table_from_excel()
    print("Raw data:")
    print(df)
    print("\n" + "="*50 + "\n")
    
    # Check controls and filter data
    filtered_df = check_control_samples(df)
    print("\nFiltered data:")
    print(filtered_df)
    print("\n" + "="*50 + "\n")
    
    # Analyze results
    analyzed_df = analyze_results(filtered_df)
    print("\nAnalyzed data:")
    print(analyzed_df)
    print("\n" + "="*50 + "\n")

    # Export to CSV
    analyzed_df.to_csv('analyzed_results.csv', index=False)
    
   # Only create plots and do statistical analysis if plots are requested
    if args.plots.lower() == 'yes':
        results = create_bar_plot(analyzed_df)
        print("\nStatistical results:")
        print(results)
    else:
        print("\nPlot creation skipped as per user request.")

if __name__ == "__main__":
    main()
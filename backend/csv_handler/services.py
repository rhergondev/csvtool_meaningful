import pandas as pd


def process_csv_files(file1, file2):
    """
    Process the uploaded CSV files and return a summary.
    """

    required_columns = {"data", "concelho", "var", "n"}
    try:
        # Read the CSV files into DataFrames
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)

        # Check for required columns
        if not required_columns.issubset(df1.columns):
            missing = required_columns - set(df1.columns)
            raise ValueError(f"Missing columns in file1: {missing}")
        if not required_columns.issubset(df2.columns):
            missing = required_columns - set(df2.columns)
            raise ValueError(f"Missing columns in file2: {missing}")

        # Combine the DataFrames
        combined_df = pd.concat([df1, df2], ignore_index=True)
        print("Service: combined_df")

        # Pivot the DataFrame
        try:
            all_vars = combined_df["var"].unique()
            pivot_df = combined_df.pivot_table(
                index=["data", "concelho"], columns="var", values="n", aggfunc="first"
            )

        except KeyError as e:
            raise ValueError(
                f"Error pivoting. Check columns 'var' and 'n'. Missing: {e}"
            ) from e

        pivot_df.reset_index(inplace=True)
        pivot_df.columns.name = None

        print("Service: pivot_df")

        column_mapping = {
            "Fogos em Oferta": "unidades_oferta",
            "Valor de Oferta / m2": "valor_oferta",
            "Fogos Vendidos": "unidades_vendidos",
            "Preço de Venda / m2": "valor_venda",
        }
        expected_output_columns = set(
            ["data", "concelho"] + list(column_mapping.values())
        )

        # Rename columns based on the mapping
        pivot_df.rename(
            columns={k: v for k, v in column_mapping.items() if k in pivot_df.columns},
            inplace=True,
        )

        final_columns = set(pivot_df.columns)
        unexpected_columns = final_columns - expected_output_columns

        # Check for unexpected columns
        if unexpected_columns:
            original_unexpected_vars = []
            reversed_mapping = {v: k for k, v in column_mapping.items()}
            for col in unexpected_columns:
                if col not in reversed_mapping and col in all_vars:
                    original_unexpected_vars.append(col)

            if original_unexpected_vars:
                raise ValueError(
                    f"Unexpected 'var' values in the pivoted DataFrame: {', '.join(original_unexpected_vars)}. Expected columns: {expected_output_columns}"
                )
            else:
                raise ValueError(
                    f"Unexpected columns generated after processing: {unexpected_columns}. Expected columns: {expected_output_columns}"
                )
        print("Service: pivot_df after rename")

        return pivot_df
    except (pd.errors.EmptyDataError, KeyError, ValueError) as e:
        error_message = str(e)
        print(f"Service Error (Validation/Format): {error_message}")
        raise ValueError(error_message) from e

    except Exception as e:
        print(f"Service Error (Unexpected Processing): {type(e).__name__} - {e}")
        raise RuntimeError(
            "An unexpected server error occurred, try reloading the page"
        ) from e

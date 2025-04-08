from pathlib import Path
import pandas as pd


def create_a_file(file_name: str) -> Path:
    file_path = Path(file_name)

    if not file_path.exists():
        # Create an empty Excel file
        df = pd.DataFrame()
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)

    return file_path


def add_columns_to_the_excel_file(file_path: Path, columns: list[str]) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(f"The file does not exist: {file_path}")

    # Ensure 'S.No' is always the first column
    if "S.No" not in columns:
        columns = ["S.No"] + columns

    df = pd.DataFrame(columns=columns)

    with pd.ExcelWriter(file_path, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, index=False)

    return df


def delete_columns_from_excel_file(
    file_path: Path, columns_to_delete: list[str]
) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(f"The file does not exist: {file_path}")

    df = pd.read_excel(file_path)

    existing_cols = [
        col for col in columns_to_delete if col in df.columns and col != "S.No"
    ]
    df.drop(columns=existing_cols, inplace=True)

    with pd.ExcelWriter(file_path, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, index=False)

    return df


def add_question_to_excel(
    file_path: Path, question_data: dict[str, str]
) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(f"The file does not exist: {file_path}")

    try:
        df = pd.read_excel(file_path)
    except Exception:
        df = pd.DataFrame()

    next_serial = 1 if df.empty else df["S.No"].max() + 1

    entry = {"S.No": next_serial}
    entry.update(question_data)

    # Use concat instead of append (for pandas >= 2.0)
    new_row_df = pd.DataFrame([entry])
    df = pd.concat([df, new_row_df], ignore_index=True)

    with pd.ExcelWriter(file_path, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, index=False)

    return df

import json
import logging
from pathlib import Path
from typing import Dict, List, Union

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
import pandas as pd

# Configure logger for tracking export operations
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class FileToSpreadsheetConverter:
    """
    Helper class that reads a plain text file containing sorted phone numbers
    (with country codes, e.g., '+373...') and exports them into professionally 
    formatted Excel (.xlsx), CSV, and JSON files.
    """

    def __init__(self, output_dir: Union[str, Path] = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def read_numbers_from_file(self, txt_file_path: Union[str, Path]) -> List[str]:
        """
        Reads lines from the sorted TXT file, preserving exact string representations 
        including '+' sign and country code without modifying digits.

        :param txt_file_path: Path to the sorted phone numbers .txt file.
        :return: List of phone number strings exactly as saved in the TXT file.
        """
        file_path = Path(txt_file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Source text file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as file:
            # Read non-empty lines and strip only trailing/leading whitespace
            numbers = [line.strip() for line in file if line.strip()]

        logging.info("Successfully read %d formatted numbers from %s", len(numbers), file_path)
        return numbers

    def convert_txt_to_excel(
        self,
        txt_file_path: Union[str, Path],
        output_filename: str,
        column_name: str = "Phone Number"
    ) -> Path:
        """
        Converts phone numbers from TXT to a styled Excel (.xlsx) spreadsheet.
        Enforces strict Text formatting ('@') on cells to guarantee that country codes,
        leading plus signs ('+'), and zero prefixes remain completely intact.
        """
        numbers = self.read_numbers_from_file(txt_file_path)
        df = pd.DataFrame({column_name: numbers})

        excel_path = self.output_dir / f"{output_filename}.xlsx"

        with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
            sheet_name = "Sorted Phone Numbers"
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            worksheet = writer.sheets[sheet_name]

            # Professional styling for table header (Dark Blue with white text)
            header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
            header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
            data_font = Font(name="Calibri", size=11)
            align_left = Alignment(horizontal="left", vertical="center")

            # Apply header styling
            for cell in worksheet[1]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center", vertical="center")

            # Format data rows as explicit text (@) to preserve '+' and country code exactly
            for row in worksheet.iter_rows(min_row=2, max_row=len(df) + 1, min_col=1, max_col=1):
                for cell in row:
                    cell.font = data_font
                    cell.alignment = align_left
                    cell.number_format = "@"

            # Dynamically calculate column width based on the longest phone number string
            max_len = max([len(str(num)) for num in numbers] + [len(column_name)]) if numbers else len(column_name)
            col_letter = openpyxl.utils.get_column_letter(1)
            worksheet.column_dimensions[col_letter].width = max(max_len + 6, 20)

        logging.info("Excel spreadsheet successfully created: %s", excel_path)
        return excel_path

    def convert_txt_to_csv(
        self,
        txt_file_path: Union[str, Path],
        output_filename: str,
        column_name: str = "Phone Number"
    ) -> Path:
        """
        Exports phone numbers from TXT to a standard CSV file.
        Uses UTF-8 BOM encoding ('utf-8-sig') to ensure Excel opens the CSV seamlessly
        without corrupting international numbers or special characters.
        """
        numbers = self.read_numbers_from_file(txt_file_path)
        df = pd.DataFrame({column_name: numbers})

        csv_path = self.output_dir / f"{output_filename}.csv"
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")

        logging.info("CSV file successfully created: %s", csv_path)
        return csv_path

    def convert_txt_to_json(
        self,
        txt_file_path: Union[str, Path],
        output_filename: str,
        key_name: str = "phone_numbers"
    ) -> Path:
        """
        Exports phone numbers from TXT to a formatted JSON file.
        Maintains UTF-8 encoding and exact formatting (including '+' and country codes).
        """
        numbers = self.read_numbers_from_file(txt_file_path)
        json_path = self.output_dir / f"{output_filename}.json"

        data_to_save = {
            key_name: numbers,
            "total_count": len(numbers)
        }

        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(data_to_save, json_file, ensure_ascii=False, indent=2)

        logging.info("JSON file successfully created: %s", json_path)
        return json_path

    def convert_txt_to_all(
        self,
        txt_file_path: Union[str, Path],
        output_filename: str,
        column_name: str = "Phone Number"
    ) -> Dict[str, Path]:
        """
        Convenience wrapper method that generates Excel (.xlsx), CSV, and JSON files
        from the source TXT file in a single step.
        """
        excel_path = self.convert_txt_to_excel(txt_file_path, output_filename, column_name)
        csv_path = self.convert_txt_to_csv(txt_file_path, output_filename, column_name)
        json_path = self.convert_txt_to_json(txt_file_path, output_filename)
        return {
            "excel": excel_path,
            "csv": csv_path,
            "json": json_path
        }


# =====================================================================
# Main Execution Block / Example Usage
# =====================================================================
    # Export to all formats simultaneously (Excel, CSV, JSON)
    # Uncomment and adjust path to execute:
    # generated_files = converter.convert_txt_to_all(
    #     txt_file_path=source_txt_file,
    #     output_filename="999_sorted_phone_numbers"
    # )
    # print(f"Excel report: {generated_files['excel']}")
    # print(f"CSV report:   {generated_files['csv']}")
    # print(f"JSON report:  {generated_files['json']}")

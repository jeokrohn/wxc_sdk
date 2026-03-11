#!/usr/bin/env python3
"""
Add user emails to Excel sheet
"""
import argparse
import asyncio
import logging
import sys

import pandas as pd
from dotenv import load_dotenv

from wxc_sdk.as_api import AsWebexSimpleApi
from wxc_sdk.as_rest import AsRestError


async def resolve_name(name, api: AsWebexSimpleApi) -> str:
    """
    Resolve employee name to email using Webex API.
    """
    name = ' '.join(name.split())  # Normalize name by removing extra spaces

    try:
        persons = await api.people.list(display_name=name)
        if persons:
            if len(persons) > 1:
                print(f"Warning: Multiple matches for name '{name}'. Skipping", file=sys.stderr)
                return ''
            return persons[0].emails[0]
        else:
            print(f"Warning: No match found for name   '{name}'", file=sys.stderr)
            return ''
    except Exception as e:
        print(f"Error resolving name '{name}': {str(e)}", file=sys.stderr)
        return ''


async def process_excel_names(file_path, api: AsWebexSimpleApi):
    """
    Process employee names in Excel file.
    """
    try:
        # Read the Excel file
        df = pd.read_excel(file_path, dtype=str)

        # Get employee names from first column (index 0)
        employee_names = df.iloc[:, 0]

        # Create tasks for all names to process in parallel
        tasks = [resolve_name(name, api) for name in employee_names]

        # Run all tasks concurrently
        resolved_names = await asyncio.gather(*tasks)

        # Save results to second column
        # Handle case where second column doesn't exist
        if df.shape[1] < 2:
            # Add a new column if it doesn't exist
            df['Resolved_Name'] = resolved_names
        else:
            # Update existing second column
            df.iloc[:, 1] = resolved_names

        # Save back to Excel
        df.to_excel(file_path, index=False)

        print(f"Processed {len(employee_names)} names")
        print(f'Resolved names: {sum(1 for name in resolved_names if name)}')
        print(f"Results saved to: {file_path}")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {str(e)}", file=sys.stderr)
        sys.exit(1)


# Example usage
async def main():
    parser = argparse.ArgumentParser(description='Process employee names in Excel file using Webex API')
    parser.add_argument('excel_file', help='Path to Excel file to process')
    parser.add_argument('--token', '-t', help='Access token from developer.webex.com. If not provided, '
                                              'token is read from WEBEX_ACCESS_TOKEN environment variable', )
    args = parser.parse_args()
    load_dotenv(override=True)
    logging.getLogger('wxc_sdk.as_rest').setLevel(logging.ERROR)

    try:
        async with AsWebexSimpleApi(tokens=args.token, concurrent_requests=50, ssl=False) as api:
            try:
                await api.people.me()
            except AsRestError as e:
                print(f"Authentication error: {e}", file=sys.stderr)
                sys.exit(1)
            await process_excel_names(args.excel_file, api)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

# VMware vCloud Director vApp Template Fetcher

This script allows you to fetch vApp templates from VMware vCloud Director (vCD) that match a specific metadata property. It connects to a VMware vCloud Director instance using administrator credentials and writes the filtered vApp templates to a CSV file.

## Prerequisites

Before using this script, make sure you have the following requirements installed:

- Python 3.7 or higher: [Python Download](https://www.python.org/downloads/)
- Required Python packages: You can install the required packages using the following command:

```
pip install -r requirements.txt
```

## Installation

1. Clone the repository to your local machine or download the script:

   ```bash
   git clone https://github.com/joroaf/vcd-template-fetcher.git
   ```

2. Install the required Python packages (if not already installed):

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script with the following command:

```bash
python get_templates.py --vcd-host <VCD_HOST> --username <USERNAME> --password <PASSWORD> --metadata-key <METADATA_KEY> --no-verify-ssl
```

- `--vcd-host`: The URL of the vCD instance.
- `--username`: Your administrator username for vCD authentication.
- `--password`: Your administrator password for vCD authentication.

Optional arguments:
- `--metadata-key`: The key of the metadata property to filter on.
- `--metadata-value`: The value of the metadata property to filter on.
- `--api-version`: The vCD API version (default is '37.0').
- `--no-verify-ssl`: Disable SSL certificate verification (default is False).

## Example

```bash
python script.py --vcd-host https://vcd.example.com --username admin_username --password admin_password --metadata-key your.metadata.key
```

The script will fetch vApp templates with the specified metadata property and write the results to a CSV file.

## Output

The script generates a CSV file named `output.csv` containing the filtered vApp templates.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [pyvcloud](https://github.com/vmware/pyvcloud) - Python SDK for VMware vCloud Director.
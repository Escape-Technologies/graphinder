# Graphinder

Graphinder is a tool that extracts all GraphQL endpoints from a given domain.

## Run with docker

```bash
docker run --rm escapetech/graphinder -it -v $(pwd):/usr/bin/graphinder
```

```bash
# Local build
docker build -t escapetech/graphinder .
```

## Installation

Clone the repository and run the installation script

```bash
git clone "url-of-this-project"
cd Graphinder
./install-dev.sh
```

Run this command to enter the virtual enviroment

```bash
poetry shell
```

## Usage

A Scan consistes of:

- Running on a specific domain (`-d`, `--domain`) or a list of domains (`-f`, `--input-file`).
- Searching all scripts loaded by the browser for graphql endpoint (`-s`, `--script`)
- Brute forcing the directories of all discovered urls (`-b`, `--bruteforce`)

By default, bruteforce and script search are enabled.

```bash
graphinder -d example.com
```

```bash
graphinder -f domains.txt
```

### Extra features

- `--no-bruteforce`: Disable bruteforce
- `--no-script`: Disable script search
- `-f --input-file <FILE_PATH>`: Input domain names from file
- `-w --max-workers <int>`: Maximum of concurrent workers on multiple domains.
- `-o --output-file <FILE_PATH>`: Output the results to file
- `-v --verbose --no-verbose`: Verbose mode
- `-r --reduce`: The maximum number of subdomains to scan.

If you experience any issues, irregularities or networking bottlenecks, please reduce your number of workers, otherwise, better is your network, the more workers you can have.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

# Graphinder

Graphinder is a tool that extracts all GraphQL endpoints from a given domain.

## Installation

Clone the repository and run the installation script

```bash
git clone "url-of-this-project"
cd Graphinder
./install-dev.sh
```

## Usage

run this command to enter the virtual enviroment

```bash
poetry shell
```

### Basic Scan

The basic scan consitutes of finding GraphQL requests found on the given domain

using the `-n` flag which causes the scanner to look inside network calls that the page does, looking for GraphQL endpoints

```bash
graphinder finder -n -u example.com
```

### Deep Scan

A deep scan consistes of:

- running basic scan on all detected subdomains (`-b`)
- searching all scripts loaded by the browser for graphql endpoint (`-s`)
- brute forcing the directories of all discovered urls (`-g`)

```bash
graphinder finder -s -b -g -u example.com
```

### Extra features

`-f <FILE_PATH>`: input domain names from file
`-o <FILE_PATH>`: output the results to file
`-v`: Verbose mode
`-r <INT>`: when the number of discovered domains exceeds the supplied parameter, graphinder will choose a subset of those domains to run the scan on

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

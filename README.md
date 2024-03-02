# Gen-Tanakh

## What is this?

This is a project that allows you to generate a `Hebrew - English Bible` according to the Masoretic Text and the JPS 1917 Edition, then parse it into a full-scope Tanakh stored in `tanakh.json`.

### Some notes

- The `self.order_map` list object is provided for outputting the Tanakh in the correct order if you wish.  
- The contents are already provided in this library, unzipped.
- The generated Tanakh is already provided in this project.
- You are free to enrich this content however you deem

## Usage

### Installation

```
git clone https://github.com/MarkBuffalo/gen-tanakh.git && cd gen-tanakh && chmod +x parse_mm_db.py
```

### Running the script

```
./parse_mm_db.py
```

### Using the output

At this point, you can simply use `tanakh.json` to enrich your APIs / Web Apps / whatever. The included `tanakh.json` file is already included.

# Introduction to awk

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/awk/Introduction-to-awk/page

Awk is a powerful language for text processing, enabling easy filtering, transforming, and formatting of structured text.

Awk is a powerful, domain-specific language for text processing. Whether you’re automating seat lookups in a movie theater or parsing system statistics, Awk’s field-oriented syntax and built-in variables make it easy to filter, transform, and format structured text.

## Why Use Awk?

* Processes structured data by rows (records) and columns (fields)
* Handles irregular whitespace automatically
* Integrates seamlessly into Unix pipelines
* Offers concise one-liners or full-fledged scripts

## Fields and Records

Imagine a seating chart stored in `minimovies.txt`, where “Y” means a seat is taken and “N” means it’s available. Awk treats each line as a **record** and each whitespace-separated item as a **field**.

![The image is an "Introduction to awk" diagram showing a table with columns labeled 1 to 5 and rows containing letters "a" to "e" with "y" and "n" indicating whether something is taken or not. A legend explains that "y" means it's taken and "n" means it's not.](../../../../images/kodekloud.com/kk-media/image/upload/v1752868662/notes-assets/images/Advanced-Bash-Scripting-Introduction-to-awk/introduction-to-awk-diagram.jpg)

* Columns ➔ Fields (`$1`, `$2`, …)
* Rows ➔ Records (`NR` is the built-in record counter)

### Extracting a Specific Seat

Step 1: Select the third column (`$3`) for every record.\
Step 2: Filter for record number 2 using `NR`.

![The image is an introduction to the "awk" command, showing a table with columns labeled a, b, c, d, e, and highlighting column c. It includes instructions for using "awk" to extract column c and create a comparison operation for equality.](../../../../images/kodekloud.com/kk-media/image/upload/v1752868663/notes-assets/images/Advanced-Bash-Scripting-Introduction-to-awk/awk-command-introduction-column-c.jpg)

```bash theme={null}

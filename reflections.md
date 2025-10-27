| **Issue Type**               | **Line** | **Description**                                                     | **Fix Approach**                                          |
| ---------------------------- | -------- | ------------------------------------------------------------------- | --------------------------------------------------------- |
| Mutable default argument     | 9        | `logs=[]` shares the same list across function calls                | Change default to `None` and initialize inside function   |
| Broad `except:`              | 21       | Swallows all exceptions silently                                    | Use `except KeyError:` or specific exception              |
| No input validation          | 15, 34   | Invalid types (`addItem(123, "ten")`) cause runtime issues          | Add type checking and return early for invalid data       |
| Unused import (`logging`)    | 2        | Imported but never used                                             | Remove import or use it for proper logging                |
| Use of `eval()`              | 36       | Security risk (arbitrary code execution)                            | Remove or replace with a safe alternative                 |
| Missing file handling safety | 29, 33   | Files not closed safely on exception                                | Use `with open(...) as f:` syntax                         |
| Missing key check            | 26       | `getQty()` assumes item always exists                               | Use `dict.get()` with default value or exception handling |
| Non-PEP8 naming              | All      | Functions not following snake_case properly, some constants missing | Ensure spacing, naming, and docstrings follow PEP8        |


**REFLECTION QUESTIONS:**

1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest fixes were renaming functions to snake_case and adding docstrings. The hardest was removing the global keyword and eval, since that required changing how data was handled and making sure the program still worked correctly.

2. Did the static analysis tools report any false positives? If so, describe one example.

Yes, pylint warned about using global, which made sense for larger projects but was okay for this small script. So it felt like a false positive in this context.

3. How would you integrate static analysis tools into your actual software development workflow? Consider continuous integration or local development practices.

I’d use these tools in VS Code or Codespaces before committing and also add them to a GitHub Actions CI pipeline so they automatically check code for errors and security issues.

4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

The code became cleaner, safer, and easier to read. Using with open, removing eval, and adding validation made it more reliable and professional-looking.